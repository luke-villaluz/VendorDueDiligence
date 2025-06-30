"""
Configuration settings for Vendor Due Diligence Automation Tool.
"""
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables with error handling
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")
    print("Using default configuration values")

class Settings:
    """Application settings and configuration."""
    
    def __init__(self):
        # Base paths
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "data"
        self.vendor_dir = self.data_dir / "2025 Vendor Due Diligence"
        self.excel_file = self.data_dir / "2025 Vendors - Information Received.xlsx"
        self.logs_dir = self.project_root / "logs"
        
        # Ensure directories exist
        self.logs_dir.mkdir(exist_ok=True)
        
        # Logging configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = self.logs_dir / "vendor_dd.log"
        
        # Ollama configuration
        self.ollama_model = os.getenv("OLLAMA_MODEL", "tinyllama")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_timeout = int(os.getenv("OLLAMA_TIMEOUT", "300"))
        
        # Processing configuration
        self.max_file_size_mb = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
        self.supported_extensions = [".pdf", ".PDF"]
        
        # Vendor processing range
        self.start_vendor = int(os.getenv("START_VENDOR", "0"))
        self.end_vendor = int(os.getenv("END_VENDOR", "0"))  # 0 means process all
        
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
        
    def validate_paths(self) -> bool:
        """Validate that required paths exist."""
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")
        
        if not self.vendor_dir.exists():
            raise FileNotFoundError(f"Vendor directory not found: {self.vendor_dir}")
            
        if not self.excel_file.exists():
            raise FileNotFoundError(f"Excel file not found: {self.excel_file}")
            
        return True

# Global settings instance
settings = Settings()
