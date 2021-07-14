# JewelSim

**JewelSim** is a machine learning system predicting the similarity of jewelry
goods. It is being trained on the web-crawled data (retrieved from the websites
of russian jewelery retailers). The data itself includes: 

* *textual attributes* (title, jewel and gems description, etc.)
* *numerical attributes* (physical characteristics, like weight, width, etc.)
* *categorical attributes* (metal, category, collection, etc.)
* *visual data*, i.e. jewel images.

## Environment

### Setup

1. Install [Anaconda with Python 3](https://www.anaconda.com/download/) or
[Miniconda with Python 3](https://conda.io/miniconda.html)
and follow the [installation guide](https://docs.python.org/3/using/index.html).
1. Create `jewelsim` conda environment by invoking `conda env create -f enviromnent.yml`
1. Activate the environment with `conda activate jewelsim`

### Update
1. Activate the environment with `conda activate jewelsim`
1. Install a new package with `conda install ...`
1. Update the `environment.yml` file by invoking
`conda env export --no-builds | grep -v "^prefix: " > environment.yml`
1. Commit the updates and push them to the remote repository.

## Project structure

The structure of this project is inspired by
[Cookiecutter Data Science](
  https://drivendata.github.io/cookiecutter-data-science/
)
template.
