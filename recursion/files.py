from pathlib import Path


def _get_all_files(path: Path, _paths: list[Path] = []):
    if path.is_dir():
        for _path in path.iterdir():
            _get_all_files(_path, _paths)
    else:
        _paths.insert(0, path)
    return _paths


def get_all_files(path: Path) -> list[Path]:
    return _get_all_files(path)
