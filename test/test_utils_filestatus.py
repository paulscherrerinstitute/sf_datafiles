#!/usr/bin/env python

import tempfile
import os
import grp
import getpass
from pathlib import Path
from datetime import datetime

from utils import TestCase

from sfdata.utils.filestatus import FileStatus


class TestUtilsFileStatus(TestCase):

    def run(self, *args, **kwargs):
        with tempfile.NamedTemporaryFile() as tf:
            self.tf = tf
            self.fs = FileStatus(tf.name)
            super().run(*args, **kwargs)


    def test_name(self):
        self.assertEqual(
            self.fs.name, self.tf.name
        )

    def test_repr(self):
        self.assertEqual(
            repr(self.fs), self.tf.name
        )

    def test_owner(self):
        self.assertEqual(
            self.fs.owner, getpass.getuser()
        )

    def test_group(self):
        groups = [grp.getgrgid(g).gr_name for g in os.getgroups()]
        self.assertTrue(
            self.fs.group in groups
        )

    def test_path(self):
        self.assertEqual(
            self.fs.path, Path(self.tf.name)
        )


    def test_times(self):
        stat = os.stat(self.tf.name)
        for a in ("atime", "mtime", "ctime"):
            v1 = getattr(self.fs, a)
            v2 = getattr(stat, "st_" + a)
            v2 = datetime.fromtimestamp(v2)
            self.assertEqual(
                v1, v2
            )

    def test_size(self):
        stat = os.stat(self.tf.name)
        self.assertEqual(
            self.fs.size, stat.st_size
        )



