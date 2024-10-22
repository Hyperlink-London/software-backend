# Hyperlink-backend


This project, hyperlink-api, is a Python-based API designed to interface with hyperlink databases. It leverages the FastAPI and SQLModel libraries to provide a set of endpoints for managing and interacting with microcontroller data and experiments. The API supports CRUD operations, allowing users to create, read, update, and delete data related to both microcontrollers and experiments.

## Overview

hyperlink-api is a Python-based API designed to interface with hyperlink databases. It provides a set of endpoints to interact with microcontroller data and experiments.

## Installation

You can install `hyperlink-api` via git:

```bash
git clone https://github.com/Hyperlink-London/hyperlink-backend.git
cd hyperlink-api
```

then create a conda envrioemnt (you should install conda [here](https://anaconda.org/anaconda/conda))

```bash
conda create --name hyperlink-backend python=3.10
```

then activate the conda environment

```bash
conda activate hyperlink-backend
```

then pip install in the conda environment

```bash
pip install -r requirements.txt
pip install -e .
```

## To run

You can run the Hyperlink Data Dashboard by running:

```bash
hyperlink-backend
```
