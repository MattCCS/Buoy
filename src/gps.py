"""
"""

from PIL.ExifTags import TAGS, GPSTAGS


def get_decimal_coordinates(info):
    for key in ['Latitude', 'Longitude']:
        if ('GPS' + key) in info and ('GPS' + key + 'Ref') in info:
            e = info['GPS' + key]
            ref = info['GPS' + key + 'Ref']
            info[key] = (float(e[0]) +  # noqa
                         float(e[1]) / 60 +  # noqa
                         float(e[2]) / 3600  # noqa
            ) * (-1 if ref in ['S', 'W'] else 1)

    if 'Latitude' in info and 'Longitude' in info:
        return [info['Latitude'], info['Longitude']]

    return None


def gps_from_image(img):
    """Source: https://www.sylvaindurand.org/gps-data-from-photos-with-python/"""

    exif = img._getexif()

    if exif is not None:
        for k, v in exif.items():
            name = TAGS.get(k, k)
            exif[name] = exif.pop(k)

        if 'GPSInfo' in exif:
            for k in exif['GPSInfo'].keys():
                name = GPSTAGS.get(k, k)
                exif['GPSInfo'][name] = exif['GPSInfo'].pop(k)

    gpsinfo = exif['GPSInfo']
    print(gpsinfo)
    return get_decimal_coordinates(gpsinfo)
