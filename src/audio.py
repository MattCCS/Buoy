"""
Audio helpers.
"""


import pathlib
import subprocess


BITRATE = '12k'


def shrink(audio_path, tempdir, name):
    out_path = (pathlib.Path(tempdir) / name).with_suffix('.m4a')
    args = [
        'ffmpeg',
        '-i', audio_path,
        '-vn',  # no video
        '-ac', '1',  # channels=1
        '-ab', BITRATE,  # bitrate=BITRATE
        out_path,
    ]
    assert not subprocess.call(args)
    return out_path
