# SwissFEL Data Files

This module provides an easy way of dealing with SwissFEL data files.

The main entry point is the `SFDataFile` class:

```python
from sfdata import SFDataFile
```

which itself is an `SFData` subclass that handles HDF5 files.

Files can be opened as contexts:

```python
with SFDataFile("run_000041.BSREAD.h5") as data:
    do_something_with(data)
```

in which case, they don't need to be closed manually. Or assigned to a variable

```python
data = SFDataFile("run_000041.BSREAD.h5")
do_something_with(data)
data.close()
```

where they should be closed at the end.

The channels within the HDF5 files are represented by the `SFChannel` class and can be retrieved from the SFData object like from a dictionary:

```python
ch = data["SLAAR11-LTIM01-EVR0:DUMMY_PV1_NBS"]
```

The pulse IDs and data content can be accessed via

```python
ch.pids
ch.data
```

which are HDF5 datasets. In order to actually read the data from the file, standard HDF5 syntax applies:

```python
ch.pids[:]
ch.data[100:200]
```

Subsets of the data can be accessed by giving several channel names

```python
subset = data["SLAAR11-LTIM01-EVR0:DUMMY_PV1_NBS", "SLAAR11-LTIM01-EVR0:DUMMY_PV2_NBS"]
```

which returns an `SFData` object that contains only the specified channels.

For correlating channels, a list of common pulse IDs needs to be created such that data points that belong to the same pulse can be matched. `SFData` can be converted to [pandas](https://pandas.pydata.org/) [DataFrames](https://pandas.pydata.org/docs/reference/frame.html) for this purpose:

```python
df = subset.to_dataframe()
```

This way, missing entries will be marked as NaNs, and can be dealt with via, e.g., [`dropna()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html).
