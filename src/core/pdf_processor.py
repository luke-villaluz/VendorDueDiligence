"""
PDF processing module for Vendor Due Diligence Automation Tool.
"""
import PyPDF2
from pathlib import Path
from typing import List, Optional, Dict
from src.config.settings import settings
from src.utils.logger import logger
from src.utils.file_utils import validate_file_size

class PDFProcessor:
    """Handles PDF file processing and text extraction."""
    
    def __init__(self):
        self.max_file_size_mb = settings.max_file_size_mb
        self.supported_extensions = settings.supported_extensions
    
    def extract_text_from_pdf(self, pdf_path: Path) -> Optional[str]:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content or None if failed
        """
        if not pdf_path.exists():
            logger.error(f"PDF file does not exist: {pdf_path}")
            return None
        
        if not validate_file_size(pdf_path, self.max_file_size_mb):
            logger.error(f"PDF file too large: {pdf_path}")
            return None
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                if len(pdf_reader.pages) == 0:
                    logger.warning(f"PDF has no pages: {pdf_path}")
                    return None
                
                text_content = []
                total_pages = len(pdf_reader.pages)
                
                logger.info(f"Processing PDF: {pdf_path.name} ({total_pages} pages)")
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text.strip():
                            text_content.append(page_text)
                        
                        # Log progress every 10 pages
                        if page_num % 10 == 0:
                            logger.debug(f"Processed {page_num}/{total_pages} pages of {pdf_path.name}")
                            
                    except Exception as e:
                        logger.warning(f"Failed to extract text from page {page_num} of {pdf_path.name}: {e}")
                        continue
                
                full_text = '\n\n'.join(text_content)
                
                if not full_text.strip():
                    logger.warning(f"No text content extracted from PDF: {pdf_path}")
                    return None
                
                logger.info(f"Successfully extracted {len(full_text)} characters from {pdf_path.name}")
                return full_text
                
        except Exception as e:
            logger.error(f"Failed to process PDF {pdf_path}: {e}")
            return None
    
    def process_vendor_pdfs(self, vendor_folder: Path) -> Dict[str, str]:
        """
        Process all PDF files in a vendor folder.
        
        Args:
            vendor_folder: Path to vendor folder
            
        Returns:
            Dictionary mapping PDF filenames to extracted text
        """
        from src.utils.file_utils import get_pdf_files
        
        pdf_files = get_pdf_files(vendor_folder)
        if not pdf_files:
            logger.info(f"No PDF files found in {vendor_folder.name}")
            return {}
        
        extracted_texts = {}
        
        for pdf_file in pdf_files:
            logger.info(f"Processing PDF: {pdf_file.name}")
            text_content = self.extract_text_from_pdf(pdf_file)
            
            if text_content:
                extracted_texts[pdf_file.name] = text_content
            else:
                logger.warning(f"Failed to extract text from {pdf_file.name}")
        
        logger.info(f"Processed {len(extracted_texts)}/{len(pdf_files)} PDFs in {vendor_folder.name}")
        return extracted_texts
