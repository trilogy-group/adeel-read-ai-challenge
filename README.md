# Read.AI Meeting Converter

Convert Read.AI meeting data into structured document formats (PDF and Markdown) with accurate timestamp synchronization and professional formatting.

## Features

- **Multiple Input Sources**: Process Read.AI JSON data, meeting transcripts, and video recordings
- **Flexible Output Formats**: Generate both PDF and Markdown documents
- **Professional PDF Generation**: Clean layout, proper typography, and organized sections
- **Accurate Timestamp Handling**: Support for various timestamp formats and synchronization
- **Rich Meeting Context**: Includes participants, summary, and full transcript
- **User-Friendly CLI**: Simple command-line interface with progress indicators

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

The converter supports both directory-based and individual file inputs:

```bash
# View all options
python readai-convert.py --help

# Convert using directory input (auto-detects files)
python readai-convert.py --input-dir ./examples --output-dir ./output

# Convert specific files (video is optional)
python readai-convert.py \
  --json-file ./examples/raw_Event.json \
  --transcript-file ./examples/transcript.txt \
  --output-dir ./output

# With video file (optional)
python readai-convert.py \
  --json-file ./examples/raw_Event.json \
  --transcript-file ./examples/transcript.txt \
  --video-file ./examples/recording.mp4 \
  --output-dir ./output

# Specify output format
python readai-convert.py --input-dir ./examples --format pdf  # or md, both

# Choose timestamp format
python readai-convert.py --input-dir ./examples --timestamp-format minutes  # or seconds
```

## Technical Approach

### Architecture

1. **Modular Design**
   - `cli.py`: Command-line interface using Click
   - `config.py`: Configuration and input validation
   - `processor.py`: Core data processing and synchronization
   - `markdown_generator.py`: Markdown document generation
   - `pdf_generator.py`: PDF document generation using ReportLab

2. **Data Flow**
   - Load and validate input files
   - Parse JSON meeting data and transcript
   - Synchronize timestamps across sources
   - Generate structured output documents

3. **Key Features**
   - Robust timestamp parsing and normalization
   - Clean handling of speaker transitions
   - Professional document formatting
   - Progress tracking and user feedback

### AI Tool Usage

This project was developed with assistance from Codeium AI, which helped with:

1. **Code Generation**
   - Initial project structure
   - PDF generation using ReportLab
   - CLI implementation with Click

2. **Problem Solving**
   - Timestamp parsing and synchronization
   - Document formatting strategies
   - Error handling approaches

3. **Code Review**
   - Identifying potential issues
   - Suggesting improvements
   - Maintaining code quality

## Sample Data

The `examples` directory contains sample files:
- `raw_Event.json`: Example Read.AI meeting event data
- `transcript.txt`: Example meeting transcript

Note: For video synchronization testing, provide your own MP4 recording file matching the meeting duration.

## Video Demo

[Video demonstration](https://drive.google.com/file/d/1a9P_2lFY4RdZATZoDpjMQAqK_KLrRRpH/view?usp=sharing)

## Future Enhancements

1. **PDF Features**
   - Table of contents
   - Page numbers and headers
   - Bookmarks for navigation
   - Custom themes and fonts

2. **Additional Features**
   - Video timestamp synchronization
   - Speaker statistics
   - Meeting analytics
   - Custom output templates
