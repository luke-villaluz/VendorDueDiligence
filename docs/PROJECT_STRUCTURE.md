# Project Structure Documentation

## Overview

This document provides a detailed breakdown of the Vendor Due Diligence project structure, explaining the purpose and organization of each component.

## Root Directory Structure

```
VendorDueDiligence/
├── 📁 .git/                    # Git version control
├── 📁 data/                    # Data storage (gitignored)
├── 📁 env/                     # Virtual environment (gitignored)
├── 📁 logs/                    # Application logs (gitignored)
├── 📁 scripts/                 # Utility scripts
├── 📁 src/                     # Source code
├── 📁 tests/                   # Test files
├── 📄 .gitignore              # Git ignore rules
├── 📄 README.md               # Main project documentation
├── 📄 USER_GUIDE.md           # User guide for non-technical users
├── 📄 PROJECT_STRUCTURE.md    # This file
├── 📄 requirements.txt        # Python dependencies
├── 📄 env_template.txt        # Environment variables template
├── 📄 main.py                 # Command-line entry point
├── 📄 vendor_dd_gui.py        # GUI application
├── 📄 Run_Vendor_DD.bat       # Windows launcher
├── 📄 install.bat             # Installation script
└── 📄 Create_Desktop_Shortcut.bat  # Desktop shortcut creator
```

## Core Application Files

### Entry Points
- **`main.py`**: Command-line interface for developers
- **`vendor_dd_gui.py`**: Graphical user interface for non-technical users
- **`Run_Vendor_DD.bat`**: Windows batch file for easy launching

### Configuration
- **`requirements.txt`**: Python package dependencies
- **`env_template.txt`**: Template for environment variables
- **`.gitignore`**: Git ignore patterns

### Documentation
- **`README.md`**: Comprehensive project documentation
- **`USER_GUIDE.md`**: Simple guide for non-technical users
- **`PROJECT_STRUCTURE.md`**: This detailed structure guide

### Setup Scripts
- **`install.bat`**: Automated installation for Windows users
- **`Create_Desktop_Shortcut.bat`**: Creates desktop shortcut

## Source Code (`src/`)

### Core Modules (`src/core/`)
- **`excel_updater.py`**: Excel file operations and updates
- **`pdf_processor.py`**: PDF text extraction
- **`pdf_generator.py`**: PDF report generation
- **`summarizer.py`**: AI-powered document analysis
- **`sharepoint_client.py`**: SharePoint integration (future)

### Configuration (`src/config/`)
- **`settings.py`**: Application settings and configuration
- **`prompts.py`**: AI prompt templates

### Models (`src/models/`)
- **`vendor_data.py`**: Data models and structures

### Utilities (`src/utils/`)
- **`file_utils.py`**: File operations and utilities
- **`logger.py`**: Logging configuration

## Scripts (`scripts/`)

### Utility Scripts
- **`convert_summary_to_pdf.py`**: Convert individual summaries to PDF
- **`convert_all_summaries_to_pdf.py`**: Batch convert all summaries
- **`demo_prompt_change.py`**: Demo script for prompt modifications

## Data Directory (`data/`)

### Structure
```
data/
├── 📁 2025 Vendor Due Diligence/    # Vendor folders with PDFs
│   ├── 📁 Vendor A/
│   │   ├── 📄 document1.pdf
│   │   └── 📄 document2.pdf
│   ├── 📁 Vendor B/
│   │   └── 📄 document1.pdf
│   └── ...
├── 📁 summaries/                    # Generated vendor summaries
├── 📄 2025 Vendors - Information Received.xlsx  # Input tracking sheet
└── 📄 2025 Vendors - ResultSheet.xlsx           # Output results
```

### Notes
- All data files are gitignored for privacy
- Vendor folders should contain subfolders (one per vendor)
- Each vendor subfolder should contain PDF documents
- Excel files track document requirements and results

## Environment Configuration

### Required Environment Variables
```bash
# AI Configuration
OLLAMA_MODEL=tinyllama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=300

# Processing Configuration
START_VENDOR=0
END_VENDOR=0
MAX_FILE_SIZE_MB=50
LOG_LEVEL=INFO
```

### Optional Settings
```bash
# AI Model Settings
MAX_CHUNK_SIZE=15000
TEMPERATURE=0.3
TOP_P=0.9
MAX_TOKENS=1000
BATCH_SIZE=3
DELAY_BETWEEN_REQUESTS=1.0

# Output Settings
SAVE_INDIVIDUAL_SUMMARIES=False
SAVE_VENDOR_SUMMARY=True
SUMMARY_FORMAT=markdown
```

## Testing (`tests/`)

### Structure
```
tests/
├── 📄 __init__.py
├── 📄 test_excel_updater.py
├── 📄 test_pdf_processor.py
├── 📄 test_summarizer.py
└── 📄 test_utils.py
```

## Logs (`logs/`)

### Log Files
- **`vendor_dd.log`**: Main application log
- **`error.log`**: Error-specific logging
- **`debug.log`**: Debug information (when enabled)

## Git Ignored Items

### Directories
- `data/`: Contains sensitive vendor data
- `env/`: Virtual environment
- `logs/`: Application logs
- `temp_processing/`: Temporary processing files
- `__pycache__/`: Python cache files

### Files
- `.env`: Environment variables (contains sensitive data)
- `*.log`: Log files
- `VendorDD_Results_*.xlsx`: Output files
- `*.tmp`: Temporary files

## Development Workflow

### For Developers
1. Clone repository
2. Create virtual environment: `python -m venv env`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `env_template.txt` to `.env` and configure
5. Run tests: `pytest`
6. Use `main.py` for command-line processing

### For Non-Technical Users
1. Download project
2. Install Python from python.org
3. Double-click `install.bat`
4. Double-click `Run_Vendor_DD.bat`
5. Follow GUI instructions

## File Naming Conventions

### Python Files
- Use snake_case for file names
- Use descriptive names that indicate purpose
- Group related functionality in modules

### Batch Files
- Use PascalCase for user-facing scripts
- Use descriptive names that indicate action
- Include version or purpose in name

### Data Files
- Use descriptive names with dates
- Include vendor names where appropriate
- Use consistent naming patterns

## Security Considerations

### Data Protection
- All vendor data is gitignored
- Environment variables contain sensitive configuration
- Temporary files are automatically cleaned up
- No data is sent to external servers

### Access Control
- Local processing only
- No network dependencies for core functionality
- Optional SharePoint integration for enterprise use

## Maintenance

### Regular Tasks
- Clean up temporary directories
- Update dependencies in requirements.txt
- Review and update documentation
- Test with new vendor data

### Backup Strategy
- Version control for code only
- Separate backup for vendor data
- Regular testing of processing pipeline 