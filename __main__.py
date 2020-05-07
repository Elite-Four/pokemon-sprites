#!/usr/bin/env python

from logging import getLogger, StreamHandler
from os import path
from sys import stderr

from jinja2 import Environment, FileSystemLoader
import requests

base_dir = path.dirname(path.abspath(__file__))

logger = getLogger(__name__)
logger.setLevel('INFO')
logger.addHandler(StreamHandler(stream=stderr))

env = Environment(loader=FileSystemLoader(base_dir))


def main():
    national_id = 1
    form_index = 0
    images = []

    while True:
        if form_index == 0:
            sprite_id = '%d' % (national_id,)
            url = ('https://assets.pokemon.com'
                   '/assets/cms2/img/pokedex/full/'
                   '%03d.png') % (national_id,)
        else:
            sprite_id = '%d-%d' % (national_id, form_index)
            url = ('https://assets.pokemon.com'
                   '/assets/cms2/img/pokedex/full/'
                   '%03d_f%d.png') % (national_id, form_index + 1)

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
        images.append('%s.png' % (sprite_id,))

        logger.info('%s saved.', file_path)

        form_index += 1

    file_path = path.join(base_dir, 'docs/index.html')
    template = env.get_template('index.jinja2')
    with open(file_path, 'w') as f:
        f.write(template.render(images=images))


if __name__ == '__main__':
    main()
