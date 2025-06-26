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
from src.utils.file_utils import get_vendor_folders, get_pdf_files
from src.utils.logger import logger

def count_total_pdfs(vendor_folders):
    """Count total PDFs across all vendors for progress tracking."""
    total = 0
    for folder in vendor_folders:
        total += len(get_pdf_files(folder))
    return total

def main():
    """Main function to run the vendor due diligence automation."""
    try:
        logger.info("🚀 Starting Vendor Due Diligence Automation")
        
        # ===== VENDOR RANGE SETTINGS =====
        # Set these to limit which vendors to process
        # Use 0-based indexing: 0 = first vendor, 1 = second vendor, etc.
        START_VENDOR = 14  # Start from first vendor
        END_VENDOR = 15    # Process first 5 vendors (0,1,2,3,4)
        # To process vendors 3-6: START_VENDOR = 3, END_VENDOR = 7
        # To process vendors 7-10: START_VENDOR = 7, END_VENDOR = 11
        # =================================
        
        # Initialize components
        processor = PDFProcessor()
        summarizer = Summarizer()
        updater = ExcelUpdater()
        
        # Get all vendor folders
        vendor_folders = get_vendor_folders()
        logger.info(f"📁 Found {len(vendor_folders)} vendor folders")
        
        # Limit vendors based on range
        if END_VENDOR > 0:
            vendor_folders = vendor_folders[START_VENDOR:END_VENDOR]
            logger.info(f"🎯 Processing vendors {START_VENDOR}-{END_VENDOR-1} ({len(vendor_folders)} vendors)")
        
        # Count total PDFs for progress tracking
        total_pdfs = count_total_pdfs(vendor_folders)
        logger.info(f"📄 Found {total_pdfs} total PDFs to process")
        
        # Process each vendor
        total_processed = 0
        total_documents = 0
        pdfs_processed = 0
        start_time = time.time()
        
        for i, vendor_folder in enumerate(vendor_folders, 1):
            try:
                vendor_pdfs = get_pdf_files(vendor_folder)
                if not vendor_pdfs:
                    logger.info(f"[{i}/{len(vendor_folders)}] ⚠️  {vendor_folder.name}: No PDFs")
                    continue
                
                logger.info(f"[{i}/{len(vendor_folders)}] 🔍 {vendor_folder.name}: Processing {len(vendor_pdfs)} PDFs")
                
                # Process PDFs
                texts = processor.process_vendor_pdfs(vendor_folder)
                print(f"DEBUG: {vendor_folder.name} - PDFs found: {list(texts.keys())}")
                if not texts:
                    logger.info(f"   ⚠️  No PDFs processed for {vendor_folder.name}")
                    continue
                
                pdfs_processed += len(texts)
                logger.info(f"   📄 Extracted {len(texts)} PDFs ({pdfs_processed}/{total_pdfs} total)")
                
                # Generate summaries
                logger.info(f"   🤖 Generating AI summaries...")
                analyses = summarizer.summarize_vendor_documents(vendor_folder.name, texts)
                print(f"DEBUG: {vendor_folder.name} - Summaries generated: {list(analyses.keys())}")
                if not analyses:
                    logger.info(f"   ⚠️  No summaries generated for {vendor_folder.name}")
                    continue
                
                # Update Excel
                success = updater.update_vendor_documents(vendor_folder, analyses)
                if success:
                    total_processed += 1
                    total_documents += len(analyses)
                    elapsed = time.time() - start_time
                    avg_time = elapsed / pdfs_processed if pdfs_processed > 0 else 0
                    remaining_pdfs = total_pdfs - pdfs_processed
                    eta_minutes = (remaining_pdfs * avg_time) / 60
                    
                    logger.info(f"   ✅ Successfully processed {vendor_folder.name} ({len(analyses)} documents)")
                    logger.info(f"   ⏱️  Progress: {pdfs_processed}/{total_pdfs} PDFs ({pdfs_processed/total_pdfs*100:.1f}%)")
                    logger.info(f"   🕐 ETA: ~{eta_minutes:.1f} minutes remaining")
                else:
                    logger.warning(f"   ❌ Failed to update Excel for {vendor_folder.name}")
                    
            except Exception as e:
                logger.error(f"   ❌ Error processing {vendor_folder.name}: {e}")
                continue
        
        # Save the final Excel file
        logger.info("💾 Saving final Excel file...")
        save_success = updater.save_excel()
        if save_success:
            logger.info("✅ Successfully saved ResultSheet.xlsx")
        else:
            logger.error("❌ Failed to save Excel file")
        
        # Final summary
        total_time = time.time() - start_time
        logger.info("🎉 Processing complete!")
        logger.info(f"   📊 Processed {total_processed} vendors")
        logger.info(f"   📄 Analyzed {total_documents} documents")
        logger.info(f"   ⏱️  Total time: {total_time/60:.1f} minutes")
        logger.info(f"   📁 Summaries saved to: data/summaries/")
        logger.info(f"   📊 Results saved to: data/2025 Vendors - ResultSheet.xlsx")
        
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 