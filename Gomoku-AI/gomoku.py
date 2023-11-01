import pygame, sys, gomokuAI

# set black, white and empty in every cell of the board
EMPTY, BLACK, WHITE = 0, 1, 2

# set black and white color for window display
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)

buttons = []

class Button:
	def __init__(self,text,width,height,pos,elevation, gui_font):
		# Core attributes 
		self.pressed, self.released = False, False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.original_y_pos = pos[1]

		# top rectangle 
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = '#475F77'
 
		# bottom rectangle 
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = '#354B5E'

		# text
		self.text = text
		self.text_surf = gui_font.render(text,True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

		buttons.append(self)
 
	def change_text(self, newtext, gui_font):
		self.text_surf = gui_font.render(newtext, True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
 
	def draw(self, win, gui_font, color1, color2, clicksound):
		# elevation logic 
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center 
 
		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation
 
		pygame.draw.rect(win,self.bottom_color, self.bottom_rect,border_radius = 12)
		pygame.draw.rect(win,self.top_color, self.top_rect,border_radius = 12)
		win.blit(self.text_surf, self.text_rect)
		self.check_click(gui_font, color1, color2, clicksound)
 
	def check_click(self, gui_font, color1, color2, clicksound):

	    mouse_pos = pygame.mouse.get_pos()
	    if self.top_rect.collidepoint(mouse_pos):
		    self.top_color = color1
		    if pygame.mouse.get_pressed()[0]:
			    self.dynamic_elecation = 0
			    self.pressed = True

		    else:
			    self.dynamic_elecation = self.elevation
			    if self.pressed:
				    clicksound.play()
				    self.pressed, self.released = False, True

	    else:
		    self.dynamic_elecation = self.elevation
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
        self.whitepiece = pygame.transform.scale(pygame.image.load('whitepiece.png'), (40, 40))
        self.blackpiece = pygame.transform.scale(pygame.image.load('blackpiece.png'), (40, 40))
        self.background = pygame.transform.scale(pygame.image.load('background.jpg'), (640, 640))
        self.ending = pygame.transform.scale(pygame.image.load('ending.jpg'), (640, 640))
        self.ai, self.aiHard = False, False


    def move(self, row, column):
        if 0 <= row < 15 and 0 <= column < 15:
            if self.board[row][column] == EMPTY:
                self.board[row][column] = BLACK if self.isblack else WHITE
                self.isblack = not self.isblack
                return True

        # invalid move
        return False

    # apply dfs to decide winner
    def win(self, coordinate, direction, level, currentpiece):
        row, column = coordinate
        dx, dy = Gomoku.DIRECTIONS[direction]
        next_coordinate = (row + dx, column + dy)
        
        if currentpiece == 'White':
            piece_value = WHITE
        else:
            piece_value = BLACK

        if not (0 <= row < 15 and 0 <= column < 15 and self.board[row][column] == piece_value):
            return ''

        if level == 5:
            return currentpiece

        return self.win(next_coordinate, direction, level + 1, currentpiece)


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
    startGame = Button('Start Game',210,30,(100,380),5, gui_font)
    startGameAI = Button('Start Game AI', 210, 30, (100, 420), 5, gui_font)
    startGameAIhard = Button('Start Game AI Hard', 210, 30, (100, 460), 5, gui_font)
    about = Button('About',210,30,(100,500),5, gui_font)
    exit = Button('Exit',210,30,(100,540),5, gui_font)
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

        elif exit.pressed == False and exit.released == True:
            run = False
            return False

    return True

def playgame(gomoku, win, piecesound, clicksound, gui_font):
    if gomoku.ai == True or gomoku.aiHard == True:
        AIplayer = gomokuAI.GomokuAI(gomoku.board)


    run = True
    while run:
        # get mouse click position
        y, x = pygame.mouse.get_pos()
        # transfer to array position
        row = round(x/40 - 1)
        column = round(y/40 - 1)
        i, j = (-1, -1)
                    
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
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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

                # check 8 directions from current move
                for directions in ['north', 'south', 'west', 'east', 'northwest', 'northeast', 'southwest', 'southeast']:
                    winner = gomoku.win((row, column), directions, 1, currentpiece)

                    if winner != '':
                        run = False
                        endgame(gomoku, win, gui_font, piecesound, clicksound, winner)
                        break

                # if next move is AI
                if gomoku.ai == True or gomoku.aiHard == True:
                    AImove = (-1, -1)
                    if gomoku.ai == True:
                        AImove = AIplayer.evaluate()
                    elif gomoku.aiHard == True:
                        AImove = AIplayer.evaluateAdvanced(row, column)
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

                    # check 8 directions from current move
                    for directions in ['north', 'south', 'west', 'east', 'northwest', 'northeast', 'southwest', 'southeast']:
                        winner = gomoku.win((i, j), directions, 1, currentpiece)

                        if winner != '':
                            run = False
                            endgame(gomoku, win, gui_font, piecesound, clicksound, winner)
                            break



def endgame(gomoku, win, gui_font, piecesound, clicksound, winner):
    # ending interface
    # draw ending background
    win.blit(gomoku.ending, (0, 0))
    startagain = Button('Start Again',210,30,(225,300),5, gui_font)
    startagainAI = Button('Start Again AI',210,30,(225,340),5, gui_font)
    startagainAIhard = Button('Start Again AI Hard',210,30,(225,380),5, gui_font)
    exit = Button('Exit',210,30,(225,420),5, gui_font)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # draw winner
        win.blit(pygame.font.Font(None,80).render('GAME OVER',True, (100, 100, 100), WHITE_COLOR), (175, 150))
        win.blit(pygame.font.Font(None,60).render('Winner: ',True, (100, 100, 100), WHITE_COLOR), (190, 240))
        win.blit(pygame.font.Font(None,60).render(winner ,True, (100, 100, 100), WHITE_COLOR), (355, 240))


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
    piecesound = pygame.mixer.Sound('piece.wav')
    clicksound = pygame.mixer.Sound('click.wav')

    # set font for buttons
    gui_font = pygame.font.Font(None,30)

    # prepare game interface
    if startgame(gomoku, win, gui_font, clicksound):
   
        # play the whole game
        playgame(gomoku, win, piecesound, clicksound, gui_font)

    
    pygame.quit()


if __name__ == '__main__':
    main()

