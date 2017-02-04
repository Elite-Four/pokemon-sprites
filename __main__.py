#!/usr/bin/env python

from io import BytesIO
from os import path

import requests
from PIL import Image


def get_url(national_id, form_index):
    code = national_id | (form_index << 16)
    code = 0x159a55e5 * code & 0xFFFFFF
    return ('https://n-3ds-pgl-contents.pokemon-gl.com'
            '/share/images/pokemon/300/%06x.png') % (code,)


def main():
    base_dir = path.dirname(path.abspath(__file__))
    national_id = 1
    form_index = 0

    while True:
        sprite_id = '%d-%d' % (national_id, form_index)
        url = get_url(national_id, form_index)
        response = requests.get(url)

        if response.status_code != requests.codes.ok:
            print(sprite_id, 'fetch failed.')
            if form_index == 0:
                break
            national_id += 1
            form_index = 0
            continue

        print(sprite_id, 'fetched.')

        image = Image.open(BytesIO(response.content))
        width, height = image.size

        left_top = image.crop((0, 0, width >> 1, height >> 1))
        right_top = image.crop((width >> 1, 0, width, height >> 1))
        left_bottom = image.crop((0, height >> 1, width >> 1, height))
        right_bottom = image.crop((width >> 1, height >> 1, width, height))
        image.paste(left_top, (width >> 1, height >> 1))
        image.paste(right_top, (0, height >> 1))
        image.paste(left_bottom, (width >> 1, 0))
        image.paste(right_bottom, (0, 0))
        print(sprite_id, 'processed.')

        file_path = path.join(base_dir, 'docs/%s.png' % (sprite_id,))
        image.save(file_path, optimize=True)
        print(file_path, 'saved.')

        form_index += 1


if __name__ == '__main__':
    main()
