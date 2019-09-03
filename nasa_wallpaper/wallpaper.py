from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import sys
import time
import click

import xml.etree.ElementTree as ET
import requests

from functools import wraps
from bs4 import BeautifulSoup

from .native import LiveWallpaper

def live_wallpaper(images_per_day, change_rate):

    images = load_nasa_images(images_per_day=images_per_day)
    current_image = -1
    keep_running = True
    wallpaper = LiveWallpaper()

    @terminate_handler
    def exit_handler():
        # nonlocal keep_running
        exit_handler.keep_running = False
        print("Terminating live_wallpaper...")

    exit_handler.keep_running = True
    while exit_handler.keep_running:
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
        except IOError as e:
            print("Failed to load image {0} caused by {1}".format(image['image_url'], e))

        time.sleep(change_rate)


def load_nasa_images(images_per_day=5):

    images = []
    NASE_RSS_FEED = 'https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss'
    NASA_APOD_URL = 'https://apod.nasa.gov/apod/'

    res = requests.get(NASE_RSS_FEED)
    tree = ET.fromstring(res.content)

    for index, item in enumerate(tree.findall('./channel/item'), 0):
        if images_per_day > 0 and index >= images_per_day - 1:
            break

        images.append({
            'image_url': item.find('enclosure').get('url')
        })

    res = requests.get(NASA_APOD_URL)
    soup = BeautifulSoup(res.content, 'html.parser')
    items = soup.select('a > img')
    for item in items:
        image_url = NASA_APOD_URL + item.find_parent('a')['href']
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
            with requests.get(image_url) as image:
                with open(image_path, 'wb') as out:
                    out.write(image.content)
        except Exception as e:
            print("Failed to download file caused by {0}".format(e))
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

