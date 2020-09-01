"""
Bouy packing tool.
"""

import argparse
# import base64
import os
import random
import tempfile
import time
import traceback

from PIL import Image
# from PIL import ImageFont
from PIL import ImageDraw
import msgpack
import qrcode

from stega import hide
from src import gps
from src import image as image_helpers
from src import audio as audio_helpers


def size(path):
    return os.path.getsize(path)


def draw_text(img):
    msg1 = " STOP!  Do not delete this image!\n This file is a message from someone using the BUOY messaging service."
    msg2 = " It may contain their last known location, or some other important information."
    msg3 = " Please upload this file to                    when you have Internet access."
    msg3a = " www.BUOY.one/found"

    draw = ImageDraw.Draw(img)
    draw.text((0, 0), msg1, (255, 255, 255))
    draw.text((0, 30), msg2, (255, 120, 120))
    draw.text((0, 45), msg3, (255, 255, 255))
    draw.text((161, 45), msg3a, (120, 255, 120))


def make_msg(data):
    head = f"BUOY Message\nSent by:Matt Cotton\ngeo:{data['gps']}\ntel:6175550123\nBASE64:".encode("utf-8")
    # tail = base64.b64encode(msgpack.dumps(data))
    tail = repr(data).encode("utf-8")
    msg = head + tail
    print(len(msg))
    return msg


def make_qr(bytez):
    qr = qrcode.QRCode()
    qr.add_data(bytez)
    return qr.make_image()


def add_qr(img, qr):
    qr = qr.resize((img.size[0] // 2, img.size[1] // 2))
    img.paste(qr, (img.size[0] // 4, img.size[1] // 4))


def add_extras(img, extras):
    out_path = "src-poc/poc.png"
    img.save(out_path, format='png')

    cap = img.size[0] * img.size[1]
    print(f"Capacity: {cap} bytes.")

    total = 0
    background = []
    if 'qr' in extras:
        part = len(extras['qr'])
        total += part
        print(f"qr: {part}")
        background.append(('qr', extras['qr']))
    if 'text' in extras:
        part = len(extras['text'])
        total += part
        print(f"text: {part}")
        background.append(('text', extras['text']))
    if 'audio' in extras:
        part = size(extras['audio'])
        total += part
        print(f"audio: {part}")
        with open(extras['audio'], 'rb') as infile:
            background.append(('audio', infile.read()))
    for image in extras['images']:
        part = size(image)
        total += part
        print(f"image: {part}")
        with open(image, 'rb') as infile:
            background.append(('image', infile.read()))

    print(f"Total: {total}")
    print(f"Remaining: {cap - total}")
    assert (cap - total) > 0

    packed = msgpack.dumps(background)
    print(f"Packed: {len(packed)}")
    print(f"True remaining: {cap - len(packed)}")
    assert len(packed) <= cap

    with open("data.raw", "wb") as datafile:
        datafile.write(packed)

    hide.hide(out_path, "data.raw", out_path)


def form_message(extras):
    has_text = 'text' in extras
    has_audio = 'audio' in extras
    has_images = len(extras['images'])

    data = {
        "v": 1,
        "uu": random.getrandbits(64),
        "gps": extras.get("gps", None),
        "t": int(time.time()),
        "s": "Matt Cotton",
        "e": [has_text, has_audio, has_images],
        "h": "...hash...",
    }
    return data


def form_extras(tempdir, images, audio=None, text=None):
    out = {}
    print(tempdir)

    if text:
        out['text'] = text

    if audio:
        out['audio'] = audio_helpers.shrink(audio, tempdir, "audio")

    out['images'] = []
    for (i, img_path) in enumerate(images, 1):
        try:
            img = Image.open(img_path)
            out['images'].append(image_helpers.shrink(img, tempdir, f"image{i}", length=700))

            gps_data = gps.gps_from_image(img)
            if gps_data:
                out['gps'] = gps_data
        except Exception:
            print(traceback.format_exc())

    return out


def form_buoy(extras):
    img = Image.new('RGB', (500, 500))
    draw_text(img)

    # data = form_message()
    # qr_msg = make_msg(data)
    # qr = make_qr(qr_msg)
    # add_qr(img, qr)
    # img.show()
    msg = make_msg(form_message(extras))
    add_qr(img, make_qr(msg))
    img.show()

    extras['qr'] = msg
    add_extras(img, extras)
    Image.open("src-poc/poc.png").show()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="*")
    parser.add_argument("-a", "--audio", nargs="?", type=str)
    parser.add_argument("-t", "--text", nargs="?", type=str)
    return parser.parse_args()


def main():
    args = parse_args()
    print(args)

    with tempfile.TemporaryDirectory() as tempdir:
        extras = form_extras(tempdir, args.images, audio=args.audio, text=args.text)
        print(extras)

        form_buoy(extras)


if __name__ == '__main__':
    main()
