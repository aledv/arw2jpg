# arw2jpg

[![CI](https://github.com/aledv/arw2jpg/actions/workflows/ci.yml/badge.svg)](https://github.com/aledv/arw2jpg/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Command-line tool to convert a folder of camera RAW files (Sony `.ARW` by default) to JPEG, using all your CPU
cores. RAW files are developed with [rawpy](https://github.com/letmaik/rawpy) (LibRaw) using the camera white
balance, and saved with [imageio](https://imageio.readthedocs.io/).

## Features

- Converts a whole folder in parallel (all cores but one by default).
- Camera white balance, JPEG quality of your choice, existing JPEGs skipped unless `--overwrite`.
- Any RAW format LibRaw supports (`.ARW`, `.NEF`, `.CR2`/`.CR3`, `.RAF`, `.DNG`...), case-insensitive.
- Pure Python package with a `arw2jpg` command; no GUI, works over SSH.

## Install

Requires Python 3.10+.

```bash
pip install git+https://github.com/aledv/arw2jpg.git
# or, from a clone
pip install .
```

## Usage

```bash
arw2jpg ~/Pictures/shoot              # JPEGs go to ~/Pictures/shoot/converted
arw2jpg -o ~/Pictures/jpg -q 90 ~/Pictures/shoot
arw2jpg -e arw nef cr2 dng ~/Pictures/mixed
```

```
usage: arw2jpg [-h] [-o OUTPUT] [-n NUMB_CORES] [-q QUALITY] [-e EXT [EXT ...]] [-f] [-d] folder

  folder                    folder with the RAW files (not scanned recursively)
  -o, --output OUTPUT       output folder (default: <folder>/converted)
  -n, --numb-cores N        parallel workers (default: cores - 1, at least 1)
  -q, --quality Q           JPEG quality 1-100 (default: 95)
  -e, --ext EXT [EXT ...]   RAW extensions to convert, case-insensitive (default: arw)
  -f, --overwrite           overwrite JPEGs that already exist (skipped by default)
  -d, --debug               print arguments and timing
```

Any format LibRaw supports works with `--ext`: e.g. `nef` (Nikon), `cr2`/`cr3` (Canon), `raf` (Fujifilm), `dng`.

## Development

```bash
pip install -e . ruff
python -m unittest discover -s tests -v    # tests (conversion is mocked, no RAW samples needed)
ruff check . && ruff format --check .      # linter
```

CI (GitHub Actions) runs the linter and the tests on Python 3.10, 3.12 and 3.13.

## Contributing

Issues and pull requests are welcome. Please run the linters and tests (see [Development](#development)) before opening a pull request.

## License

MIT, see [LICENSE](LICENSE). Thanks to [devincody](https://github.com/devincody) for the parallel version.
