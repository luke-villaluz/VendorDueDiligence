"""
AI summarization module for Vendor Due Diligence Automation Tool.
"""
import requests
import json
from pathlib import Path
from typing import Dict, List, Optional
from src.config.settings import settings
from src.utils.logger import logger
import time

class Summarizer:
    """Handles AI-powered document summarization using Ollama."""
    
    def __init__(self):
        self.model = settings.ollama_model
        self.base_url = settings.ollama_base_url
        self.api_url = f"{self.base_url}/api/generate"
        
    def _check_ollama_connection(self) -> bool:
        """
        Check if Ollama is running and accessible.
        
        Returns:
            True if Ollama is available, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                logger.info("Ollama connection successful")
                return True
            else:
                logger.error(f"Ollama API returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return False
    
    def _split_text_for_summarization(self, text: str, max_chunk_size: int = 15000) -> List[str]:
        """
        Split large text into chunks suitable for summarization.
        
        Args:
            text: Text to split
            max_chunk_size: Maximum characters per chunk
            
        Returns:
            List of text chunks
        """
        if len(text) <= max_chunk_size:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= max_chunk_size:
                current_chunk += paragraph + '\n\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + '\n\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        logger.debug(f"Split text into {len(chunks)} chunks for summarization")
        return chunks
    
    def summarize_text(self, text: str, context: str = "") -> Optional[str]:
        """
        Summarize text using Ollama.
        
        Args:
            text: Text to summarize
            context: Additional context for the summarization
            
        Returns:
            Summarized text or None if failed
        """
        if not self._check_ollama_connection():
            return None
        
        if not text.strip():
            logger.warning("Empty text provided for summarization")
            return None
        
        # Split text into manageable chunks
        chunks = self._split_text_for_summarization(text)
        summaries = []
        
        for i, chunk in enumerate(chunks):
            try:
                prompt = self._create_summarization_prompt(chunk, context, i + 1, len(chunks))
                
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "max_tokens": 1000
                    }
                }
                
                logger.debug(f"Summarizing chunk {i + 1}/{len(chunks)} ({len(chunk)} chars)")
                
                chunk_start_time = time.time()
                response = requests.post(self.api_url, json=payload, timeout=None)  # No timeout
                chunk_time = time.time() - chunk_start_time
                
                logger.info(f"Chunk {i + 1}/{len(chunks)} completed in {chunk_time:.1f}s")
                
                if response.status_code == 200:
                    result = response.json()
                    summary = result.get('response', '').strip()
                    if summary:
                        summaries.append(summary)
                        logger.debug(f"Generated summary for chunk {i + 1}: {len(summary)} chars")
                    else:
                        logger.warning(f"Empty summary generated for chunk {i + 1}")
                else:
                    logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                    return None
                    
            except Exception as e:
                logger.error(f"Failed to summarize chunk {i + 1}: {e}")
                return None
        
        if not summaries:
            logger.error("No summaries generated")
            return None
        
        # Combine summaries if multiple chunks
        if len(summaries) == 1:
            final_summary = summaries[0]
        else:
            final_summary = self._combine_summaries(summaries)
        
        logger.info(f"Successfully summarized {len(text)} chars into {len(final_summary)} chars")
        return final_summary
    
    def _create_summarization_prompt(self, text: str, context: str, chunk_num: int, total_chunks: int) -> str:
        """
        Create a prompt for document analysis.
        
        Args:
            text: Text to analyze
            context: Additional context
            chunk_num: Current chunk number
            total_chunks: Total number of chunks
            
        Returns:
            Formatted prompt
        """
        chunk_info = f" (Part {chunk_num} of {total_chunks})" if total_chunks > 1 else ""
        
        prompt = f"""You are a vendor due diligence analyst. Analyze the following document{chunk_info} to identify what type of document it is and what information it contains.

Context: {context if context else "Vendor due diligence document"}

Document text:
{text}

Please identify:
1. Document type (e.g., SOC 1 Report, SOC 2 Report, Financial Statement, Cyber Insurance Certificate, etc.)
2. Report period or date
3. Key certifications or compliance information
4. Any notable findings or concerns

Document Analysis:"""
        
        return prompt
    
    def _combine_summaries(self, summaries: List[str]) -> str:
        """
        Combine multiple summaries into a final summary.
        
        Args:
            summaries: List of individual summaries
            
        Returns:
            Combined summary
        """
        combined_text = "\n\n".join(summaries)
        
        # Create a prompt to combine the summaries
        prompt = f"""You are a vendor due diligence analyst. Combine the following summary sections into one cohesive summary:

{combined_text}

Please provide a unified summary that:
1. Eliminates redundancy
2. Maintains all key information
3. Flows logically
4. Is concise and professional

Combined Summary:"""
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "max_tokens": 1500
                }
            }
            
            response = requests.post(self.api_url, json=payload, timeout=None)  # No timeout
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                logger.error(f"Failed to combine summaries: {response.status_code}")
                return "\n\n".join(summaries)  # Fallback to simple concatenation
                
        except Exception as e:
            logger.error(f"Failed to combine summaries: {e}")
            return "\n\n".join(summaries)  # Fallback to simple concatenation
    
    def summarize_vendor_documents(self, vendor_name: str, document_texts: Dict[str, str]) -> Dict[str, str]:
        """
        Summarize all documents for a vendor.
        
        Args:
            vendor_name: Name of the vendor
            document_texts: Dictionary mapping document names to text content
            
        Returns:
            Dictionary mapping document names to summaries
        """
        if not document_texts:
            logger.info(f"No documents to summarize for {vendor_name}")
            return {}
        
        summaries = {}
        context = f"Vendor: {vendor_name}"
        
        for doc_name, text_content in document_texts.items():
            logger.info(f"Summarizing document: {doc_name}")
            summary = self.summarize_text(text_content, context)
            
            if summary:
                summaries[doc_name] = summary
            else:
                logger.warning(f"Failed to summarize {doc_name}")
        
        logger.info(f"Summarized {len(summaries)}/{len(document_texts)} documents for {vendor_name}")
        return summaries
