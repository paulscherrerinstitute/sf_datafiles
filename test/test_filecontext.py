#!/usr/bin/env python

import unittest.mock

from utils import TestCase

from sfdata.utils import FileContext


class TestFileContext(TestCase):

    def test_filecontext_init(self):
        """
        FileContext cannot be instantiated
        """
        with self.assertRaises(TypeError):
            FileContext()

    @unittest.mock.patch.multiple(FileContext, __abstractmethods__=set())
    def test_filecontext_close(self):
        """
        FileContext.close is an abstractmethod and not implemented
        """
        fc = FileContext()
        with self.assertRaises(NotImplementedError):
            fc.close()



