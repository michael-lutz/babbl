"""Command-line interface for babbl."""

from pathlib import Path
from typing import Optional

import click

from babbl.cache import CacheManager
from babbl.frontmatter import FrontmatterProcessor
from babbl.renderer import MarkdownRenderer


@click.group()
@click.version_option()
def main():
    """Babbl: Turn markdown into beautiful research blog posts."""
    pass


@main.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output HTML file path")
@click.option("--cache-dir", type=click.Path(path_type=Path), help="Cache directory")
@click.option("--force", "-f", is_flag=True, help="Force regeneration (ignore cache)")
@click.option("--clear-cache", is_flag=True, help="Clear cache before processing")
def render(input_file: Path, output: Optional[Path], cache_dir: Optional[Path], force: bool, clear_cache: bool):
    """Render a markdown file to HTML."""
    cache_manager = CacheManager(cache_dir)
    renderer = MarkdownRenderer(cache_manager=cache_manager)
    if output is None:
        output = input_file.with_suffix(".html")

    if clear_cache:
        cache_manager.clear_cache()
        click.echo("Cache cleared.")

    # check if we need to regenerate
    if not force and not cache_manager.is_stale(input_file):
        cached_path = cache_manager.get_cached_output_path(input_file)
        if cached_path:
            click.echo(f"Using cached output: {cached_path}")
            return

    try:
        result_path = renderer.render_file(input_file, output, force=force)
        click.echo(f"Successfully rendered: {result_path}")
    except Exception as e:
        click.echo(f"Error rendering file: {e}", err=True)
        raise click.Abort()


@main.command()
@click.argument("input_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--output-dir", "-o", type=click.Path(path_type=Path), help="Output directory")
@click.option("--pattern", default="*.md", help="File pattern to match")
@click.option("--recursive", "-r", is_flag=True, help="Process subdirectories recursively")
@click.option("--force", "-f", is_flag=True, help="Force regeneration (ignore cache)")
def build(input_dir: Path, output_dir: Optional[Path], pattern: str, recursive: bool, force: bool):
    """Build multiple markdown files in a directory."""
    renderer = MarkdownRenderer()
    if output_dir is None:
        output_dir = input_dir / "output"
    output_dir.mkdir(exist_ok=True)

    if recursive:
        md_files = list(input_dir.rglob(pattern))
    else:
        md_files = list(input_dir.glob(pattern))

    if not md_files:
        click.echo(f"No markdown files found matching pattern '{pattern}'")
        return

    click.echo(f"Found {len(md_files)} markdown files to process...")

    for md_file in md_files:
        try:
            rel_path = md_file.relative_to(input_dir)
            output_file = output_dir / rel_path.with_suffix(".html")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            result_path = renderer.render_file(md_file, output_file)
            click.echo(f"✓ {md_file.name} → {result_path}")

        except Exception as e:
            click.echo(f"✗ Error processing {md_file.name}: {e}", err=True)

    click.echo(f"\nBuild complete! Output directory: {output_dir}")


@main.command()
@click.option("--cache-dir", type=click.Path(path_type=Path), help="Cache directory to clear")
def clear_cache(cache_dir: Optional[Path]):
    """Clear the cache."""
    cache_manager = CacheManager(cache_dir)
    cache_manager.clear_cache()
    click.echo("Cache cleared successfully.")


@main.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
def info(input_file: Path):
    """Show information about a markdown file."""
    processor = FrontmatterProcessor()

    try:
        frontmatter, content = processor.process_file(input_file)

        click.echo(f"File: {input_file}")
        click.echo(f"Size: {input_file.stat().st_size} bytes")
        click.echo(f"Content length: {len(content)} characters")

        if frontmatter:
            click.echo("\nFrontmatter:")
            for key, value in frontmatter.items():
                click.echo(f"  {key}: {value}")
        else:
            click.echo("\nNo frontmatter found.")

    except Exception as e:
        click.echo(f"Error reading file: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
