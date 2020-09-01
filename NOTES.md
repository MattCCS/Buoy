# Notes


## Audio
- AAC (via .m4a and ffmpeg) is very flexible w/r/t bitrate.

- 12k AAC is still intelligble.
    - This comes out to about 100KB per minute.


## QR Code
- Max data size is about 3KB.

- This could store:
    - (version, UUID)
    - GPS
    - date/time
    - sender, signature, public key hash
    - recipient, public key hash
    - checksum
    - IP, domain, email
    - (presence of image, video, audio)

- msgpack data before qr code


## Image
- How to encode an image behind a human-readable QR code and text?
    1. All pixels must be black or white.  Any deviation is data.
        - problem: how much deviation to allow?
            - Must be such that the highest value on black next to lowest on white is easily distinguished.
            - E.g. assuming [0,255], say [65,190].  Thus each pixel can have 128 values (2^7).
        - problem: this prevents the possibility of color.
            - May or may not be an issue.
            - But hamstringing ourselves early is undesirable.
    2. All pixels must be 100% luminance or 0% luminance.  Any deviation is data.
        - problem: how to enforce this?  sounds slow.
    3. All pixels' 8 LSBs are data.
        - allows color!
        - not much math involved, just bit slicing.
