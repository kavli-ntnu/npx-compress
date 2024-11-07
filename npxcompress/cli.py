import click
from mtscomp import compress, decompress

from npxcompress.sglx_utils import get_num_saved_channels, get_sample_rate, read_meta
from npxcompress.utils import delete_files, find_pairs, get_status_and_color, run_and_get_status


def run_compression(root_dir: str, dry_run: bool, keep_original: bool):
    click.echo(f"Starting to compress files found under {root_dir}")
    bin_files, metadata_files = find_pairs(root_dir)
    click.echo(f"Number of bin/meta pairs: {len(bin_files)}")

    dtype = "int16"
    for bin_file, metadata_file in zip(bin_files, metadata_files):
        meta = read_meta(metadata_file)
        sample_rate = get_sample_rate(meta)
        n_channels = get_num_saved_channels(meta)

        # use default filenames for compressed files
        compressed_ok = run_and_get_status(
            compress,
            dry_run,
            path=str(bin_file),
            sample_rate=sample_rate,
            n_channels=n_channels,
            dtype=dtype,
            check_after_compress=True,
        )
        status, bg_color = get_status_and_color(compressed_ok, dry_run)
        click.echo(f"Compress {bin_file}" + "... " + click.style(status, bg=bg_color))
        if compressed_ok and not dry_run and not keep_original:
            deleted_ok = run_and_get_status(delete_files, dry_run, files=(bin_file,))
            status, bg_color = get_status_and_color(deleted_ok)
        else:
            status, bg_color = get_status_and_color(False, True)
        click.echo(f"\tRAW files deleted... " + click.style(status, bg=bg_color))
    return


def run_decompression(root_dir: str, dry_run: bool, keep_original: bool):
    click.echo(f"Starting to decompress files found under {root_dir}")
    bin_files, metadata_files = find_pairs(root_dir, bin_ext="cbin", meta_ext="ch")
    click.echo(f"Number of bin/meta pairs: {len(bin_files)}")

    for bin_file, metadata_file in zip(bin_files, metadata_files):
        output_name = bin_file.parent / f"{bin_file.stem}.bin"

        decompressed_ok = run_and_get_status(
            decompress, dry_run, cdata=str(bin_file), cmeta=str(metadata_file), out=str(output_name), check_after_decompress=True
        )
        status, bg_color = get_status_and_color(decompressed_ok, dry_run)
        click.echo(f"Decompress {bin_file}" + "... " + click.style(status, bg=bg_color))

        if decompressed_ok and not dry_run and not keep_original:
            deleted_ok = run_and_get_status(delete_files, dry_run, files=(bin_file, metadata_file))
            status, bg_colors = get_status_and_color(deleted_ok)
        else:
            status, bg_color = get_status_and_color(False, True)
        click.echo(f"\tCompressed files deleted... " + click.style(status, bg=bg_color))
    return


@click.command()
@click.argument("root_dir", type=click.Path(exists=True, file_okay=False))
@click.option(
    "-d",
    "--decompress",
    default=False,
    is_flag=True,
    help="Whether to decompress files instead of compressing them.",
)
@click.option(
    "--dry-run",
    default=False,
    is_flag=True,
    help="Perform a dry-run, no compression or decompression will be performed.",
)
@click.option(
    "-k",
    "--keep-original",
    default=False,
    is_flag=True,
    help="Keep the source files after compression/decompression (otherwise deleted by default).",
)
def main(root_dir: str, decompress: bool, dry_run: bool, keep_original: bool):
    """Compress/decompress all bin files in a directory tree

    ROOT_DIR is the path from which the script will start looking for .(c)bin files. The script will traverse all folders
    starting from ROOT_DIR, find all .(c)bin/.(c)meta files and compress or decompress them.
    """
    if decompress:
        run_decompression(root_dir, dry_run, keep_original)
    else:
        run_compression(root_dir, dry_run, keep_original)


if __name__ == "__main__":
    main()
