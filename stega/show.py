
from PIL import Image

import argparse
import math
import struct


def show(image_filename, outfile):
    img = Image.open(image_filename)
    (x, y) = img.size

    assert img.format == "PNG"
    assert img.mode == "RGB"

    cr = img.crop((0, 0, 4, 1))
    data = cr.getdata()
    # print(list(data))

    msglen_bytes = bytearray(
        (((r & 0b111) << 5) + ((g & 0b111) << 2) + (b & 0b11))
        for (r, g, b) in data
    )
    # print(msglen_bytes)
    expected_bytes = struct.unpack("I", msglen_bytes)[0]
    # print(expected_bytes)
    # exit(1)

    remaining = expected_bytes
    lines = math.ceil(expected_bytes / x)
    # print(lines, x, remaining)

    with open(outfile, "wb") as outfile:
        for i in range(lines):
            # print(i)

            width = min(x, remaining)

            cr = img.crop((0 if i else 4, i, width, i + 1))
            data = cr.getdata()
            remaining -= len(data)

            out_data = bytearray(
                (((r & 0b111) << 5) + ((g & 0b111) << 2) + (b & 0b11))
                for (r, g, b) in data
            )

            outfile.write(out_data)
            outfile.flush()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("imagefile")
    parser.add_argument("outfile")
    return parser.parse_args()


def main():
    args = parse_args()
    show(args.imagefile, args.outfile)


if __name__ == '__main__':
    main()
