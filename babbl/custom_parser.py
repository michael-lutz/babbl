"""Custom parser with table support for babbl."""

from marko import Parser
from marko.block import BlockElement

from babbl.table_parser import Table


class BabblParser(Parser):
    """Custom parser that includes table support."""

    def __init__(self):
        super().__init__()
        # Add table support
        self.add_element(Table)

    def parse(self, text: str):
        """Parse text with table support."""
        return super().parse(text)
