import os
import sys
import subprocess
import time

from functools import wraps
from urllib.request import urlopen

from lxml import etree
from lxml import html


BACKGROUND_SCHEMA = '/org/gnome/desktop/background'
BACKGROUND_IMAGE_URI = 'picture-uri'
BACKGROUND_IMAGE_OPTIONS = 'picture-options'
WALLPAPER_FOLDER = '~/Pictures/Wallpapers/nasa'
WALLPAPER_CHANGE_RATE = 20


def live_wallpaper():

    images = load_nasa_images()
    current_image = -1
    keep_running = True

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
            image_path = download_when_required(image['image_url'])
            set_image(image_path)
        except:
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
        if item and len(item) > 0 and item[0].has_key('href'):
            image_url = nasa_apod + item[0].get('href')
            images.insert(0, {
                'image_url': image_url
            })
    return images


def download_when_required(image_url):
    wallpaper_folder = os.path.expanduser(WALLPAPER_FOLDER)

    if not os.path.isdir(wallpaper_folder):
        os.mkdir(wallpaper_folder)

    image_name = image_url.split('/')[-1]
    image_path = os.path.join(wallpaper_folder, image_name)

    if not os.path.isfile(image_path):
        try:
            with urlopen(image_url) as image:
                with open(image_path, 'wb') as out:
                    out.write(image.read())
        except:
            # Remove uncomplete files when a download failed
            os.unlink(image_path)

    return image_path


def set_image(image_path):
    """
    Set the image at the given path as the current wallpaper.

    image_path  -   The path to the wallpaper image.

    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(image_path)

    if not os.path.isabs(image_path):
        image_path = os.path.realpath(image_path)

    if sys.platform == 'linux':
        if not image_path.startswith('file://'):
            image_path = 'file://' + image_path

        image_path = "\"{0}\"".format(image_path)
        dconf_args = ['/usr/bin/dconf', 'write', BACKGROUND_SCHEMA + '/' + BACKGROUND_IMAGE_URI, image_path]
        subprocess.run(dconf_args, stdout=subprocess.PIPE)

    if sys.platform == 'win32':
        import ctypes
        SPI_SETDESKWALLPAPER = 0x0014
        SPIF_SENDWININICHANGE = 0x2
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, SPIF_SENDWININICHANGE)


def terminate_handler(handler):
    sys_excepthook = sys.excepthook

    @wraps(handler)
    def terminate_handler(extype, value, tb):
        if extype is KeyboardInterrupt:
            if callable(handler):
                handler()
        else:
            sys_excepthook(extype, value, tb)
    sys.excepthook = terminate_handler
    return terminate_handler


if __name__ == '__main__':
    live_wallpaper()
