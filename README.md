# Buoy

An emergency message format.

[buoy.one](http://buoy.one/)


# Goals
- human-"friendly"
    - meaning a human can see the file and understand what it is, and what to do
    - does not mean totally human friendly
- multimedia support
    - text, gps
    - audio, image
    - video
- robust; qr code for essential data
    - if message is printed/screenshotted
    - less essential data xor'd within image (a la steganography)
- flexible delivery
    - image format
    - can be Airdropped, or otherwise sent over Bluetooth
    - should be friendly between devices/manufacturers/carriers
- dynamic
    - public and/or private info
    - optional delivery instructions (server, email, IP, etc.)
    - optional sender info
    - ?
