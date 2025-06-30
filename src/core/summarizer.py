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
            
            response = requests.post(self.api_url, json=payload, timeout=None)
            
            if response.status_code == 200:
                result = response.json()
                combined_summary = result.get('response', '').strip()
                logger.info(f"Successfully combined {len(summaries)} summaries into {len(combined_summary)} chars")
                return combined_summary
            else:
                logger.error(f"Failed to combine summaries: {response.status_code}")
                return combined_text  # Fallback to simple concatenation
                
        except Exception as e:
            logger.error(f"Failed to combine summaries: {e}")
            return combined_text  # Fallback to simple concatenation
    
    def summarize_vendor_documents(self, vendor_name: str, document_texts: Dict[str, str]) -> Dict[str, str]:
        """
        Summarize individual documents for a vendor.
        
        Args:
            vendor_name: Name of the vendor
            document_texts: Dictionary mapping document names to text content
            
        Returns:
            Dictionary mapping document names to summaries
        """
        summaries = {}
        
        for doc_name, text in document_texts.items():
            logger.info(f"Summarizing document: {doc_name}")
            summary = self.summarize_text(text, f"Vendor: {vendor_name}")
            
            if summary:
                summaries[doc_name] = summary
                logger.info(f"Generated summary for {doc_name}: {len(summary)} chars")
            else:
                logger.warning(f"Failed to generate summary for {doc_name}")
        
        return summaries
    
    def create_vendor_summary(self, vendor_name: str, document_texts: Dict[str, str]) -> Optional[str]:
        """
        Create a numbered list summary for all possible document types (Excel columns).
        If a document is missing, put 'x'. If present, summarize it.
        Also print debug info for document matching.
        """
        if not document_texts:
            logger.warning(f"No documents to summarize for {vendor_name}")
            return None

        doc_types = [
            "DD Response", "SOC 1", "SOC 2", "SOC 3", "COI", "GCM Program", "BRP", "BCP", "GRI", "OISP", "DRP",
            "Information Security Policy", "Xponance Diverse Opportunities Fund", "SCA", "SIG", "Financial Statement",
            "Certificates", "Other", "BCP", "GCM", "Info Security", "Technology & Security", "Cybersecurity",
            "Software Development", "SOC Summary", "SOC Questions"
        ]

        # Debug: print all document filenames
        print(f"[DEBUG] Vendor '{vendor_name}' document files:")
        for doc_name in document_texts:
            print(f"  - {doc_name}")

        # Helper: normalize strings for matching
        def normalize(s):
            import re
            return re.sub(r'[^a-z0-9]', '', s.lower())

        summaries = []
        used_docs = set()
        for idx, doc_type in enumerate(doc_types, 1):
            best_match = None
            best_score = 0
            norm_type = normalize(doc_type)
            for doc_name in document_texts:
                norm_name = normalize(doc_name)
                # Score: count of doc_type words in doc_name
                score = sum(1 for word in norm_type.split() if word in norm_name)
                # Also check if doc_type is a substring
                if norm_type in norm_name:
                    score += 2
                if score > best_score:
                    best_score = score
                    best_match = doc_name
            # Debug: print matching info
            if best_match and best_score > 0:
                print(f"[DEBUG] Matched '{doc_type}' to file '{best_match}' (score {best_score})")
                used_docs.add(best_match)
                summary = self.summarize_text(document_texts[best_match], f"Vendor: {vendor_name}, Document: {best_match}")
                if summary:
                    summaries.append(f"{idx}. {doc_type}:\n{summary.strip()}\n")
                else:
                    summaries.append(f"{idx}. {doc_type}:\nx\n")
            else:
                print(f"[DEBUG] No match for '{doc_type}'")
                summaries.append(f"{idx}. {doc_type}:\nx\n")

        # Debug: print unmatched files
        unmatched = [doc for doc in document_texts if doc not in used_docs]
        if unmatched:
            print(f"[DEBUG] Unmatched files for vendor '{vendor_name}':")
            for doc in unmatched:
                print(f"  - {doc}")

        final_summary = "\n".join(summaries)
        logger.info(f"Created vendor summary for {vendor_name} with {len(summaries)} document types")
        return final_summary
