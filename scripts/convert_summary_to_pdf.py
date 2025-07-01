#!/usr/bin/env python3
"""
Script to convert summary.txt files to PDF format.
Usage: python scripts/convert_summary_to_pdf.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.core.pdf_generator import PDFGenerator
from src.utils.logger import logger


def main():
    """Convert summary.txt files to PDF format."""
    
    # Path to the DTCC summary file
    summary_file = Path("data/summaries/DTCC (Omgeo)/DTCC_Omgeo_Summary_summary.txt")
    
    if not summary_file.exists():
        logger.error(f"Summary file not found: {summary_file}")
        return
    
    # Initialize PDF generator
    pdf_generator = PDFGenerator()
    
    # Generate PDF
    logger.info(f"Converting {summary_file} to PDF...")
    pdf_path = pdf_generator.generate_pdf_from_summary(summary_file)
    
    if pdf_path:
        logger.info(f"Successfully created PDF: {pdf_path}")
        logger.info(f"PDF saved to: {pdf_path.absolute()}")
    else:
        logger.error("Failed to generate PDF")


if __name__ == "__main__":
    main() 