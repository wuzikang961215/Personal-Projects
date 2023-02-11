import pygame, sys

# set black, white and empty in every cell of the board
EMPTY = 0
BLACK = 1
WHITE = 2

# set black and white color for window display
black = (0, 0, 0)
white = (255, 255, 255)

buttons = []

class Button:
	def __init__(self,text,width,height,pos,elevation, gui_font):
		#Core attributes 
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
		#text
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
			    self.change_text(f"{self.text}", gui_font)
		    else:
			    self.dynamic_elecation = self.elevation
			    if self.pressed == True:
				    clicksound.play()
				    self.pressed, self.released = False, True
				    self.change_text(self.text, gui_font)
	    else:
		    self.dynamic_elecation = self.elevation
		    self.top_color = color2

                    


class Gomoku:

    # initialize the board
    def _init_(self):
        # create empty board 15 * 15
        self.board = [[]] * 15
        for row in range(15):
            self.board[row] = [EMPTY] * 15
        self.isblack = True

        # initialize black and white pieces
        self.whitepiece = pygame.image.load('whitepiece.png')
        # decrease image size
        self.whitepiece = pygame.transform.scale(self.whitepiece, (40, 40))

        self.blackpiece = pygame.image.load('blackpiece.png')
        # decrease image size
        self.blackpiece = pygame.transform.scale(self.blackpiece, (40, 40))

        # initialize start game background
        self.background = pygame.image.load('background.jpg')
        self.background = pygame.transform.scale(self.background, (640, 640))
        self.ending = pygame.image.load('ending.jpg')
        self.ending = pygame.transform.scale(self.ending, (640, 640))

    def move(self, row, column):
        if 0 <= row < 15 and 0 <= column < 15:
            if self.board[row][column] == EMPTY:
                self.board[row][column] = BLACK if self.isblack else WHITE
                self.isblack = not self.isblack
                return True

        # invalid move
        return False

    # apply dfs to decide winner
    def win(self, cordinate, direction, level, currentpiece):
        row, column = cordinate
        if currentpiece == 'White':
            temp = WHITE
        elif currentpiece == 'Black':
            temp = BLACK

        if 0 <= row < 15 and 0 <= column < 15:
            # base case: found winner
            if level == 6:
                return currentpiece
            
            # base case: no winner
            if self.board[row][column] != temp:
                return ''

        else:
            return ''

        # move 8 directions
        if direction == 'north':
            return self.win((row - 1, column), 'north', level + 1, currentpiece)
        elif direction == 'south':
            return self.win((row + 1, column), 'south', level + 1, currentpiece)
        elif direction == 'west':
            return self.win((row, column - 1), 'west', level + 1, currentpiece)
        elif direction == 'east':
            return self.win((row, column + 1), 'east', level + 1, currentpiece)
        elif direction == 'northwest':
            return self.win((row - 1, column - 1), 'northwest', level + 1, currentpiece)
        elif direction == 'northeast':
            return self.win((row - 1, column + 1), 'northeast', level + 1, currentpiece)
        if direction == 'southwest':
            return self.win((row + 1, column - 1), 'southwest', level + 1, currentpiece)
        if direction == 'southeast':
            return self.win((row + 1, column + 1), 'southeast', level + 1, currentpiece)

        

        

    # method to draw everything for the game
    def draw(self, win):
        # draw lines for board
        for i in range(1, 16):
            # horizontally
            pygame.draw.line(win, black, (40, i * 40), (600, i * 40))
            # vertically
            pygame.draw.line(win, black, (40 * i, 40), (i * 40, 600))
            # draw board frame
            pygame.draw.rect(win, black, (36, 36, 568, 568), 5)

            # draw several centers
            pygame.draw.circle(win, black, (320, 320), 6, 0)
            pygame.draw.circle(win, black, (160, 160), 6, 0)
            pygame.draw.circle(win, black, (160, 480), 6, 0)
            pygame.draw.circle(win, black, (480, 160), 6, 0)
            pygame.draw.circle(win, black, (480, 480), 6, 0)

            # draw moves from player
            for row in range(len(self.board)):
                for column in range(len(self.board[row])):
                    if self.board[row][column] != EMPTY:
                        color = self.board[row][column]
                        x = (row + 1) * 40
                        y = (column + 1) * 40

                        if color == WHITE:
                            win.blit(self.whitepiece, (y - 20, x - 20))

                        else:
                            win.blit(self.blackpiece, (y - 20, x - 20))

def startgame(gomoku, win, gui_font, clicksound):
    # draw background
    win.blit(gomoku.background, (0, 0))
    
    # draw buttons
    button1 = Button('Start',200,40,(100,400),5, gui_font)
    button2 = Button('About',200,40,(100,450),5, gui_font)
    button3 = Button('Exit',200,40,(100,500),5, gui_font)
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
        if button1.pressed == False and button1.released == True:
            run = False
        elif button3.pressed == False and button3.released == True:
            run = False
            return False

    return True

def playgame(gomoku, win, piecesound, clicksound, gui_font):
    run = True
    while run:
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
            pygame.draw.rect(win, white, (y - 20, x - 20, 40, 40), 2, 1)

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

                # check 8 directions from current move
                for directions in ['north', 'south', 'west', 'east', 'northwest', 'northeast', 'southwest', 'southeast']:
                    winner = gomoku.win((row, column), directions, 1, currentpiece)
                    if winner != '':
                        run = False
                        endgame(gomoku, win, gui_font, piecesound, clicksound, winner)
                        break

def endgame(gomoku, win, gui_font, piecesound, clicksound, winner):
    # ending interface
    # draw ending background
    win.blit(gomoku.ending, (0, 0))
    startagain = Button('Start Again',200,40,(225,350),5, gui_font)
    exit = Button('Exit',200,40,(225,400),5, gui_font)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # draw winner
        win.blit(pygame.font.Font(None,80).render('GAME OVER',True, (100, 100, 100), white), (175, 150))
        win.blit(pygame.font.Font(None,60).render('Winner: ',True, (100, 100, 100), white), (190, 240))
        win.blit(pygame.font.Font(None,60).render(winner ,True, (100, 100, 100), white), (355, 240))


        # draw buttons again
        startagain.draw(win, gui_font, (250, 155, 40), (150, 150, 150), clicksound)
        exit.draw(win, gui_font, (250, 155, 40), (150, 150, 150), clicksound)

        # restart game with 'start' button
        if startagain.pressed == False and startagain.released == True:
            gomoku._init_()
            playgame(gomoku, win, piecesound, clicksound, gui_font)
        elif exit.pressed == False and exit.released == True:
            pygame.quit()

        pygame.display.update()


def main():
    # initialize the game
    gomoku = Gomoku()
    gomoku._init_()

    # initialize a game window
    pygame.init()

    win = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("Gomoku (Five in a Row)")

    # get sound effect
    piecesound = pygame.mixer.Sound('piece.wav')
    clicksound = pygame.mixer.Sound('click.wav')
    pygame.mixer.music.load('fridays.mp3')
    pygame.mixer.music.play(-1)

    # set font for buttons
    gui_font = pygame.font.Font(None,30)

    # prepare game interface
    if startgame(gomoku, win, gui_font, clicksound):
   
        # play the whole game
        playgame(gomoku, win, piecesound, clicksound, gui_font)

    
    pygame.quit()


if __name__ == '__main__':
    main()

