import pytest

import datetime
import json
import time

from src.io.fs import FS

# pytest -v tests/test_fs.py

def test_as_unix_filename():
    assert FS.as_unix_filename(None) == None 
    assert FS.as_unix_filename('  ') == ''
    assert FS.as_unix_filename("C:\\Users\\cjoakim\\some_file.txt") == '/Users/cjoakim/some_file.txt'
    assert FS.as_unix_filename("  cjoakim\\some_file.txt  ") == 'cjoakim/some_file.txt'
    assert FS.as_unix_filename('/Users/cjoakim/some_file.txt') == '/Users/cjoakim/some_file.txt'

def test_list_directories_in_dir():
    dirs = FS.list_directories_in_dir('.')
    assert str(type(dirs)) == "<class 'list'>" 
    print(dirs)
    assert 'src' in dirs
    assert 'tests' in dirs
    assert 'templates' in dirs
    assert len(dirs) > 6
    assert len(dirs) < 12

    assert FS.list_directories_in_dir('/not_there') == None

def test_list_files_in_dir():
    files = FS.list_files_in_dir('horse')
    assert files == None

    files = FS.list_files_in_dir('src/io')
    assert str(type(files)) == "<class 'list'>" 
    print(files)
    assert 'fs.py' in files
    # assert 'env.py' in files
    # assert 'system.py' in files
    assert len(files) > 0
    assert len(files) < 3

    files = FS.list_files_in_dir('data/timezones')
    assert str(type(files)) == "<class 'list'>" 
    print(files)
    assert 'timezones.csv' in files
    assert len(files) > 0
    assert len(files) < 2

def test_read():
    s = FS.read("data/u2.txt")
    assert len(s) == 43
    assert s == "bono\nthe edge\nadam clayton\nlarry mullen jr\n"

    s = FS.read("data/nc_zipcodes.json")
    assert len(s) == 304618

    s = FS.read("TYPO/nc_zipcodes.json")
    assert s == None 

    s = FS.read("data/img/cosmos-db.png")  # fails due to not a text file
    assert s == None 

def test_read_lines():
    lines = FS.read_lines("data/postal_codes_nc.csv")
    assert len(lines) == 1081
    assert (
        lines[0] == "id,postal_cd,country_cd,city_name,state_abbrv,latitude,longitude\n"
    )
    assert lines[-1] == "12028,28909,US,Warne,NC,35.0118070000,-83.9188180000\n"

    lines = FS.read_lines("TYPO/postal_codes_nc.csv")
    assert lines == None 

def test_read_json():
    obj = FS.read_json("data/nc_zipcodes.json")
    # print(obj)
    assert str(type(obj)) == "<class 'list'>"
    assert len(obj) == 1075

    obj = FS.read_json("TYPO/nc_zipcodes.json")
    assert obj == None 

    obj = FS.read_json("requirements.txt")
    assert obj == None 

def test_read_csv_as_rows_with_header():
    rows = FS.read_csv_as_rows("data/postal_codes_nc.csv")
    assert len(rows) == 1081
    print(rows[0])
    print(rows[-1])
    assert rows[0] == [
        "id",
        "postal_cd",
        "country_cd",
        "city_name",
        "state_abbrv",
        "latitude",
        "longitude",
    ]
    assert rows[-1] == [
        "12028",
        "28909",
        "US",
        "Warne",
        "NC",
        "35.0118070000",
        "-83.9188180000",
    ]

    rows = FS.read_csv_as_rows("TYPO/postal_codes_nc.csv")
    assert rows == None 

    rows = FS.read_csv_as_rows("data/img/cosmos-db.png")
    assert rows == None 

def test_read_csv_as_rows_skip_header():
    rows = FS.read_csv_as_rows("data/postal_codes_nc.csv", skip=1)
    assert len(rows) == 1080
    print(rows[0])
    print(rows[-1])
    assert rows[0] == [
        "10949",
        "27006",
        "US",
        "Advance",
        "NC",
        "35.9445620000",
        "-80.4376310000",
    ]
    assert rows[-1] == [
        "12028",
        "28909",
        "US",
        "Warne",
        "NC",
        "35.0118070000",
        "-83.9188180000",
    ]

def test_read_csv_as_dicts():
    rows = FS.read_csv_as_dicts("data/postal_codes_nc.csv")
    assert len(rows) == 1080
    assert rows[0]["postal_cd"] == "27006"
    assert rows[-1]["postal_cd"] == "28909"

    rows = FS.read_csv_as_dicts("TYPO/postal_codes_nc.csv")
    assert rows == None

    rows = FS.read_csv_as_dicts("data/img/cosmos-db.png")
    assert rows == None 

def test_text_file_iterator():
    it = FS.text_file_iterator("data/postal_codes_nc.csv")
    first_line, curr_line, count = None, None, 0
    for i, line in enumerate(it):
        count = count + 1
        if i == 0:
            first_line = line
        curr_line = line
    assert (
        first_line == "id,postal_cd,country_cd,city_name,state_abbrv,latitude,longitude"
    )
    assert curr_line == "12028,28909,US,Warne,NC,35.0118070000,-83.9188180000"
    assert count == 1081

def test_walk():
    entries = FS.walk("not_there", include_dirs=[], include_types=[])
    assert entries == None

    entries = FS.walk("data", include_dirs=['data/img'], include_types=['horse'])
    assert len(entries) == 0

    entries = FS.walk(".", include_dirs=[], include_types=['json'])
    assert len(entries) > 99

    entries = FS.walk("src", include_dirs=[], include_types=['py'])
    print(json.dumps(entries, sort_keys=True, indent=2))
    result = FS.write_json(entries, "tmp/test_walk.json")
    assert len(entries) > 10
    assert len(entries) < 20
    fs_found = False
    for e in entries:
        if e["base"] == "fs.py":
            fs_found = True
    assert fs_found == True

    entries = FS.walk("src", include_dirs=[], include_types=['py'])
    print(json.dumps(entries, sort_keys=True, indent=2))
    assert len(entries) == 15
    bytes_found = False
    for e in entries:
        if e["base"] == "bytes.py":
            bytes_found = True
    assert bytes_found == True

def test_write():
    testfile = "tmp/test_write.txt"
    s1 = "line 1\nline2\ncreated at {}".format(datetime.datetime.now())
    result = FS.write(s1, testfile)
    assert result == True
    s2 = FS.read(testfile)
    assert s1 == s2

    testfile = "TYPO/test_write.txt"
    s1 = "line 1\nline2\ncreated at {}".format(datetime.datetime.now())
    result = FS.write(s1, testfile)
    assert result == False

def test_write_json():
    filename = 'tmp/test_write_json.json'
    now = time.time()
    things = list()
    data = dict()
    data['epoch'] = now
    things.append(data)
    FS.write_json(things, filename, pretty=False)
    result = FS.write_json(things, filename)
    assert result == True

    objects = FS.read_json(filename)
    assert str(type(objects)) == "<class 'list'>"
    assert len(objects) == 1
    assert objects[0]['epoch'] == now

    result = FS.write_json(things, 'TYPO/test_write_json.json')
    assert result == False

def test_write_lines():
    filename = 'tmp/test_write_lines.txt'
    now = time.time()
    lines = list()
    lines.append('apples')
    lines.append(str(now))
    lines.append('pears')
    result = FS.write_lines(lines, filename)
    assert result == True

    lines = FS.read_lines(filename)
    assert lines[0].strip() == 'apples'
    assert float(lines[1]) == now
    assert lines[2].strip() == 'pears'

    result = FS.write_lines(lines, 'TYPO/test_write_lines.txt')
    assert result == False
