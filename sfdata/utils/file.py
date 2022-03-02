import os
from pathlib import Path


class File:

    def __init__(self, fname):
        self.name = fname


    @property
    def group(self):
        return self.path.group()

    @property
    def owner(self):
        return self.path.owner()

    @property
    def path(self):
        return Path(self.name)


    @property
    def atime(self):
        """Time of most recent access in seconds."""
        return self._stat().st_atime

    @property
    def mtime(self):
        """Time of most recent content modification in seconds."""
        return self._stat().st_mtime

    @property
    def ctime(self):
        """Time of most recent metadata change in seconds."""
        return self._stat().st_ctime

    @property
    def size(self):
        """Size of the file in bytes"""
        return self._stat().st_size

    def _stat(self):
        return os.stat(self.name)



