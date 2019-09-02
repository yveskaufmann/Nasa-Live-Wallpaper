from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

import sys

if sys.platform.startswith('linux'):
    from .linux import LinuxLiveWallpaper as LiveWallpaper

if sys.platform.startswith('win32'):
    from .win32 import Win32LiveWallpaper as LiveWallpaper

if sys.platform.startswith('darwin'):
    from .macosx import MacOSLiveWallpaper as LiveWallpaper
