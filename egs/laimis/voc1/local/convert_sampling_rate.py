#!/usr/bin/env python3
import argparse
import logging
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm


def make_output(output_dir, f):
    base = os.path.basename(f)
    name, _ = os.path.splitext(base)
    return os.path.join(output_dir, f"{name}.wav")


def main(args):
    logging.info(f"Input dir: {args.input_dir}")
    logging.info(f"Output dir: {args.output_dir}")
    os.makedirs(args.output_dir, exist_ok=True)
    wav_files = []
    for root, _, files in os.walk(args.input_dir):
        for f in files:
            if f.lower().endswith(".wav"):
                wav_files.append(os.path.join(root, f))
    logging.info(f"Found {len(wav_files)} WAV files in source directory.")
    if not wav_files:
        raise RuntimeError("No WAV files found in the input directory.")

    logging.info(f"Converting {len(wav_files)} WAV files with {args.workers} workers...")

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(convert_wav, f, make_output(args.output_dir, f), args.cmd): f for f in wav_files}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Converting WAVs"):
            success, input_file = future.result()
            if not success:
                raise RuntimeError(f"Conversion failed")
            os.remove(input_file)

    logging.info("All done.")


def convert_wav(input, output, cmd):
    cmd = cmd.replace("{input}", input).replace("{output}", output)
    cmd = cmd.split()
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        logging.error(f"Conversion failed for {input}")
        return False, ""
    except Exception as e:
        logging.error(f"Unexpected error for {input}: {e}")
        return False, ""
    return True, input


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_dir",
        type=str,
        help="""Input directory.
        """,
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        help="""Output directory.
            """,
    )
    parser.add_argument(
        "--workers",
        type=int,
        help="""Number of workers for parallel conversion.
            """,
    )

    parser.add_argument(
        "--cmd",
        type=str,
        help="""Run command to convert a single file, should contain `{input}` and `{output}` placeholders.
            """,
    )

    return parser.parse_args()


if __name__ == "__main__":
    formatter = "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
    logging.basicConfig(format=formatter,
                        level=getattr(logging, os.environ.get("LOGLEVEL", "INFO").upper(), logging.WARNING))

    logging.info(f"Starting")
    args = get_args()
    main(args)
    logging.info(f"Done")
