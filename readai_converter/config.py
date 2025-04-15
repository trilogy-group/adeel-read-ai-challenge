"""Configuration classes for the Read.AI converter."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class OutputFormat(str, Enum):
    """Output format options."""
    PDF = "pdf"
    MARKDOWN = "md"
    BOTH = "both"


class TimestampFormat(str, Enum):
    """Timestamp format options."""
    MINUTES = "minutes"
    SECONDS = "seconds"
    BOTH = "both"


@dataclass
class ConversionConfig:
    """Configuration for the conversion process."""
    # Output options (required)
    output_dir: Path
    
    # Input options (optional)
    input_dir: Optional[Path] = None
    json_file: Optional[Path] = None
    transcript_file: Optional[Path] = None
    video_file: Optional[Path] = None
    
    # Output format options
    output_format: OutputFormat = OutputFormat.BOTH
    timestamp_format: TimestampFormat = TimestampFormat.MINUTES
    include_extras: bool = True

    def validate(self) -> list[str]:
        """Validate the configuration.
        
        Returns:
            list[str]: List of validation errors, empty if valid.
        """
        errors = []
        
        # Check if either input_dir or individual files are provided
        if not self.input_dir and not all([self.json_file, self.transcript_file, self.video_file]):
            errors.append("Must provide either input_dir or all individual files")
        
        # Validate file existence if specified
        for file_path, file_type in [
            (self.json_file, "JSON"),
            (self.transcript_file, "Transcript"),
            (self.video_file, "Video")
        ]:
            if file_path and not file_path.exists():
                errors.append(f"{file_type} file not found: {file_path}")
        
        # Validate input directory if specified
        if self.input_dir and not self.input_dir.is_dir():
            errors.append(f"Input directory not found: {self.input_dir}")
        
        return errors
