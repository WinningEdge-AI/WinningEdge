# Component

## Data Base

- Name: PokerGamesData

- What it does: It takes in the raw files that we have and stores all the valuable information in accessible and compact form. Later, we might add certain columns to it that help us build our model. Additionally, we might have to drop certain hands for being too long/complex.

- Inputs (with type info): Text files with hands played. (.txt)

- Outputs (with type info): Structured database in pandas.DataFrame format, containing user id, bet amount, actions, etc.

- How to use other components: Other components should be able to pull values from the database to enable training a ML algorithm, running statistical probabilities (evaluator), and eventually return recommended decisions based on current game input such as hand decisions and bet size according to bet action and pot size of the current and previous rounds of the game. 

