"""
This modules implements the Linux implementation of LiveWallpaper
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import subprocess

from .base import AbstractLiveWallpaper


IMAGE_FOLDER = '/Library/Desktop Pictures'


class MacOSLiveWallpaper(AbstractLiveWallpaper):
    """
    MacOS implementation of LiveWallpaper
    """

    def set_image(self, path_to_image):

        image_path = "\"{0}\"".format(path_to_image)
        SCRIPT = """/usr/bin/osascript<<END
        tell application "Finder"
        set desktop picture to POSIX file "{0}"
        end tell
        END"""

        subprocess.Popen(SCRIPT.format(path_to_image), shell=True)

    def get_picture_folder(self):
        return os.path.expanduser(IMAGE_FOLDER)
