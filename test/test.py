#!/usr/bin/env python3

# coverage run --source sfdata -m unittest discover && coverage report -m

#TODO:
# add test for unique pids handling


import os
import sys

this_dir = os.path.dirname(__file__)
sys.path.insert(0, (os.path.join(this_dir, "..")))


if __name__ == '__main__':
    from test_sfdata import TestSFData
    from test_sfdatafile import TestSFDataFile
    from test_sfdatafiles import TestSFDataFiles
    from test_sfchannel import TestSFChannel
    from test_sfchanneljf import TestSFChannelJF
    from test_sfscaninfo import TestSFScanInfo
    from test_sfprocfile import TestSFProcFile
    from test_errors import TestErrors
    from test_filecontext import TestFileContext
    from test_ign import TestIgn
    from test_utils import TestUtils
    from test_utils_filestatus import TestUtilsFileStatus

    import unittest
    unittest.main()



