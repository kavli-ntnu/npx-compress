# npx-compress

Script to compress NPX binary files.

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

```
pip install -e .[dev]
pre-commit install
```

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

Created `.msi` file will be in `dist` folder.
