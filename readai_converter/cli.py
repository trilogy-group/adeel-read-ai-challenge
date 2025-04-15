"""Command-line interface for the Read.AI converter."""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel

from .config import ConversionConfig, OutputFormat, TimestampFormat

console = Console()


def validate_input_args(
    input_dir: Optional[str],
    json_file: Optional[str],
    transcript_file: Optional[str],
    video_file: Optional[str],
) -> None:
    """Validate input arguments combination."""
    if input_dir and any([json_file, transcript_file, video_file]):
        console.print(
            "[red]Error:[/red] Cannot specify both input directory and individual files"
        )
        sys.exit(1)
    
    if not input_dir and not all([json_file, transcript_file, video_file]):
        console.print(
            "[red]Error:[/red] Must specify either input directory or all individual files"
        )
        sys.exit(1)


@click.command()
@click.option(
    "--input-dir",
    "-i",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Directory containing Read.AI meeting files",
)
@click.option(
    "--json-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    help="Path to raw_Event.json file",
)
@click.option(
    "--transcript-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    help="Path to transcript file",
)
@click.option(
    "--video-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    help="Path to video recording file",
)
@click.option(
    "--output-dir",
    "-o",
    required=True,
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    help="Output directory for generated files",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice([f.value for f in OutputFormat], case_sensitive=False),
    default=OutputFormat.BOTH.value,
    help="Output format (pdf, md, or both)",
)
@click.option(
    "--timestamp-format",
    type=click.Choice([f.value for f in TimestampFormat], case_sensitive=False),
    default=TimestampFormat.MINUTES.value,
    help="Timestamp format in output",
)
@click.option(
    "--include-extras/--no-extras",
    default=True,
    help="Include extra information like action items and chapter summaries",
)
def main(
    input_dir: Optional[Path],
    json_file: Optional[Path],
    transcript_file: Optional[Path],
    video_file: Optional[Path],
    output_dir: Path,
    output_format: str,
    timestamp_format: str,
    include_extras: bool,
) -> None:
    """Convert Read.AI meeting data to structured document formats."""
    # Show welcome message
    console.print(
        Panel.fit(
            "[bold blue]Read.AI Meeting Converter[/bold blue]\n"
            "Converting meeting data to structured documents..."
        )
    )
    
    # Validate input arguments
    validate_input_args(input_dir, json_file, transcript_file, video_file)
    
    # Create configuration
    config = ConversionConfig(
        input_dir=input_dir,
        json_file=json_file,
        transcript_file=transcript_file,
        video_file=video_file,
        output_dir=output_dir,
        output_format=OutputFormat(output_format),
        timestamp_format=TimestampFormat(timestamp_format),
        include_extras=include_extras,
    )
    
    # Validate configuration
    if errors := config.validate():
        for error in errors:
            console.print(f"[red]Error:[/red] {error}")
        sys.exit(1)
    
    # TODO: Initialize and run the converter
    console.print("[green]Configuration validated successfully![/green]")


if __name__ == "__main__":
    main()
