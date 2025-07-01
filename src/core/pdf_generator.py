"""
PDF Generator module for Vendor Due Diligence Automation Tool.
Converts summary.txt files to professionally formatted PDF reports.
"""

import re
from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.utils.logger import logger


class PDFGenerator:
    """Handles PDF report generation from summary text files."""
    
    def __init__(self):
        self.page_size = letter
        self.margin = 0.75 * inch
        self.styles = self._create_styles()
        
    def _create_styles(self):
        """Create custom paragraph styles for the PDF."""
        styles = getSampleStyleSheet()
        
        # Header style
        styles.add(ParagraphStyle(
            name='CustomHeader',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            textColor=HexColor('#2E5090'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subheader style
        styles.add(ParagraphStyle(
            name='CustomSubheader',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            textColor=HexColor('#2E5090'),
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        ))
        
        # Document title style
        styles.add(ParagraphStyle(
            name='DocumentTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=16,
            textColor=HexColor('#1F4E79'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Document number style
        styles.add(ParagraphStyle(
            name='DocumentNumber',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            textColor=HexColor('#666666'),
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        ))
        
        # Document content style
        styles.add(ParagraphStyle(
            name='DocumentContent',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            textColor=black,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leftIndent=20
        ))
        
        # Meta info style
        styles.add(ParagraphStyle(
            name='MetaInfo',
            parent=styles['Normal'],
            fontSize=9,
            spaceAfter=4,
            textColor=HexColor('#666666'),
            alignment=TA_LEFT,
            fontName='Helvetica'
        ))
        
        return styles
    
    def _parse_summary_content(self, content: str) -> Tuple[str, str, str, List[Tuple[str, str]]]:
        """
        Parse the summary.txt content to extract metadata and document summaries.
        
        Returns:
            Tuple of (vendor_name, document_name, generated_date, document_summaries)
        """
        lines = content.split('\n')
        
        # Extract metadata
        vendor_name = ""
        document_name = ""
        generated_date = ""
        
        for line in lines[:10]:  # Check first 10 lines for metadata
            if line.startswith('Vendor:'):
                vendor_name = line.replace('Vendor:', '').strip()
            elif line.startswith('Document:'):
                document_name = line.replace('Document:', '').strip()
            elif line.startswith('Generated:'):
                generated_date = line.replace('Generated:', '').strip()
        
        # Extract document summaries
        document_summaries = []
        current_doc = None
        current_summary = []
        
        for line in lines:
            # Check for document number pattern (e.g., "1. filename.pdf:")
            doc_match = re.match(r'^(\d+)\.\s+(.+?):$', line.strip())
            if doc_match:
                # Save previous document if exists
                if current_doc and current_summary:
                    document_summaries.append((current_doc, '\n'.join(current_summary)))
                
                # Start new document
                current_doc = doc_match.group(2)
                current_summary = []
            elif current_doc and line.strip():
                # Add to current summary
                current_summary.append(line.strip())
        
        # Add the last document
        if current_doc and current_summary:
            document_summaries.append((current_doc, '\n'.join(current_summary)))
        
        return vendor_name, document_name, generated_date, document_summaries
    
    def _create_header(self, vendor_name: str, document_name: str, generated_date: str) -> List:
        """Create the header section of the PDF."""
        elements = []
        
        # Title
        title = f"Vendor Due Diligence Summary Report"
        elements.append(Paragraph(title, self.styles['DocumentTitle']))
        
        # Vendor and document info
        if vendor_name:
            elements.append(Paragraph(f"<b>Vendor:</b> {vendor_name}", self.styles['CustomSubheader']))
        
        if document_name:
            elements.append(Paragraph(f"<b>Document:</b> {document_name}", self.styles['MetaInfo']))
        
        if generated_date:
            elements.append(Paragraph(f"<b>Generated:</b> {generated_date}", self.styles['MetaInfo']))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_document_summary(self, doc_num: int, doc_name: str, summary: str) -> List:
        """Create a document summary section."""
        elements = []
        
        # Document number and name
        doc_header = f"{doc_num}. {doc_name}"
        elements.append(Paragraph(doc_header, self.styles['DocumentNumber']))
        
        # Summary content
        # Clean up the summary text
        clean_summary = summary.strip()
        if clean_summary:
            elements.append(Paragraph(clean_summary, self.styles['DocumentContent']))
        
        elements.append(Spacer(1, 12))
        
        return elements
    
    def generate_pdf_from_summary(self, summary_file_path: Path, output_path: Optional[Path] = None) -> Optional[Path]:
        """
        Generate a PDF report from a summary.txt file.
        
        Args:
            summary_file_path: Path to the summary.txt file
            output_path: Optional output path for the PDF
            
        Returns:
            Path to the generated PDF file, or None if failed
        """
        if not summary_file_path.exists():
            logger.error(f"Summary file does not exist: {summary_file_path}")
            return None
        
        try:
            # Read the summary content
            with open(summary_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the content
            vendor_name, document_name, generated_date, document_summaries = self._parse_summary_content(content)
            
            # Determine output path
            if output_path is None:
                output_path = summary_file_path.parent / f"{summary_file_path.stem}.pdf"
            
            # Create PDF document
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=self.page_size,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin,
                bottomMargin=self.margin
            )
            
            # Build the PDF content
            story = []
            
            # Add header
            story.extend(self._create_header(vendor_name, document_name, generated_date))
            
            # Add document summaries
            for i, (doc_name, summary) in enumerate(document_summaries, 1):
                story.extend(self._create_document_summary(i, doc_name, summary))
                
                # Add page break every 5 documents to avoid overcrowding
                if i % 5 == 0 and i < len(document_summaries):
                    story.append(PageBreak())
            
            # Build the PDF
            doc.build(story)
            
            logger.info(f"Successfully generated PDF: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to generate PDF from {summary_file_path}: {e}")
            return None
    
    def generate_pdf_from_text(self, content: str, output_path: Path, title: str = "Vendor Due Diligence Summary") -> Optional[Path]:
        """
        Generate a PDF report from text content.
        
        Args:
            content: The text content to convert
            output_path: Path for the output PDF
            title: Title for the PDF
            
        Returns:
            Path to the generated PDF file, or None if failed
        """
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=self.page_size,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin,
                bottomMargin=self.margin
            )
            
            # Build the PDF content
            story = []
            
            # Add title
            story.append(Paragraph(title, self.styles['DocumentTitle']))
            story.append(Spacer(1, 20))
            
            # Add content
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), self.styles['DocumentContent']))
                    story.append(Spacer(1, 8))
            
            # Build the PDF
            doc.build(story)
            
            logger.info(f"Successfully generated PDF: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")
            return None

    def generate_pdf_from_summaries(self, vendor_name: str, document_summaries: dict, overall_summary: str, output_path: Path, generated_date: str = None) -> Optional[Path]:
        """
        Generate a PDF report from a mapping of document names to summaries and an overall summary.
        Args:
            vendor_name: Name of the vendor
            document_summaries: Dict of {filename: summary}
            overall_summary: The overall summary paragraph
            output_path: Path for the output PDF
            generated_date: Optional generation date string
        Returns:
            Path to the generated PDF file, or None if failed
        """
        try:
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=self.page_size,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin,
                bottomMargin=self.margin
            )
            story = []
            # Title (large, bold, centered)
            story.append(Paragraph("Vendor Due Diligence Summary Report", self.styles['DocumentTitle']))
            story.append(Spacer(1, 8))
            # Vendor and timestamp
            story.append(Paragraph(f"<b>Vendor:</b> {vendor_name}", self.styles['CustomSubheader']))
            if generated_date is not None:
                story.append(Paragraph(f"<b>Generated:</b> {str(generated_date)}", self.styles['MetaInfo']))
            story.append(Spacer(1, 20))
            # Numbered list of files as headers, with summary paragraphs
            for idx, (doc_name, summary) in enumerate(document_summaries.items(), 1):
                # Numbered, bold, colored header for filename
                story.append(Paragraph(f"<font size=13 color='#2E5090'><b>{idx}. {doc_name}</b></font>", self.styles['Heading2']))
                # Clean, justified summary paragraph
                clean_summary = summary.replace('\n', ' ').replace('\r', ' ').strip()
                story.append(Paragraph(clean_summary, self.styles['DocumentContent']))
                story.append(Spacer(1, 16))
            # Overall summary (optional, at the end)
            if overall_summary is not None and str(overall_summary).strip():
                story.append(Spacer(1, 20))
                story.append(Paragraph("<b>Overall Summary:</b>", self.styles['CustomSubheader']))
                story.append(Paragraph(str(overall_summary).strip(), self.styles['DocumentContent']))
            doc.build(story)
            logger.info(f"Successfully generated PDF: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")
            return None


def convert_summary_to_pdf(summary_file_path: Path) -> Optional[Path]:
    """
    Convenience function to convert a summary.txt file to PDF.
    
    Args:
        summary_file_path: Path to the summary.txt file
        
    Returns:
        Path to the generated PDF file, or None if failed
    """
    generator = PDFGenerator()
    return generator.generate_pdf_from_summary(summary_file_path) 