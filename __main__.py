#!/usr/bin/env python

from logging import getLogger, StreamHandler
from os import path
from sys import stderr

import requests

logger = getLogger(__name__)
logger.setLevel('INFO')
logger.addHandler(StreamHandler(stream=stderr))


def _get_url(national_id, form_index):
    if form_index == 0:
        return ('https://assets.pokemon.com'
                '/assets/cms2/img/pokedex/full/'
                '%03d.png') % (national_id,)
    else:
        return ('https://assets.pokemon.com'
                '/assets/cms2/img/pokedex/full/'
                '%03d_f%d.png') % (national_id, form_index + 1)


def main():
    base_dir = path.dirname(path.abspath(__file__))
    national_id = 1
    form_index = 0

    while True:
        if form_index == 0:
            sprite_id = '%d' % (national_id,)
        else:
            sprite_id = '%d-%d' % (national_id, form_index)
        url = _get_url(national_id, form_index)
        response = requests.get(url)

        if response.status_code != requests.codes.ok:
            logger.warning('%s fetch failed.', sprite_id)
            if form_index == 0:
                break
            national_id += 1
            form_index = 0
            continue

        logger.info('%s fetched.', sprite_id)

        file_path = path.join(base_dir, 'docs/%s.png' % (sprite_id,))
        with open(file_path, 'wb') as f:
            f.write(response.content)
        logger.info('%s saved.', file_path)

        form_index += 1


if __name__ == '__main__':
    main()
