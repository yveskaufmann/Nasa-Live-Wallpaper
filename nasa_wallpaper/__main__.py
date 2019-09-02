from __future__ import absolute_import

import click
import nasa_wallpaper

@click.command()
@click.option("-i", "--images-per-day", default=5, type=click.IntRange(min=-1), help='The count of images that should be loaded each day. The default is 5. A negative value will disable this limit.')
@click.option("-r", "--change-rate", default=20, type=click.IntRange(min=0), help='The time in seconds after which the image should change. The default is 5.')
def main(images_per_day, change_rate):
    nasa_wallpaper.live_wallpaper(images_per_day, change_rate)

if __name__ == '__main__':
    main()