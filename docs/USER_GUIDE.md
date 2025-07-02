# Vendor Due Diligence Tool - User Guide

## For Non-Technical Users

This guide will help you run the Vendor Due Diligence tool without any coding knowledge.

## Quick Start

### Step 1: Prepare Your Files

1. **Vendor Folder**: Create a folder containing subfolders for each vendor. Each vendor subfolder should contain their PDF documents.
   ```
   My Vendor Folder/
   ├── Vendor A/
   │   ├── document1.pdf
   │   ├── document2.pdf
   │   └── ...
   ├── Vendor B/
   │   ├── document1.pdf
   │   └── ...
   └── ...
   ```

### Step 2: Run the Tool

**Option A: Double-click method (Recommended)**
1. Double-click the `windows/Run_Vendor_DD.bat` file
2. Wait for the GUI to open
3. Follow the on-screen instructions

**Option B: Manual method**
1. Open Command Prompt
2. Navigate to this folder
3. Run: `python vendor_dd_gui.py`

### Step 3: Use the Interface

1. **Select Vendor Folder**: Click "Browse" next to "Vendor Folder" and select your folder containing vendor subfolders
2. **Choose Vendors**: 
   - The tool will show you a list of all vendors found
   - Click on individual vendors to select them, or
   - Click "Select All Vendors" to process everything
3. **Start Processing**: Click "Start Processing" and wait for completion

### Step 4: Get Results

- The tool will automatically process all PDFs in your selected vendor folders
- It will generate comprehensive summaries for each vendor
- Results will be saved as professional PDF reports in each vendor folder

## What the Tool Does

1. **Reads PDFs**: Extracts text from all PDF documents in vendor folders
2. **Analyzes Content**: Uses AI to understand what each document contains
3. **Creates Summaries**: Generates detailed summaries of each vendor's documents
4. **Generates PDF Reports**: Creates professional PDF reports with the format your boss requested:
   - List of all documents submitted
   - Brief summary of each document
   - Overall summary with key items for follow-up

## Automatic Ollama Management

The tool automatically handles the Ollama AI server for you:
- **Starts automatically**: When you open the GUI, it will start Ollama if needed
- **Stops automatically**: When you close the GUI, it will stop Ollama
- **No manual work**: You don't need to run `ollama serve` or `Ctrl+C` anything

## Troubleshooting

### Common Issues

**"Python is not installed"**
- Download and install Python from https://python.org
- Make sure to check "Add Python to PATH" during installation

**"Ollama not found"**
- Download and install Ollama from https://ollama.ai
- The GUI will show a warning if Ollama isn't installed

**"No vendor folders found"**
- Make sure your vendor folder contains subfolders (not just PDF files)
- Each vendor should have their own subfolder

**"Ollama won't start automatically"**
- The GUI will show a warning message
- You can start Ollama manually by opening Command Prompt and running: `ollama serve`
- Then try the GUI again

**Processing takes a long time**
- This is normal for large numbers of PDFs
- The tool shows progress and estimated time remaining
- Don't close the window while processing

### Getting Help

If you encounter issues:
1. Check the processing log in the GUI for error messages
2. Make sure all files are in the correct format
3. Contact your IT support if Python or Ollama installation issues persist

## File Requirements

### Vendor Folder Structure
- Must contain subfolders (one per vendor)
- Each subfolder should contain PDF files
- PDF files should not be password-protected
- Maximum file size: 50MB per PDF

## Output Files

After processing, you'll find:
- Professional PDF reports in each vendor folder
- `logs/` - Processing logs for troubleshooting

## GUI Tips

- **Select All**: Use the "Select All Vendors" button to process everything at once
- **Individual Selection**: Click on specific vendors to process only those
- **Progress Tracking**: Watch the progress bar and status messages
- **Log View**: Check the processing log for detailed information
- **Auto-cleanup**: The tool automatically starts and stops Ollama for you

## Security Notes

- The tool processes files locally on your computer
- No data is sent to external servers
- Temporary files are automatically cleaned up
- Original files are never modified (only copied for processing)
- Ollama server is managed automatically and stops when you close the GUI 

## How to Launch the Tool (No Terminal Window)

1. Open your project folder in File Explorer.
2. Right-click `run_gui_silent.bat` and select 'Create shortcut'.
3. Move the shortcut to your desktop.
4. (Optional) Rename the shortcut to 'Vendor Due Diligence Tool'.
5. Double-click the shortcut to launch the app in fullscreen mode with no terminal window.

This is the recommended way for all users. You do NOT need to use any other shortcut or batch file. 