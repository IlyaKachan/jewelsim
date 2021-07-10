# JewelSim

**JewelSim** is a machine learning system predicting the similarity of jewelry
goods. It is being trained on the web-crawled data (retrieved from the websites
of russian jewelery retailers). The data itself includes: 

* *textual attributes* (title, jewel and gems description, etc.)
* *numerical attributes* (physical characteristics, like weight, width, etc.)
* *categorical attributes* (metal, category, collection, etc.)
* *visual data*, i.e. jewel images.

## Environment setup

1. Install **python 3.8.3** (or any newer one), choose an installer for your
system [here](https://www.python.org/downloads/release/python-373/)
and follow the [installation guide](https://docs.python.org/3/using/index.html)
1. Install **virtualenv** and its wrapper for managing python virtual
environments
``` bash
pip install virtualenv

# for Unix-like systems
pip install virtualenvwrapper

# for Windows
pip install virtualenvwrapper-win
```
1. Clone this repo, change directory to *jewelsim* in your terminal,
create and activate project virtual environment by invoking the commands:
``` bash
virtualenv --python=<PATH TO PYTHON 3.8.3 INSTALLATION> venv

# activate venv
./venv/Scripts/activate 
```
1. Install the required python packages into the virtual environment
``` bash
pip install -r requirements.txt
```

## Project structure

The structure of this project is inspired by
[Cookiecutter Data Science](
  https://drivendata.github.io/cookiecutter-data-science/
)
template.
