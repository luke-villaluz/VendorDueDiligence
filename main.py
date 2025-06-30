#!/usr/bin/env python3
"""
Vendor Due Diligence Automation Tool
Main entry point - run with: python3 main.py
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.excel_updater import ExcelUpdater
from src.core.summarizer import Summarizer
from src.core.pdf_processor import PDFProcessor
from src.utils.file_utils import get_vendor_folders, get_pdf_files, match_vendor_folder_to_excel
from src.utils.logger import logger
from src.config.settings import settings

def count_total_pdfs(vendor_folders):
    """Count total PDFs across all vendors for progress tracking."""
    total = 0
    for folder in vendor_folders:
        total += len(get_pdf_files(folder))
    return total

def main():
    """Main function to run the vendor due diligence automation."""
    start_time = time.time()
    
    try:
        logger.info("Starting Vendor Due Diligence Automation")
        
        # Load Excel data
        excel_updater = ExcelUpdater()
        
        # Get vendor folders
        vendor_folders = get_vendor_folders()
        if not vendor_folders:
            logger.error("No vendor folders found")
            return
        
        # Get vendor range from .env file
        START_VENDOR = settings.start_vendor
        END_VENDOR = settings.end_vendor
        
        if END_VENDOR == 0:
            logger.info("Processing ALL vendors")
            END_VENDOR = len(vendor_folders)
        else:
            logger.info(f"Processing vendors {START_VENDOR}-{END_VENDOR-1}")
        
        # Limit vendors based on range
        vendor_folders = vendor_folders[START_VENDOR:END_VENDOR]
        logger.info(f"Processing {len(vendor_folders)} vendors (range {START_VENDOR}-{END_VENDOR-1})")
        
        # Initialize counters
        total_pdfs = 0
        pdfs_processed = 0
        total_processed = 0
        total_documents = 0
        
        # Count total PDFs first
        for vendor_folder in vendor_folders:
            vendor_pdfs = get_pdf_files(vendor_folder)
            total_pdfs += len(vendor_pdfs)
        
        logger.info(f"Found {total_pdfs} total PDFs to process")
        
        # Initialize PDF processor
        pdf_processor = PDFProcessor()
        
        # Process each vendor
        for i, vendor_folder in enumerate(vendor_folders, 1):
            vendor_pdfs = get_pdf_files(vendor_folder)
            
            if not vendor_pdfs:
                logger.info(f"[{i}/{len(vendor_folders)}] WARNING: {vendor_folder.name}: No PDFs")
                continue
            
            logger.info(f"[{i}/{len(vendor_folders)}] PROCESSING: {vendor_folder.name}: Processing {len(vendor_pdfs)} PDFs")
            
            # Process PDFs for this vendor
            document_texts = {}
            for pdf_file in vendor_pdfs:
                try:
                    text = pdf_processor.extract_text_from_pdf(pdf_file)
                    if text:
                        document_texts[pdf_file.name] = text
                        pdfs_processed += 1
                except Exception as e:
                    logger.error(f"Failed to process {pdf_file.name}: {e}")
            
            if not document_texts:
                logger.warning(f"No text extracted from PDFs in {vendor_folder.name}")
                continue
            
            logger.info(f"   Extracted {len(document_texts)} PDFs ({pdfs_processed}/{total_pdfs} total)")
            
            # Generate AI summary
            logger.info(f"   Generating AI summary for all documents...")
            try:
                summarizer = Summarizer()
                vendor_summary = summarizer.create_vendor_summary(vendor_folder.name, document_texts)
                
                if vendor_summary:
                    # Update Excel with vendor summary
                    vendor_analyses = {f"{vendor_folder.name}_Summary": vendor_summary}
                    success = excel_updater.update_vendor_documents(vendor_folder, vendor_analyses)
                    
                    if success:
                        total_processed += 1
                        total_documents += 1
                        logger.info(f"   SUCCESS: Successfully processed {vendor_folder.name} (1 vendor summary)")
                    else:
                        logger.error(f"Failed to update Excel for {vendor_folder.name}")
                else:
                    logger.error(f"Failed to generate summary for {vendor_folder.name}")
                
            except Exception as e:
                logger.error(f"Failed to process {vendor_folder.name}: {e}")
            
            # Progress update
            logger.info(f"   Progress: {pdfs_processed}/{total_pdfs} PDFs ({pdfs_processed/total_pdfs*100:.1f}%)")
            
            # Calculate ETA
            if pdfs_processed > 0:
                elapsed_time = time.time() - start_time
                avg_time_per_pdf = elapsed_time / pdfs_processed
                remaining_pdfs = total_pdfs - pdfs_processed
                eta_seconds = remaining_pdfs * avg_time_per_pdf
                eta_minutes = eta_seconds / 60
                logger.info(f"   ETA: ~{eta_minutes:.1f} minutes remaining")
        
        # Save final Excel file
        logger.info("Saving final Excel file...")
        if excel_updater.save_excel():
            logger.info("SUCCESS: Successfully saved ResultSheet.xlsx")
        else:
            logger.error("Failed to save Excel file")
        
        # Final summary
        total_time = time.time() - start_time
        logger.info("Processing complete!")
        logger.info(f"   Processed {total_processed} vendors")
        logger.info(f"   Analyzed {total_documents} vendor summaries")
        logger.info(f"   Total time: {total_time/60:.1f} minutes")
        logger.info(f"   Summaries saved to: data/summaries/")
        logger.info(f"   Results saved to: data/2025 Vendors - ResultSheet.xlsx")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 