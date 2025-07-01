#!/usr/bin/env python3
"""
Script to convert all summary.txt files to PDF format.
Usage: python convert_all_summaries_to_pdf.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.pdf_generator import PDFGenerator
from src.utils.logger import logger


def find_summary_files():
    """Find all summary.txt files in the data/summaries directory."""
    summaries_dir = Path("data/summaries")
    if not summaries_dir.exists():
        logger.error(f"Summaries directory not found: {summaries_dir}")
        return []
    
    summary_files = []
    for summary_file in summaries_dir.rglob("*_summary.txt"):
        summary_files.append(summary_file)
    
    return summary_files


def main():
    """Convert all summary.txt files to PDF format."""
    
    # Find all summary files
    summary_files = find_summary_files()
    
    if not summary_files:
        logger.info("No summary files found to convert")
        return
    
    logger.info(f"Found {len(summary_files)} summary files to convert")
    
    # Initialize PDF generator
    pdf_generator = PDFGenerator()
    
    # Convert each summary file
    successful_conversions = 0
    failed_conversions = 0
    
    for i, summary_file in enumerate(summary_files, 1):
        logger.info(f"[{i}/{len(summary_files)}] Converting: {summary_file.name}")
        
        try:
            pdf_path = pdf_generator.generate_pdf_from_summary(summary_file)
            
            if pdf_path:
                logger.info(f"  ✓ Successfully created: {pdf_path.name}")
                successful_conversions += 1
            else:
                logger.error(f"  ✗ Failed to generate PDF for: {summary_file.name}")
                failed_conversions += 1
                
        except Exception as e:
            logger.error(f"  ✗ Error converting {summary_file.name}: {e}")
            failed_conversions += 1
    
    # Summary
    logger.info("=" * 50)
    logger.info("CONVERSION SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Total files processed: {len(summary_files)}")
    logger.info(f"Successful conversions: {successful_conversions}")
    logger.info(f"Failed conversions: {failed_conversions}")
    logger.info(f"Success rate: {successful_conversions/len(summary_files)*100:.1f}%")


if __name__ == "__main__":
    main() 