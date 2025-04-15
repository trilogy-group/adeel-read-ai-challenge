# Read.AI Meeting Converter

Convert Read.AI meeting data into structured document formats (PDF and Markdown).

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python readai-convert.py --help

# Example with directory input
python readai-convert.py --input-dir ./examples --output-dir ./output

# Example with individual files
python readai-convert.py \
  --json-file ./examples/raw_Event.json \
  --transcript-file ./examples/transcript.txt \
  --output-dir ./output
```

## Sample Data

The `examples` directory contains sample data files:
- `raw_Event.json`: Example Read.AI meeting event data
- `transcript.txt`: Example meeting transcript

Note: For video synchronization testing, you'll need to provide your own MP4 recording file that matches the meeting duration in the JSON file.
