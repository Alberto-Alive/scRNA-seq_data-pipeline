"""A minimal FastAPI service exposing QC + annotation over HTTP.

Design note: heavy steps such as scVI training are deliberately *not* run inside
a request. In production they would be dispatched to a worker / GPU job and
polled. This endpoint runs the fast path (QC + clustering + marker annotation
with the CPU 'none' integrator) and returns a JSON summary -- the right shape for
an interactive QC service.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import anndata as ad
from fastapi import FastAPI, File, HTTPException, UploadFile

from scpipe.config import IntegrateConfig, PipelineConfig
from scpipe.pipeline import run_pipeline

app = FastAPI(title="scpipe", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)) -> dict:
    if not file.filename or not file.filename.endswith(".h5ad"):
        raise HTTPException(status_code=400, detail="Please upload a .h5ad file.")

    with tempfile.NamedTemporaryFile(suffix=".h5ad", delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = Path(tmp.name)

    try:
        adata = ad.read_h5ad(tmp_path)
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"Could not read AnnData: {exc}"
        ) from exc
    finally:
        tmp_path.unlink(missing_ok=True)

    cfg = PipelineConfig(integrate=IntegrateConfig(method="none"))
    adata = run_pipeline(adata, cfg)

    return {
        "n_cells": int(adata.n_obs),
        "n_genes": int(adata.n_vars),
        "qc": adata.uns.get("qc", {}),
        "clusters": {str(k): int(v) for k, v in adata.obs["leiden"].value_counts().items()},
        "cell_types": {str(k): int(v) for k, v in adata.obs["cell_type"].value_counts().items()},
        "integration_metrics": adata.uns.get("integration_metrics", {}),
    }
