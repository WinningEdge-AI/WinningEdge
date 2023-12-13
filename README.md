# WinningEdge

WinningEdge is a strategy optimization tool for online, low-stakes Texas hold'em players. The application will provide real time probabilities and suggest action based on an ML algorithm trained using historical data. In using WinningEdge, players will be able to make better informed decisions with the goal of winning and being profitable.
<br>

### Organization of the Project<br>
The project has the following structure:
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


### Installation<br>
To install `WinningEdge` first it must be cloned to your computer using
the `git` command:<br>

```
git clone git@github.com:WinningEdge-AI/WinningEdge.git
```

Next, the user will need to go into the WinningEdge directory and run the setup.py file.<br>
```
cd WinningEdge/
python setup.py install
```

To ensure that dependencies to run `WinningEdge` are install, the user will need to run the following commands.

```
conda env create -f environment.yml -n WinningEdge
conda activate WinningEdge
```
<br>

### Project History <br>
The Winning Edge Software was originally started by Peter Sushko who purchased the original dataset from 888poker.com. As part of CSE583: Software Development for Data Scientists class (Fall 2023) for the University of Washington, the software was developed by Peter Sushko, Dylan Heino, John Tatka,  Victor Tian, and Eric Gibson. 
<br>

### Software Dependencies <br>
The evaluator, card, and lookup modules are fork of the Deuces python poker hand evaluation library which can be found at the following github URL:

```
https://github.com/worldveil/deuces/tree/master
```
<br>

### Data Source
Data for all heads up, low-stakes poker games was purchased from `888poker.com`.
An example of data from one of the >500,000 games is below:
```
#Game No : 502745408
***** 888poker Hand History for Game 502745408 *****
$0.01/$0.02 Blinds No Limit Holdem - *** 06 06 2018 04:49:57
Table Bedford 6 Max (Real Money)
Seat 1 is the button
Total number of players : 2
Seat 1: ponte1001 ( $0.80 )
Seat 4: Bolorig888 ( $1.01 )
ponte1001 posts small blind [$0.01]
Bolorig888 posts big blind [$0.02]
** Dealing down cards **
ponte1001 calls [$0.01]
Bolorig888 checks
** Dealing flop ** [ 2c, Qh, Jd ]
Bolorig888 checks
ponte1001 checks
** Dealing turn ** [ 9h ]
Bolorig888 bets [$0.04]
ponte1001 calls [$0.04]
** Dealing river ** [ Js ]
Bolorig888 bets [$0.06]
ponte1001 calls [$0.06]
** Summary **
Bolorig888 shows [ 9c, Qs ]
ponte1001 mucks [ 9s, 6h ]
Bolorig888 collected [ $0.23 ]
```


