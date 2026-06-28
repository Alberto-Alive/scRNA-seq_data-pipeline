# scRNA-seq Data Pipeline

A small Python project for analyzing single-cell RNA-seq `.h5ad` files.

The project provides two ways to run the pipeline:

1. A **FastAPI web API** for uploading `.h5ad` files
2. A **CLI command** for running the pipeline from the terminal

The pipeline reads an AnnData file, performs quality control, preprocessing, clustering, cell type annotation, and returns or saves useful analysis results.

---

## Project Structure

```text
api/main.py              # FastAPI app
src/scpipe/pipeline.py   # Main pipeline steps
src/scpipe/qc.py         # Quality control
src/scpipe/preprocess.py # Normalization and preprocessing
src/scpipe/integrate.py  # Integration / embedding setup
src/scpipe/cluster.py    # Clustering and UMAP
src/scpipe/annotate.py   # Cell type annotation
src/scpipe/evaluate.py   # Metrics
src/scpipe/cli.py        # Command line interface
configs/default.yaml     # Default pipeline config