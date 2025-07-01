"""Frontmatter processing for markdown files."""

import re
from pathlib import Path
from typing import Any, Optional, Tuple

import yaml


class FrontmatterProcessor:
    """Process frontmatter from markdown files and sidecar YAML files."""

    def __init__(self):
        self.frontmatter_pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL | re.MULTILINE)

    def extract_frontmatter(self, content: str) -> Tuple[Optional[dict[str, Any]], str]:
        """
        Extract frontmatter from markdown content.

        Args:
            content: The markdown content to process

        Returns:
            Tuple of (frontmatter_dict, content_without_frontmatter)
        """
        match = self.frontmatter_pattern.match(content)
        if not match:
            return None, content

        frontmatter_text = match.group(1)
        content_without_frontmatter = content[match.end() :]

        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            return frontmatter, content_without_frontmatter
        except yaml.YAMLError as e:
            # If YAML parsing fails, treat as regular content
            return None, content

    def load_sidecar_yaml(self, md_path: Path) -> Optional[dict[str, Any]]:
        """
        Load sidecar YAML file for a markdown file.

        Args:
            md_path: Path to the markdown file

        Returns:
            dictionary of frontmatter data or None if no sidecar file exists
        """
        # Try different sidecar file patterns
        sidecar_patterns = [
            md_path.with_suffix(".yaml"),
            md_path.with_suffix(".yml"),
            md_path.with_name(f"{md_path.stem}.yaml"),
            md_path.with_name(f"{md_path.stem}.yml"),
        ]

        for sidecar_path in sidecar_patterns:
            if sidecar_path.exists():
                try:
                    with open(sidecar_path, "r", encoding="utf-8") as f:
                        return yaml.safe_load(f)
                except (yaml.YAMLError, IOError) as e:
                    # Log error but continue
                    print(f"Warning: Could not load sidecar file {sidecar_path}: {e}")
                    continue

        return None

    def merge_frontmatter(self, inline: Optional[dict[str, Any]], sidecar: Optional[dict[str, Any]]) -> dict[str, Any]:
        """
        Merge inline and sidecar frontmatter.

        Args:
            inline: Frontmatter from within the markdown file
            sidecar: Frontmatter from sidecar YAML file

        Returns:
            Merged frontmatter dictionary
        """
        result = {}

        # Start with sidecar (lower priority)
        if sidecar:
            result.update(sidecar)

        # Override with inline frontmatter (higher priority)
        if inline:
            result.update(inline)

        return result

    def process_file(self, md_path: Path) -> Tuple[dict[str, Any], str]:
        """
        Process a markdown file and extract all frontmatter.

        Args:
            md_path: Path to the markdown file

        Returns:
            Tuple of (merged_frontmatter, content_without_frontmatter)
        """
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()

        inline_frontmatter, content_without_frontmatter = self.extract_frontmatter(content)
        sidecar_frontmatter = self.load_sidecar_yaml(md_path)

        merged_frontmatter = self.merge_frontmatter(inline_frontmatter, sidecar_frontmatter)

        return merged_frontmatter, content_without_frontmatter


def extract_frontmatter(content: str) -> Tuple[Optional[dict[str, Any]], str]:
    """Extract frontmatter from markdown content.

    Args:
        content: The markdown content to process

    Returns:
        Tuple of (frontmatter_dict, content_without_frontmatter)
    """
    frontmatter_pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL | re.MULTILINE)
    match = frontmatter_pattern.match(content)
    if not match:
        return None, content

    frontmatter_text = match.group(1)
    content_without_frontmatter = content[match.end() :]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        return frontmatter, content_without_frontmatter
    except yaml.YAMLError as e:
        # If YAML parsing fails, treat as regular content
        return None, content


def load_sidecar_yaml(md_path: Path) -> Optional[dict[str, Any]]:
    """Load sidecar YAML file for a markdown file.

    Args:
        md_path: Path to the markdown file

    Returns:
        dictionary of frontmatter data or None if no sidecar file exists
    """
    # Try different sidecar file patterns
    sidecar_patterns = [
        md_path.with_suffix(".yaml"),
        md_path.with_suffix(".yml"),
        md_path.with_name(f"{md_path.stem}.yaml"),
        md_path.with_name(f"{md_path.stem}.yml"),
    ]

    for sidecar_path in sidecar_patterns:
        if sidecar_path.exists():
            try:
                with open(sidecar_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)
            except (yaml.YAMLError, IOError) as e:
                # Log error but continue
                print(f"Warning: Could not load sidecar file {sidecar_path}: {e}")
                continue

    return None


def merge_frontmatter(inline: Optional[dict[str, Any]], sidecar: Optional[dict[str, Any]]) -> dict[str, Any]:
    """Merge inline and sidecar frontmatter.

    Args:
        inline: Frontmatter from within the markdown file
        sidecar: Frontmatter from sidecar YAML file

    Returns:
        Merged frontmatter dictionary
    """
    result = {}

    # Start with sidecar (lower priority)
    if sidecar:
        result.update(sidecar)

    # Override with inline frontmatter (higher priority)
    if inline:
        result.update(inline)

    return result


def process_file(md_path: Path) -> Tuple[dict[str, Any], str]:
    """Process a markdown file and extract all frontmatter.

    Args:
        md_path: Path to the markdown file

    Returns:
        Tuple of (merged_frontmatter, content_without_frontmatter)
    """
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    inline_frontmatter, content_without_frontmatter = extract_frontmatter(content)
    sidecar_frontmatter = load_sidecar_yaml(md_path)

    merged_frontmatter = merge_frontmatter(inline_frontmatter, sidecar_frontmatter)

    return merged_frontmatter, content_without_frontmatter
