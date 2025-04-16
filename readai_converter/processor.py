"""Core converter implementation."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Protocol

from .config import ConversionConfig, OutputFormat
from .markdown_generator import MarkdownGenerator
import re


class ProgressCallback(Protocol):
    """Protocol for progress callbacks."""
    
    def __call__(
        self,
        stage: str,
        progress: float,
        message: str,
        details: Optional[dict] = None
    ) -> None:
        """Called to report progress.
        
        Args:
            stage: Current processing stage
            progress: Progress as float between 0 and 1
            message: Human-readable status message
            details: Optional additional details
        """
        ...


class MeetingConverter:
    """Main converter class."""
    
    def __init__(
        self,
        config: ConversionConfig,
        callback: Optional[ProgressCallback] = None
    ):
        """Initialize the converter.
        
        Args:
            config: Conversion configuration
            callback: Optional progress callback
        """
        self.config = config
        self.callback = callback
    
    def _notify_progress(
        self,
        stage: str,
        progress: float,
        message: str,
        details: Optional[dict] = None
    ) -> None:
        """Notify progress callback if set."""
        if self.callback:
            self.callback(stage, progress, message, details)
            
    def _load_json_data(self) -> dict:
        """Load and parse the JSON file.
        
        Returns:
            Parsed JSON data with Unix timestamps
        """
        self._notify_progress('json', 0.0, 'Loading JSON data')
        with open(self.config.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Convert ISO timestamps to Unix timestamps
        start_time = datetime.fromisoformat(data['start_time']).timestamp()
        end_time = datetime.fromisoformat(data['end_time']).timestamp()
        data['start_time'] = int(start_time)
        data['end_time'] = int(end_time)
            
        self._notify_progress('json', 1.0, 'JSON data loaded')
        return data
    
    def _parse_timestamp(self, ts_str: str) -> int:
        """Parse MM:SS format timestamp into seconds from start.
        
        Args:
            ts_str: Timestamp string in MM:SS format
            
        Returns:
            Seconds from meeting start
        """
        try:
            minutes, seconds = map(int, ts_str.split(':'))
            return minutes * 60 + seconds
        except ValueError:
            return 0
    
    def _load_transcript(self) -> list[dict]:
        """Load and parse the transcript file.
        
        Returns:
            List of transcript entries
        """
        self._notify_progress('transcript', 0.0, 'Loading transcript')
        
        entries = []
        current_speaker = None
        current_text = []
        current_timestamp = None
        
        with open(self.config.transcript_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # regex to match timestamp from start of line, assume that minutes maybe any number
        timestamp_regex = re.compile(r'^(\d+:\d{2}) - (.+)$')
        for line in lines:
            # first few lines maybe header and they will get skipped
            # because we will not have current_speaker set
            line = line.strip()
            if not line:
                # Empty line - save current entry if we have one
                if current_speaker and current_text:
                    entries.append({
                        'speaker': current_speaker,
                        'text': ' '.join(current_text),
                        'timestamp': current_timestamp
                    })
                    current_speaker = None
                    current_text = []
                    current_timestamp = None
                continue
                
            # Check if this is a timestamp line
            match = timestamp_regex.match(line)
            if match:
                timestamp, speaker = match.groups()
                # Save previous entry if we have one
                # this should not happen as usually there is a blank line
                # before start of new tmestamped entry
                if current_speaker and current_text:
                    entries.append({
                        'speaker': current_speaker,
                        'text': ' '.join(current_text),
                        'timestamp': current_timestamp
                    })
                
                # Parse new timestamp line
                try:
                    current_timestamp = self._parse_timestamp(timestamp)
                    current_speaker = speaker.strip()
                    current_text = []
                except ValueError:
                    current_text.append(line)
            else:
                # Continuation of current text
                if current_speaker:
                    current_text.append(line)
                
        # Add final entry
        if current_speaker and current_text:
            entries.append({
                'speaker': current_speaker,
                'text': ' '.join(current_text),
                'timestamp': current_timestamp
            })
            
        self._notify_progress('transcript', 1.0, 'Transcript loaded')
        return entries
    
    def convert(self) -> None:
        """Convert meeting data to output formats."""
        # Load data
        data = self._load_json_data()
        self.start_time = data['start_time']  # Store for timestamp conversion
        transcript = self._load_transcript()
        
        # Generate markdown
        if self.config.output_format in [OutputFormat.MARKDOWN, OutputFormat.BOTH]:
            self._notify_progress('convert', 0.3, 'Generating Markdown')
            generator = MarkdownGenerator(
                title=data['title'],
                start_time=data['start_time'],
                end_time=data['end_time'],
                participants=data['participants'],
                summary=data['summary'],
                transcript=transcript,
                timestamp_format=self.config.timestamp_format.value
            )
            
            md_path = self.config.output_dir / f"{data['title']}.md"
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(generator.generate())
                
        # Generate PDF
        if self.config.output_format in [OutputFormat.PDF, OutputFormat.BOTH]:
            self._notify_progress('convert', 0.6, 'Generating PDF')
            # TODO: Implement PDF generation
            
        self._notify_progress('convert', 1.0, 'Conversion complete')
