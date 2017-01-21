import sys

if sys.platform == 'linux':
    from .linux import LinuxLiveWallpaper as LiveWallpaper
elif sys.platform == 'win32':
    from .win32 import Win32LiveWallpaper as LiveWallpaper
