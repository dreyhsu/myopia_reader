# PDF Processor Documentation

## Overview
The PDF Processor is a comprehensive Python component designed for extracting text content from PDF files with advanced chapter detection and organized file output. It supports multiple PDF libraries for maximum compatibility and includes robust error handling.

## Features

### Core Functionality
- **Multi-library Support**: Uses PyPDF2, pdfplumber, and PyMuPDF (fitz) with automatic fallback
- **Encrypted PDF Detection**: Handles password-protected PDFs gracefully
- **Metadata Extraction**: Retrieves PDF metadata including title, author, creation date, etc.
- **Text Cleaning**: Removes excessive whitespace and formats text for readability
- **Logging**: Comprehensive logging system with configurable levels

### Chapter Detection & Organization
- **Exact Chapter Matching**: Detects chapters using precise pattern matching for `CHAPTER {number}` format
- **Content Segmentation**: Splits content from one chapter marker to the next
- **Introduction Support**: Handles content before the first chapter as introduction
- **Organized Folder Structure**: Creates structured output directories

### File Output Structure
```
output/
└── {PDF_NAME}/
    ├── intro/
    │   └── introduction.txt
    ├── 01/
    │   └── chapter_1.txt
    ├── 02/
    │   └── chapter_2.txt
    └── ...
```

## Class: PDFProcessor

### Constructor
```python
PDFProcessor(log_level: str = "INFO")
```
- **log_level**: Logging level (DEBUG, INFO, WARNING, ERROR)

### Key Methods

#### Text Extraction Methods
```python
extract_text_pypdf2(file_path: str) -> Optional[str]
extract_text_pdfplumber(file_path: str) -> Optional[str]
extract_text_pymupdf(file_path: str) -> Optional[str]
extract_text(file_path: str, preferred_method: str = "auto") -> Optional[str]
```

#### Chapter Detection
```python
detect_chapters(text: str) -> List[Tuple[str, int, str]]
```
- **Input**: Full extracted text
- **Output**: List of tuples (chapter_name, chapter_index, chapter_content)
- **Pattern**: Matches lines containing exactly `CHAPTER {number}` (case-sensitive, uppercase)

#### File Organization
```python
create_chapter_folders(base_output_dir: str, pdf_name: str) -> Dict[str, str]
save_chapter_files(chapters: List[Tuple], folders: Dict, pdf_name: str) -> List[str]
```

#### Main Processing
```python
process_pdf(
    file_path: str,
    clean_text: bool = True,
    save_to_output: bool = False,
    output_dir: str = "output",
    split_chapters: bool = True
) -> Dict[str, Any]
```

### Return Structure
```python
{
    "success": bool,
    "file_path": str,
    "text": str,
    "metadata": dict,
    "chapters": List[Tuple[str, int, int]],  # (name, index, content_length)
    "saved_files": List[str],
    "error": Optional[str],
    "output_folder": Optional[str]
}
```

## Chapter Detection Logic

### Pattern Matching
- **Regex Pattern**: `^CHAPTER\\s+(\\d+)$`
- **Requirements**:
  - Line must contain only `CHAPTER` followed by space and number
  - Must be uppercase
  - No additional text on the same line
  - Numbers only (no roman numerals or words)

### Content Extraction
1. **First Pass**: Identify all chapter markers and their positions
2. **Second Pass**: Extract content between markers
3. **Introduction**: Content before first chapter becomes introduction
4. **Chapter Content**: Includes the chapter header line through to the next chapter

### Example Detection
```
✓ Matches:
- "CHAPTER 1"
- "CHAPTER 2"
- "CHAPTER 10"

✗ Does not match:
- "Chapter 1" (not uppercase)
- "CHAPTER ONE" (not a number)
- "CHAPTER 1 - Introduction" (additional text)
- "  CHAPTER 1  " (extra spacing - handled by strip())
```

## Dependencies

### Required Libraries
```python
import os
import logging
import re
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

# PDF Processing Libraries
import PyPDF2        # Basic PDF reading
import pdfplumber    # Complex layout handling
import fitz          # PyMuPDF - fastest option
```

### Installation Requirements
```bash
pip install PyPDF2 pdfplumber PyMuPDF
```

## Usage Examples

### Basic Usage
```python
from pdf_processor import PDFProcessor

processor = PDFProcessor()
result = processor.process_pdf("document.pdf", save_to_output=True)

if result["success"]:
    print(f"Processed {len(result['chapters'])} chapters")
    print(f"Output saved to: {result['output_folder']}")
```

### Custom Configuration
```python
processor = PDFProcessor(log_level="DEBUG")
result = processor.process_pdf(
    file_path="document.pdf",
    clean_text=True,
    save_to_output=True,
    output_dir="custom_output",
    split_chapters=True
)
```

### Chapter Information
```python
for chapter_name, chapter_idx, content_length in result["chapters"]:
    print(f"{chapter_name}: {content_length} characters")
```

## Error Handling

### Common Error Scenarios
- **File Not Found**: Returns error with detailed message
- **Invalid PDF**: Attempts validation before processing
- **Encrypted PDFs**: Detects and reports encryption status
- **Extraction Failures**: Tries multiple libraries as fallback
- **Permission Issues**: Handles file system permission errors

### Logging Levels
- **DEBUG**: Detailed processing information
- **INFO**: General processing steps and success messages
- **WARNING**: Non-critical issues (encrypted PDFs, page extraction failures)
- **ERROR**: Critical failures that prevent processing

## Configuration Options

### Text Processing
- **clean_text**: Remove excessive whitespace and format text
- **save_to_output**: Enable file output generation
- **split_chapters**: Enable chapter detection and splitting
- **output_dir**: Custom output directory path

### Library Preferences
The processor tries libraries in this order:
1. **PyMuPDF (fitz)**: Fastest, good for most PDFs
2. **pdfplumber**: Better for complex layouts and tables
3. **PyPDF2**: Fallback option for compatibility

## Performance Considerations

### Speed Optimization
- PyMuPDF is typically fastest for large documents
- Chapter detection is performed on cleaned text for better accuracy
- File I/O is minimized through batch operations

### Memory Usage
- Text is processed in memory before writing
- Large PDFs may require significant RAM
- Chapter content is extracted sequentially to manage memory

## Best Practices

### File Organization
- Use descriptive PDF filenames (used for folder names)
- Ensure sufficient disk space for output files
- Consider using absolute paths for reliability

### Chapter Formatting
- Ensure chapter headers follow exact format: `CHAPTER {number}`
- Use uppercase consistently
- Avoid additional text on chapter header lines
- Number chapters sequentially (1, 2, 3, ...)

### Error Recovery
- Check return status before accessing results
- Review logs for detailed error information
- Validate PDF files before bulk processing
- Handle missing dependencies gracefully

## Troubleshooting

### Common Issues
1. **No chapters detected**: Check chapter header format
2. **Missing libraries**: Install all PDF processing dependencies
3. **Permission errors**: Ensure write access to output directory
4. **Encoding issues**: PDFs with special characters may need encoding handling

### Debug Tips
- Set log level to DEBUG for detailed information
- Test with a simple PDF first
- Verify chapter header format manually
- Check file permissions and paths