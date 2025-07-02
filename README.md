# Vendor Due Diligence Automation Tool

An AI-powered automation tool for processing vendor due diligence PDF documents and generating comprehensive summaries and professional PDF reports.

## 🚀 Features

- **PDF Processing**: Extracts text from vendor PDF documents
- **AI Analysis**: Uses Ollama to analyze and summarize documents
- **Vendor Summaries**: Generates comprehensive summaries for each vendor
- **🆕 Professional PDF Reports**: Automatically creates beautifully formatted PDF reports from summaries
- **🆕 User-Friendly GUI**: Simple interface for non-technical users
- **🆕 One-Click Setup**: Automated installation and setup scripts
- **🆕 Automatic Ollama Management**: Starts and stops Ollama server automatically
- **🆕 Vendor Selection**: Choose specific vendors or process all at once
- **🆕 Local Summaries**: Saves summaries directly in vendor folders

## 👥 For Non-Technical Users

If you're not a programmer, you can use this tool with just a few clicks:

### Quick Start (No Coding Required)

1. **First Time Setup**: Double-click `windows/install.bat` to set up the tool
2. **Run the Tool**: Double-click `windows/Run_Vendor_DD.bat` to start
3. **Use the Interface**: 
   - Select your vendor folder (containing vendor subfolders with PDFs)
   - Choose which vendors to process (or click "Select All")
   - Click "Start Processing"
4. **Get Results**: Find professional PDF reports in each vendor folder

For detailed instructions, see [docs/USER_GUIDE.md](docs/USER_GUIDE.md)

## 🚀 How to Launch the App (For Non-Technical Users)

After setup, launching the app is easy and does not require any terminal window:

1. **Navigate to your project folder in File Explorer.**
2. **Right-click `run_gui_silent.bat` and select 'Create shortcut'.**
3. **Move the shortcut to your desktop.**
4. (Optional) Rename the shortcut to 'Vendor Due Diligence Tool'.
5. **Double-click the shortcut to launch the app in fullscreen mode with no terminal window.**

This is the most robust and user-friendly way to launch the tool. You do NOT need to use any other shortcut or batch file.

## 📁 Project Structure

```
VendorDueDiligence/
├── vendor_dd_gui.py        # 🆕 GUI application for non-technical users
├── README.md               # This file
├── .gitignore              # Git ignore rules
├── windows/                # 🆕 Windows-specific files
│   ├── Run_Vendor_DD.bat       # One-click launcher
│   ├── install.bat             # Automated installation script
│   └── Create_Desktop_Shortcut.bat  # Desktop shortcut creator
├── config/                 # 🆕 Configuration files
│   └── requirements.txt        # Python dependencies
├── docs/                   # Documentation
├── src/                    # Source code
│   ├── config/
│   │   └── settings.py    # Application settings
│   ├── core/
│   │   ├── pdf_processor.py      # PDF text extraction
│   │   ├── pdf_generator.py      # PDF report generation
│   │   ├── summarizer.py         # AI document analysis
│   │   └── sharepoint_client.py  # SharePoint integration (future)
│   ├── models/
│   │   └── vendor_data.py        # Data models
│   └── utils/
│       ├── file_utils.py         # File operations
│       └── logger.py             # Logging configuration
├── data/                   # Data storage
│   └── 2025 Vendor Due Diligence/  # Vendor folders with PDFs
│       ├── Vendor A/
│       │   ├── document1.pdf
│       │   ├── document2.pdf
│       │   └── Vendor A_Summary_Report.pdf  # 🆕 Professional PDF report
│       └── Vendor B/
│           ├── document1.pdf
│           └── Vendor B_Summary_Report.pdf  # 🆕 Professional PDF report
├── logs/                   # Application logs
├── scripts/                # Utility scripts
├── env/                    # Virtual environment (created by install.bat)
└── tests/                  # Test files
```

## 🛠️ Setup Instructions

### For Non-Technical Users

1. **Install Python**: Download from [https://python.org](https://python.org) (check "Add Python to PATH")
2. **Install Ollama**: Download from [https://ollama.ai](https://ollama.ai)
3. **Run Installation**: Double-click `windows/install.bat`
4. **Create Shortcut** (Optional): Double-click `windows/Create_Desktop_Shortcut.bat`
5. **Start Using**: Double-click `windows/Run_Vendor_DD.bat`

**Note**: The GUI will automatically start and stop the Ollama server for you.

### For Developers

#### 1. Install Dependencies

```bash
pip install -r config/requirements.txt
```

#### 2. Install Ollama

Download and install Ollama from [https://ollama.ai](https://ollama.ai)

#### 3. Download AI Model

```bash
ollama pull tinyllama
```

#### 4. Configure Environment

Copy the `env_template.txt` file to `.env` and modify settings:

```bash
# AI Configuration
OLLAMA_MODEL=tinyllama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=300

# Processing Configuration
MAX_FILE_SIZE_MB=50
LOG_LEVEL=INFO
```

#### 5. Prepare Data Structure

Ensure you have:
- `data/2025 Vendor Due Diligence/` folder with vendor subfolders
- PDF documents in vendor folders

## 🚀 Usage

### For Non-Technical Users

**GUI Method (Recommended)**
```bash
# Double-click windows/Run_Vendor_DD.bat
# Or run manually:
python vendor_dd_gui.py
```

**GUI Features:**
- **Automatic Ollama Management**: No need to manually start/stop Ollama
- **Vendor Selection**: Choose specific vendors or select all
- **Real-time Progress**: See processing status and logs
- **Local Results**: Professional PDF reports saved directly in vendor folders

### PDF Report Generation

The tool automatically generates professional PDF reports from summary files. Features include:

- **Professional Formatting**: Company branding colors and clean layout
- **Structured Content**: Clear document summaries with numbering
- **Metadata**: Vendor name, document information, generation date
- **Automatic Page Breaks**: Optimized for readability
- **Professional Typography**: Clean fonts and spacing

You can also manually convert existing summaries:

```bash
# Convert a specific summary file
python scripts/convert_summary_to_pdf.py

# Convert all summary files to PDFs
python scripts/convert_all_summaries_to_pdf.py
```

### Configuration Options

- **AI Model**: Change `OLLAMA_MODEL` to use different models
- **File Size**: Adjust `MAX_FILE_SIZE_MB` for larger documents
- **Logging**: Set `LOG_LEVEL` to DEBUG, INFO, WARNING, or ERROR

### Processing Flow

1. **PDF Extraction**: Extracts text from all PDFs in vendor folders
2. **AI Analysis**: Uses Ollama to analyze document content
3. **Summary Generation**: Creates comprehensive vendor summaries
4. **PDF Report Generation**: Automatically generates professionally formatted PDF reports

## 📊 Output

- **Professional PDF Reports**: Beautifully formatted PDF reports with company branding
- **Logs**: Detailed processing logs in `logs/vendor_dd.log`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_MODEL` | AI model to use | `tinyllama` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `MAX_FILE_SIZE_MB` | Maximum PDF file size | `50` |
| `LOG_LEVEL` | Logging level | `INFO` |

### SharePoint Integration (Future)

Add these to `.env` for SharePoint integration:

```
SHAREPOINT_SITE_URL=your-sharepoint-site-url
SHAREPOINT_CLIENT_ID=your-client-id
SHAREPOINT_CLIENT_SECRET=your-client-secret
SHAREPOINT_TENANT_ID=your-tenant-id
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src
```

## 📝 Logging

Logs are written to:
- Console: INFO level and above
- File: `logs/vendor_dd.log` (DEBUG level and above)

## 🔒 Security

- Environment variables for sensitive configuration
- File size limits to prevent memory issues
- Error handling and logging for debugging
- Local processing only - no data sent to external servers
- Automatic cleanup of temporary processes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is proprietary and confidential.

## 🆘 Troubleshooting

### For Non-Technical Users

**Common Issues:**
- **"Python is not installed"**: Download from https://python.org
- **"Ollama not found"**: Download from https://ollama.ai
- **"No vendor folders found"**: Make sure your folder contains subfolders (not just PDF files)
- **Processing takes a long time**: This is normal for large numbers of PDFs
- **Ollama won't start**: The GUI will show a warning and guide you to start it manually

**GUI Tips:**
- The GUI automatically manages Ollama - no need to run `ollama serve` manually
- Use "Select All Vendors" to process everything at once
- Check the processing log for detailed status updates
- Professional PDF reports are saved directly in vendor folders

See [docs/USER_GUIDE.md](docs/USER_GUIDE.md) for detailed troubleshooting.

### For Developers

**Common Issues**

1. **Ollama Connection Failed**
   - Ensure Ollama is installed: `ollama --version`
   - Check if model is downloaded: `ollama list`
   - GUI will attempt to start Ollama automatically

2. **PDF Processing Errors**
   - Check file size limits in `.env`
   - Ensure PDFs are not password-protected

3. **Memory Issues**
   - Reduce `MAX_FILE_SIZE_MB` in `.env`
   - Process fewer vendors at once

### Getting Help

Check the logs in `logs/vendor_dd.log` for detailed error information.
