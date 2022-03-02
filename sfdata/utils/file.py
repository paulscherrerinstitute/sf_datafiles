import os
from datetime import datetime
from pathlib import Path


fromtimestamp = datetime.fromtimestamp


class File:

    def __init__(self, fname):
        self.name = fname

    def __repr__(self):
        return self.name


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
        t = self._stat().st_atime
        return fromtimestamp(t)

    @property
    def mtime(self):
        """Time of most recent content modification in seconds."""
        t = self._stat().st_mtime
        return fromtimestamp(t)

    @property
    def ctime(self):
        """Time of most recent metadata change in seconds."""
        t = self._stat().st_ctime
        return fromtimestamp(t)

    @property
    def size(self):
        """File size in bytes"""
        return self._stat().st_size

    def _stat(self):
        return os.stat(self.name)



