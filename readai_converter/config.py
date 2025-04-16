"""Configuration classes for the Read.AI converter."""

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Tuple


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
    
    # Validation flags
    json_file_validated: bool = False
    transcript_file_validated: bool = False
    video_file_validated: bool = False

    def _find_input_files(self) -> Tuple[Optional[Path], Optional[Path], Optional[Path]]:
        """Find input files in the input directory.
        If corresponding file is already provided, use it and ignore candidates.

        Returns:
            Tuple[Optional[Path], Optional[Path], Optional[Path]]: Paths to json, transcript, and video files
        """
        if not self.input_dir:
            return None, None, None

        # Look for files by extension
        json_candidates = list(self.input_dir.glob("*.json"))
        transcript_candidates = list(self.input_dir.glob("*.txt"))
        video_candidates = list(self.input_dir.glob("*.mp4"))

        # Find first valid JSON file
        if self.json_file:
            json_file = self.json_file
        else:
            json_file = None
            for candidate in json_candidates:
                if not self._validate_json_content(candidate):  # Empty list means no errors
                    json_file = candidate
                    self.json_file_validated = True
                    break

        # Find first valid transcript file
        if self.transcript_file:
            transcript_file = self.transcript_file
        else:
            transcript_file = None
            for candidate in transcript_candidates:
                if not self._validate_transcript_content(candidate):
                    transcript_file = candidate
                    self.transcript_file_validated = True
                    break

        if self.video_file:
            video_file = self.video_file
        else:
            video_file = None
            for candidate in video_candidates:
                if candidate.exists():
                    video_file = candidate
                    self.video_file_validated = True
                    break
        return (
            json_file,
            transcript_file,
            video_file
        )

    def _validate_json_content(self, path: Path) -> list[str]:
        """Validate JSON file content.

        Args:
            path: Path to the JSON file

        Returns:
            list[str]: List of validation errors
        """
        errors = []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Check required fields
            required_fields = ['title', 'start_time', 'end_time', 'participants', 'transcript']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                errors.append(f"Missing required fields in JSON: {', '.join(missing_fields)}")
                
            # Validate transcript format if present
            if 'transcript' in data and isinstance(data['transcript'], list):
                for i, entry in enumerate(data['transcript']):
                    if not isinstance(entry, dict) or \
                       not all(key in entry for key in ['speaker', 'text', 'timestamp']):
                        errors.append(f"Invalid transcript entry at index {i}")
                        break
        except json.JSONDecodeError:
            errors.append("Invalid JSON format")
        except Exception as e:
            errors.append(f"Error reading JSON file: {str(e)}")
            
        return errors

    def _validate_transcript_content(self, path: Path) -> list[str]:
        """Validate transcript file content.

        Args:
            path: Path to the transcript file

        Returns:
            list[str]: List of validation errors
        """
        errors = []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if not lines:
                errors.append("Transcript file is empty")
                return errors

            # Find first timestamp line and validate format
            transcript_started = False
            current_speaker = None
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if not line:  # Skip empty lines
                    continue

                # Try to match timestamp line format: "M:SS - Speaker Name"
                if ' - ' in line and ':' in line.split(' - ')[0]:
                    try:
                        timestamp, speaker = line.split(' - ', 1)
                        # Validate timestamp format (M:SS)
                        minutes, seconds = timestamp.split(':')
                        int(minutes)
                        int(seconds)
                        current_speaker = speaker
                        transcript_started = True  # Found first valid timestamp
                    except ValueError:
                        if transcript_started:
                            errors.append(f"Invalid timestamp format at line {i}. Expected 'M:SS - Speaker'")
                            break
                        # If transcript hasn't started, this might be header text, skip it
                        continue
                # Once transcript has started, validate text lines
                elif transcript_started:
                    if current_speaker is None:
                        errors.append(f"Found text without speaker at line {i}")
                        break
                    # else: this is valid text for the current speaker

            if not transcript_started:
                errors.append("No valid transcript entries found. Expected format: 'M:SS - Speaker'")

        except Exception as e:
            errors.append(f"Error reading transcript file: {str(e)}")

        return errors

    def validate(self) -> list[str]:
        """Validate the configuration.
        
        Returns:
            list[str]: List of validation errors, empty if valid.
        """
        errors = []
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # If input_dir is provided, find files
        if self.input_dir:
            if not self.input_dir.is_dir():
                errors.append(f"Input directory does not exist: {self.input_dir}")
                return errors

            self.json_file, self.transcript_file, self.video_file = self._find_input_files()
            

        # Validate individual files
        if self.json_file:
            if not self.json_file_validated:
                errors.extend(self._validate_json_content(self.json_file))
        else:
            errors.append("JSON file is required")

        if self.transcript_file:
            if not self.transcript_file_validated:
                errors.extend(self._validate_transcript_content(self.transcript_file))
        else:
            errors.append("Transcript file is required")

        # Video file is optional
        if self.video_file and not self.video_file.exists():
            errors.append(f"Video file does not exist: {self.video_file}")

        return errors
        