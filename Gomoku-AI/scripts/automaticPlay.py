import pygame
from gomoku import *
import gomokuAI
import gomokuAIAggressive
from copy import deepcopy
from gameData import GameManager, GameData

class AIAutomaticPlay:
    def __init__(self, num_games=500):
        self.num_games = num_games
        self.manager = GameManager.load_state()
        self.MAX_MOVES = 120  # Set a reasonable move limit for AI vs AI games

    def play_game(self):
        game = GameData()
        gomoku = Gomoku()
        AIplayer1 = gomokuAI.GomokuAI(gomoku.board)
        AIplayer2 = gomokuAIAggressive.GomokuAI(gomoku.board)

        move_count = 0
        i, j = -1, -1
        current_player = AIplayer1
        current_piece = 'Black'

        while move_count < self.MAX_MOVES:
            AIEvaluation = current_player.evaluateAdvanced(i, j)
            AImove = AIEvaluation[0]
            AIscore = AIEvaluation[1]
            i, j = AImove
            if not gomoku.move(i, j):
                break  # Invalid move, end the game

            # Record AI movement data
            game.record_move(current_piece, i, j, deepcopy(gomoku.board), AIscore)
            move_count += 1

            # Check for win
            if gomoku.win((i, j), current_piece) != '':
                game.end_game(current_piece, deepcopy(gomoku.board))
                self.manager.finish_game(game)
                self.manager.save_state()
                return

            # Switch player
            current_player = AIplayer2 if current_player == AIplayer1 else AIplayer1
            current_piece = 'White' if current_piece == 'Black' else 'Black'

         # If max moves reached, do not record the game
        if move_count < self.MAX_MOVES:
            game.end_game('Draw', deepcopy(gomoku.board))
            self.manager.finish_game(game)
            self.manager.save_state()

    def run(self):
        for _ in range(self.num_games):
            self.play_game()

if __name__ == '__main__':
    auto_play = AIAutomaticPlay(num_games=500)
    auto_play.run()
    print("Finished playing 500 games")
