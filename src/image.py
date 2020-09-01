"""
Image helpers.
"""


import pathlib


def cap(img, length=1000):
    dmax = max(img.size)
    if dmax <= length:
        return img
    r = dmax / length
    return img.resize((round(img.size[0] / r), round(img.size[1] / r)))


def shrink(img, dirpath, name, length=1000, quality=50):
    out_path = (pathlib.Path(dirpath) / name).with_suffix(".jpg")
    cap(img, length=length).save(out_path, quality=quality, optimize=True)
    return out_path
