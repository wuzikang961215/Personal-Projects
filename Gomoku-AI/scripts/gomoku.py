import pygame, sys, gomokuAI, gomokuAIAggressive, gomokuAIRandomForest
from copy import deepcopy
from gameData import GameManager  # Adjust the import path

# set black, white and empty in every cell of the board
EMPTY, BLACK, WHITE = 0, 1, 2

# set black and white color for window display
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)

buttons = []

class Button:
    def __init__(self, text, width, height, pos, elevation, gui_font):
        # Core attributes
        self.pressed, self.released = False, False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'

        # text
        self.text = text
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        buttons.append(self)

    def change_text(self, newtext, gui_font):
        self.text_surf = gui_font.render(newtext, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, win, gui_font, color1, color2, clicksound):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(win, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(win, self.top_color, self.top_rect, border_radius=12)
        win.blit(self.text_surf, self.text_rect)
        self.check_click(gui_font, color1, color2, clicksound)

    def check_click(self, gui_font, color1, color2, clicksound):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = color1
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    clicksound.play()
                    self.pressed, self.released = False, True
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = color2


class Gomoku:
    DIRECTIONS = {
        'north': (-1, 0),
        'south': (1, 0),
        'west': (0, -1),
        'east': (0, 1),
        'northwest': (-1, -1),
        'northeast': (-1, 1),
        'southwest': (1, -1),
        'southeast': (1, 1)
    }

    # initialize the board
    def __init__(self):
        self.board = [[EMPTY] * 15 for _ in range(15)]
        self.isblack = True
        self.whitepiece = pygame.transform.scale(pygame.image.load('../images/whitepiece.png'), (40, 40))
        self.blackpiece = pygame.transform.scale(pygame.image.load('../images/blackpiece.png'), (40, 40))
        self.background = pygame.transform.scale(pygame.image.load('../images/background.jpg'), (640, 640))
        self.ending = pygame.transform.scale(pygame.image.load('../images/ending.jpg'), (640, 640))
        self.ai, self.aiHard, self.aiVsAi = False, False, False

    def move(self, row, column):
        if 0 <= row < 15 and 0 <= column < 15:
            if self.board[row][column] == EMPTY:
                self.board[row][column] = BLACK if self.isblack else WHITE
                self.isblack = not self.isblack
                return True
        # invalid move
        return False

    def check_direction(self, coordinate, direction, currentpiece):
        row, column = coordinate
        dx, dy = Gomoku.DIRECTIONS[direction]

        if currentpiece == 'White':
            piece_value = WHITE
        else:
            piece_value = BLACK

        count = 0
        for _ in range(4):  # We only need to check 4 more stones to make a total of 5
            row += dx
            column += dy
            if 0 <= row < 15 and 0 <= column < 15 and self.board[row][column] == piece_value:
                count += 1
            else:
                break

        return count

    def win(self, coordinate, currentpiece):
        for direction in Gomoku.DIRECTIONS:
            dx, dy = Gomoku.DIRECTIONS[direction]
            # Check one direction
            count = self.check_direction(coordinate, direction, currentpiece)
            # Check the opposite direction
            opposite_direction = (dx * -1, dy * -1)
            for opp_dir, (ox, oy) in Gomoku.DIRECTIONS.items():
                if (ox, oy) == opposite_direction:
                    count += self.check_direction(coordinate, opp_dir, currentpiece)
                    break
            # Add the current stone to the count
            count += 1
            # If we have 5 or more stones in total, we have a winner
            if count >= 5:
                return currentpiece
        return ''

    # method to draw everything for the game
    def draw(self, win):
        # draw lines for board
        for i in range(15):
            # horizontally
            pygame.draw.line(win, BLACK_COLOR, (40, i * 40), (600, i * 40))
            # vertically
            pygame.draw.line(win, BLACK_COLOR, (40 * i, 40), (i * 40, 600))
            # draw board frame
            pygame.draw.rect(win, BLACK_COLOR, (36, 36, 568, 568), 5)

            # draw several centers
            pygame.draw.circle(win, BLACK_COLOR, (320, 320), 6, 0)
            pygame.draw.circle(win, BLACK_COLOR, (160, 160), 6, 0)
            pygame.draw.circle(win, BLACK_COLOR, (160, 480), 6, 0)
            pygame.draw.circle(win, BLACK_COLOR, (480, 160), 6, 0)
            pygame.draw.circle(win, BLACK_COLOR, (480, 480), 6, 0)

            # draw moves from player
            for row in range(len(self.board)):
                for column in range(len(self.board[row])):
                    if self.board[row][column] == BLACK:
                        win.blit(self.blackpiece, ((column + 1) * 40 - 20, (row + 1) * 40 - 20))
                    elif self.board[row][column] == WHITE:
                        win.blit(self.whitepiece, ((column + 1) * 40 - 20, (row + 1) * 40 - 20))


def startgame(gomoku, win, gui_font, clicksound):
    # draw background
    win.blit(gomoku.background, (0, 0))
    
    # draw buttons
    startGame = Button('Start Game', 210, 30, (100, 380), 5, gui_font)
    startGameAI = Button('Start Game AI', 210, 30, (100, 420), 5, gui_font)
    startGameAIhard = Button('Start Game AI Hard', 210, 30, (100, 460), 5, gui_font)
    AIvsAI = Button('AI VS AI', 210, 30, (100, 500), 5, gui_font)
    exit = Button('Exit', 210, 30, (100, 540), 5, gui_font)
    pygame.display.update()

    run = True

    while run:
        # click to continue game
        # check out all user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        for b in buttons:
            b.draw(win, gui_font, (250, 155, 40), (150, 150, 150), clicksound)

        pygame.display.update()

        # enter game with 'start' button
        if startGame.pressed == False and startGame.released == True:
            run = False

        # if play with ai
        if startGameAI.pressed == False and startGameAI.released == True:
            gomoku.ai = True
            run = False

        # if play with ai hard
        if startGameAIhard.pressed == False and startGameAIhard.released == True:
            gomoku.aiHard = True
            run = False

        # if ai versus ai
        if AIvsAI.pressed == False and AIvsAI.released == True:
            gomoku.aiVsAi = True
            run = False

        elif exit.pressed == False and exit.released == True:
            run = False
            return False

    return True

def playgame(gomoku, win, piecesound, clicksound, gui_font):
    if gomoku.ai:
        AIplayer = gomokuAI.GomokuAI(gomoku.board)

    if gomoku.aiHard:
        AIplayer = gomokuAIRandomForest.GomokuAIRandomForest('../data/random_forest_gomoku.pkl')

    if gomoku.aiVsAi:
        AIplayer1 = gomokuAI.GomokuAI(gomoku.board)
        AIplayer2 = gomokuAIAggressive.GomokuAI(gomoku.board)

    # record data here
    manager = GameManager.load_state()
    game = manager.create_new_game()

    run = True

    # initialize i, j before game runs
    i, j = (-1, -1)

    while run:

        # when AI versus AI
        if gomoku.aiVsAi:

            # refreshing the whole board
            win.fill([255, 200, 100])
            gomoku.draw(win)
            pygame.display.update()
            
            # AI player 1 moves
            AImove = (-1, -1)
            AIEvaluation = AIplayer1.evaluateAdvanced(i, j)
            AImove = AIEvaluation[0]
            AIscore = AIEvaluation[1]
            i, j = AImove
            gomoku.move(i, j)
            piecesound.play()
            # after movement, piece color is opposite
            if gomoku.isblack == False:
                currentpiece = 'Black'
            else:
                currentpiece = 'White'

            # record AI movement data
            game.record_move(currentpiece, i, j, deepcopy(gomoku.board), AIscore)

            # refreshing the whole board after ai moves
            win.fill([255, 200, 100])
            gomoku.draw(win)
            pygame.display.update()

            # check 8 directions from current move
            for directions in ['north', 'west', 'northwest', 'northeast']:
                winner = gomoku.win((i, j), currentpiece)

                if winner != '':
                    # record winner data here
                    game.end_game(winner, deepcopy(gomoku.board))
                    manager.finish_game(game)
                    manager.save_state()

                    run = False
                    endgame(gomoku, win, gui_font, piecesound, clicksound, winner)

                    break

            # AI player 2 moves
            AIEvaluation = AIplayer2.evaluateAdvanced(i, j)
            AImove = AIEvaluation[0]
            AIscore = AIEvaluation[1]
            i, j = AImove
            gomoku.move(i, j)
            piecesound.play()
            # after movement, piece color is opposite
            if gomoku.isblack == False:
                currentpiece = 'Black'
            else:
                currentpiece = 'White'

            # record AI movement data
            game.record_move(currentpiece, i, j, deepcopy(gomoku.board), AIscore)

            # refreshing the whole board after ai moves
            win.fill([255, 200, 100])
            gomoku.draw(win)
            pygame.display.update()

            # check 8 directions from current move
            for directions in ['north', 'south', 'west', 'east', 'northwest', 'northeast', 'southwest', 'southeast']:
                winner = gomoku.win((i, j), currentpiece)

                if winner != '':
                    # record winner data here
                    game.end_game(winner, deepcopy(gomoku.board))
                    manager.finish_game(game)
                    manager.save_state()

                    run = False
                    endgame(gomoku, win, gui_font, piecesound, clicksound, winner)
                    break
                
        # get mouse click position
        y, x = pygame.mouse.get_pos()
        # transfer to array position
        row = round(x/40 - 1)
        column = round(y/40 - 1)
                    
        # refreshing the whole board
        win.fill([255, 200, 100])
        gomoku.draw(win)
        # draw a small rectangle to represent available moves
        if 0 <= row < 15 and 0 <= column < 15 and gomoku.board[row][column] == EMPTY:
            pygame.draw.rect(win, WHITE_COLOR, (y - 20, x - 20, 40, 40), 2, 1)

        pygame.display.update()

        # check out all user inputs
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            # get mouse left click
            if not gomoku.aiVsAi and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gomoku.move(row, column)
                piecesound.play()

                # after movement, piece color is opposite
                if gomoku.isblack == False:
                    currentpiece = 'Black'
                else:
                    currentpiece = 'White'

                # refreshing the whole board after player moves
                win.fill([255, 200, 100])
                gomoku.draw(win)
                pygame.display.update()

                # record human movement data here
                game.record_move(currentpiece, row, column, deepcopy(gomoku.board), gomokuAI.GomokuAI(gomoku.board).calculateScore(row, column))

                # check 8 directions from current move
                for directions in ['north', 'south', 'west', 'east', 'northwest', 'northeast', 'southwest', 'southeast']:
                    winner = gomoku.win((row, column), currentpiece)

                    if winner != '':
                        # record winner data here
                        game.end_game(winner, deepcopy(gomoku.board))
                        manager.finish_game(game)
                        manager.save_state()
                        run = False
                        endgame(gomoku, win, gui_font, piecesound, clicksound, winner)
                        break

                # if next move is AI
                if gomoku.ai or gomoku.aiHard:
                    AImove = (-1, -1)
                    if gomoku.ai:
                        AIEvaluation = AIplayer.evaluateAdvanced(row, column)
                        AImove = AIEvaluation[0]
                        AIscore = AIEvaluation[1]
                    elif gomoku.aiHard:
                        AImove, AIscore = AIplayer.evaluate(gomoku.board, len(game.moves))
                    i, j = AImove
                    gomoku.move(i, j)
                    piecesound.play()

                    # after movement, piece color is opposite
                    if gomoku.isblack == False:
                        currentpiece = 'Black'
                    else:
                        currentpiece = 'White'

                    # refreshing the whole board after ai moves
                    win.fill([255, 200, 100])
                    gomoku.draw(win)
                    pygame.display.update()

                    # record AI movement data
                    game.record_move(currentpiece, i, j, deepcopy(gomoku.board), AIscore)

                    # check 8 directions from current move
                    for directions in ['north', 'south', 'west', 'east', 'northwest', 'northeast', 'southwest', 'southeast']:
                        winner = gomoku.win((i, j), currentpiece)

                        if winner != '':
                            # record winner data here
                            game.end_game(winner, deepcopy(gomoku.board))
                            manager.finish_game(game)
                            manager.save_state()
                            run = False
                            endgame(gomoku, win, gui_font, piecesound, clicksound, winner)
                            break

def endgame(gomoku, win, gui_font, piecesound, clicksound, winner):
    # ending interface
    # draw ending background
    win.blit(gomoku.ending, (0, 0))
    startagain = Button('Start Again', 210, 30, (225, 300), 5, gui_font)
    startagainAI = Button('Start Again AI', 210, 30, (225, 340), 5, gui_font)
    startagainAIhard = Button('Start Again AI Hard', 210, 30, (225, 380), 5, gui_font)
    exit = Button('Exit', 210, 30, (225, 420), 5, gui_font)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # draw winner
        win.blit(pygame.font.Font(None, 80).render('GAME OVER', True, (100, 100, 100), WHITE_COLOR), (175, 150))
        win.blit(pygame.font.Font(None, 60).render('Winner: ', True, (100, 100, 100), WHITE_COLOR), (190, 240))
        win.blit(pygame.font.Font(None, 60).render(winner, True, (100, 100, 100), WHITE_COLOR), (355, 240))

        # draw buttons again
        startagain.draw(win, gui_font, (250, 155, 40), (150, 150, 150), clicksound)
        startagainAI.draw(win, gui_font, (250, 155, 40), (150, 150, 150), clicksound)
        startagainAIhard.draw(win, gui_font, (250, 155, 40), (150, 150, 150), clicksound)
        exit.draw(win, gui_font, (250, 155, 40), (150, 150, 150), clicksound)

        # restart game with 'start' button
        if startagain.pressed == False and startagain.released == True:
            gomoku.__init__()
            playgame(gomoku, win, piecesound, clicksound, gui_font)
        elif startagainAI.pressed == False and startagainAI.released == True:
            gomoku.__init__()
            gomoku.ai = True
            playgame(gomoku, win, piecesound, clicksound, gui_font)
        elif startagainAIhard.pressed == False and startagainAIhard.released == True:
            gomoku.__init__()
            gomoku.aiHard = True
            playgame(gomoku, win, piecesound, clicksound, gui_font)
        elif exit.pressed == False and exit.released == True:
            pygame.quit()

        pygame.display.update()

def main():
    # initialize the game
    gomoku = Gomoku()
    gomoku.__init__()

    # initialize a game window
    pygame.init()

    win = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("Gomoku (Five in a Row)")

    # get sound effect
    piecesound = pygame.mixer.Sound('../sounds/piece.wav')
    clicksound = pygame.mixer.Sound('../sounds/click.wav')

    # set font for buttons
    gui_font = pygame.font.Font(None, 30)

    # prepare game interface
    if startgame(gomoku, win, gui_font, clicksound):
        # play the whole game
        playgame(gomoku, win, piecesound, clicksound, gui_font)

    pygame.quit()

if __name__ == '__main__':
    main()
