# Myopia Reader Project - Component Breakdown

## Project Overview
A PDF ebook reader application that displays text in a dark theme with large fonts (similar to Edge browser's read mode) and generates audiobook files for each chapter.

## Key Features
- PDF text extraction and display
- Dark theme with large, readable fonts, User can adjust the font size
- Chapter-based text-to-speech audio generation
- Clean, accessible reading interface
- Audio file management and playback

## Component Architecture

### 1. PDF Processing Component
**Purpose**: Extract text content from PDF files
**Key Functions**:
- Load and parse PDF files
- Extract text while preserving structure
- Handle different PDF formats and encodings
- Error handling for corrupted or protected PDFs

**Dependencies**: PyPDF2, pdfplumber, or similar PDF processing library
**Input**: PDF file path
**Output**: Structured text content

### 2. Text Parser Component
**Purpose**: Organize extracted text into chapters and sections
**Key Functions**:
- Identify chapter boundaries using headings, page breaks, or patterns
- Split text into manageable sections
- Clean and format text for display and TTS
- Handle various chapter numbering schemes

**Input**: Raw extracted text
**Output**: Organized chapter/section data structure

### 3. Display Engine Component
**Purpose**: Render text with optimal reading experience
**Key Functions**:
- Dark theme styling (dark background, light text)
- Large, readable font rendering for myopia without glasses
- Text flow and pagination
- Smooth scrolling and navigation
- Responsive layout for different screen sizes

**Technologies**: HTML/CSS styling or native GUI framework
**Features**:
- Adjustable font size (default to largest readable size)
- High contrast color scheme
- Comfortable line spacing and margins
- Chapter navigation controls

### 4. Text-to-Speech Component
**Purpose**: Convert text to audio files
**Key Functions**:
- Generate natural-sounding speech from text
- Process each chapter separately
- Handle punctuation, formatting, and special characters
- Support multiple voice options and languages

**Dependencies**: pyttsx3, gTTS, or Azure/Google TTS APIs
**Input**: Chapter text content
**Output**: Audio files (MP3, WAV, etc.)

### 5. Audio Management Component
**Purpose**: Organize and manage generated audio files
**Key Functions**:
- Save audio files with meaningful names (e.g., "Chapter_01.mp3")
- Create audio file directory structure
- Track generation progress and status
- Provide audio playback controls
- Manage file cleanup and organization

**File Structure**:
```
/audio_files/
  ├── [book_title]/
    ├── Chapter_01.mp3
    ├── Chapter_02.mp3
    └── ...
```

### 6. User Interface Component
**Purpose**: Main application interface and user interaction
**Key Functions**:
- File selection dialog for PDF input
- Reading view with text display
- Navigation controls (next/previous chapter)
- Audio generation and playback controls
- Progress indicators for long operations

**Layout Sections**:
- Menu bar with file operations
- Main reading area
- Chapter navigation sidebar
- Audio controls panel
- Status bar for operations

### 7. Settings Component
**Purpose**: User preferences and configuration
**Key Functions**:
- Font size and family selection
- Theme customization (color schemes)
- TTS voice and speed settings
- Audio format preferences
- Default directories for files

**Configuration Options**:
- Display settings (font, colors, layout)
- Audio settings (voice, speed, format)
- File management (default paths, naming conventions)
- Performance settings (chunk sizes, concurrent processing)

## Technical Implementation Plan

### Phase 1: Core PDF Processing
1. PDF text extraction functionality
2. Basic text cleaning and formatting
3. Simple chapter detection

### Phase 2: Display Engine
1. Dark theme text renderer
2. Large font display optimization
3. Basic navigation controls

### Phase 3: Audio Generation
1. Text-to-speech integration
2. Chapter-based audio file generation
3. File organization system

### Phase 4: User Interface Integration
1. Complete GUI implementation
2. Settings and preferences
3. Error handling and user feedback

### Phase 5: Polish and Optimization
1. Performance optimization
2. Enhanced chapter detection
3. Additional customization options

## Technology Stack Recommendations

### Python-based Implementation
- **GUI Framework**: tkinter (built-in) or PyQt5/6
- **PDF Processing**: PyPDF2, pdfplumber, or pymupdf
- **Text-to-Speech**: pyttsx3 (offline) or cloud APIs
- **Audio Processing**: pydub for file manipulation
- **Styling**: Custom CSS-like styling for dark theme

### Web-based Alternative
- **Frontend**: HTML/CSS/JavaScript with Electron
- **Backend**: Node.js or Python Flask
- **PDF Processing**: PDF.js or server-side processing
- **TTS**: Web Speech API or cloud services

## File Structure
```
myopia_reader/
├── src/
│   ├── pdf_processor.py
│   ├── text_parser.py
│   ├── display_engine.py
│   ├── tts_engine.py
│   ├── audio_manager.py
│   ├── ui_manager.py
│   └── settings.py
├── resources/
│   ├── themes/
│   └── fonts/
├── audio_output/
├── tests/
└── main.py
```

## Success Criteria
- Successfully extract text from various PDF formats
- Display text in readable dark theme with large fonts
- Generate clear audio files for each chapter
- Provide intuitive user interface
- Handle errors gracefully
- Maintain good performance with large documents