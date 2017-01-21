import os
import sys
import time

from functools import wraps
from urllib.request import urlopen

from lxml import etree
from lxml import html

from .native import LiveWallpaper 

WALLPAPER_CHANGE_RATE = 20

def live_wallpaper():

    images = load_nasa_images()
    current_image = -1
    keep_running = True
    wallpaper = LiveWallpaper()

    @terminate_handler 
    def exit_handler():
        nonlocal keep_running
        keep_running = False
        print("Terminating live_wallpaper...")

    while keep_running:
        current_image += 1
        if current_image >= len(images):
            current_image = 0
        image = images[current_image]
        try:
            image_path = download_when_required(
                image['image_url'],
                wallpaper.get_wallpaper_folder()
            )
            wallpaper.set_image(image_path)
        except IOError:
            print("Failed to load image {0}".format(image['image_url']))

        time.sleep(WALLPAPER_CHANGE_RATE)


def load_nasa_images(): 

    images = []
    nasa_rss_feed = 'https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss'
    nasa_apod = 'https://apod.nasa.gov/apod/'

    with urlopen(nasa_rss_feed) as res:
        tree = etree.parse(res)

        for item in tree.findall('./channel/item'):
            images.append({
                'image_url': item.find('enclosure').get('url')
            })

    with urlopen(nasa_apod) as res:
        tree = html.parse(res)
        item = tree.xpath('/html/body/center[1]/p[2]/a')
        if item and len(item) > 0 and item[0].get('href'):
            image_url = nasa_apod + item[0].get('href')
            images.insert(0, {
                'image_url': image_url
            })
    return images


def download_when_required(image_url, wallpaper_folder):

    wallpaper_folder = os.path.expanduser(wallpaper_folder)
    if not os.path.isdir(wallpaper_folder):
        os.makedirs(wallpaper_folder)

    image_name = image_url.split('/')[-1]
    image_path = os.path.join(wallpaper_folder, image_name)

    if not os.path.isfile(image_path):
        try:
            with urlopen(image_url) as image:
                with open(image_path, 'wb') as out:
                    out.write(image.read())
        except:
            # A existence of a uncomplete files prevents its redownload and
            # its usage is not desired hence we have to delete them.
            os.unlink(image_path)

    return image_path

def terminate_handler(handler):
    """
    Terminate handler decorator, is used to mark
    a function which should be called if a user
    triggers a KeyboardInterrupt by pressing ctrl+c.
    """

    sys_excepthook = sys.excepthook
    @wraps(handler)
    def _terminate_handler(extype, value, tb_param):
        if extype is KeyboardInterrupt:
            if callable(handler):
                handler()
        else:
            sys_excepthook(extype, value, tb_param)
    sys.excepthook = _terminate_handler
    return _terminate_handler


if __name__ == '__main__':
    live_wallpaper()
