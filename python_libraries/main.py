"""
Usage:
  python main.py <func>
  python main.py seed_from_15k_csv 16000
  python main.py gen_pip_compiles_script
  python main.py parse_pip_compiles
  python main.py merge_parsed_libs
  python main.py get_pypi_html_pages
  python main.py parse_pypi_html_pages
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# TODO - the data directory has been move to data/python_libs/pip/
# in this repo.  Therefore need to refactor this code accordingly.

import base64
import json
import logging
import sys
import time
import os
import traceback

import duckdb 
import httpx

from pprint import pprint

from docopt import docopt
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader

from src.util.bytes import Bytes
from src.util.counter import Counter
from src.os.env import Env
from src.io.fs import FS
from src.os.system import System
from src.util.requirements import Libraries, RequirementsTxtParser


def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version="1.0.0")
    print(arguments)

def seed_from_15k_csv(first_n):
    libs = FS.read_csv_as_dicts("data/csv/top-pypi-packages.csv")
    for idx, lib in enumerate(libs):
        if idx < 1:
            # Add a custom set of libs that may not be in the top-pypi-packages.csv dataset
            for libname in "ageqrp,ggps,m26,gdg".split(","):
                content = "{}".format(libname).strip()
                outfile = "data/pip/{}.in".format(libname)
                FS.write(content, outfile)

        if idx < first_n:
            libname = lib['project']
            content = "{}".format(libname).strip()
            outfile = "data/pip/{}.in".format(libname)
            FS.write(content, outfile)

def gen_pip_compiles_script():
    script_lines = list()
    script_lines.append("#!/bin/bash")
    script_lines.append("")
    script_lines.append("source venv/bin/activate")
    script_lines.append("")
    pip_filenames_dict = dict()
    infiles = list()
    files = FS.list_files_in_dir("data/pip")

    # first get a list of all the *.in, *.txt, and *.json files in the pip 
    # directory to determine which libs need to be pi-compiled.
    for f in files:
        stripped = f.strip()
        if is_pip_processing_file(stripped):
            pip_filenames_dict[stripped] = False
    print("{} files in pip_filenames_dict".format(len(pip_filenames_dict)))

    for f in files:
        if f.endswith(".in"):
            libname = f.split(".")[0]
            txtfile = "{}.txt".format(libname)
            if txtfile in pip_filenames_dict.keys():
                print("already pip-compiled: {}".format(txtfile))
            else:
                infiles.append(f.strip())

    for fidx, f in enumerate(sorted(infiles)):
            script_lines.append("")
            script_lines.append("echo '========== {} {} =========='".format(fidx + 1, f))
            script_lines.append("sleep 1")
            script_lines.append("pip-compile {}".format(f))

    script_lines.append("")
    FS.write_lines(script_lines, "data/pip/pip_compiles2.sh")

def parse_pip_compiles():
    pip_filenames_dict = dict()
    files = FS.list_files_in_dir("data/pip")

    # first get a list of all the *.in, *.txt, and *.json files in the pip 
    # directory to determine which files need to be parsed.
    for f in files:
        stripped = f.strip()
        if is_pip_processing_file(stripped):
            pip_filenames_dict[stripped] = False
    print("{} files in pip_filenames_dict".format(len(pip_filenames_dict)))

    # second loop, the parsing loop, parse a file if not yet parsed
    for f in sorted(files):
        filename = f.strip()
        if filename.endswith(".txt"):  # the output of a pip-compile
            libname = filename.split(".")[0]
            jsonfile = "{}.json".format(libname)
            if jsonfile in pip_filenames_dict.keys():
                print("already parsed: {}".format(filename))
            else:
                outfile = "data/pip/{}".format(jsonfile)
                print("===")
                print("parsing: {}".format(filename))
                rtp = RequirementsTxtParser()
                results = rtp.parse(filename)
                #print(json.dumps(results, sort_keys=False, indent=2))
                FS.write_json(results, outfile, sort_keys=False)

def is_pip_processing_file(filename):
    if filename.endswith(".in"):
        return True
    if filename.endswith(".txt"):
        return True
    if filename.endswith(".json"):
        return True
    return False 

def merge_parsed_libs():
    json_filenames = list()
    merged_dict = dict()
    files = FS.list_files_in_dir("data/pip")

    # first get a list of all the *.in, *.txt, and *.json files in the pip 
    # directory to determine which files need to be parsed.
    for f in files:
        stripped = f.strip()
        if stripped.endswith(".json"):
            json_filenames.append(stripped)

    # second loop, the parsing loop, parse a file if not yet parsed
    for f in sorted(json_filenames):
        infile = "data/pip/{}".format(f.strip())
        print("reading {}".format(infile))
        obj = FS.read_json(infile)
        print(obj)
        libname = obj["libname"]
        merged_dict[libname] = obj 

    outfile = "data/pip_merged/merged_libs.json"
    FS.write_json(merged_dict, outfile, sort_keys=True)
    print("{} merged libs".format(len(merged_dict.keys())))

# def get_pypi_html_pages():
#     url = "https://pypi.org/project/ageqrp/"
#     loader = WebBaseLoader(url)
#     text = loader.load()
#     print(text)
#     # This method doesn't work because the WebBaseLoader is not designed to handle JavaScript.
#     # WebBaseLoader Client Challenge - JavaScript is disabled in your browser

def get_pypi_html_pages():
    files = pip_files_list([".in"])
    for idx, filename in enumerate(files):
        time.sleep(1)
        libname = filename.split(".")[0]
        capture_pypi_html(idx, libname)

def capture_pypi_html(idx, libname):
    # this approach also doesn't work because the client is expected to implement JS
    # alternative is to selenium webdriver
    try:
        url = "https://pypi.org/project/{}/".format(libname.strip())
        print("idx: {} url: {}".format(idx, url))
        response = httpx.get(url)
        text = response.text
        outfile = "data/pypi_html/{}.html".format(libname.strip())
        FS.write(text, outfile)
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())

def parse_pypi_html_pages():
    # use beautifulsoup4
    pass 


def pip_files_list(suffixes: list):
    files = FS.list_files_in_dir("data/pip")
    filtered_list = list()

    for f in files:
        stripped = f.strip()
        for suffix in suffixes:
            if stripped.endswith(suffix):
                filtered_list.append(stripped)
    return sorted(filtered_list)


if __name__ == "__main__":
    try:
        func = sys.argv[1].lower()
        if func == "seed_from_15k_csv":
            first_n = int(sys.argv[2])
            seed_from_15k_csv(first_n)
        elif func == "gen_pip_compiles_script":
            gen_pip_compiles_script()
        elif func == "parse_pip_compiles":
            parse_pip_compiles()
        elif func == "merge_parsed_libs":
            merge_parsed_libs()
        elif func == "get_pypi_html_pages":
            get_pypi_html_pages()
        elif func == "parse_pypi_html_pages":
            parse_pypi_html_pages()
        else:
            print_options("Error: invalid function: {}".format(func))
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())
