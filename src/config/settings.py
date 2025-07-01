"""
Configuration settings for Vendor Due Diligence Automation Tool.
"""
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Explicitly load .env from project root
dotenv_path = Path(__file__).parent.parent.parent / ".env"
print(f"[DEBUG] Attempting to load .env from: {dotenv_path}")
load_dotenv(dotenv_path, override=True)

class Settings:
    """Application settings and configuration."""
    
    def __init__(self):
        # Base paths
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "data"
        self.vendor_dir = self.data_dir / "2025 Vendor Due Diligence"
        self.logs_dir = self.project_root / "logs"
        
        # Ensure directories exist
        self.logs_dir.mkdir(exist_ok=True)
        
        # Logging configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = self.logs_dir / "vendor_dd.log"
        
        # Ollama configuration
        self.ollama_model = os.getenv("OLLAMA_MODEL", "tinyllama")
        print(f"[DEBUG] GUI loaded model: {self.ollama_model}")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_timeout = int(os.getenv("OLLAMA_TIMEOUT", "300"))
        
        # Processing configuration
        self.max_file_size_mb = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
        self.supported_extensions = [".pdf", ".PDF"]
        
        # AI processing settings
        self.max_chunk_size = int(os.getenv("MAX_CHUNK_SIZE", "15000"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.3"))
        self.top_p = float(os.getenv("TOP_P", "0.9"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1000"))
        
        # Performance settings
        self.batch_size = int(os.getenv("BATCH_SIZE", "3"))
        self.delay_between_requests = float(os.getenv("DELAY_BETWEEN_REQUESTS", "1.0"))
        
        # SharePoint integration (future)
        self.sharepoint_site_url = os.getenv("SHAREPOINT_SITE_URL", "")
        self.sharepoint_client_id = os.getenv("SHAREPOINT_CLIENT_ID", "")
        self.sharepoint_client_secret = os.getenv("SHAREPOINT_CLIENT_SECRET", "")
        self.sharepoint_tenant_id = os.getenv("SHAREPOINT_TENANT_ID", "")
        
        # Output configuration
        self.save_individual_summaries = os.getenv("SAVE_INDIVIDUAL_SUMMARIES", "false").lower() == "true"
        self.save_vendor_summary = os.getenv("SAVE_VENDOR_SUMMARY", "true").lower() == "true"
        self.summary_format = os.getenv("SUMMARY_FORMAT", "markdown")
        
        # Debug: Show what was loaded for every environment variable
        print(f"[DEBUG] OLLAMA_MODEL from env: {os.getenv('OLLAMA_MODEL')}, settings.ollama_model: {self.ollama_model}")
        print(f"[DEBUG] OLLAMA_BASE_URL from env: {os.getenv('OLLAMA_BASE_URL')}, settings.ollama_base_url: {self.ollama_base_url}")
        print(f"[DEBUG] OLLAMA_TIMEOUT from env: {os.getenv('OLLAMA_TIMEOUT')}, settings.ollama_timeout: {self.ollama_timeout}")
        print(f"[DEBUG] MAX_FILE_SIZE_MB from env: {os.getenv('MAX_FILE_SIZE_MB')}, settings.max_file_size_mb: {self.max_file_size_mb}")
        print(f"[DEBUG] MAX_CHUNK_SIZE from env: {os.getenv('MAX_CHUNK_SIZE')}, settings.max_chunk_size: {self.max_chunk_size}")
        print(f"[DEBUG] TEMPERATURE from env: {os.getenv('TEMPERATURE')}, settings.temperature: {self.temperature}")
        print(f"[DEBUG] TOP_P from env: {os.getenv('TOP_P')}, settings.top_p: {self.top_p}")
        print(f"[DEBUG] MAX_TOKENS from env: {os.getenv('MAX_TOKENS')}, settings.max_tokens: {self.max_tokens}")
        print(f"[DEBUG] BATCH_SIZE from env: {os.getenv('BATCH_SIZE')}, settings.batch_size: {self.batch_size}")
        print(f"[DEBUG] DELAY_BETWEEN_REQUESTS from env: {os.getenv('DELAY_BETWEEN_REQUESTS')}, settings.delay_between_requests: {self.delay_between_requests}")
        print(f"[DEBUG] LOG_LEVEL from env: {os.getenv('LOG_LEVEL')}, settings.log_level: {self.log_level}")
        print(f"[DEBUG] SAVE_INDIVIDUAL_SUMMARIES from env: {os.getenv('SAVE_INDIVIDUAL_SUMMARIES')}, settings.save_individual_summaries: {self.save_individual_summaries}")
        print(f"[DEBUG] SAVE_VENDOR_SUMMARY from env: {os.getenv('SAVE_VENDOR_SUMMARY')}, settings.save_vendor_summary: {self.save_vendor_summary}")
        print(f"[DEBUG] SUMMARY_FORMAT from env: {os.getenv('SUMMARY_FORMAT')}, settings.summary_format: {self.summary_format}")
        print(f"[DEBUG] SHAREPOINT_SITE_URL from env: {os.getenv('SHAREPOINT_SITE_URL')}, settings.sharepoint_site_url: {self.sharepoint_site_url}")
        print(f"[DEBUG] SHAREPOINT_CLIENT_ID from env: {os.getenv('SHAREPOINT_CLIENT_ID')}, settings.sharepoint_client_id: {self.sharepoint_client_id}")
        print(f"[DEBUG] SHAREPOINT_CLIENT_SECRET from env: {os.getenv('SHAREPOINT_CLIENT_SECRET')}, settings.sharepoint_client_secret: {self.sharepoint_client_secret}")
        print(f"[DEBUG] SHAREPOINT_TENANT_ID from env: {os.getenv('SHAREPOINT_TENANT_ID')}, settings.sharepoint_tenant_id: {self.sharepoint_tenant_id}")
        
    def validate_paths(self) -> bool:
        """Validate that required paths exist."""
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")
        
        if not self.vendor_dir.exists():
            raise FileNotFoundError(f"Vendor directory not found: {self.vendor_dir}")
            
        return True

# Global settings instance
settings = Settings()
