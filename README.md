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
