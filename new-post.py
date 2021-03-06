#!/usr/bin/env python

import sys
import os
import datetime
import pipes
import subprocess

SETTINGS_FILE = '~/.office-doodles'

DEFAULT_SETTINGS = dict(
    office='Moscow, Yandex',
    taken_by='Alexander Artemenko',
    author='',
)


def readline(prompt=None):
    if prompt is not None:
        sys.stdout.write(prompt)
        sys.stdout.flush()
    return sys.stdin.readline().strip()


def read_settings():
    filename = os.path.expanduser(SETTINGS_FILE)
    if os.path.exists(filename):
        with open(filename) as f:
            return dict(
                map(lambda x: x.strip(), line.split(':', 1))
                for line in f.readlines()
            )
    return DEFAULT_SETTINGS


def write_settings(settings):
    with open(os.path.expanduser(SETTINGS_FILE), 'w') as f:
        f.write('\n'.join('%s: %s' % item for item in settings.items()))


def main():

    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s "Image Title"\n' % sys.argv[0])
        sys.exit(1)

    settings = read_settings()

    title = sys.argv[1]
    slug = '-'.join(title.lower().split())
    today = datetime.date.today()

    slug = readline('Slug [{0}]: '.format(slug)) or slug

    filename = os.path.join('_posts', '%s-%s.md' % (
        today.strftime('%Y-%m-%d'),
        slug
    ))

    if os.path.exists(filename):
        print('Warning: there is a post named "%s" for today already!' % slug)

    image_filename = os.path.join('images', '%s.jpg' % slug)

    office = readline('Office [{office}]: '.format(**settings))
    if not office:
        office = settings['office']

    taken_by = readline('Taken by [{taken_by}]: '.format(**settings))
    if not taken_by:
        taken_by = settings['taken_by']

    author = readline('Author [{author}]: '.format(**settings))
    if not author:
        author = settings['author']

    with open(filename, 'w') as f:
        f.write("""---
layout: post
slug: {slug}
title: {title}
office: {office}
by: {taken_by}
author: {author}
---""".format(**locals()))

    print('\n"{0}" written'.format(filename))

    commands = [
        ['git', 'add', filename, image_filename],
        ['git', 'commit', '-m', '%s added.' % title],
        ['git', 'push'],
    ]

    if os.path.isfile(image_filename):
        for command in commands:
            subprocess.call(command)
    else:
        print("\nImage %s not found! Post would not be added.\n"
              "You should add image and commit the post by "
              "hand:\n" % image_filename)
        for command in commands:
            print(' '.join(pipes.quote(i) for i in command))
        print("")

    write_settings(settings)


if __name__ == '__main__':
    main()
