"""PDF document generator for meeting transcripts."""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle
)


class PdfGenerator:
    """Generates PDF documents from meeting data."""
    
    def __init__(
        self,
        title: str,
        start_time: int,
        end_time: int,
        participants: List[Dict[str, str]],
        summary: str,
        transcript: List[Dict[str, str]],
        timestamp_format: str = "minutes"
    ):
        """Initialize the PDF generator.
        
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
        
        # Initialize styles
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceBefore=20,
            spaceAfter=12
        )
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceBefore=6,
            spaceAfter=6
        )
        
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
        
    def _create_meeting_details(self, story: list) -> None:
        """Add meeting details section to the document.
        
        Args:
            story: List of flowables to add to
        """
        # Title
        story.append(Paragraph(self.title, self.title_style))
        
        # Meeting Details
        story.append(Paragraph("Meeting Details", self.heading_style))
        
        # Date and duration
        story.append(Paragraph(
            f"<b>Date:</b> {self._format_datetime(self.start_time)}",
            self.body_style
        ))
        story.append(Paragraph(
            f"<b>Duration:</b> {self._format_duration()}",
            self.body_style
        ))
        
        # Participants
        story.append(Paragraph("Participants", self.heading_style))
        for p in self.participants:
            participant_info = [p['name']]
            if 'role' in p:
                participant_info.append(f"<i>{p['role']}</i>")
            if 'email' in p and p['email']:
                participant_info.append(f"({p['email']})")
            story.append(Paragraph(
                "• " + " ".join(participant_info),
                self.body_style
            ))
            
    def _create_summary(self, story: list) -> None:
        """Add meeting summary section to the document.
        
        Args:
            story: List of flowables to add to
        """
        story.append(Paragraph("Meeting Summary", self.heading_style))
        story.append(Paragraph(self.summary, self.body_style))
        
    def _create_transcript(self, story: list) -> None:
        """Add transcript section to the document.
        
        Args:
            story: List of flowables to add to
        """
        story.append(Paragraph("Full Transcript", self.heading_style))
        
        current_speaker = None
        for entry in self.transcript:
            timestamp = self._format_timestamp(entry['timestamp'])
            
            # Only show speaker name if it changes
            if entry['speaker'] != current_speaker:
                if current_speaker is not None:
                    story.append(Spacer(1, 0.1 * inch))
                story.append(Paragraph(
                    f"<b>{entry['speaker']}</b> ({timestamp})",
                    self.body_style
                ))
                current_speaker = entry['speaker']
            else:
                story.append(Paragraph(
                    f"({timestamp})",
                    self.body_style
                ))
            
            story.append(Paragraph(entry['text'], self.body_style))
            
    def generate(self, output_path: Path) -> None:
        """Generate and save the PDF document.
        
        Args:
            output_path: Path to save the PDF file
        """
        # Create document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build story
        story = []
        self._create_meeting_details(story)
        story.append(Spacer(1, 0.2 * inch))
        self._create_summary(story)
        story.append(Spacer(1, 0.2 * inch))
        self._create_transcript(story)
        
        # Generate PDF
        doc.build(story)
