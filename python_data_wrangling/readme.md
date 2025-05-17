# Python Data

This directory contains **data wrangling** logic to create the
files in the **data/ directory** of this repo.

The **duckdb** library is used in some cases here, such as with
the OpenFlights headerless CSV files which are cleansed and
converted to JSON document-per-line format.

## Sample Usage

### Create the Virtual Environment

Execute one of the following commands, macOS/Linux and Windows, respectively.

```
./venv.sh
.\venv.ps1
```

### Execute the program with CLI args

```
$ python main.py
Error: no CLI args provided
Usage:
  python main.py <func>
  python main.py merge_car_makes
  python main.py download_cars_data
  python main.py merge_downloaded_cars_data
  python main.py openflights_wrangle
```
