"""
Usage:
  python main_hf.py <func>
  python main_hf.py list_available_datasets > tmp/huggingface_datasets.txt
  python main_hf.py download_python_libs_dataset
  python main_hf.py download_adhoc
  python main_hf.py cleanup_cache
Options: 
  -h --help     Show this screen.
  --version     Show version.
"""

import asyncio
import os
import sys
import traceback

from docopt import docopt

from datasets import load_dataset

from src.io.fs import FS


def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version="1.0.0")
    print(arguments)


def list_available_datasets():
    print("list_available_datasets ...")
    from huggingface_hub import list_datasets
    for idx, dataset in enumerate(list_datasets()):
        print(f"{idx} {dataset.id}")

def cleanup_cache():
    print("simply execute 'rm -rf ~/.cache/huggingface/' from your shell")
    print("see cleanup_hf_cache.sh in this directory")

def download_python_libs_dataset():
    print("download_python_libs_dataset ...")
    dataset_name =  "KingfernJohn/kfj-pypi-packages-metadata"
    # use the main-data.zip beneath the ~/.cache/huggingface/ directory
    dashed_dataset_name = dataset_name.replace("/", "-")
    outfile = f"tmp/{dashed_dataset_name}.json"
    print(f"outfile: {outfile}")
    print(f"loading: {dataset_name}")
    dataset = load_dataset(dataset_name)

    #dataset = load_dataset("imdb", data_dir="/path/to/your/local/directory")
    # print(str(type(dataset)))  # <class 'datasets.dataset_dict.DatasetDict'>  (Not JSON serializable)
    # outfile = f"tmp/{dataset_name}.json".replace("/", "-")
    # dataset.to_csv(outfile, indent=2)

def download_adhoc():
    print("download_adhoc ...")
    dataset_name =  "omgbobbyg/Zip-Code-to-Timezone"
    dashed_dataset_name = dataset_name.replace("/", "-")
    outfile = f"tmp/{dashed_dataset_name}.json"
    print(f"outfile: {outfile}")
    print(f"loading: {dataset_name}")
    
    dataset = load_dataset(dataset_name)
    print(str(type(dataset)))  # <class 'datasets.dataset_dict.DatasetDict'>  (Not JSON serializable)
    outfile = f"tmp/{dataset_name}.json".replace("/", "-")
    print(dataset)
    # <class 'datasets.dataset_dict.DatasetDict'>
    # DatasetDict({
    #     train: Dataset({
    #         features: ['zipCode', 'gmtOffset', 'gmtOffsetDST', 'dstObserved'],
    #         num_rows: 70102
    #     })
    # })

    train = dataset["train"]
    print(str(type(train)))
    print(train)

    for d in train:
        print(d) # {'zipCode': '85143', 'gmtOffset': -7, 'gmtOffsetDST': -7, 'dstObserved': 0}
        print(d["zipCode"]) # 85143


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_options("Error: no CLI function")
    else:
        try:
            func = sys.argv[1].lower()
            if func == "list_available_datasets":
                list_available_datasets()
            elif func == "download_python_libs_dataset":
                download_python_libs_dataset()
            elif func == "download_adhoc":
                download_adhoc()
            elif func == "cleanup_cache":
                cleanup_cache()
            else:
                print_options("Error: invalid function: {}".format(func))
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())

"""
$ cat data/flask.json | jq
{
  "name": "Flask",
  "version": "2.2.3",
  "description": "Flask\n=====\n\nFlask is a lightweight `WSGI`_ web application framework. It is designed\nto make getting started quick and easy, with the ability to scale up to\ncomplex applications. It began as a simple wrapper around `Werkzeug`_\nand `Jinja`_ and has become one of the most popular Python web\napplication frameworks.\n\nFlask offers suggestions, but doesn't enforce any dependencies or\nproject layout. It is up to the developer to choose the tools and\nlibraries they want to use. There are many extensions provided by the\ncommunity that make adding new functionality easy.\n\n.. _WSGI: https://wsgi.readthedocs.io/\n.. _Werkzeug: https://werkzeug.palletsprojects.com/\n.. _Jinja: https://jinja.palletsprojects.com/\n\n\nInstalling\n----------\n\nInstall and update using `pip`_:\n\n.. code-block:: text\n\n    $ pip install -U Flask\n\n.. _pip: https://pip.pypa.io/en/stable/getting-started/\n\n\nA Simple Example\n----------------\n\n.. code-block:: python\n\n    # save this as app.py\n    from flask import Flask\n\n    app = Flask(__name__)\n\n    @app.route(\"/\")\n    def hello():\n        return \"Hello, World!\"\n\n.. code-block:: text\n\n    $ flask run\n      * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n\n\nContributing\n------------\n\nFor guidance on setting up a development environment and how to make a\ncontribution to Flask, see the `contributing guidelines`_.\n\n.. _contributing guidelines: https://github.com/pallets/flask/blob/main/CONTRIBUTING.rst\n\n\nDonate\n------\n\nThe Pallets organization develops and supports Flask and the libraries\nit uses. In order to grow the community of contributors and users, and\nallow the maintainers to devote more time to the projects, `please\ndonate today`_.\n\n.. _please donate today: https://palletsprojects.com/donate\n\n\nLinks\n-----\n\n-   Documentation: https://flask.palletsprojects.com/\n-   Changes: https://flask.palletsprojects.com/changes/\n-   PyPI Releases: https://pypi.org/project/Flask/\n-   Source Code: https://github.com/pallets/flask/\n-   Issue Tracker: https://github.com/pallets/flask/issues/\n-   Website: https://palletsprojects.com/p/flask/\n-   Twitter: https://twitter.com/PalletsTeam\n-   Chat: https://discord.gg/pallets\n",
  "author": "Armin Ronacher",
  "author_email": "armin.ronacher@active-4.com",
  "maintainer": "Pallets",
  "maintainer_email": "contact@palletsprojects.com",
  "license": "BSD-3-Clause",
  "keywords": "",
  "classifiers": "Development Status :: 5 - Production/Stable, Environment :: Web Environment, Framework :: Flask, Intended Audience :: Developers, License :: OSI Approved :: BSD License, Operating System :: OS Independent, Programming Language :: Python, Topic :: Internet :: WWW/HTTP :: Dynamic Content, Topic :: Internet :: WWW/HTTP :: WSGI, Topic :: Internet :: WWW/HTTP :: WSGI :: Application, Topic :: Software Development :: Libraries :: Application Frameworks",
  "download_url": "",
  "platform": null,
  "homepage": "https://palletsprojects.com/p/flask",
  "project_urls": "Changes: https://flask.palletsprojects.com/changes/, Chat: https://discord.gg/pallets, Documentation: https://flask.palletsprojects.com/, Donate: https://palletsprojects.com/donate, Homepage: https://palletsprojects.com/p/flask, Issue Tracker: https://github.com/pallets/flask/issues/, Source Code: https://github.com/pallets/flask/, Twitter: https://twitter.com/PalletsTeam",
  "requires_python": ">=3.7",
  "requires_dist": "Werkzeug (>=2.2.2), Jinja2 (>=3.0), itsdangerous (>=2.0), click (>=8.0), importlib-metadata (>=3.6.0) ; python_version < \"3.10\", asgiref (>=3.2) ; extra == 'async', python-dotenv ; extra == 'dotenv'",
  "provides_dist": "",
  "obsoletes_dist": "",
  "summary": "A simple framework for building complex web applications."
}
"""