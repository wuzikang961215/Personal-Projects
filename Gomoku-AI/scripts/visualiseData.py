import pickle
from gameData import GameManager

def print_board(board):
    for row in board:
        print(' '.join(str(cell) for cell in row))

def visualize_game_data():
    manager = GameManager.load_state()
    
    for game_index, game in enumerate(manager.games):
        print(f"\n--- Game {game_index + 1} ---")
        print(f"Winner: {game.winner}")
        for move in game.moves:
            player = move['player']
            position = move['position']
            score = move['score']
            print(f"\nMove by {player} at position {position} with score {score}:")
            print_board(move['board_state'])

if __name__ == '__main__':
    visualize_game_data()
