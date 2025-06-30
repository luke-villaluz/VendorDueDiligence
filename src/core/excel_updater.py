"""
Excel updater module for Vendor Due Diligence Automation Tool.
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from src.config.settings import settings
from src.utils.logger import logger
from src.utils.file_utils import load_excel_data, match_vendor_folder_to_excel

class ExcelUpdater:
    """Handles Excel file updates based on document analysis."""
    
    def __init__(self):
        self.excel_file = settings.excel_file
        self.df = None
        self.headers = None
        self.vendors = None
        self.summaries_dir = settings.data_dir / "summaries"
        self.summaries_dir.mkdir(exist_ok=True)
        self._load_excel_data()
        self.clear_vendor_checks()
        
    def _load_excel_data(self):
        """Load and prepare Excel data."""
        try:
            self.df, self.vendors = load_excel_data()
            if self.df is None:
                raise ValueError("Failed to load Excel data - DataFrame is None")
            # Get headers from row 1 (index 1)
            self.headers = self.df.iloc[1].tolist()
            logger.info(f"Loaded Excel with {len(self.vendors)} vendors and {len(self.headers)} columns")
        except Exception as e:
            logger.error(f"Failed to load Excel data: {e}")
            raise
    
    def _map_document_type_to_column(self, document_type: str) -> Optional[str]:
        """
        Map a document type to an Excel column header.
        
        Args:
            document_type: Type of document identified by AI
            
        Returns:
            Excel column header or None if no match
        """
        document_type_lower = document_type.lower()
        
        # Define mapping rules
        mapping_rules = {
            'soc 1': 'SOC 1',
            'soc 2': 'SOC 2', 
            'soc 3': 'SOC 3',
            'cyber': 'COI',
            'insurance': 'COI',
            'certificate': 'COI',
            'gcm': 'GCM Program',
            'disaster recovery': 'DRP',
            'brp': 'BRP',
            'gri': 'GRI',
            'oisp': 'OISP',
            'financial': 'Financial Statement',
            'audit': 'Financial Statement',
            'certificate': 'Certificates',
            'iso': 'Certificates',
            'summary': 'Summaries'
        }
        
        # Check for exact matches first
        for keyword, column in mapping_rules.items():
            if keyword in document_type_lower:
                logger.debug(f"Mapped '{document_type}' to column '{column}'")
                return column
        
        # Check for partial matches in headers
        for header in self.headers:
            if pd.notna(header):
                header_lower = str(header).lower()
                if any(keyword in header_lower for keyword in document_type_lower.split()):
                    logger.debug(f"Partial match: '{document_type}' to column '{header}'")
                    return header
        
        logger.warning(f"No column match found for document type: {document_type}")
        return None
    
    def _find_vendor_row(self, vendor_name: str) -> Optional[int]:
        """
        Find the row index for a vendor in the Excel file.
        
        Args:
            vendor_name: Name of the vendor
            
        Returns:
            Row index or None if not found
        """
        # Vendors start from row 4 (index 3)
        # But we need to check the actual Excel data, not just the vendors list
        for i in range(3, len(self.df)):  # Start from row 4 (index 3)
            cell_value = self.df.iloc[i, 0]  # First column
            if pd.notna(cell_value) and str(cell_value).strip() == vendor_name.strip():
                logger.debug(f"Found vendor '{vendor_name}' at row {i}")
                return i
        
        logger.warning(f"Vendor '{vendor_name}' not found in Excel")
        return None
    
    def _find_column_index(self, column_header: str) -> Optional[int]:
        """
        Find the column index for a header in the Excel file.
        
        Args:
            column_header: Column header name
            
        Returns:
            Column index or None if not found
        """
        for i, header in enumerate(self.headers):
            if pd.notna(header) and str(header).strip() == column_header.strip():
                logger.debug(f"Found column '{column_header}' at index {i}")
                return i
        
        logger.warning(f"Column '{column_header}' not found in Excel")
        return None
    
    def update_vendor_documents(self, vendor_folder: Path, document_analyses: Dict[str, str]) -> bool:
        """
        Update Excel file based on documents found for a vendor.
        
        Args:
            vendor_folder: Path to vendor folder
            document_analyses: Dictionary mapping document names to AI analysis
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Match vendor folder to Excel vendor
            excel_vendor = match_vendor_folder_to_excel(vendor_folder, self.vendors)
            if not excel_vendor:
                logger.warning(f"Could not match vendor folder '{vendor_folder.name}' to Excel")
                return False
            
            vendor_row = self._find_vendor_row(excel_vendor)
            if vendor_row is None:
                return False
            
            updates_made = 0
            
            # Process each document analysis
            for doc_name, analysis in document_analyses.items():
                logger.info(f"Processing document: {doc_name}")
                
                # Extract document type from analysis
                document_type = self._extract_document_type(analysis)
                if not document_type:
                    logger.warning(f"Could not extract document type from analysis for {doc_name}")
                    continue
                
                # Map to Excel column
                column_header = self._map_document_type_to_column(document_type)
                if not column_header:
                    logger.warning(f"Could not map document type '{document_type}' to Excel column")
                    continue
                
                # Find column index
                column_index = self._find_column_index(column_header)
                if column_index is None:
                    continue
                
                # Update Excel cell with checkmark
                self.df.iloc[vendor_row, column_index] = "✔️"
                updates_made += 1
                logger.info(f"Updated {excel_vendor} - {column_header}: ✔️")
            
            # Save all summaries for this vendor after processing is complete
            for doc_name, analysis in document_analyses.items():
                self.save_summary(excel_vendor, doc_name, analysis)
            
            logger.info(f"Made {updates_made} updates for vendor {excel_vendor}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update vendor documents for {vendor_folder.name}: {e}")
            return False
    
    def _extract_document_type(self, analysis: str) -> Optional[str]:
        """
        Extract document type from AI analysis.
        
        Args:
            analysis: AI analysis text
            
        Returns:
            Document type or None if not found
        """
        analysis_lower = analysis.lower()
        
        # Look for document type indicators with more specific matching
        type_indicators = [
            ('dd response', 'DD Response'),
            ('vendor dd response', 'DD Response'),
            ('due diligence response', 'DD Response'),
            ('soc 1 report', 'SOC 1'),
            ('soc 2 report', 'SOC 2'),
            ('soc 3 report', 'SOC 3'),
            ('cyber insurance certificate', 'COI'),
            ('certificate of insurance', 'COI'),
            ('business continuity plan', 'BCP'),
            ('disaster recovery plan', 'DRP'),
            ('financial statement', 'Financial Statement'),
            ('audit report', 'Financial Statement'),
            ('iso certificate', 'Certificates'),
            ('summary', 'Summaries')
        ]
        
        # Check for exact matches first (more specific)
        for indicator, column in type_indicators:
            if indicator in analysis_lower:
                logger.debug(f"Found document type: {indicator} -> {column}")
                return indicator
        
        # If no specific type found, try to extract from the analysis
        lines = analysis.split('\n')
        for line in lines:
            if 'document type' in line.lower() or 'type:' in line.lower():
                # Extract the type from the line
                parts = line.split(':')
                if len(parts) > 1:
                    return parts[1].strip()
        
        # Fallback: look for single keywords only if they appear in a document context
        single_keywords = {
            'soc 1': 'SOC 1',
            'soc 2': 'SOC 2', 
            'soc 3': 'SOC 3',
            'cyber': 'COI',
            'insurance': 'COI',
            'gcm': 'GCM Program',
            'brp': 'BRP',
            'gri': 'GRI',
            'oisp': 'OISP',
            'financial': 'Financial Statement',
            'audit': 'Financial Statement',
            'iso': 'Certificates'
        }
        
        # Only use single keywords if they appear in a document context
        for keyword, column in single_keywords.items():
            if keyword in analysis_lower and any(context in analysis_lower for context in ['document', 'report', 'certificate', 'plan']):
                logger.debug(f"Found document type (context): {keyword} -> {column}")
                return keyword
        
        return None
    
    def save_summary(self, vendor_name: str, document_name: str, summary: str) -> bool:
        """
        Save a document summary to a file in the summaries folder.
        
        Args:
            vendor_name: Name of the vendor
            document_name: Name of the document
            summary: Summary text
            
        Returns:
            True if successful, False otherwise
        """
        print(f"DEBUG: Saving summary for {vendor_name} - {document_name}")
        try:
            # Create vendor subfolder - strip whitespace to prevent path issues
            vendor_name_clean = vendor_name.strip()
            vendor_dir = self.summaries_dir / vendor_name_clean
            vendor_dir.mkdir(exist_ok=True)
            
            # Create filename from document name
            safe_doc_name = "".join(c for c in document_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_doc_name = safe_doc_name.replace(' ', '_')
            summary_file = vendor_dir / f"{safe_doc_name}_summary.txt"
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(f"Vendor: {vendor_name_clean}\n")
                f.write(f"Document: {document_name}\n")
                f.write(f"Generated: {pd.Timestamp.now()}\n")
                f.write("-" * 50 + "\n\n")
                f.write(summary)
            
            logger.info(f"Saved summary: {summary_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save summary for {vendor_name}/{document_name}: {e}")
            return False
    
    def save_excel(self) -> bool:
        """
        Save the updated Excel file as a new ResultSheet.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create new filename with ResultSheet
            result_file = self.excel_file.parent / "2025 Vendors - ResultSheet.xlsx"
            
            # Save with the new name
            self.df.to_excel(result_file, index=False, header=False)
            logger.info(f"Successfully saved result Excel file: {result_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save Excel file: {e}")
            return False
    
    def get_vendor_status(self, vendor_name: str) -> Dict[str, str]:
        """
        Get current status of a vendor in the Excel file.
        
        Args:
            vendor_name: Name of the vendor
            
        Returns:
            Dictionary mapping column headers to status (✔️, ❌, or empty)
        """
        vendor_row = self._find_vendor_row(vendor_name)
        if vendor_row is None:
            return {}
        
        status = {}
        for i, header in enumerate(self.headers):
            if pd.notna(header):
                cell_value = self.df.iloc[vendor_row, i]
                status[header] = str(cell_value) if pd.notna(cell_value) else ""
        
        return status

    def clear_vendor_checks(self):
        # For all vendor rows and all relevant columns, set to blank
        for row in range(3, len(self.df)):
            for col in range(1, len(self.headers)):  # Assuming first column is vendor name
                self.df.iloc[row, col] = ""
