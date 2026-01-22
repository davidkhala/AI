import os

from huggingface_hub import snapshot_download


def clone(git_dir: os.PathLike,
          *,
          owner: str | None = None,
          repository: str | None = None,
          repo_id: str | None = None,
          **kwargs
          ) -> str:
    """
    :return: path of model directory
    """
    if not repo_id:
        repo_id = f"{owner}/{repository}"
    return snapshot_download(
        repo_id=repo_id,
        local_dir=git_dir,
        local_dir_use_symlinks=False,
        **kwargs
    )