import random
from pathlib import Path
from typing import Callable, List, Sequence, Tuple


def decision(probability: float) -> bool:
    return random.random() < probability


def find_pairs(root_dir: str, bin_ext: str = "bin", meta_ext: str = "meta") -> Tuple[List[Path], List[Path]]:
    bin_candidates = list(Path(root_dir).rglob(f"**/*.{bin_ext}"))
    metadata_candidates = [x.parent / f"{x.stem}.{meta_ext}" for x in bin_candidates]
    bin_files = []
    metadata_files: List[Path] = []
    for bin_file, metadata_file in zip(bin_candidates, metadata_candidates):
        if metadata_file.is_file():
            bin_files.append(bin_file)
            metadata_files.append(metadata_file)

    return bin_files, metadata_files


def get_status_and_color(flag: bool, skip: bool = False) -> Tuple[str, str]:
    if skip:
        status = "Skipped"
        bg_color = "yellow"
    else:
        status = "OK" if flag else "Failed"
        bg_color = "green" if flag else "red"

    return status, bg_color


def run_and_get_status(func: Callable[..., int], dry_run: bool, **kwargs) -> bool:
    run_ok = True
    try:
        if dry_run:
            raise Exception("Dry run")
        else:
            func(**kwargs)
    except:
        run_ok = False
    return run_ok


def delete_files(files: Sequence[Path]):
    for file in files:
        file.unlink()
