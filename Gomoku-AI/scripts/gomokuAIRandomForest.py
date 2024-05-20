import numpy as np
import joblib
import pandas as pd
import random

class GomokuAIRandomForest:
    def __init__(self, model_path, scaler_path=None):
        self.model = joblib.load(model_path)
        if scaler_path:
            self.scaler = joblib.load(scaler_path)
        else:
            self.scaler = None

    def evaluate(self, board, move_number):
        if move_number <= 2:
            return self.evaluate_first_move(board, move_number)
        
        available_moves = self.get_available_moves(board)
        best_score = float('-inf')
        best_moves = []

        for move in available_moves:
            features_df = self.extract_features(board, move, move_number)
            score = self.model.predict(features_df)[0]

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

            # Introduce randomness in selecting the best move
            best_move = random.choice(best_moves)

        # # Print the best move's features for debugging
        # print(f"\nBest Move: {best_move}, Best Score: {best_score}")
        # for feature_name, value in features_df.iloc[0].items():
        #     print(f"{feature_name}: {value}")

        return best_move, best_score

    def evaluate_first_move(self, board, move_number):
        # Check for enemy stones on the board
        enemy_stones = [(row, col) for row in range(len(board)) for col in range(len(board[0])) if board[row][col] == 1]

        if not enemy_stones:
            return self.evaluate(board, move_number)  # No enemy stones, use normal evaluation

        # Get the enemy stone positions
        enemy_row, enemy_col = enemy_stones[0]

        # Define potential first moves 1-2 grids away from the enemy stone
        potential_moves = [
            (enemy_row + i, enemy_col + j)
            for i in range(-2, 3)
            for j in range(-2, 3)
            if 0 <= enemy_row + i < len(board) and 0 <= enemy_col + j < len(board[0]) and (i != 0 or j != 0)
        ]

        best_score = float('-inf')
        best_moves = []

        for move in potential_moves:
            row, col = move
            if board[row][col] == 0:  # Check if the position is empty
                features_df = self.extract_features(board, move, move_number)
                score = self.model.predict(features_df)[0]
                if score > best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)

        # Introduce randomness in selecting the best move
        best_move = random.choice(best_moves)

        # Print the best move's features for debugging
        print(f"\nBest First Move: {best_move}, Best Score: {best_score}")
        for feature_name, value in features_df.iloc[0].items():
            print(f"{feature_name}: {value}")

        return best_move, best_score


    def get_available_moves(self, board):
        available_moves = []
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 0:  # Empty position
                    available_moves.append((row, col))
        return available_moves

    def extract_features(self, board, move, move_number):
        row, column = move

        features = {
            'move_number': move_number,
            'distance_from_center': self.calculate_distance_from_center(row, column)
        }

        # Calculate the other features
        total_opportunities, total_threats, minor_opportunity, moderate_opportunity, major_opportunity, critical_open, win_sequence, moderate_threat, major_threat, critical_threat, lose_sequence = self.calculate_patterns(board, row, column)

        features.update({
            'total_opportunities': total_opportunities,
            'total_threats': total_threats,
            'minor_opportunity': minor_opportunity,
            'moderate_opportunity': moderate_opportunity,
            'major_opportunity': major_opportunity,
            'critical_open': critical_open,
            'win_sequence': win_sequence,
            'moderate_threat': moderate_threat,
            'major_threat': major_threat,
            'critical_threat': critical_threat,
            'lose_sequence': lose_sequence,
            'total_local_stones': self.count_local_stones(board, row, column)
        })

        return pd.DataFrame([features])

    def count_local_stones(self, board, row, column, radius=3):
        total_stones = 0
        start_row = max(0, row - radius)
        end_row = min(len(board), row + radius + 1)
        start_col = max(0, column - radius)
        end_col = min(len(board[0]), column + radius + 1)

        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                if board[r][c] != 0:  # Count both AI and enemy stones
                    total_stones += 1

        return total_stones

    def calculate_distance_from_center(self, row, column):
        center = 7
        return abs(row - center) + abs(column - center)

    def calculate_patterns(self, board, row, column):
        total_opportunities = total_threats = 0
        minor_opportunity = moderate_opportunity = major_opportunity = critical_open = win_sequence = 0
        moderate_threat = major_threat = critical_threat = lose_sequence = 0
        
        directions = ['north', 'west', 'northwest', 'northeast']
        situations = [self.calculateDir(row, column, direction, 4, False, board) for direction in directions]
        situations.extend(self.calculateDir(row, column, direction, 4, True, board) for direction in directions)

        for situation in situations:
            for feature, patterns in ai_patterns.items():
                if any(pattern in situation for pattern in patterns):
                    if feature == 'minor_opportunity':
                        minor_opportunity += 1
                    elif feature == 'moderate_opportunity':
                        moderate_opportunity += 1
                    elif feature == 'major_opportunity':
                        major_opportunity += 1
                    elif feature == 'critical_open':
                        critical_open += 1
                    elif feature == 'win_sequence':
                        win_sequence += 1
                    total_opportunities += 1

            for feature, patterns in enemy_patterns.items():
                if any(pattern in situation for pattern in patterns):
                    if feature == 'moderate_threat':
                        moderate_threat += 1
                    elif feature == 'major_threat':
                        major_threat += 1
                    elif feature == 'critical_threat':
                        critical_threat += 1
                    elif feature == 'lose_sequence':
                        lose_sequence += 1
                    total_threats += 1

        return total_opportunities, total_threats, minor_opportunity, moderate_opportunity, major_opportunity, critical_open, win_sequence, moderate_threat, major_threat, critical_threat, lose_sequence

    def calculateDir(self, row, column, direction, depth, enemy, board):
        s = '1' if enemy else '2'  # Set in the middle if it's AI's turn (white stone by default)

        i = 1
        while depth > 0:
            if direction == 'north':
                if row - i >= 0:
                    s = str(board[row - i][column]) + s
                if row + i < len(board):
                    s += str(board[row + i][column])

            elif direction == 'west':
                if column - i >= 0:
                    s = str(board[row][column - i]) + s
                if column + i < len(board[0]):
                    s += str(board[row][column + i])

            elif direction == 'northwest':
                if row - i >= 0 and column - i >= 0:
                    s = str(board[row - i][column - i]) + s
                if column + i < len(board[0]) and row + i < len(board):
                    s += str(board[row + i][column + i])

            elif direction == 'northeast':
                if row - i >= 0 and column + i < len(board[0]):
                    s = str(board[row - i][column + i]) + s
                if row + i < len(board) and column - i >= 0:
                    s += str(board[row + i][column - i])

            i += 1
            depth -= 1

        return s

# Patterns
ai_patterns = {
    'minor_opportunity': ['022100', '002210', '001220', '012200', '002020', '020200', '00200', '020000', '000020'],
    'moderate_opportunity': ['002221', '020221', '022021', '122200', '122020', '002200', '022000', '000220'],
    'major_opportunity': ['002220', '022200', '020220', '022020', '22220', '02222', '20222', '22022', '22202'],
    'critical_open': ['022220'],
    'win_sequence': ['22222']
}

enemy_patterns = {
    'moderate_threat': ['001112', '010112', '011012', '211100', '211010', '001100', '011000', '000110'],
    'major_threat': ['001110', '011100', '010110', '011010', '11110', '01111', '10111', '11011', '11101'],
    'critical_threat': ['011110'],
    'lose_sequence': ['11111']
}


