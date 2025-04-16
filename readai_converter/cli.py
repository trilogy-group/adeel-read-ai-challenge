"""Command-line interface for the Read.AI converter."""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from .config import ConversionConfig, OutputFormat, TimestampFormat
from .processor import MeetingConverter

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
    output_format: str = "both",
    timestamp_format: str = "minutes",
    include_extras: bool = True,
) -> None:
    """Convert Read.AI meeting data to structured documents."""
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
    errors = config.validate()
    if errors:
        console.print("\n[red]Validation errors:[/red]")
        for error in errors:
            console.print(f"  • {error}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create progress display
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    )

    # Run conversion with progress display
    with progress:
        # Add progress tasks
        tasks = {
            'json': progress.add_task("[cyan]Loading JSON...", total=100),
            'transcript': progress.add_task("[cyan]Loading transcript...", total=100),
            'convert': progress.add_task("[cyan]Converting...", total=100)
        }

        try:
            # Create converter with progress callback using tasks
            converter = MeetingConverter(
                config=config,
                callback=lambda stage, prog, msg, details: update_progress(progress, tasks, stage, prog, msg)
            )
            
            # Run conversion
            converter.convert()
            console.print("\n[green]✓[/green] Conversion complete!")
        except Exception as e:
            console.print(f"\n[red]Error:[/red] {str(e)}")
            sys.exit(1)


def update_progress(progress: Progress, tasks: dict, stage: str, prog: float, msg: str) -> None:
    """Update progress display for a stage.
    
    Args:
        progress: Progress display instance
        tasks: Dictionary of task IDs by stage
        stage: Current stage identifier
        prog: Progress value (0-1)
        msg: Status message
    """
    if stage in tasks:
        progress.update(tasks[stage], completed=prog * 100, description=f"[cyan]{msg}")


if __name__ == "__main__":
    main()
