"""CLI package for BalamPi.

Expose `app` from `cli.cli` when used as a package.
"""
from .cli import app  # re-export for `from cli import app`

__all__ = ["app"]
