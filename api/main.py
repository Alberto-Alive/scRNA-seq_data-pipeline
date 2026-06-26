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


@app.post("/analyse")
async def analyze(file: UploadFile = File(...)) -> dict:
    if not file.filename or not file.filename.endswith(".h5ad"):
        raise HTTPException(status_code=400, detail="Please upload a .h5ad file.")

    with tempfile.NamedTemporaryFile(suffix=".h5ad", delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = Path(temp.name)
    
    try:
        adata = ad.read_h5ad(tmp_path)
    except Exception as exec:
        raise HTTPException(status_code=400, detail=f"Could not read AnnData: {exc}") from exc
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
        "integration_metrics": adata.uns.get("integration_metrics", {})
    }
