"""
This modules implements the Windows implementation of LiveWallpaper
"""

import ctypes
from ctypes import Structure

from .base import AbstractLiveWallpaper
from .base import BackgroundChangeNotPossible

class Win32LiveWallpaper(AbstractLiveWallpaper):
    """
    Windows implementation of LiveWallpaper
    """

    def set_image(self, path_to_image):

        succeeds = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0,
            path_to_image, SPIF_SENDWININICHANGE
        )

        if not succeeds:
            raise BackgroundChangeNotPossible(
                "Failed to change background to {0}".format(path_to_image)
            )


    def get_picture_folder(self):

        picture_folder = ctypes.c_wchar_p(chr(0) * 255)
        ctypes.windll.shell32.SHGetKnownFolderPath(
            ctypes.byref(_FOLDERID_PICTURES),
            0,
            None,
            ctypes.byref(picture_folder)
        )

        return picture_folder.value


class _GUID(Structure):
    _fields_ = [
        ('Data1', ctypes.c_ulong),
        ('Data2', ctypes.c_ushort),
        ('Data3', ctypes.c_ushort),
        ('Data4', ctypes.c_char * 8)
    ]

"""
Known Folder id for the picture folder.
See https://msdn.microsoft.com/en-us/library/windows/desktop/dd378457(v=vs.85).aspx for details.
"""
_FOLDERID_PICTURES = _GUID(
    0x33E28130,
    0x4E1E,
    0x4676,
    bytes([0x83, 0x5A, 0x98, 0x39, 0x5C, 0x3B, 0xC3, 0xBB]))

"""
SystemParametersInfo param uiAction: Change Desktop Win32LiveWallpaper

See https://msdn.microsoft.com/en-us/library/windows/desktop/ms724947(v=vs.85).aspx
"""
SPI_SETDESKWALLPAPER = 0x0014

"""
SystemParametersInfo param fWinIni

See https://msdn.microsoft.com/en-us/library/windows/desktop/ms724947(v=vs.85).aspx
"""
SPIF_SENDWININICHANGE = 0x2
