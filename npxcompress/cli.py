from pathlib import Path

import click
from mtscomp import compress

from npxcompress.sglx_utils import get_num_saved_channels, get_sample_rate, read_meta


@click.command()
@click.argument("root_dir", type=click.Path(exists=True, file_okay=False))
def main(root_dir: str):
    """Compress all .bin files in a directory tree

    ROOT_DIR is the path from which the script will start looking for .bin files. The script will traverse all folders
    starting from ROOT_DIR, find all .bin/.meta files and compress them.
    """
    bin_candidates = list(Path(root_dir).rglob("**/*.bin"))
    metadata_candidates = [x.parent / f"{x.stem}.meta" for x in bin_candidates]
    bin_files = []
    metadata_files: list[Path] = []
    for bin_file, metadata_file in zip(bin_candidates, metadata_candidates):
        if metadata_file.is_file():
            bin_files.append(bin_file)
            metadata_files.append(metadata_file)
    click.echo(f"Number of .bin/meta pairs: {len(bin_files)}")

    dtype = "int16"
    for bin_file, metadata_file in zip(bin_files, metadata_files):
        meta = read_meta(metadata_file)
        sample_rate = get_sample_rate(meta)
        n_channels = get_num_saved_channels(meta)

        # use default filenames for compressed files
        compressed_ok = True
        try:
            compress(str(bin_file), sample_rate=sample_rate, n_channels=n_channels, dtype=dtype, check_after_compress=True)
        except:
            compressed_ok = False
        status = "OK" if compressed_ok else "Failed"
        bg_color = "green" if compressed_ok else "red"
        click.echo(f"Compress {bin_file}" + "... " + click.style(status, bg=bg_color))


if __name__ == "__main__":
    main()
