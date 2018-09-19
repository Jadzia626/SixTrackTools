# SixTrack Tools

Written by: Veronica Berglyd Olsen, CERN (BE-ABP-HSS), Geneva, Switzerland

A Python module, `sttools`, with tools for analysing data from [SixTrack](http://sixtrack.web.cern.ch) simulations.

To test that the module is working, run `pytest-3` from the root folder.

## Main Features

### Simulation Wrapper

The `SixTrackSim` wrapper class provides an iterable object that wraps a folder containing a set of related simulations. The class will create an instance of either the `H5Wrapper` if the folder contains HDF5 files, or `FileWrapper` if the folder contains subfolders.

Since `SixTrackSim` is an iterable object, it behaves like a list of simulations. The following operations are therefor valid:

```python
from sttools import SixTrackSim

with SixTrackSim("/path/to/datafolder") as stSim:
    print(stSim)                       # Prints a summary of the simulations in the set
    nSims = len(stSim)                 # The number of simulations available
    hasSim = "SimulationName" in stSim # Check if a certain simulation exists
    simData = stSim["SimulationName"]  # Access a numpy matrix of the data referenced by name
    simData = stSim[0]                 # Access a numpy matrix of the data referenced by index
    for simData in stSim:              # Iterate through all available simulations
        simData.something()            
```
### DataSet Wrapper

The `DataSet` class provides a similar interface for a specific dataset of the simulation. Its constructor takes a `SixTrackSim` object as input as well as the name of a dataSet.

The resulting object is also iterable over simulations in the folder, as above, but will now contain a set of numpy arrays representing the data contained in that dataset. This interface is uniform for HDF5 and TEXT format in terms of columns (as long as they are produced by SixTrack), but the TEXT version does not contain the same meta data.

```python
from sttools import SixTrackSim, DataSet

with SixTrackSim("/path/to/datafolder") as stSim:
    with DataSet("dist0",stSim) as dSet:
        for dist0 in dSet:
            print(sum(dist0["X"]))
```