"""
Bouy unpacking tool.
"""

import argparse
import pathlib

import msgpack

from stega import show


def unpack(filepath):
    show.show(filepath, "data.raw")
    with open("data.raw", "rb") as infile:
        extras = msgpack.loads(infile.read())

    outdir = pathlib.Path(filepath + ".contents")
    outdir.mkdir(exist_ok=False)

    for (i, (typ, data)) in enumerate(extras):
        suffix = ".dat"
        mode = "wb"
        if typ == "text":
            suffix = ".txt"
            mode = "w"
        elif typ == "image":
            suffix = ".png"
        elif typ == "audio":
            suffix = ".m4a"
        elif typ == "qr":
            suffix = ".txt"

        with open(outdir / f"{i}-{typ}{suffix}", mode) as outfile:
            outfile.write(data)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    return parser.parse_args()


def main():
    args = parse_args()
    unpack(args.filepath)


if __name__ == '__main__':
    main()
