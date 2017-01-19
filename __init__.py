"""
Nase Live Wallpaper
~~~~~~~~~~~~~~~~~~~

Is a python script, that fetches NASA Images of the day
and sets one after another as your desktop background.
"""

__title__ = 'Nase Live Wallpaper'
__version__ = '0.1.0'
__author__ = 'Yves Kaufmann'
__all__ = ['live_wallpaper', 'set_image']

import sys
if sys.platform != 'linux' and sys.platform != 'win32':
    raise NotImplementedError(
        'The platform %s isn\'t supported.' % sys.platform
    )

from .wallpaper import set_image
from .wallpaper import live_wallpaper
