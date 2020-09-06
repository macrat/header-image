from typing import Tuple
import argparse
import re

from PIL import Image, ImageDraw


Size = Tuple[int, int]
Color = Tuple[int, int, int]


def genImage(size: Size, bg: Color, fg: Color, rate=0.75) -> Image:
    img = Image.new('RGB', size, bg)
    draw = ImageDraw.Draw(img)

    width, height = size

    for x in range(1, width, 2):
        length = x * rate

        for i in range(0, width, x):
            draw.line((i, 0, i, length), fill=fg)
            draw.line((i, height, i, height - length), fill=fg)

        for i in range(0, height, x):
            draw.line((0, i, length, i), fill=fg)
            draw.line((width, i, width - length, i), fill=fg)

    return img


def size(string: str) -> Size:
    """ Parse size string like a "1200x600"

    >>> size('1200x600')
    (1200, 600)
    >>> size('1x2')
    (1, 2)

    >>> size('1200')
    Traceback (most recent call last):
      ...
    TypeError: "1200" is invalid size.

    >>> size('0x1')
    Traceback (most recent call last):
      ...
    TypeError: "0x1" is invalid size.
    >>> size('1x0')
    Traceback (most recent call last):
      ...
    TypeError: "1x0" is invalid size.
    """

    m = re.match(
        '^(?P<width>[1-9][0-9]*)[xX](?P<height>[1-9][0-9]*)$',
        string,
    )

    if m is None:
        raise TypeError(f'"{string}" is invalid size.')

    return (
        int(m.group('width')),
        int(m.group('height')),
    )


def color(string: str) -> Color:
    """ Parse color string like a "#007fff"

    >>> color('#007fff')
    (0, 127, 255)
    >>> color('#000000')
    (0, 0, 0)
    >>> color('#fFfFfF')
    (255, 255, 255)

    >>> color('#1234567')
    Traceback (most recent call last):
      ...
    TypeError: "#1234567" is invalid color format.

    >>> color('#00000G')
    Traceback (most recent call last):
      ...
    TypeError: "#00000G" is invalid color format.
    """

    m = re.match(
        '^#(?P<red>[0-9a-fA-F]{2})(?P<green>[0-9a-fA-F]{2})(?P<blue>[0-9a-fA-F]{2})$',
        string,
    )

    if m is None:
        raise TypeError(f'"{string}" is invalid color format.')

    return (
        int(m.group('red'), 16),
        int(m.group('green'), 16),
        int(m.group('blue'), 16),
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'size',
        help='width of the header image.',
        default='1280x640',
        type=size,
    )
    parser.add_argument(
        '-o',
        '--output',
        help='output file name.',
        metavar='FILE',
    )
    parser.add_argument(
        '--bg',
        type=color,
        default='#000000',
        metavar='#000000',
        help='background color.',
    )
    parser.add_argument(
        '--fg',
        type=color,
        default='#ffffff',
        metavar='#ffffff',
        help='foreground color.',
    )

    args = parser.parse_args()

    img = genImage(args.size, args.bg, args.fg)
    if args.output is None:
        img.show()
    else:
        img.save(args.output)
