"""Markdown document generator for meeting transcripts."""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class MarkdownGenerator:
    """Generates markdown documents from meeting data."""

    def __init__(self, 
                 title: str,
                 start_time: int,
                 end_time: int,
                 participants: List[Dict[str, str]],
                 summary: str,
                 transcript: List[Dict[str, str]],
                 timestamp_format: str = "minutes"):
        """Initialize the markdown generator.
        
        Args:
            title: Meeting title
            start_time: Start time in Unix timestamp
            end_time: End time in Unix timestamp
            participants: List of participant dictionaries with 'name' and optional 'email'/'role'
            summary: Meeting summary text
            transcript: List of transcript entries with 'speaker', 'text', and 'timestamp'
            timestamp_format: Format for timestamps ('minutes' or 'seconds')
        """
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.participants = participants
        self.summary = summary
        self.transcript = transcript
        self.timestamp_format = timestamp_format

    def _format_timestamp(self, seconds_from_start: int) -> str:
        """Format seconds from start based on configured format.
        
        Args:
            seconds_from_start: Seconds from meeting start
            
        Returns:
            Formatted timestamp string (decimal minutes or total seconds)
        """
        if self.timestamp_format == 'minutes':
            minutes = seconds_from_start / 60
            return f"{minutes:.2f} minutes"
        else:
            return f"{seconds_from_start} seconds"

    def _format_datetime(self, unix_timestamp: int) -> str:
        """Format Unix timestamp as human readable date.
        
        Args:
            unix_timestamp: Unix timestamp in seconds
            
        Returns:
            Formatted date string
        """
        dt = datetime.fromtimestamp(unix_timestamp)
        return dt.strftime("%a, %b %d, %Y")

    def _format_duration(self) -> str:
        """Calculate and format meeting duration.
        
        Returns:
            Duration string in format HH:MM:SS
        """
        duration = self.end_time - self.start_time
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"

    def _generate_header(self) -> str:
        """Generate the meeting header section.
        
        Returns:
            Markdown string with meeting details
        """
        lines = [
            f"# {self.title}",
            "",
            "## Meeting Details",
            "",
            f"**Date:** {self._format_datetime(self.start_time)}",
            f"**Duration:** {self._format_duration()}",
            "",
            "### Participants",
            ""
        ]
        
        # Add participants with any additional info
        for p in self.participants:
            participant_info = [p['name']]
            if 'role' in p:
                participant_info.append(f"_{p['role']}_")
            if 'email' in p:
                participant_info.append(f"({p['email']})")
            lines.append(f"* {' '.join(participant_info)}")
        
        return "\n".join(lines)

    def _generate_summary(self) -> str:
        """Generate the meeting summary section.
        
        Returns:
            Markdown string with meeting summary
        """
        return "\n".join([
            "",
            "## Meeting Summary",
            "",
            self.summary
        ])

    def _generate_transcript(self) -> str:
        """Generate the transcript section.
        
        Returns:
            Markdown string with timestamped transcript
        """
        lines = [
            "",
            "## Full Transcript",
            ""
        ]
        
        current_speaker = None
        for entry in self.transcript:
            timestamp = self._format_timestamp(entry['timestamp'])
            
            # Only show speaker name if it changes
            if entry['speaker'] != current_speaker:
                lines.append(f"\n**{entry['speaker']}** ({timestamp})")
                current_speaker = entry['speaker']
            else:
                lines.append(f"({timestamp})")
            
            lines.append(entry['text'])
            lines.append("")
            
        return "\n".join(lines)

    def generate(self) -> str:
        """Generate the markdown document.
        
        Returns:
            Generated markdown content
        """
        return "\n".join([
            self._generate_header(),
            self._generate_summary(),
            self._generate_transcript()
        ])
