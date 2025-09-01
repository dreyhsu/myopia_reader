"""
PDF Processing Component for Myopia Reader
Extracts text content from PDF files with error handling and structure preservation.
"""

import os
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
import PyPDF2
import pdfplumber
import fitz  # PyMuPDF

class PDFProcessor:
    """
    Main PDF processing class that handles text extraction from PDF files.
    Supports multiple PDF libraries for better compatibility and error handling.
    """
    
    def __init__(self, log_level: str = "INFO"):
        """Initialize PDF processor with logging configuration."""
        self.setup_logging(log_level)
        self.logger = logging.getLogger(__name__)
        
    def setup_logging(self, level: str):
        """Configure logging for the PDF processor."""
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def validate_pdf_file(self, file_path: str) -> bool:
        """
        Validate if the file exists and is a valid PDF.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            bool: True if valid PDF file, False otherwise
        """
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return False
            
        if not file_path.lower().endswith('.pdf'):
            self.logger.error(f"Not a PDF file: {file_path}")
            return False
            
        try:
            # Quick validation by trying to open with PyPDF2
            with open(file_path, 'rb') as file:
                PyPDF2.PdfReader(file)
            return True
        except Exception as e:
            self.logger.error(f"Invalid PDF file {file_path}: {str(e)}")
            return False
    
    def extract_text_pypdf2(self, file_path: str) -> Optional[str]:
        """
        Extract text using PyPDF2 library.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            str: Extracted text or None if extraction fails
        """
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Check if PDF is encrypted
                if pdf_reader.is_encrypted:
                    self.logger.warning(f"PDF is encrypted: {file_path}")
                    return None
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num + 1} ---\n"
                            text += page_text
                    except Exception as e:
                        self.logger.warning(f"Error extracting page {page_num + 1}: {str(e)}")
                        continue
                        
            return text.strip() if text.strip() else None
            
        except Exception as e:
            self.logger.error(f"PyPDF2 extraction failed for {file_path}: {str(e)}")
            return None
    
    def extract_text_pdfplumber(self, file_path: str) -> Optional[str]:
        """
        Extract text using pdfplumber library (better for complex layouts).
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            str: Extracted text or None if extraction fails
        """
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num + 1} ---\n"
                            text += page_text
                    except Exception as e:
                        self.logger.warning(f"Error extracting page {page_num + 1}: {str(e)}")
                        continue
                        
            return text.strip() if text.strip() else None
            
        except Exception as e:
            self.logger.error(f"pdfplumber extraction failed for {file_path}: {str(e)}")
            return None
    
    def extract_text_pymupdf(self, file_path: str) -> Optional[str]:
        """
        Extract text using PyMuPDF (fastest option).
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            str: Extracted text or None if extraction fails
        """
        try:
            text = ""
            pdf_document = fitz.open(file_path)
            
            for page_num in range(pdf_document.page_count):
                try:
                    page = pdf_document[page_num]
                    page_text = page.get_text()
                    if page_text:
                        text += f"\n--- Page {page_num + 1} ---\n"
                        text += page_text
                except Exception as e:
                    self.logger.warning(f"Error extracting page {page_num + 1}: {str(e)}")
                    continue
            
            pdf_document.close()
            return text.strip() if text.strip() else None
            
        except Exception as e:
            self.logger.error(f"PyMuPDF extraction failed for {file_path}: {str(e)}")
            return None
    
    def extract_text(self, file_path: str, preferred_method: str = "auto") -> Optional[str]:
        """
        Extract text from PDF using multiple libraries as fallback.
        
        Args:
            file_path: Path to the PDF file
            preferred_method: Preferred extraction method ("auto", "pypdf2", "pdfplumber", "pymupdf")
            
        Returns:
            str: Extracted text or None if all methods fail
        """
        if not self.validate_pdf_file(file_path):
            return None
        
        self.logger.info(f"Starting text extraction from: {file_path}")
        
        # Define extraction methods in order of preference
        methods = {
            "pymupdf": self.extract_text_pymupdf,
            "pdfplumber": self.extract_text_pdfplumber,
            "pypdf2": self.extract_text_pypdf2
        }
        
        # If specific method requested, try it first
        if preferred_method in methods:
            text = methods[preferred_method](file_path)
            if text:
                self.logger.info(f"Successfully extracted text using {preferred_method}")
                return text
            else:
                self.logger.warning(f"{preferred_method} failed, trying other methods...")
        
        # Try all methods as fallback
        for method_name, method_func in methods.items():
            if preferred_method == method_name:
                continue  # Skip if already tried
                
            self.logger.info(f"Attempting extraction with {method_name}")
            text = method_func(file_path)
            
            if text:
                self.logger.info(f"Successfully extracted text using {method_name}")
                return text
            else:
                self.logger.warning(f"{method_name} extraction failed")
        
        self.logger.error(f"All extraction methods failed for: {file_path}")
        return None
    
    def get_pdf_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            dict: PDF metadata information
        """
        metadata = {
            "title": None,
            "author": None,
            "subject": None,
            "creator": None,
            "producer": None,
            "creation_date": None,
            "modification_date": None,
            "page_count": 0,
            "file_size": 0
        }
        
        try:
            # Get file size
            metadata["file_size"] = os.path.getsize(file_path)
            
            # Try PyPDF2 for metadata
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata["page_count"] = len(pdf_reader.pages)
                
                if pdf_reader.metadata:
                    metadata.update({
                        "title": pdf_reader.metadata.get('/Title'),
                        "author": pdf_reader.metadata.get('/Author'),
                        "subject": pdf_reader.metadata.get('/Subject'),
                        "creator": pdf_reader.metadata.get('/Creator'),
                        "producer": pdf_reader.metadata.get('/Producer'),
                        "creation_date": pdf_reader.metadata.get('/CreationDate'),
                        "modification_date": pdf_reader.metadata.get('/ModDate')
                    })
                    
        except Exception as e:
            self.logger.warning(f"Could not extract metadata from {file_path}: {str(e)}")
        
        return metadata
    
    def clean_extracted_text(self, text: str) -> str:
        """
        Clean and format extracted text for better readability.
        
        Args:
            text: Raw extracted text
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                cleaned_lines.append(line)
        
        # Join lines with single newlines
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Remove multiple consecutive newlines
        while '\n\n\n' in cleaned_text:
            cleaned_text = cleaned_text.replace('\n\n\n', '\n\n')
        
        return cleaned_text
    
    def save_to_file(self, text: str, output_path: str, encoding: str = 'utf-8') -> bool:
        """
        Save extracted text to a file.
        
        Args:
            text: Text content to save
            output_path: Full path where to save the file
            encoding: File encoding (default: utf-8)
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            # Ensure output directory exists
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding=encoding) as file:
                file.write(text)
            
            self.logger.info(f"Text saved to: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save text to {output_path}: {str(e)}")
            return False
    
    def process_pdf(self, file_path: str, clean_text: bool = True, save_to_output: bool = False, output_dir: str = "output") -> Dict[str, Any]:
        """
        Complete PDF processing: extract text, metadata, and clean text.
        
        Args:
            file_path: Path to the PDF file
            clean_text: Whether to clean the extracted text
            save_to_output: Whether to save extracted text to output folder
            output_dir: Directory to save output files (default: "output")
            
        Returns:
            dict: Processing results containing text, metadata, and status
        """
        result = {
            "success": False,
            "file_path": file_path,
            "text": None,
            "metadata": {},
            "error": None,
            "output_file": None
        }
        
        try:
            # Extract metadata
            result["metadata"] = self.get_pdf_metadata(file_path)
            
            # Extract text
            raw_text = self.extract_text(file_path)
            
            if raw_text:
                result["text"] = self.clean_extracted_text(raw_text) if clean_text else raw_text
                result["success"] = True
                self.logger.info(f"Successfully processed PDF: {file_path}")
                
                # Save to output file if requested
                if save_to_output and result["text"]:
                    pdf_name = Path(file_path).stem
                    output_filename = f"{pdf_name}_extracted.txt"
                    output_path = Path(output_dir) / output_filename
                    
                    if self.save_to_file(result["text"], str(output_path)):
                        result["output_file"] = str(output_path)
                    
            else:
                result["error"] = "Text extraction failed"
                self.logger.error(f"Failed to extract text from: {file_path}")
                
        except Exception as e:
            result["error"] = str(e)
            self.logger.error(f"Error processing PDF {file_path}: {str(e)}")
        
        return result


def main():
    """Example usage of the PDF processor."""
    processor = PDFProcessor()
    
    # Example: Process a PDF file and save to output folder
    pdf_path = r"C:\Users\Drey\Documents\Python_Scripts\myopia_reader\pdf\Trade+Your+Way+to+Financial+Freedom+by+Van+Tharp.pdf"
    
    if os.path.exists(pdf_path):
        print("Processing PDF file...")
        result = processor.process_pdf(pdf_path, save_to_output=True)
        
        if result["success"]:
            print(f"✓ Successfully processed: {pdf_path}")
            print(f"  Pages: {result['metadata']['page_count']}")
            print(f"  File size: {result['metadata']['file_size']} bytes")
            print(f"  Text length: {len(result['text'])} characters")
            
            if result["output_file"]:
                print(f"  Saved to: {result['output_file']}")
            
            # Show first 500 characters
            print("\nFirst 500 characters:")
            print("-" * 50)
            print(result["text"][:500] + "..." if len(result["text"]) > 500 else result["text"])
        else:
            print(f"✗ Failed to process: {pdf_path}")
            print(f"  Error: {result['error']}")
    else:
        print(f"PDF file not found: {pdf_path}")


if __name__ == "__main__":
    main()