"""Core converter implementation."""

from pathlib import Path
from typing import Optional, Protocol

from .config import ConversionConfig


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
    
    # TODO: Implement conversion methods
