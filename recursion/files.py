from pathlib import Path


def get_all_files(path: Path, _paths=None):
    if _paths is None:
        _paths = []
    if path.is_dir():
        for _path in path.iterdir():
            get_all_files(_path, _paths)
    else:
        _paths.insert(0, path)
    return _paths
