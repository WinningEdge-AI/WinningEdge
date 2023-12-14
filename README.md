# WinningEdge
WinningEdge Poker Hand Optimization Software <br>
<br>

### Software dependencies


### Directory structure
The repository is organized into several directories, each tailored for specific aspects of the project. Below is the structure and description of each directory:

- `dataframe`: This directory contains all the modules and Jupyter notebooks associated with the manipulation and formatting of dataframes. It includes a Jupyter notebook for converting data to dataframes (`convert_data_to_dataframe.ipynb`) and a Python module for creating dataframes (`create_dataframe.py`). It also contains the actual dataframes in `.pkl` files, such as `poker_dataframe_bugfixed.pkl` and `poker_dataframe_with_age_columns.pkl`.

- `doc`: This directory houses documentation related to the project, including component and functional specifications in PDF format and slides for technology review.

- `ml`: The machine learning directory includes text files, dataframes, and Jupyter notebooks that are specific to the machine learning aspect of the project.

- `notebooks`: This directory is for Jupyter notebooks that are considered module prototypes or for testing purposes.

- `winedge`: Contains Python scripts for data and dataframe analysis modules.

<br>
Class project for CSE583: Software Development for Data Scientists <br>(University of Washington Fall 2023)<br>
<br>
<br>
<br>
WinningEdge is a strategy optimization tool for online, low-stakes Texas hold'em players. The application will provide real time probabilities and suggest action based on an ML algorithm trained using historical data. In using WinningEdge, players will be able to make better informed decisions with the goal of winning and being profitable.
<br>
<br>
### Organization of the Project<br>
The project has the following structure<br>
<br>

```
WinningEdge/
|-- LICENSE
|-- README.md
|-- dataframe
|   |-- convert_data_to_dataframe.ipynb
|   |-- create_dataframe.py
|   |-- poker_dataframe_bugfixed.pkl
|   |-- poker_dataframe_with_agg_columns.pkl
|-- doc
|   |-- Component Specification.pdf
|   |-- Functional Specifications.pdf
|   |-- Technology Review Slides.pdf
|   |-- use-case.md
|-- environment.yml
|-- examples
|   |-- README.md
|   |-- eval_comp_demo.ipynb
|-- ml
|   |-- README.txt
|   |-- df_filtered_w_flush.pkl
|   |-- df_filtered_w_flush_strength.pkl
|   |-- make_ml_df.ipynb
|   |-- make_regression_model.ipynb
|   |-- needs_labels.pkl
|   |-- ready_to_model.pkl
|-- notebooks
|   |-- AddingFlush.ipynb
|   |-- AddingRank.ipynb
|   |-- WIP.ipynb
|   |-- bluff_metric_prototype.ipynb
|   |-- straight_risk_prototype.ipynb
|   |-- testing_create_dataframe.ipynb
|-- setup.py
|-- winedge
    |-- Folded.ipynb
    |-- __init__.py
    |-- __pycache__
    |   |--...
    |-- add_aggression_column.py
    |-- add_fold_column.py
    |-- adding_flush.py
    |-- adding_rank.py
    |-- bluff_eval.py
    |-- card.py
    |-- evaluator.py
    |-- lookup.py
    |-- straight_risk_eval.py<
    |-- tests.py
```

<br>
### Installation<br>
To install `WinningEdge` first it must be cloned to your computer using<br>
the `git` command:<br>
```git clone git@github.com:WinningEdge-AI/WinningEdge.git```<br>
Next, the user will need to go into the WinningEdge directory and run the setup.py file.<br>
```
cd WinningEdge/
python setup.py install
``` <br>
To ensure that dependencies to run `WinningEdge` are install, the user will need to run the following commands.<br>
```
conda env create -f environment.yml -n WinningEdge
conda activate WinningEdge
```

<br>
### Examples <br>
<br>
### Examples <br>
<br>
### Software Dependencies <br>



