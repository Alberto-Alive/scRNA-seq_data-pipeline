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
    run.add_argument("--input", required=True, type=Path)
    run.add_argument("--output", required=True, type=Path)
    run.add_argument("--config", type=Path, default=None)
    run.add_argument("--backend", action="store_true", help="Read input out-of-core")

    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if args.command == "run":
        cfg = PipelineConfig.from_yaml(args.config) if args.config else PipelineCofing()

        adata = io.read_h5ad(args.input, backend=args.backed)
        if args.backed:
            adata = adata.to_memory()
        adata = run_pipeline(adata, cfg)
        io.write_h5ad(adata, args.output)
        io.export_obs_parquet(adata, args.output.with_suffix(".obs.parquet"))
        print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
