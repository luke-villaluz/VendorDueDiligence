#!/usr/bin/env python3
"""
Development Setup Script
Run this script to set up the development environment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path(".env")
    template_file = Path("env_template.txt")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if template_file.exists():
        shutil.copy(template_file, env_file)
        print("✅ Created .env file from template")
        return True
    else:
        print("❌ env_template.txt not found")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Vendor Due Diligence Development Environment")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not Path("env").exists():
        if not run_command("python -m venv env", "Creating virtual environment"):
            sys.exit(1)
    else:
        print("✅ Virtual environment already exists")
    
    # Activate virtual environment and install requirements
    if os.name == 'nt':  # Windows
        activate_cmd = "env\\Scripts\\activate"
        pip_cmd = "env\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        activate_cmd = "source env/bin/activate"
        pip_cmd = "env/bin/pip"
    
    # Install requirements
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Create necessary directories
    directories = ["logs", "data/summaries"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Run tests
    print("\n🧪 Running tests...")
    if run_command(f"{pip_cmd} install pytest", "Installing pytest"):
        if run_command(f"{pip_cmd} run pytest", "Running tests"):
            print("✅ All tests passed")
        else:
            print("⚠️  Some tests failed - check the output above")
    
    print("\n" + "=" * 60)
    print("🎉 Development environment setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your configuration")
    print("2. Install Ollama: https://ollama.ai")
    print("3. Download AI model: ollama pull tinyllama")
    print("4. Run the application: python main.py")
    print("\nFor non-technical users:")
    print("- Double-click install.bat")
    print("- Double-click Run_Vendor_DD.bat")

if __name__ == "__main__":
    main() 