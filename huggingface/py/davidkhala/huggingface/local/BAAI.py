import os
from pathlib import Path

from davidkhala.huggingface.local import clone


def download_bge_m3(git_dir: os.PathLike) -> Path:
    model_dir = clone(git_dir, repo_id="BAAI/bge-m3", allow_patterns=["onnx/*"])
    onnx_path = Path(model_dir) / "onnx" / "model.onnx"
    assert onnx_path.is_file() and onnx_path.exists()
    return onnx_path
