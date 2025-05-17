import csv
import json
import logging
import os
import traceback

from typing import Iterator

# This class is used to interact with the local filesystem,
# such as reading and writing text, csv, and json files.
# Chris Joakim, 2025

class FS:

    @classmethod
    def as_unix_filename(cls, filename: str) -> str:
        """ Return the given filename with unix slashes, and without Windows C: """
        try:
            if filename.upper().startswith("C:"):
                return filename[2:].replace("\\", "/")
            else:
                return filename.replace("\\", "/").strip()
        except Exception as e:
            print(traceback.format_exc())
            return filename

    @classmethod
    def list_files_in_dir(cls, basedir: str) -> list[str] | None:
        """ Return a list of files in the given directory, or None """
        if os.path.isdir(basedir):
            files = []
            for file in os.listdir(basedir):
                dir_or_file = os.path.join(basedir, file)
                if os.path.isdir(dir_or_file):
                    pass
                else:
                    files.append(file)
            return files
        return None

    @classmethod
    def list_directories_in_dir(cls, basedir: str) -> list[str] | None:
        """ Return a list of directories in the given directory, or None """
        if os.path.isdir(basedir):
            files = []
            for file in os.listdir(basedir):
                dir_or_file = os.path.join(basedir, file)
                if os.path.isdir(dir_or_file):
                    files.append(file)
            return files
        return None

    @classmethod
    def walk(cls, directory: str, include_dirs=[], include_types=[]) -> list[dict] | None:
        """
        Recursively walk the given directory and return a list of dicts;
        one for each file that matches the given include_dirs and include_types.
        If include_dirs and include_types are empty lists, then all dirs/files
        will be returned.  include_types is a list of filetypes like ['py', 'ps1']
        """
        if os.path.isdir(directory):
            files, seq = [], 0
            for dir_name, _, base_names in os.walk(directory):
                include_this_dir = False
                if len(include_dirs) > 0:
                    if dir_name in include_dirs:
                        include_this_dir = True
                else:
                    include_this_dir = True

                if include_this_dir == True:
                    for base_name in base_names:
                        suffix = base_name.split('.')[-1]
                        include_this_file = False
                        if len(include_types) > 0:
                            if suffix in include_types:
                                include_this_file = True
                        if include_this_file == True:
                            seq = seq + 1
                            full_name = f"{dir_name}/{base_name}"
                            entry = {}
                            entry["seq"] = seq
                            entry["base"] = base_name
                            entry["suffix"] = suffix
                            entry["dir"] = dir_name
                            entry["full"] = full_name
                            entry["abspath"] = os.path.abspath(full_name)
                            files.append(entry)
            return files
        return None

    @classmethod
    def read(cls, infile: str, encoding="utf-8", mode="rt") -> str | None:
        """
        Read the given file, return the contents as a str or None.
        The encoding param defaults to 'utf-8'. but 'cp1252' is common on Windows.
        The mode defaults to 'rt'. 'r' and 'rb' (binary) are possible values.  
        """
        try:
            if os.path.isfile(infile):
                with open(file=infile, encoding=encoding, mode=mode) as file:
                    return file.read()
        except Exception as e:
            print(traceback.format_exc())
        return None

    @classmethod
    def read_lines(cls, infile: str, encoding="utf-8", mode="rt") -> list[str] | None:
        """ Read the given file, return an array of lines(strings) or None """
        if os.path.isfile(infile):
            lines = []
            with open(file=infile, encoding=encoding, mode=mode) as file:
                for line in file:
                    lines.append(line)
            return lines
        return None

    @classmethod
    def read_json(cls, infile: str, encoding="utf-8", mode="rt") -> dict | list | None:
        """ Read the given JSON file, return either a list, a dict, or None """
        try:
            if os.path.isfile(infile):
                with open(file=infile, encoding=encoding, mode=mode) as file:
                    return json.loads(file.read())
        except Exception as e:
            print(traceback.format_exc())
        return None

    @classmethod
    def read_csv_as_dicts(
        cls, infile: str, delim=",", dialect="excel",
        encoding="utf-8", mode="rt") -> list[str] | None:
        """
        Read the given csv filename, return an array of dicts or None.
        Implementation uses csv.DictReader.
        """
        try:
            if os.path.isfile(infile):
                rows = []
                with open(file=infile, encoding=encoding, mode=mode) as csvfile:
                    rdr = csv.DictReader(csvfile, dialect=dialect, delimiter=delim)
                    for row in rdr:
                        rows.append(row)
                return rows
        except Exception as e:
            print(traceback.format_exc())
        return None

    @classmethod
    def read_csv_as_rows(cls, infile: str, delim=",", skip=0, encoding="utf-8", mode="rt") -> list[str] | None:
        """
        Read the given csv filename, return an array of csv rows or None.
        Implementation uses csv.reader.
        """
        try:
            if os.path.isfile(infile):
                rows = []
                with open(file=infile, encoding=encoding, mode=mode) as csvfile:
                    rdr = csv.reader(csvfile, delimiter=delim)
                    for idx, row in enumerate(rdr):
                        if idx >= skip:
                            rows.append(row)
                return rows
        except Exception as e:
            print(traceback.format_exc())
        return None


    @classmethod
    def text_file_iterator(cls, infile: str, encoding="utf-8", mode="rt") -> Iterator[str] | None:
        """ Return a line generator that can be iterated with iterate() """
        if os.path.isfile(infile):
            with open(file=infile, encoding=encoding, mode=mode) as file:
                for line in file:
                    yield line.strip()

    # write methods follow the convention: write_xxx(thing_to_be_written, outfile)

    @classmethod
    def write(cls, string_value: str, outfile: str, verbose=True) -> bool:
        """ Write the given str to the given file """
        try:
            if outfile is not None:
                if string_value is not None:
                    with open(file=outfile, encoding="utf-8", mode="w") as file:
                        file.write(string_value)
                        if verbose is True:
                            logging.warning(f"file written: {outfile}")
                    return True
        except Exception as e:
            print(traceback.format_exc())
        return False
    
    @classmethod
    def write_json(cls, obj: object, outfile: str, pretty=True, sort_keys=True, verbose=True) -> None:
        """ Write the given object to the given file as JSON """
        try:
            if obj is not None:
                jstr = None
                if pretty is True:
                    jstr = json.dumps(obj, sort_keys=sort_keys, indent=2)
                else:
                    jstr = json.dumps(obj)

                with open(file=outfile, encoding="utf-8", mode="w") as file:
                    file.write(jstr)
                    if verbose is True:
                        logging.warning(f"file written: {outfile}")
                return True
        except Exception as e:
            print(traceback.format_exc())
        return False
    
    @classmethod
    def write_lines(cls, lines: list[str], outfile: str, verbose=True) -> bool:
        """ Write the given str lines to the given file """
        try:
            if lines is not None:
                with open(file=outfile, encoding="utf-8", mode="w") as file:
                    for line in lines:
                        file.write(line + "\n")  # os.linesep)  # \n works on Windows
                    if verbose is True:
                        logging.warning(f"file written: {outfile}")
                return True
        except Exception as e:
            print(traceback.format_exc())
        return False

