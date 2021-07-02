#!/usr/bin/env python

from utils import TestCase

from sfdata.errors import NoMatchingFileError, NoUsableFileError


class TestErrors(TestCase):

    def test_NoMatchingFileError(self):
        with self.assertRaises(NoMatchingFileError):
            raise NoMatchingFileError("some pattern")

    def test_NoUsableFileError(self):
        with self.assertRaises(NoUsableFileError):
            raise NoUsableFileError



