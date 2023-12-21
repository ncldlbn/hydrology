# Hydropower plant exercise

## Set up
Run from command line to install dependencies:
```
pip install requirements.txt
```
### Input files
The following input files must located in `./data/in` folder.

- *hypsometric-curve.csv*
- *reservoir-elevation-volume.csv*

### Parameters
Model parameters can be set in `/src/params.py` file.

## Usage
Run from command line to perform calculation:
```
python main.py [--snow]
```
- `--snow` [*optional*] - to perform calculation considering snow precipitation.

## Output
### Main output files
Water level and overflow time series for each scenario.

Files are located in `./data/out`:
- *output.csv*
- *output-snow.csv*

### Detailed output files
Time series of all variables used in the reservoir water balance simulations. 

Files are located in `./data/out/detailed-output`:
- *scenario_1.csv*
- *scenario_2.csv*
- *scenario_3.csv*
- *scenario_1_snow.csv*
- *scenario_2_snow.csv*
- *scenario_3_snow.csv*

The following output are also available in `./data/out/detailed-output`:
- *hydrograph.png*
- *hydrograph.csv*
- *elevation-volume-interpolation.png*