"""Convert camera RAW files (Sony .ARW by default) in a folder to JPEG, in parallel."""

import argparse
import multiprocessing as mp
import sys
import time
from pathlib import Path

DEFAULT_EXTENSIONS = ("arw",)


def find_raw_files(folder: Path, extensions=DEFAULT_EXTENSIONS) -> list[Path]:
    """RAW files directly inside `folder`, matching the extensions case-insensitively, sorted by name."""
    wanted = {"." + e.lower().lstrip(".") for e in extensions}
    return sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in wanted)


def output_path(raw: Path, out_dir: Path) -> Path:
    return out_dir / (raw.stem + ".jpg")


def convert(job: tuple[Path, Path, int]) -> Path:
    """Develop one RAW file with the camera white balance and save it as JPEG."""
    import imageio.v3 as iio
    import rawpy

    raw_path, jpg_path, quality = job
    with rawpy.imread(str(raw_path)) as raw:
        rgb = raw.postprocess(use_camera_wb=True)
    iio.imwrite(jpg_path, rgb, quality=quality)
    return jpg_path


def parse_args(argv=None):
    parser = argparse.ArgumentParser(prog="arw2jpg", description="Convert camera RAW files to JPEG.")
    parser.add_argument("folder", type=Path, help="folder with the RAW files")
    parser.add_argument("-o", "--output", type=Path, help="output folder (default: <folder>/converted)")
    parser.add_argument(
        "-n", "--numb-cores", type=int, default=max(1, mp.cpu_count() - 1), help="parallel workers (default: cores - 1)"
    )
    parser.add_argument("-q", "--quality", type=int, default=95, help="JPEG quality 1-100 (default: 95)")
    parser.add_argument(
        "-e", "--ext", nargs="+", default=list(DEFAULT_EXTENSIONS), help="RAW extensions to convert (default: arw)"
    )
    parser.add_argument("-f", "--overwrite", action="store_true", help="overwrite existing JPEGs")
    parser.add_argument("-d", "--debug", action="store_true", help="print arguments and timing")
    args = parser.parse_args(argv)
    if not 1 <= args.quality <= 100:
        parser.error("--quality must be between 1 and 100")
    if args.numb_cores < 1:
        parser.error("--numb-cores must be at least 1")
    return args


def main(argv=None) -> int:
    args = parse_args(argv)
    if args.debug:
        print(args)
    if not args.folder.is_dir():
        print(f"error: {args.folder} is not a folder", file=sys.stderr)
        return 2

    out_dir = args.output or args.folder / "converted"
    files = find_raw_files(args.folder, args.ext)
    jobs = [(f, output_path(f, out_dir), args.quality) for f in files]
    if not args.overwrite:
        jobs = [j for j in jobs if not j[1].exists()]
    print(f"RAW files found: {len(files)}, to convert: {len(jobs)}")
    if not jobs:
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    start = time.time()
    if args.numb_cores == 1:
        done = [convert(j) for j in jobs]
    else:
        # "spawn": rawpy's OpenMP build can deadlock in forked workers (rawpy checks the global method)
        mp.set_start_method("spawn", force=True)
        with mp.Pool(min(args.numb_cores, len(jobs))) as pool:
            done = []
            for jpg in pool.imap_unordered(convert, jobs):
                print(f"converted --> {jpg}")
                done.append(jpg)
    if args.debug:
        print(f"Conversion finished, took {time.time() - start:.1f} s")
    print(f"{len(done)} JPEG files in {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
