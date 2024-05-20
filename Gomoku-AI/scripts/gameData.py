import pickle, os

class GameData:
    def __init__(self):
        self.moves = []
        self.winner = None
        self.final_board = None

    def record_move(self, player, row, col, board_state, score):
        move_record = {
            'player': player,
            'position': (row, col),
            'board_state': board_state,
            'score': score,
            'distance_from_center': abs(7 - row) + abs(7 - col)
        }
        self.moves.append(move_record)

    def end_game(self, winner, final_board):
        print("Received final board in end_game:", final_board)
        self.winner = winner
        self.final_board = final_board

    def print_details(self):
        print("Game Details:")
        print("Moves:")
        for index, move in enumerate(self.moves):
            move_info = f"Move {index + 1}:"
            for key, value in move.items():
                if key != 'board_state':  # Skip printing the entire board state to keep output clean
                    move_info += f" {key}: {value},"
            print(move_info.rstrip(','))  # Remove the trailing comma
        print("\nWinner:", self.winner)
        print("Final Board State:")
        # Print the final board state more compactly
        for row in self.final_board:
            print(' '.join(str(cell) for cell in row))




class GameManager:
    def __init__(self):
        self.games = []

    def create_new_game(self):
        return GameData()

    def finish_game(self, game_data):
        self.games.append(game_data)

    def delete_last_game(self):
        if self.games:  # Check if there are any games recorded
            self.games.pop()  # Remove the last game from the list
        else:
            print("No games to delete.")

    def save_state(self, file_path=os.path.join(os.path.dirname(__file__), '..', 'data', 'game_manager.pkl')):
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_state(file_path=os.path.join(os.path.dirname(__file__), '..', 'data', 'game_manager.pkl')):
        try:
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return GameManager()  # Return a new instance if no file exists
        
    def update_board_structures(self):
        for game in self.games:
            for move in game.moves:
                if isinstance(move['board_state'], list) and len(move['board_state']) == 1:
                    move['board_state'] = move['board_state'][0]
            if isinstance(game.final_board, list) and len(game.final_board) == 1:
                game.final_board = game.final_board[0]
        
    def print_all_game_details(self):
        if not self.games:
            print("No games recorded.")
        for game_index, game in enumerate(self.games):
            print(f"--- Game {game_index + 1} ---")
            game.print_details()
            print("\n")

    def correct_last_game_data(self):
        if self.games:
            last_game = self.games[-1]  # Access the last game
            if len(last_game.moves) > 1:
                # Remove the second-to-last move as it was the unrecognized winning move
                winning_move = last_game.moves[-2]
                del last_game.moves[-1]  # Delete the second-to-last move

                # Update the final board state to the board state of the winning move
                last_game.final_board = winning_move['board_state']

                # Set 'black' as the winner
                last_game.winner = winning_move['player']

            else:
                print("No moves recorded in the last game to correct.")
        else:
            print("No games to correct.")

    def update_games_with_new_feature(self):
        center_row, center_col = 7, 7  # Assuming the board is 15x15 and center is at (7, 7)
        for game in self.games:
            for move in game.moves:
                row, col = move['position']
                # Calculate distance from center and update the move record
                move['distance_from_center'] = abs(center_row - row) + abs(center_col - col)

# Example usage
'''if __name__ == "__main__":
    manager = GameManager.load_state()
    game = manager.create_new_game()
    game.record_move('player1', 0, 1, [[0]*15 for _ in range(15)], 10)
    game.record_move('player2', 0, 2, [[0]*15 for _ in range(15)], 15)
    game.end_game('player1', [[0]*15 for _ in range(15)])
    manager.finish_game(game)
    manager.save_state()'''
