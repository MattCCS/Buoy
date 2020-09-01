# Audio

To convert audio to mono, at a specific bitrate:

    ffmpeg -i source.m4a -ac 1 -ab 12k mono12k.m4a

ac = audio channels
ab = audio bitrate
