"""
This modules implements the Linux implementation of LiveWallpaper
"""

import os
import subprocess

from .base import AbstractLiveWallpaper

BACKGROUND_SCHEMA = '/org/gnome/desktop/background'
BACKGROUND_IMAGE_URI = 'picture-uri'
BACKGROUND_IMAGE_OPTIONS = 'picture-options'
IMAGE_FOLDER = '~/Pictures'

class LinuxLiveWallpaper(AbstractLiveWallpaper):
    """
    Linux implementation of LiveWallpaper
    """ 

    def set_image(self, path_to_image):

        if not path_to_image.startswith('file://'):
            path_to_image = 'file://' + path_to_image

        image_path = "\"{0}\"".format(path_to_image)
        dconf_args = [
            '/usr/bin/dconf',
            'write',
            BACKGROUND_SCHEMA + '/' + BACKGROUND_IMAGE_URI, image_path
        ]
        subprocess.run(dconf_args, stdout=subprocess.PIPE)



    def get_picture_folder(self):
        return os.path.expanduser(IMAGE_FOLDER)

