
from PIL import Image

import argparse
import math
import os
import struct


def hide(image_filename, data_filename, out_filename):
    img = Image.open(image_filename)
    print(repr(img))
    # assert img.format == "PNG"
    if not img.format == "PNG":
        img.save(image_filename + ".png")
        img = Image.open(image_filename + ".png")
    # assert img.mode == "RGB"
    if not img.mode == "RGB":
        img = img.convert("RGB")
    print(repr(img))

    with open(data_filename, "rb") as infile:
        msg = infile.read()

    msglen = len(msg)
    assert msglen < 2**32
    msglen_bytes = struct.pack("I", msglen)
    msg = msglen_bytes + msg
    print(msglen, msglen_bytes)

    (w, h) = img.size
    pixels = w * h
    assert len(msg) <= pixels

    lines = math.ceil(len(msg) / w)
    zone = img.crop((0, 0, w, lines))
    zone_pixels = w * lines
    zone_remaining_bytes = zone_pixels - len(msg)

    msg += os.urandom(zone_remaining_bytes)
    out_data = zone.getdata()
    in_data = [
        (
            (out_pixel[0] & ~0b111) + (msg_byte >> 5),
            (out_pixel[1] & ~0b111) + ((msg_byte >> 2) & 0b111),
            (out_pixel[2] & ~0b11) + (msg_byte & 0b11),
        )
        for (msg_byte, out_pixel) in zip(msg, out_data)
    ]

    out_img = img.copy()
    out_img.putdata(in_data)
    print(in_data[:4])
    out_img.save(out_filename)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("imagefile")
    parser.add_argument("datafile")
    parser.add_argument("outfile")
    return parser.parse_args()


def main():
    args = parse_args()
    hide(args.imagefile, args.datafile, args.outfile)


if __name__ == '__main__':
    main()
