
FNAME_SCALARS = "fake_data/run_test.SCALARS.h5"
FNAME_ARRAYS  = "fake_data/run_test.ARRAYS.h5"
FNAME_ALL     = "fake_data/run_test.*.h5"
FNAME_DF      = "fake_data/example_df.csv"

CH_1D_NAME      = "ch1"
CH_1D_COL_NAME  = "ch2"
CH_ND_NAME      = "ch5"

CH_NAMES = ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6"]

ANY_PIDS = [0, 2]
ALL_PIDS = [0, 1, 2]

CH_1D_PIDS      = [0, 1, 2]
CH_1D_DATA      = [0.1, 2.3, 4.5]
CH_1D_COL_DATA  = [6.7, 8.9, 0.1]
CH_ND_DATA1     = [[8.9, 0.1, 2.3], [4.5, 6.7, 8.9], [0.1, 2.3, 4.5]]

CH_ND_SHAPE = (3, 3, 3)

REPR_FILES   = 'SFDataFiles("fake_data/run_test.ARRAYS.h5", "fake_data/run_test.SCALARS.h5"): 6 channels'
REPR_FILE    = 'SFDataFile("fake_data/run_test.SCALARS.h5"): 3 channels'
REPR_SUBSET  = 'SFData: 6 channels'
REPR_CHANNEL = 'SFChannel: ch5'


PRINT_STATE_COMPLETE_FALSE = """
--------------------------------------------------------------------------------

\x1b[31mch3 2 / 3 -> 33% loss ▇▇▇▇▇▇\x1b[39m
\x1b[31mch6 2 / 3 -> 33% loss ▇▇▇▇▇▇\x1b[39m

\x1b[31mover the whole data set: 2 / 3 -> 33% loss\x1b[39m
\x1b[31mcomplete channels: 4 / 6 -> 33% incomplete\x1b[39m
\x1b[32mcomplete channels are hidden\x1b[39m

--------------------------------------------------------------------------------

"""


PRINT_STATE_COMPLETE_TRUE = """
--------------------------------------------------------------------------------

\x1b[32mch1 3 / 3 ->  0% loss ▇▇▇▇▇▇▇▇▇▇\x1b[39m
\x1b[32mch2 3 / 3 ->  0% loss ▇▇▇▇▇▇▇▇▇▇\x1b[39m
\x1b[31mch3 2 / 3 -> 33% loss ▇▇▇▇▇▇\x1b[39m
\x1b[32mch4 3 / 3 ->  0% loss ▇▇▇▇▇▇▇▇▇▇\x1b[39m
\x1b[32mch5 3 / 3 ->  0% loss ▇▇▇▇▇▇▇▇▇▇\x1b[39m
\x1b[31mch6 2 / 3 -> 33% loss ▇▇▇▇▇▇\x1b[39m

\x1b[31mover the whole data set: 2 / 3 -> 33% loss\x1b[39m
\x1b[31mcomplete channels: 4 / 6 -> 33% incomplete\x1b[39m

--------------------------------------------------------------------------------

"""



