# Big Data Project

This repository contains the source code of the big data project for the Big Data Framework class at the ECE

## 1 - Install the environment

For this project, you need ti have a python version >= 3.11 and < 3.12 (as indiacted in the pyproject.toml file)
If you don't have a valid version, you can install it with the pyenv package.  
You can check your python version with the following command:
```bash
$/ python --version
```
When you have configured your python, please run the following commands for installing the project's environment:

```bash
$/ pip install poetry
$/ poetry config virtualenvs.in-project true
$/ poetry install
```
Now you can run the following to activate the environment:
```bash
poetry shell
```
It is equivalent to run `source .ven/bin/activate` in MacOs or `.venv\Scripts\activate` on Windows

### Note
If you are on a windows os, please install spark in C:\Spark folder at the root of your system C folder

## 2 - Launch the streamlit app

To launch the app, please run the following command at the root of the project
```bash
$/ streamlit run app.py
```

## 3 - Project structure

The project architecture is the following

```bash
.
├── README.md
├── app.py
├── constants.py
├── create_final_data.py
├── data
│   ├── final
│   └── intermediate
├── notebooks
├── poetry.lock
├── preprocess_data.py
└── pyproject.toml
```

There are 3 python scripts that you can execute
- preprocess_data.py
- create_final_data.py
- app.py

### Preprocess data

The *preprocess_data.py* script loads the data from yahoo finance (via the yfinance package),
preprocess this raw data (rename columns and replace "NaN" string with None) and save it in the **data/intermediate** folder.

### Create final data

The *create_final_data.py* script loads the intermediate data (saved with *preprocess_data.py*) and transforms this data
into usable information for the streamlit app.  
Here are some examples of transformations:
- compute return rate
- compute moving average

### Notebooks

The **notebooks** folder contains notebooks used to explore the data and create insights about it.
The streamlit application is made up of the most interesting insights present in the notebooks
