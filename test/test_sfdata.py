import re

from utils import TestCase
from consts import FNAME_ALL, FNAME_SCALARS, FNAME_ARRAYS, REPR_SUBSET, CH_NAMES, CH_1D_NAME, CH_ND_NAME, CH_1D_DATA, CH_1D_PIDS, ALL_PIDS, ANY_PIDS, PRINT_STATE_COMPLETE_FALSE, PRINT_STATE_COMPLETE_TRUE

from sfdata import SFDataFile, SFDataFiles


def remove_color_codes(line):
    ansi_chars = re.compile(r"\x1b\[[0-9;]*[mGKF]")
    return ansi_chars.sub("", line)



class TestSFData(TestCase):

    def run(self, *args, **kwargs):
        with SFDataFiles(FNAME_ALL) as data:
            self.data = data[data.names] # subset with all names to convert to plain SFData
            super().run(*args, **kwargs)

    def test_read_one_channel_data(self):
        self.assertAllEqual(
            self.data[CH_1D_NAME].data, CH_1D_DATA
        )

    def test_read_one_channel_pids(self):
        self.assertAllEqual(
            self.data[CH_1D_NAME].pids, CH_1D_PIDS
        )

    def test_pids(self):
        self.assertAllEqual(
            self.data.pids, ANY_PIDS
        )

    def test_all_pids(self):
        self.assertAllEqual(
            self.data.all_pids, ALL_PIDS
        )

    def test_names(self):
        self.assertEqual(
            sorted(self.data.names), CH_NAMES
        )

    def test_repr(self):
        self.assertEqual(
            repr(self.data), REPR_SUBSET
        )

    def test_names_file_vs_files(self):
        with SFDataFile(FNAME_SCALARS) as data1, SFDataFiles(FNAME_SCALARS) as data2:
            self.assertEqual(
                data1.names, data2.names
            )


    def test_print_stats(self):
#        self.maxDiff = None

        with self.assertStdout(PRINT_STATE_COMPLETE_FALSE):
            self.data.print_stats(show_complete=False, color=True)
        with self.assertStdout(PRINT_STATE_COMPLETE_TRUE):
            self.data.print_stats(show_complete=True, color=True)

        with self.assertStdout(remove_color_codes(PRINT_STATE_COMPLETE_FALSE)):
            self.data.print_stats(show_complete=False, color=False)
        with self.assertStdout(remove_color_codes(PRINT_STATE_COMPLETE_TRUE)):
            self.data.print_stats(show_complete=True, color=False)


    def test_add_channel(self):
        with SFDataFile(FNAME_SCALARS) as data1, SFDataFiles(FNAME_ARRAYS) as data2:
            old_names = data1.names
            expected_names = old_names | {CH_ND_NAME}

            addit_ch = data2[CH_ND_NAME]
            data1.add(addit_ch)

            new_names = data1.names

            self.assertEqual(
                new_names, expected_names
            )



