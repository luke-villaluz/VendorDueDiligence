"""
Configuration settings for Vendor Due Diligence Automation Tool.
"""
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
        
        # Processing configuration
        self.max_file_size_mb = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
        self.supported_extensions = [".pdf"]
        
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
