import pathlib

__all__ = [
    cog_file.stem
    for cog_file in pathlib.Path(__path__[0]).glob("*.py")
    if not (cog_file.is_dir() or cog_file.stem.startswith("__"))
]
