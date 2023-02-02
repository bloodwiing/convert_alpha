from glob import glob
import argparse
from PIL import Image
from PIL import PyAccess
from typing import Tuple
import re


def from_int_to_tuple(
    value: int
) -> Tuple[int, int, int]:
    return (value >> 16) & 255, (value >> 8) & 255, value & 255


def convert_alpha(
    image: Image.Image,
    /, *,
    alpha_colour: tuple
) -> PyAccess.PyAccess | None:
    if image.mode != 'RGBA':
        print('Cannot process image with no alpha channel')
        return None

    map = image.load()
    for y in range(image.height):
        for x in range(image.width):
            if map[x, y][3] == 0:
                map[x, y] = *alpha_colour, 0

    return map


def convert_file(
    file_name: str,
    /, *,
    alpha_colour: tuple | int
):
    print(f'Converting {file_name}')

    if isinstance(alpha_colour, int):
        alpha_colour = from_int_to_tuple(alpha_colour)

    with open(file_name, 'rb+') as file:

        image = Image.open(file)
        data = convert_alpha(image, alpha_colour=alpha_colour)

        if data:
            image.save(file_name)


def batch_convert(
    glob_path: str,
    /, *,
    alpha_colour: tuple | int
):
    print(f'Looking in pattern: {glob_path}')
    for file in glob(glob_path):
        convert_file(file, alpha_colour=alpha_colour)


HEX_PATTERN = r'([0-9a-fA-F]{6})'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Image Alpha Converter',
        description='Sets the alpha pixels to a specific colour to help combat bad compression algorithms that cause invisible pixels to bleed into opaque ones',
        epilog='Written by BLOODWIING -- Version 1.0'
    )

    parser.add_argument('files', nargs='+', help='The files to Batch convert', default=[])
    parser.add_argument('--colour', '--color', '-c', help='Converts alpha to a given RGB colour, written in the RGB format', default='000000')

    args = parser.parse_args()

    if not hasattr(args, 'colour'):
        print('Missing argument --colour\n'
              'Script terminating!\n')
        parser.print_usage()
        exit(1)

    colour_match = re.match(HEX_PATTERN, args.colour)
    if colour_match is None:
        print('Invalid value passed in --colour\n'
              'Make sure it is a HEX string of the following format: RRGGBB\n'
              'Do not add any extra characters\n')
        parser.print_usage()
        exit(2)

    alpha_colour = int(colour_match.group(1), 16)

    if not hasattr(args, 'files') or len(args.files) == 0:
        print('No file patterns were detected\n'
              'Please provide at least one file path\n')
        parser.print_usage()
        exit(3)

    for file in args.files:
        batch_convert(file, alpha_colour=alpha_colour)