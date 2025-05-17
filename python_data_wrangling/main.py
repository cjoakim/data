"""
Usage:
  python main.py <func>
  python main.py merge_car_makes
  python main.py download_cars_data
  python main.py merge_downloaded_cars_data
  python main.py openflights_wrangle
  python main.py sean_lahman_baseball_data_to_json
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import json
import logging
import sys
import time
import os
import traceback
import urllib.parse

import duckdb
import httpx

from docopt import docopt
from dotenv import load_dotenv
#from six import moves 

from src.io.fs import FS
from src.os.env import Env
from src.os.system import System


def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version="1.0.0")
    print(arguments)


def check_env():
    load_dotenv(override=True)
    for name in sorted(os.environ.keys()):
        if name.startswith("LOCAL_PG_"):
            print("{}: {}".format(name, os.environ[name]))
    print("check_env - username: {}".format(Env.username()))


def merge_car_makes():
    infiles = [ "../data/cars/makes1.json", "../data/cars/makes2.json" ]
    all_car_makes = dict()
    for infile in infiles:
        data = FS.read_json(infile)
        results = data["results"]
        for result in results:
            make = result["make"]
            all_car_makes[make] = 1
    FS.write_json(all_car_makes, "tmp/all_car_makes.json")

def download_cars_data():
    infile = "../data/cars/all_car_makes.json"
    all_car_makes = FS.read_json(infile)
    for idx, make in enumerate(all_car_makes):
        print("{}: {}".format(idx, make))
        download_models_for_make(make)

def download_models_for_make(make):
    url_template = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/all-vehicles-model/records?select=make%2C%20model%2C%20city08u%2C%20highway08u%2C%20comb08u%2C%20cylinders%2C%20displ%2C%20drive%2C%20eng_dscr%2C%20fueltype1%2C%20id%2C%20trany%2C%20vclass%2C%20year%2C%20mfrcode%2C%20basemodel&where=make%20%3D%20%22{}%22&order_by=make%2C%20model%2C%20year&limit={}&offset={}"
    continue_to_process, limit, offset, seq = True, 100, -100, 0
    encoded_make = urllib.parse.quote(make)
    print("MAKE: {}  encoded: {}".format(make, encoded_make))

    while continue_to_process:
        seq = seq + 1
        if seq > 100:
            continue_to_process = False
        else:
            try:
                offset = offset + limit
                url = url_template.format(encoded_make, limit, offset)
                print("URL: {}".format(url))
                outfile = "tmp/{}-{}.json".format(make.replace(" ", "_"), seq)
                time.sleep(1)
                resp = httpx.get(url)
                if resp.status_code == 200:
                    obj = json.loads(resp.text)
                    results = obj["results"]
                    if len(results) < 1:
                        continue_to_process = False
                    else:
                        FS.write_json(results, outfile)
            except Exception as e:
                continue_to_process = False
                logging.critical(str(e))
                print(traceback.format_exc())

def merge_downloaded_cars_data():
    entries = FS.walk("tmp", include_dirs=['tmp/cars'], include_types=['json'])
    print("entries count: {}".format(len(entries)))
    all_cars, all_files = list(), list()

    # collect the entry full filenames so as to process them
    # in a sorted manner
    for entry in entries:
        all_files.append(entry["full"])

    for idx, infile in enumerate(sorted(all_files)):
        print("processing file: {} {}".format(idx + 1, infile))
        data = FS.read_json(infile)
        for car in data:
            car["_make_model_year"] = "{}|{}|{}".format(car["make"], car["model"], car["year"])
            car["_infile"] = infile
            print(car)
            all_cars.append(car)

    sorted_cars = sorted(all_cars, key=lambda x: x['_make_model_year'])
    for idx, car in enumerate(sorted_cars):
        car["_seq"] = idx + 1

    print("all_cars count: {}".format(len(sorted_cars)))
    FS.write_json(sorted_cars, "tmp/all_cars.json", sort_keys=False)

def openflights_wrangle():
    # The OpenFlights csv files do not contain headers, therefore
    # we inject the column names and datatypes to con.read_csv(...).
    # See https://openflights.org/data.php for csv file layouts.
    # The output json files are document-per-line format.

    con = duckdb.connect(database=":memory:")
    
    openflights_wrangle_airlines(con, False)
    openflights_wrangle_airports(con, False)
    openflights_wrangle_routes(con, False)
    openflights_wrangle_countries(con, False)
    openflights_wrangle_planes(con, False)
    
def openflights_wrangle_airlines(con, verbose=False):
    airlines = con.read_csv(
        "../data/openflights/raw/airlines.dat",
        auto_detect=True,
        columns={
            'AirlineID': 'VARCHAR',
            'Name': 'VARCHAR',
            'Alias': 'VARCHAR',
            'IATA': 'VARCHAR',
            'ICAO': 'VARCHAR',
            'Callsign': 'VARCHAR',
            'Country_Territory': 'VARCHAR',
            'Active': 'VARCHAR'
        })
    if verbose:
        print(str(type(airlines))) # <class 'duckdb.duckdb.DuckDBPyRelation'>
        rows = con.execute("describe airlines;").fetchall()
        for row in rows:
            print(row)
        rows = con.execute("select * from airlines limit 999999;").fetchall()
        for row in rows:
            print(row)  # rows are simple tuples; <class 'tuple'>
    
    con.execute("copy airlines to '../data/openflights/json/airlines.json'")

def openflights_wrangle_airports(con, verbose=False):
    airports = con.read_csv(
        "../data/openflights/raw/airports.dat",
        columns={
            'AirportID': 'VARCHAR',
            'Name': 'VARCHAR',
            'City': 'VARCHAR',
            'Country': 'VARCHAR',
            'IATA': 'VARCHAR',
            'ICAO': 'VARCHAR',
            'Latitude': 'VARCHAR',
            'Longitude': 'VARCHAR',
            'Altitude': 'VARCHAR',
            'Timezone': 'VARCHAR',
            'DST': 'VARCHAR',
            'Tz': 'VARCHAR',
            'AType': 'VARCHAR',
            'Source': 'VARCHAR'
        })
    if verbose:
        print(str(type(airports))) # <class 'duckdb.duckdb.DuckDBPyRelation'>
        rows = con.execute("describe airports;").fetchall()
        for row in rows:
            print(row)
        rows = con.execute("select * from airports limit 999999;").fetchall()
        for row in rows:
            print(row)  # rows are simple tuples; <class 'tuple'>
    
    con.execute("copy airports to '../data/openflights/json/airports.json'")      

def openflights_wrangle_routes(con, verbose=False):
    routes = con.read_csv(
        "../data/openflights/raw/routes.dat",
        columns={
            'Airline': 'VARCHAR',
            'AirlineID': 'VARCHAR',
            'SourceAirport': 'VARCHAR',
            'SourceAirportID': 'VARCHAR',
            'DestinationAirport': 'VARCHAR',
            'DestinationAirportID': 'VARCHAR',
            'Codeshare': 'VARCHAR',
            'Stops': 'VARCHAR',
            'Equipment': 'VARCHAR'
        })
    if verbose:
        print(str(type(routes))) # <class 'duckdb.duckdb.DuckDBPyRelation'>
        rows = con.execute("describe routes;").fetchall()
        for row in rows:
            print(row)
        rows = con.execute("select * from routes limit 999999;").fetchall()
        for row in rows:
            print(row)  # rows are simple tuples; <class 'tuple'>
    
    con.execute("copy routes to '../data/openflights/json/routes.json'")
       
def openflights_wrangle_countries(con, verbose):
    countries = con.read_csv(
        "../data/openflights/raw/countries.dat",
        columns={
            'Name': 'VARCHAR',
            'IsoCode': 'VARCHAR',
            'DafifCode': 'VARCHAR'
        })
    if verbose:
        print(str(type(countries))) # <class 'duckdb.duckdb.DuckDBPyRelation'>
        rows = con.execute("describe countries;").fetchall()
        for row in rows:
            print(row)
        rows = con.execute("select * from countries limit 999999;").fetchall()
        for row in rows:
            print(row)  # rows are simple tuples; <class 'tuple'>
    
    con.execute("copy countries to '../data/openflights/json/countries.json'")

def openflights_wrangle_planes(con, verbose):
    planes = con.read_csv(
        "../data/openflights/raw/planes.dat",
        columns={
            'Name': 'VARCHAR',
            'IataCode': 'VARCHAR',
            'IcaoCode': 'VARCHAR'
        })	
    if verbose:
        print(str(type(planes))) # <class 'duckdb.duckdb.DuckDBPyRelation'>
        rows = con.execute("describe planes;").fetchall()
        for row in rows:
            print(row)
        rows = con.execute("select * from planes limit 999999;").fetchall()
        for row in rows:
            print(row)  # rows are simple tuples; <class 'tuple'>
    
    con.execute("copy planes to '../data/openflights/json/planes.json'")

def sean_lahman_baseball_data_to_json():
    # data/baseball/files-list.txt
    # data/baseball/lahman_1871-2023_csv/Batting.csv

    con = duckdb.connect(database=":memory:")
    
    # Read the master list of ~27 files
    list_file = "../data/baseball/files-list.txt"
    list_lines = FS.read_lines(list_file)
    for line in list_lines:
        basename = line.strip()
        sean_lahman_baseball_file_to_json(con, basename)  # Batting.csv

def sean_lahman_baseball_file_to_json(con, basename):
    barename = basename.split(".")[0]
    data_dir = "../data/baseball/lahman_1871-2023_csv"
    data_file = "{}/{}".format(data_dir, basename)
    out_file = "../data/baseball/json/{}.json".format(barename)
    print("data_file: {}".format(data_file))
    print("  out_file: {}".format(out_file))

    relation = con.read_csv(data_file)
    con.execute("copy relation to '{}'".format(out_file))



if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print_options("Error: no CLI args provided")
        else:
            func = sys.argv[1].lower()
            if func == "env":
                check_env()
            elif func == "merge_car_makes":
                merge_car_makes()
            elif func == "download_cars_data":
                download_cars_data()
            elif func == "merge_downloaded_cars_data":
                merge_downloaded_cars_data()
            elif func == "openflights_wrangle":
                openflights_wrangle()
            elif func == "sean_lahman_baseball_data_to_json":
                sean_lahman_baseball_data_to_json()
            else:
                print_options("Error: invalid function: {}".format(func))
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())
