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
from datetime import datetime

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
                response = requests.post(self.api_url, json=payload, timeout=settings.ollama_timeout)
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
        
        # ============================================================================
        # 🎯 MAIN PROMPT - CHANGE THIS TO MODIFY HOW THE AI ANALYZES DOCUMENTS
        # ============================================================================
        # 
        # This is the prompt that gets sent to the AI model (Ollama).
        # Modify the text below to change how the AI analyzes and summarizes documents.
        # 
        # Available variables you can use:
        # - {chunk_info}: Shows " (Part X of Y)" if document is split into chunks
        # - {context}: The vendor name and document context
        # - {text}: The actual document text to analyze
        #
        # ============================================================================
        
        prompt = f"""You are a vendor due diligence analyst reviewing documents for internal company use. Analyze the following document{chunk_info} and provide a brief, focused summary.

Context: {context if context else "Vendor due diligence document"}

Document text:
{text}

Please provide a concise summary (2-3 sentences maximum) in a single paragraph that:
1. Clearly identifies what type of document this is and its key purpose
2. Highlights any critical information, missing items, or follow-up actions that the Xponance team needs to be aware of
3. Mentions any deadlines, compliance issues, or concerns that require attention

Write this as one flowing paragraph without bullet points or numbered lists. Focus on actionable items and key findings that the Xponance team should follow up on. Be brief but specific.

Document Analysis:"""
        
        # ============================================================================
        # END OF MAIN PROMPT
        # ============================================================================
        
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
        
        # ============================================================================
        # 🔗 COMBINE SUMMARIES PROMPT - CHANGE THIS TO MODIFY HOW SUMMARIES ARE COMBINED
        # ============================================================================
        # 
        # This prompt is used when a document is split into multiple chunks and needs to be combined.
        # Modify the text below to change how multiple summaries are merged into one.
        #
        # Available variables:
        # - {combined_text}: The text containing all the individual summaries to combine
        #
        # ============================================================================
        
        prompt = f"""You are a vendor due diligence analyst. Combine the following summary sections into one cohesive summary:

{combined_text}

Please provide a unified summary that:
1. Eliminates redundancy
2. Maintains all key information
3. Flows logically
4. Is concise and professional

Combined Summary:"""
        
        # ============================================================================
        # END OF COMBINE SUMMARIES PROMPT
        # ============================================================================
        
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
        Create a vendor summary in the format requested by management:
        1. A list of all documents that the vendor submitted
        2. A brief summary of each document
        3. A brief overall summary outlining key items that the Xponance team needs to be aware of or to follow-up on
        """
        if not document_texts:
            logger.warning(f"No documents to summarize for {vendor_name}")
            return None

        # Debug: print all document filenames
        print(f"[DEBUG] Vendor '{vendor_name}' document files:")
        for doc_name in document_texts:
            print(f"  - {doc_name}")

        # Step 1: Create individual document summaries
        document_summaries = []
        for idx, (doc_name, text) in enumerate(document_texts.items(), 1):
            print(f"[DEBUG] Summarizing document {idx}: {doc_name}")
            
            summary = self.summarize_text(text, f"Vendor: {vendor_name}, Document: {doc_name}")
            if summary:
                document_summaries.append(f"{idx}. {doc_name}:\n    {summary.strip()}")
            else:
                logger.warning(f"Failed to generate summary for {doc_name}")

        if not document_summaries:
            logger.error(f"No summaries generated for {vendor_name}")
            return None

        # Step 2: Create overall summary with key follow-up items
        all_document_text = "\n\n".join([f"Document {i+1}: {doc_name}\n{summary}" 
                                        for i, (doc_name, summary) in enumerate(zip(document_texts.keys(), document_summaries))])
        
        overall_summary_prompt = f"""You are a vendor due diligence analyst reviewing documents for {vendor_name}. 

Based on the following document summaries, provide a brief overall summary (2-3 sentences) outlining key items that the Xponance team needs to be aware of or to follow-up on.

Document Summaries:
{all_document_text}

Please provide a concise overall summary that:
1. Identifies the most critical findings or concerns
2. Highlights any missing information or compliance gaps
3. Outlines specific follow-up actions the Xponance team should take
4. Mentions any deadlines, risks, or urgent matters

Overall Summary:"""

        try:
            payload = {
                "model": self.model,
                "prompt": overall_summary_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "max_tokens": 500
                }
            }
            
            response = requests.post(self.api_url, json=payload, timeout=None)
            
            if response.status_code == 200:
                result = response.json()
                overall_summary = result.get('response', '').strip()
            else:
                logger.error(f"Failed to generate overall summary: {response.status_code}")
                overall_summary = "Overall assessment: Review required for compliance and risk assessment."
                
        except Exception as e:
            logger.error(f"Failed to generate overall summary: {e}")
            overall_summary = "Overall assessment: Review required for compliance and risk assessment."

        # Step 3: Combine everything in the requested format
        final_summary = f"""Vendor Due Diligence Summary - {vendor_name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DOCUMENTS SUBMITTED:
{chr(10).join(document_summaries)}

OVERALL SUMMARY:
{overall_summary}"""

        logger.info(f"Created vendor summary for {vendor_name} with {len(document_summaries)} documents")
        return final_summary
