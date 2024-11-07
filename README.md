# npx-compress

Script to compress NPX binary files. It is a thin wrapper around [mtscomp](https://github.com/int-brain-lab/mtscomp).
Mtscomp can compress one file at a time. This app simply scans a given directory with subdirectories and passes all
found files to mtscomp, one at a time.

## Install

A preferred method of installation on target machine is via [`pipx`](https://github.com/pypa/pipx). Once you have pipx
installed, run

```
pipx install git+https://github.com/kavli-ntnu/npx-compress.git
npxcompress --help
```

Under the hood, `pipx` creates a private virtual environment dedicated to this tool, and will not interfere with any of
your other environments. It makes the `npxcompress` command-line tool available system-wide, without activating or
deactivating specific environments.




## Usage

The following guide assumes that you have installed the tool via pipx as above, and that you have the following example
data structure that you wish to compress (only relevant files shown
```bash
/
├── data
│   ├── subject_12345
│   │   ├── 2024-10-11_10-30-25
│   │   │   ├── probe_1
│   │   │   │   ├── npx.imec.ap.bin
│   │   │   │   ├── npx.imec.ap.meta
│   │   │   ├── probe_2
│   │   │   │   ├── npx.imec.ap.bin
│   │   │   │   ├── npx.imec.ap.meta
│   │   │
│   │   ├── 2024-10-12_09-45-10
│   │   │   ├── probe_1
│   │   │   │   ├── npx.imec.ap.bin
│   │   │   │   ├── npx.imec.ap.meta
│   │   │   ├── probe_2
│   │   │   │   ├── npx.imec.ap.bin
│   │   │   │   ├── npx.imec.ap.meta
```

### Compression

`npxcompress` searches for all (binary, meta) files in the given directory and its subdirectories, and compresses them.

```commandline
$ npxcompress /data/subject_12345
```
You should then see the following output:
```commandline
Starting to compress files found under /data/subject_12345
Number of bin/meta pairs: 4
Compressing: 100%|██████████████████████████████| 23/23 [01:08<00:00,  2.96s/it]
Checking: 100%|███████████████████████████████| 225/225 [00:25<00:00,  8.88it/s]
Compress /data/subject_12345/2024-10-11_10-30-25/probe_1/npx.imec.ap.bin... OK
	RAW files deleted... ok
Compressing: 100%|██████████████████████████████| 23/23 [01:08<00:00,  2.97s/it]
Checking: 100%|███████████████████████████████| 225/225 [00:25<00:00,  8.80it/s]
Compress /data/subject_12345/2024-10-11_10-30-25/probe_2/npx.imec.ap.bin... OK
	RAW files deleted... ok
Compressing: 100%|██████████████████████████████| 23/23 [01:08<00:00,  2.96s/it]
Checking: 100%|███████████████████████████████| 225/225 [00:25<00:00,  8.88it/s]
Compress /data/subject_12345/2024-10-12_09-45-10/probe_1/npx.imec.ap.bin... OK
	RAW files deleted... ok
Compressing: 100%|██████████████████████████████| 23/23 [01:08<00:00,  2.96s/it]
Checking: 100%|███████████████████████████████| 225/225 [00:25<00:00,  8.88it/s]
Compress /data/subject_12345/2024-10-12_09-45-10/probe_2/npx.imec.ap.bin... OK
	RAW files deleted... ok
```
Your data structure should then look like this:

```bash
/
├── data
│   ├── subject_12345
│   │   ├── 2024-10-11_10-30-25
│   │   │   ├── probe_1
│   │   │   │   ├── npx.imec.ap.cbin
│   │   │   │   ├── npx.imec.ap.meta
│   │   │   │   ├── npx.imec.ap.ch
│   │   │   ├── probe_2
│   │   │   │   ├── npx.imec.ap.cbin
│   │   │   │   ├── npx.imec.ap.meta
│   │   │   │   ├── npx.imec.ap.ch
│   │   │
│   │   ├── 2024-10-12_09-45-10
│   │   │   ├── probe_1
│   │   │   │   ├── npx.imec.ap.cbin
│   │   │   │   ├── npx.imec.ap.meta
│   │   │   │   ├── npx.imec.ap.ch
│   │   │   ├── probe_2
│   │   │   │   ├── npx.imec.ap.cbin
│   │   │   │   ├── npx.imec.ap.meta
│   │   │   │   ├── npx.imec.ap.ch
```

The `.bin` file is replaced with a `.cbin` file, typically about half the size (for Neuropixels 2, smaller for
Neuropixels 1). A new file suffixed with `.ch` is created, which provides metadata about the compression and which is
necessary for successful decompression. The original `.meta` file is left untouched.

The original binary file will _only_ be removed after the compressed file is validated against it. If, for any reason,
an error occurs, the original file will _not_ be deleted or modified.

You can also specify that the original files will be left intact via the optional `-k` or `--keep-original` argument:
```commandline
$ npxcompress /data/subject_12345 --keep-original
```

If you don't want to compress all files at once - perhaps some files are still in active use - you can compress a subset
by giving a more specific path:
```commandline
$ npxcompress /data/subject_12345/2024-10-12_09-45-10
```

### Decompression

Decompression works similarly to compression, with the `-d` or `--decompress` arguments

```commandline
$ npxcompress /data/subject_12345 --decompress
```

This will identify any (`.cbin`, `.ch`) file pairs and reproduce the original `.bin` files. By default, once decompressed,
the compressed binaries will be deleted. As with compression, you can use the `-k` or `--keep-original` arguments to
prevent this and keep the compressed files in place (and thus not have to re-compress them again afterwards)


### Dry run

You can check what files will be compressed (or decompressed) via the `--dry-run` argument. This will not modify any
files, but may be useful for identifying how many binaries are included in the requested directory

```commandline
$ npxcompress /data/subject_12345 --dry-run
```

```commandline
Starting to compress files found under /data/subject_12345
Number of bin/meta pairs: 4
Compress /data/subject_12345/2024-10-11_10-30-25/probe_1/npx.imec.ap.bin... Skipped
	RAW files deleted... Skipped
Compress /data/subject_12345/2024-10-11_10-30-25/probe_2/npx.imec.ap.bin... Skipped
	RAW files deleted... Skipped
Compress /data/subject_12345/2024-10-12_09-45-10/probe_1/npx.imec.ap.bin... Skipped
	RAW files deleted... Skipped
Compress /data/subject_12345/2024-10-12_09-45-10/probe_2/npx.imec.ap.bin... Skipped
	RAW files deleted... Skipped
```

## Command line arguments

The `npxcompress` tool uses a few command line arguments to control its behavior. Several arguments have both short and
long forms, e.g. `-d` and `--decompress`. You can use either one of these interchangably. You can use these either before
or after the path to be compressed/decompressed.

The following two examples will have the same effect:

```commandline
$ npxcompress -d /data/subject_12345
$ npxcompress /data/subject_12345 --decompress
```
