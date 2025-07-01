#!/usr/bin/env python3
"""
Vendor Due Diligence GUI Application
Simple interface for non-technical users - PDF processing only
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import sys
import time
import os
import subprocess
import signal
from pathlib import Path
import shutil
import requests

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.summarizer import Summarizer
from src.core.pdf_processor import PDFProcessor
from src.core.pdf_generator import PDFGenerator
from src.utils.file_utils import get_vendor_folders, get_pdf_files
from src.utils.logger import logger
from src.config.settings import settings

class VendorDDGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vendor Due Diligence Tool")
        self.root.geometry("800x600")
        
        self.vendor_folder_path = tk.StringVar()
        self.processing = False
        self.ollama_process = None
        self.selected_vendors = []
        self.vendor_folders = []
        
        # Load settings from .env
        self.ollama_model = settings.ollama_model
        
        self.setup_ui()
        self.start_ollama()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="Vendor Due Diligence Automation", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Instructions
        instructions = ("1. Select your vendor folder (with vendor subfolders)\n"
                       "2. Choose which vendors to process\n"
                       "3. Click 'Start Processing' to generate professional PDF reports")
        ttk.Label(main_frame, text=instructions, justify=tk.LEFT).pack(pady=(0, 20))
        
        # Settings display
        settings_frame = ttk.LabelFrame(main_frame, text="Current Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Display current settings from .env
        settings_text = f"AI Model: {self.ollama_model}\n"
        settings_text += "Ollama: Auto-managed (starts/stops automatically)\n"
        settings_text += "Output: Professional PDF reports only"
        
        ttk.Label(settings_frame, text=settings_text, justify=tk.LEFT).pack()
        
        # Vendor folder selection
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=5)
        ttk.Label(folder_frame, text="Vendor Folder:").pack(side=tk.LEFT)
        ttk.Entry(folder_frame, textvariable=self.vendor_folder_path, width=50).pack(side=tk.LEFT, padx=10)
        ttk.Button(folder_frame, text="Browse", command=self.browse_vendor_folder).pack(side=tk.LEFT)
        
        # Vendor selection frame
        self.vendor_selection_frame = ttk.LabelFrame(main_frame, text="Select Vendors to Process", padding="10")
        self.vendor_selection_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Select all button
        self.select_all_button = ttk.Button(self.vendor_selection_frame, text="Select All Vendors", 
                                           command=self.select_all_vendors)
        self.select_all_button.pack(pady=(0, 10))
        
        # Vendor listbox with scrollbar
        listbox_frame = ttk.Frame(self.vendor_selection_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.vendor_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, height=10)
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.vendor_listbox.yview)
        self.vendor_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.vendor_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Process button
        self.process_button = ttk.Button(main_frame, text="Start Processing", 
                                        command=self.start_processing)
        self.process_button.pack(pady=20)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=10)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.pack(pady=5)
        
        # Log area
        ttk.Label(main_frame, text="Processing Log:").pack(anchor=tk.W, pady=(10, 5))
        self.log_text = scrolledtext.ScrolledText(main_frame, height=12)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
    def start_ollama(self):
        """Start Ollama server automatically and wait until it's ready. On Windows, launch in a new terminal window."""
        self.log_message("Starting Ollama server...")
        # Check if Ollama is already running
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                self.log_message("Ollama server already running")
                return
        except Exception:
            pass

        # Start Ollama server
        try:
            if os.name == 'nt':
                # Windows: launch in a new terminal window
                self.log_message("Launching Ollama in a new terminal window (cmd.exe)...")
                subprocess.Popen([
                    'cmd.exe', '/c', 'start', 'Ollama Server', 'cmd.exe', '/k', 'ollama serve'
                ])
            else:
                # Other OS: fallback to previous method
                self.ollama_process = subprocess.Popen(
                    ["ollama", "serve"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            self.log_message("Waiting for Ollama server to be ready...")
            # Poll the API endpoint every second for up to 15 seconds
            max_wait = 15
            for i in range(max_wait):
                try:
                    response = requests.get("http://localhost:11434/api/tags", timeout=2)
                    if response.status_code == 200:
                        self.log_message("Ollama server started and ready!")
                        return
                except Exception:
                    pass
                self.log_message(f"  ...waiting ({i+1}/{max_wait})")
                time.sleep(1)
            # If we get here, Ollama did not start in time
            self.log_message("ERROR: Ollama server did not start within 15 seconds.")
            self.log_message("Please start Ollama manually with 'ollama serve' and try again.")
            messagebox.showerror("Ollama Error", "Ollama server did not start in time. Please start it manually with 'ollama serve' and restart the tool.")
        except Exception as e:
            self.log_message(f"Warning: Could not start Ollama automatically: {e}")
            self.log_message("Please start Ollama manually with 'ollama serve'")
            messagebox.showerror("Ollama Error", f"Could not start Ollama automatically: {e}\nPlease start it manually with 'ollama serve' and restart the tool.")
    
    def stop_ollama(self):
        """Stop Ollama server automatically."""
        if self.ollama_process:
            try:
                self.ollama_process.terminate()
                self.ollama_process.wait(timeout=5)
                self.log_message("Ollama server stopped")
            except:
                self.ollama_process.kill()
                self.log_message("Ollama server force stopped")
    
    def browse_vendor_folder(self):
        folder = filedialog.askdirectory(title="Select Vendor Folder")
        if folder:
            self.vendor_folder_path.set(folder)
            self.log_message(f"Selected vendor folder: {folder}")
            self.load_vendor_list()
    
    def load_vendor_list(self):
        """Load and display the list of vendors."""
        try:
            vendor_path = Path(self.vendor_folder_path.get())
            if not vendor_path.exists():
                self.log_message("ERROR: Selected folder does not exist")
                return
            
            # Get vendor folders
            self.vendor_folders = [f for f in vendor_path.iterdir() if f.is_dir()]
            self.vendor_folders.sort(key=lambda x: x.name.lower())
            
            # Clear and populate listbox
            self.vendor_listbox.delete(0, tk.END)
            for vendor_folder in self.vendor_folders:
                self.vendor_listbox.insert(tk.END, vendor_folder.name)
            
            self.log_message(f"Found {len(self.vendor_folders)} vendor folders")
            
        except Exception as e:
            self.log_message(f"ERROR: Failed to load vendor list: {e}")
    
    def select_all_vendors(self):
        """Select all vendors in the listbox."""
        self.vendor_listbox.selection_set(0, tk.END)
        self.log_message("All vendors selected")
    
    def get_selected_vendors(self):
        """Get list of selected vendor folders."""
        selected_indices = self.vendor_listbox.curselection()
        selected_vendors = []
        for index in selected_indices:
            if index < len(self.vendor_folders):
                selected_vendors.append(self.vendor_folders[index])
        return selected_vendors
    
    def log_message(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()
        
    def update_progress(self, value):
        self.progress_var.set(value)
        self.root.update_idletasks()
        
    def validate_inputs(self):
        if not self.vendor_folder_path.get():
            messagebox.showerror("Error", "Please select a vendor folder")
            return False
        
        selected_vendors = self.get_selected_vendors()
        if not selected_vendors:
            messagebox.showerror("Error", "Please select at least one vendor to process")
            return False
        
        return True
        
    def start_processing(self):
        if self.processing or not self.validate_inputs():
            return
            
        self.processing = True
        self.process_button.config(state="disabled")
        self.update_status("Processing...")
        self.progress_var.set(0)
        self.log_text.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self.process_vendors, daemon=True)
        thread.start()
        
    def process_vendors(self):
        try:
            start_time = time.time()
            self.log_message("Starting processing...")
            self.log_message(f"Using AI model: {self.ollama_model}")
            
            # Get selected vendors
            selected_vendors = self.get_selected_vendors()
            self.log_message(f"Processing {len(selected_vendors)} selected vendors")
            
            # Initialize components
            pdf_processor = PDFProcessor()
            pdf_generator = PDFGenerator()
            
            # Process each selected vendor
            processed_vendors = 0
            
            for i, vendor_folder in enumerate(selected_vendors, 1):
                self.update_status(f"Processing vendor {i}/{len(selected_vendors)}: {vendor_folder.name}")
                
                vendor_pdfs = get_pdf_files(vendor_folder)
                if not vendor_pdfs:
                    self.log_message(f"WARNING: {vendor_folder.name}: No PDFs")
                    continue
                
                self.log_message(f"Processing {vendor_folder.name}: {len(vendor_pdfs)} PDFs")
                
                # Extract text from PDFs
                document_texts = {}
                for pdf_file in vendor_pdfs:
                    try:
                        text = pdf_processor.extract_text_from_pdf(pdf_file)
                        if text:
                            document_texts[pdf_file.name] = text
                    except Exception as e:
                        self.log_message(f"ERROR: Failed to process {pdf_file.name}")
                
                if not document_texts:
                    self.log_message(f"WARNING: No text extracted from {vendor_folder.name}")
                    continue
                
                # Generate summary
                self.log_message(f"Generating summary for {vendor_folder.name}...")
                try:
                    summarizer = Summarizer()
                    vendor_summary = summarizer.create_vendor_summary(vendor_folder.name, document_texts)
                    
                    if vendor_summary:
                        # Generate PDF report directly (no .txt file)
                        self.log_message(f"Generating PDF report for {vendor_folder.name}...")
                        try:
                            pdf_file = vendor_folder / f"{vendor_folder.name}_Summary_Report.pdf"
                            pdf_generator.generate_pdf_from_text(vendor_summary, pdf_file, f"{vendor_folder.name} - Vendor Due Diligence Summary")
                            self.log_message(f"SUCCESS: PDF report saved to {vendor_folder.name}/{pdf_file.name}")
                            processed_vendors += 1
                        except Exception as e:
                            self.log_message(f"ERROR: Failed to generate PDF for {vendor_folder.name}: {e}")
                    else:
                        self.log_message(f"ERROR: Failed to generate summary for {vendor_folder.name}")
                    
                except Exception as e:
                    self.log_message(f"ERROR: Failed to process {vendor_folder.name}: {e}")
                
                # Update progress
                progress = (i / len(selected_vendors)) * 100
                self.update_progress(progress)
            
            # Final summary
            total_time = time.time() - start_time
            self.log_message("Processing complete!")
            self.log_message(f"Processed {processed_vendors} vendors")
            self.log_message(f"Time: {total_time/60:.1f} minutes")
            self.log_message("Professional PDF reports saved in each vendor folder")
            
            self.update_status("Complete!")
            self.update_progress(100)
            messagebox.showinfo("Success", "Processing completed successfully!\n\nProfessional PDF reports saved in each vendor folder.")
            
        except Exception as e:
            self.log_message(f"FATAL ERROR: {e}")
            self.update_status("Failed")
            messagebox.showerror("Error", f"Processing failed: {e}")
            
        finally:
            self.processing = False
            self.process_button.config(state="normal")
    
    def on_closing(self):
        """Handle window closing."""
        if self.processing:
            if not messagebox.askokcancel("Quit", "Processing is still running. Do you want to quit anyway?"):
                return
        
        self.stop_ollama()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = VendorDDGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    main() 