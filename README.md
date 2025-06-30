# Vendor Due Diligence Automation Tool

An AI-powered automation tool for processing vendor due diligence documents and updating Excel tracking sheets.

## 🚀 Features

- **PDF Processing**: Extracts text from vendor PDF documents
- **AI Analysis**: Uses Ollama to analyze and categorize documents
- **Excel Integration**: Updates tracking sheets with checkmarks for found document types
- **Vendor Summaries**: Generates comprehensive summaries for each vendor
- **Configurable Processing**: Control which vendors to process via environment variables
- **SharePoint Ready**: Architecture prepared for future SharePoint integration

## 📁 Project Structure

```
VendorDueDiligence/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── .env                    # Configuration file
├── README.md              # This file
├── src/
│   ├── config/
│   │   └── settings.py    # Application settings
│   ├── core/
│   │   ├── excel_updater.py      # Excel file operations
│   │   ├── pdf_processor.py      # PDF text extraction
│   │   ├── summarizer.py         # AI document analysis
│   │   └── sharepoint_client.py  # SharePoint integration (future)
│   ├── models/
│   │   └── vendor_data.py        # Data models
│   └── utils/
│       ├── file_utils.py         # File operations
│       └── logger.py             # Logging configuration
├── data/
│   ├── 2025 Vendor Due Diligence/  # Vendor folders with PDFs
│   └── 2025 Vendors - Information Received.xlsx  # Tracking sheet
├── logs/                   # Application logs
└── tests/                  # Test files
```

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Ollama

Download and install Ollama from [https://ollama.ai](https://ollama.ai)

### 3. Download AI Model

```bash
ollama pull tinyllama
```

### 4. Configure Environment

Copy the `.env` file and modify settings:

```bash
# AI Configuration
OLLAMA_MODEL=tinyllama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=300

# Processing Configuration
START_VENDOR=0      # Start from first vendor (0-based)
END_VENDOR=3        # Process first 3 vendors (set to 0 for all)
MAX_FILE_SIZE_MB=50
LOG_LEVEL=INFO
```

### 5. Prepare Data Structure

Ensure you have:
- `data/2025 Vendor Due Diligence/` folder with vendor subfolders
- `data/2025 Vendors - Information Received.xlsx` tracking sheet
- PDF documents in vendor folders

## 🚀 Usage

### Basic Usage

```bash
python main.py
```

### Configuration Options

- **Vendor Range**: Set `START_VENDOR` and `END_VENDOR` in `.env`
- **AI Model**: Change `OLLAMA_MODEL` to use different models
- **File Size**: Adjust `MAX_FILE_SIZE_MB` for larger documents
- **Logging**: Set `LOG_LEVEL` to DEBUG, INFO, WARNING, or ERROR

### Processing Flow

1. **PDF Extraction**: Extracts text from all PDFs in vendor folders
2. **AI Analysis**: Uses Ollama to analyze document content
3. **Document Classification**: Identifies document types (SOC 1, SOC 2, COI, etc.)
4. **Excel Updates**: Adds checkmarks to tracking sheet
5. **Summary Generation**: Creates comprehensive vendor summaries

## 📊 Output

- **Excel Updates**: Checkmarks added to tracking sheet
- **Vendor Summaries**: Saved to `data/summaries/` folder
- **Logs**: Detailed processing logs in `logs/vendor_dd.log`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_MODEL` | AI model to use | `tinyllama` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `START_VENDOR` | First vendor to process | `0` |
| `END_VENDOR` | Last vendor to process | `0` (all vendors) |
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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is proprietary and confidential.

## 🆘 Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   - Ensure Ollama is running: `ollama serve`
   - Check if model is downloaded: `ollama list`

2. **PDF Processing Errors**
   - Check file size limits in `.env`
   - Ensure PDFs are not password-protected

3. **Excel Update Failures**
   - Verify Excel file path and permissions
   - Check vendor name matching between folders and Excel

4. **Memory Issues**
   - Reduce `MAX_FILE_SIZE_MB` in `.env`
   - Process fewer vendors at once

### Getting Help

Check the logs in `logs/vendor_dd.log` for detailed error information.
