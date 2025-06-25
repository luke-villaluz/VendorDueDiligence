"""
File utility functions for Vendor Due Diligence Automation Tool.
"""
import os
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from src.config.settings import settings
from src.utils.logger import logger

def get_vendor_folders() -> List[Path]:
    """
    Get all vendor folders from the vendor directory.
    
    Returns:
        List of vendor folder paths
    """
    if not settings.vendor_dir.exists():
        logger.error(f"Vendor directory not found: {settings.vendor_dir}")
        return []
    
    vendor_folders = [f for f in settings.vendor_dir.iterdir() if f.is_dir()]
    logger.info(f"Found {len(vendor_folders)} vendor folders")
    return vendor_folders

def get_pdf_files(folder_path: Path) -> List[Path]:
    """
    Get all PDF files from a folder.
    
    Args:
        folder_path: Path to search for PDFs
        
    Returns:
        List of PDF file paths
    """
    if not folder_path.exists():
        logger.warning(f"Folder does not exist: {folder_path}")
        return []
    
    pdf_files = list(folder_path.glob("*.pdf"))
    logger.debug(f"Found {len(pdf_files)} PDF files in {folder_path.name}")
    return pdf_files

def validate_file_size(file_path: Path, max_size_mb: Optional[int] = None) -> bool:
    """
    Validate that a file is within size limits.
    
    Args:
        file_path: Path to the file to validate
        max_size_mb: Maximum file size in MB, defaults to settings.max_file_size_mb
        
    Returns:
        True if file size is acceptable, False otherwise
    """
    if max_size_mb is None:
        max_size_mb = settings.max_file_size_mb
    
    if not file_path.exists():
        logger.warning(f"File does not exist: {file_path}")
        return False
    
    file_size_mb = file_path.stat().st_size / (1024 * 1024)
    
    if file_size_mb > max_size_mb:
        logger.warning(f"File {file_path.name} is too large: {file_size_mb:.2f}MB > {max_size_mb}MB")
        return False
    
    logger.debug(f"File {file_path.name} size: {file_size_mb:.2f}MB")
    return True

def create_summary_file(vendor_folder: Path, content: str) -> Path:
    """
    Create a summary.txt file in a vendor folder.
    
    Args:
        vendor_folder: Path to vendor folder
        content: Content to write to summary file
        
    Returns:
        Path to the created summary file
    """
    summary_file = vendor_folder / "summary.txt"
    
    try:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Created summary file: {summary_file}")
        return summary_file
    except Exception as e:
        logger.error(f"Failed to create summary file {summary_file}: {e}")
        raise

def load_excel_data() -> Tuple[pd.DataFrame, List[str]]:
    """
    Load the Excel file and extract vendor names and column headers.
    
    Returns:
        Tuple of (DataFrame, list of vendor names)
    """
    try:
        # Read Excel file without header
        df = pd.read_excel(settings.excel_file, header=None)
        
        # Get column headers from row 1 (index 1)
        headers = df.iloc[1].tolist()
        
        # Get vendor names from column 0 starting from row 4 (index 3)
        vendors = df.iloc[3:, 0].dropna().tolist()
        
        logger.info(f"Loaded Excel file with {len(vendors)} vendors and {len(headers)} columns")
        logger.debug(f"Vendors: {vendors[:5]}...")  # Log first 5 vendors
        
        return df, vendors
        
    except Exception as e:
        logger.error(f"Failed to load Excel file {settings.excel_file}: {e}")
        raise

def match_vendor_folder_to_excel(vendor_folder: Path, excel_vendors: List[str]) -> Optional[str]:
    """
    Match a vendor folder name to an Excel vendor name.
    
    Args:
        vendor_folder: Path to vendor folder
        excel_vendors: List of vendor names from Excel
        
    Returns:
        Matched Excel vendor name or None
    """
    folder_name = vendor_folder.name
    
    # Direct match
    if folder_name in excel_vendors:
        return folder_name
    
    # Partial matches (handle cases like "SS&C Advent" vs "Advent")
    for excel_vendor in excel_vendors:
        if folder_name.lower() in excel_vendor.lower() or excel_vendor.lower() in folder_name.lower():
            logger.debug(f"Matched folder '{folder_name}' to Excel vendor '{excel_vendor}'")
            return excel_vendor
    
    logger.warning(f"No Excel match found for vendor folder: {folder_name}")
    return None
