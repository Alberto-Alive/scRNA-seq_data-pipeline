from __future__ import annotations


import argparse
import logging
from pathlib import Path

from scpipe import io

from scpipe.config import PipelineConfig

from scpipe.pipeline import run_pipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="scpipe")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run the full pipelien on an .h5ad file")