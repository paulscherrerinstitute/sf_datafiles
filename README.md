# SwissFEL Data Files

## Open (and close) a file

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

## Channels

A list of available channels can be viewed via

```python
data.names
```

The channels within the HDF5 files are represented by the `SFChannel` class and can be retrieved from the `SFData` object like from a dictionary:

```python
ch = data["SLAAR11-LTIM01-EVR0:DUMMY_PV1_NBS"]
```

The pulse IDs and data contents can be accessed via

```python
ch.pids
ch.data
```

which reads the full arrays at once from the HDF5 file (it should be noted that this is currently not cached!). In most cases, this will be the preferred way of reading data.

In case the underlying HDF5 datasets need to be accessed, e.g., for reading only specific parts of the data, channels have a `datasets` namespace attached: 

```python
ch.datasets.pids
ch.datasets.data
```

In order to actually read the data from the file in this case, standard HDF5 syntax applies:

```python
ch.datasets.pids[:]
ch.datasets.data[100:200]
```

## Subsets

Subsets of the data can be accessed by giving several channel names

```python
subset = data["SLAAR11-LTIM01-EVR0:DUMMY_PV1_NBS", "SLAAR11-LTIM01-EVR0:DUMMY_PV2_NBS"]
```

which returns an `SFData` object that contains only the specified channels.

## Drop missing pulses

For correlating channels, pulse IDs that are not available in all channels need to be removed. This can be achieved via

```python
subset.drop_missing()
```

resulting in data where data points that belong to the same pulse are matched. Internally, this is handled by updating each channels `.valid` attribute, which can be a boolean index or a list of coordinates (/indices) within the datasets (note: due to a [limitation of h5py](https://github.com/h5py/h5py/issues/626), this is only true for 1D datasets, for 2D or more only the latter works!).

The valid marker is per channel, and subsets are real subsets of the original data. Thus, valid markers set on a subset are also set for the larger parent data.

In case all `.drop_missing()` operations need to be reverted, both `SFChannel` and `SFData` have a `.reset_valid()` method (where the latter loops over the former). These reset the valid marker(s) to all pulse IDs that are in the respective underlying dataset. Note that each `.drop_missing()` calls `.reset_valid()` before calculating the new `valid` marker.

## Convert to DataFrame

For more complex treatment of missing pulse IDs, e.g., imputation, `SFData` can be converted to [pandas](https://pandas.pydata.org/) [DataFrames](https://pandas.pydata.org/docs/reference/frame.html):

```python
df = subset.to_dataframe()
```

This way, missing entries will be marked as NaNs, and can be dealt with via, e.g., [`dropna()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html) or [`fillna()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html).


