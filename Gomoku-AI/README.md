# Gomoku AI Project

## Game Rules
Gomoku, also known as Five in a Row, is a strategy board game played on a 15x15 grid. The goal is to be the first player to form an unbroken chain of five stones horizontally, vertically, or diagonally. Players alternate turns, placing one stone per turn.

## Menu Options
In the home menu, there are several buttons to start different game modes:

- **Start Game:** Human vs. Human
- **Start Game AI:** Play against the AI using the DFS model
- **Start Game AI Hard:** Play against the AI using the Random Forest model
- **AI vs. AI:** Two DFS models play against each other for data collection

## Technical Details

### Original AI Implementation
The original AI uses a combination of dynamic programming, depth-first search (DFS), MinMax algorithms, and a string-matching scoring system. Key features include:

- **Move Evaluation:** Evaluates all possible moves on the board and selects the one with the highest score.
- **Advanced Prediction:** Uses DFS to predict up to 7 future moves for better decision-making.
- **Scoring System:** Assigns scores based on strategic patterns, both offensive and defensive.

### Machine Learning Integration
A Random Forest model is integrated to enhance the AI's strategic thinking. Key aspects include:

- **Feature Engineering:** Extracted and engineered features such as move number, distance from center, and various game-specific patterns and opportunities.
- **Data Collection:** Simulations with AI vs. AI games are run to gather gameplay data.
- **Model Tuning:** Used a correlation matrix to drop irrelevant features and scaled the input scores to reduce Mean Squared Error (MSE) and improve cross-validation performance.

### Future Work
- **Deploying the Game:** Planning to deploy the game online to collect real-time data.
- **Exploring Q-learning:** Leveraging the existing AI vs. AI play system.
- **Model Fine-tuning:** Continuously fine-tuning the model with new data to improve its gameplay.

## Code
The full implementation is available in the repository. Key functions include:

- **extract_features:** Extracts and engineers game-specific features for the Random Forest model.
- **evaluate:** Evaluates potential moves based on the original AI algorithms.
- **evaluateAdvanced:** Uses DFS to predict future moves and select the best one.
- **calculateScore:** Calculates scores based on patterns and strategic positions on the board.

## Getting Started
Clone the repository and follow the instructions to run the game on your local machine.

```sh
git clone [repository link]
cd [repository directory]
python gomoku.py
