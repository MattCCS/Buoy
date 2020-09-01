"""
Buoy proof-of-concept.
"""

import base64

from PIL import Image
# from PIL import ImageFont
from PIL import ImageDraw
import msgpack
import qrcode

from stega import hide


def draw_text(img):
    msg1 = """STOP!  Do not delete this image!\nThis file is a message from someone using the BUOY messaging service."""
    msg2 = "It may contain their last known location, or some other important information."
    msg3 = "Please upload this file to                    when you have Internet access."
    msg3a = "www.BUOY.one/found"

    draw = ImageDraw.Draw(img)
    draw.text((0, 0), msg1, (255, 255, 255))
    draw.text((0, 30), msg2, (255, 120, 120))
    draw.text((0, 45), msg3, (255, 255, 255))
    draw.text((161, 45), msg3a, (120, 255, 120))


def make_msg(data):
    head = "BUOY Message\nSent by:Matt Cotton\ngeo:45.264612,-72.135512\ntel:6032752718\nBASE64:".encode("utf-8")
    tail = base64.b64encode(msgpack.dumps(data))
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


def main():
    img = Image.new('RGB', (500, 500))

    draw_text(img)
    # img.show()

    data = {
        "v": 1,
        "uu": 17534247867542,
        "gps": [42354, -710669444],
        "t": 163001030,
        "s": "matt",
        "r": "nat",
        "t": ["ip", "10.0.1.5"],
        "c": [False, False, True],
    }
    qr_msg = make_msg(data)
    qr = make_qr(qr_msg)
    add_qr(img, qr)
    # img.show()

    import tempfile
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.png') as temp:
        print(temp.name)
        img.save(temp, format='png')
        hide.hide(temp.name, "src-poc/mono12k.m4a", "src-poc/poc.png")

    Image.open("src-poc/poc.png").show()


if __name__ == '__main__':
    main()
