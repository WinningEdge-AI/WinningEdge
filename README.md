# WinningEdge
WinningEdge Poker Hand Optimization Software <br>
<br>

### Software dependencies


### Summary of Folder Contents


### Directory structure
The package is organized as follows:

<br>
Class project for CSE583: Software Development for Data Scientists <br>(University of Washington Fall 2023)<br>
<br>
<br>
<br>
WinningEdge is a strategy optimization tool for online, low-stakes Texas hold'em players. The application will provide real time probabilities and suggest action based on an ML algorithm trained using historical data. In using WinningEdge, players will be able to make better informed decisions with the goal of winning and being profitable.
<br>
Organization of the Project
---------------------------
The project has the following structure

'''WinningEdge/
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
    |-- add_aggression_column.py
    |-- add_fold_column.py
    |-- adding_flush.py
    |-- adding_rank.py
    |-- bluff_eval.py
    |-- card.py
    |-- evaluator.py
    |-- lookup.py
    |-- straight_risk_eval.py
    |-- tests.py'''


Installation
------------
To install `WinningEdge` first it must be cloned to your computer using
the `git` command:
```git clone git@github.com:WinningEdge-AI/WinningEdge.git```
Next, the user will need to go into the WinningEdge directory and run the setup.py file.

```
cd WinningEdge/
python setup.py install
```


