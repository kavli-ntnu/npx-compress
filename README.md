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

It is also possible to use the tool via Docker.

## Docker

```
# Build image with (use whatever tag name you want)
docker build -t npx .
# Run tool via:
docker run --rm npx --help
```

## Development

Make sure to setup git config to handle the formatting/whitespaces correctly. To be able to work cross-platform,
we upload all files in LF format. If you work on a windows machine, the default format is CRLF.

```sh
# On Windows:
git config --global core.autocrlf true
# On Linux/Mac:
git config --global core.autocrlf input
```

To turn off the warning (not the functionality), run:

```sh
$ git config --global core.safecrlf false
```

Install the project in editable mode and with development requirements:
```
pip install -e .[dev]
```

### Initialize pre-comit git hooks (on first setup)

This is only required once when you start to work on the code.

```
pre-commit install
```

### Versioning

Versioning is done via continuous integration (CI) pipelines also known as GitHub Actions. Currently, the pipeline is
triggered on every commit. It reads the version from `version.json` file (that must be in format `MAJOR.MINOR`) and
adds a build number to it, so it becomes `MAJOR.MINOR.BUILD`. The build number is simply the counter of pipeline runs.
This means that if you re-run the pipeline, you will get a version increase.

### GitHub Actions

There is one pipeline/action that runs on every commit. It increases a version number of the package, builds wheel
and msi distributables. These distributable files are available in form of an artifact. It is possible to download them
as a single .zip archive. See for example [this](https://github.com/kavli-ntnu/npx-compress/suites/5878773778/artifacts/198596214).

### Making standalone executables

[cx_Freeze](https://cx-freeze.readthedocs.io/en/latest/) may be used to create standalone executable packages for different
platforms. It's up to you to create virtual environment with cx_Freeze in it. See [original documentation](https://cx-freeze.readthedocs.io/en/latest/installation.html) for details.

In general, you should prepare the python environment on your build
machine before using cx_Freeze. Run in Python >=3.7:
```
python -m pip install --upgrade pip build cx_freeze trove-classifiers
pip install .
```

For example, one may create .msi package for usage under Windows:
```
python setup_cx.py bdist_msi
```

Created `.msi` file will be in `dist` folder. You are encouraged to use github actions in order to build .msi packages.
