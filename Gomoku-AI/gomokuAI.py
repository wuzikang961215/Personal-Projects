# set black, white and empty in every cell of the board
EMPTY = 0
BLACK = 1
WHITE = 2

class GomokuAI:

    # initialize different scores
    def __init__(self, board):
        # score: situation
        self.enemyscores = {5: ['011200', '001120', '002110', '021100', '001010', '010100', '00100', '010000', '000010'],
                            50: ['001112', '010112', '011012', '211100', '211010', '001100', '011000', '000110'],
                            500: ['001110', '011100', '010110', '011010', '11110', '01111', '10111', '11011', '11101'],
                            80000000: ['011110'],
                            800000000: ['11111']}
        self.scores = {10: ['022100', '002210', '001220', '012200', '002020', '020200', '00200', '020000', '000020'],
                       100: ['002221', '020221', '022021', '122200', '122020', '002200', '022000', '000220'],
                       1000: ['002220', '022200', '020220', '022020', '22220', '02222', '20222', '22022', '22202'],
                       100000000: ['022220'],
                       1000000000: ['22222']}

        self.board = []
        # copy from board
        for row in board:
            self.board.append(row)

        
    # evaluate every possible moves and return the best
    # board is a 2D matrix
    def evaluate(self):
        bestmove = (-1, -1)
        highestScore = float('-inf')
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == EMPTY:
                    newScore = self.calculateScore(i, j)
                    # update highest score
                    if newScore > highestScore:
                        bestmove = (i, j)
                        highestScore = newScore

        return bestmove

    # hard difficulty AI: advanced depth evaluation
    def evaluateAdvanced(self, enemyrow, enemycolumn):
        bestmove = (-1, -1)
        # If the current move is the AI's, then we want to maximize the score. 
        # If it's the enemy's, we want to minimize. We'll start with a very low 
        # initial score for the maximizing player.
        highestScore = float('-inf')

        dp = {}  # Initializing the cache as an empty dictionary

        # only evaluate around enemy move to save time
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == EMPTY:
                    discovered = set()  # For tracking visited nodes in DFS
                    # predict 11 future moves
                    newScore = self.dfs(i, j, 15, discovered, dp)
                    # get near the enemy at the beginning
                    if enemyrow - 3 <= i < enemyrow + 4 and enemycolumn - 3 <= j < enemycolumn + 4:
                        newScore += 200
                    # update highest score and corresponding move
                    if newScore > highestScore:
                        bestmove = (i, j)
                        highestScore = newScore

        return bestmove


    def dfs(self, row, column, level, discovered, dp):

        # Check if we've already computed this state
        if (row, column, level) in dp:
            return dp[(row, column, level)]

        discovered.add((row, column))

        currentscore = self.calculateScore(row, column)
        
        # Adjust score based on whose turn it is
        if level % 2 == 0:
            currentscore *= -1

        # Base case: if at the lowest depth, return the score for this move
        if level == 1:
            discovered.remove((row, column))
            return currentscore

        # Initialize best_score. If it's AI's turn, start with negative infinity (maximizing). 
        # If it's opponent's turn, start with positive infinity (minimizing).
        best_score = float('-inf') if level % 2 == 1 else float('inf')

        # Explore all possible next moves
        for i in range(row - 3, row + 4):
            for j in range(column - 3, column + 4):
                if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == EMPTY and (i, j) not in discovered:
                    # Recursive call
                    score_for_this_move = self.dfs(i, j, level - 1, discovered, dp)

                    # Update best_score based on whose turn it is
                    if level % 2 == 1:  # AI's turn: maximize
                        best_score = max(best_score, currentscore + score_for_this_move)
                    else:  # Opponent's turn: minimize
                        best_score = min(best_score, currentscore + score_for_this_move)

        # Cleanup and cache the result
        discovered.remove((row, column))
        dp[(row, column, level)] = best_score

        return best_score



    def calculateScore(self, row, column):
        # save all strings from four directions
        situations = []
        # only evaluate 4 moves from each 8 directions
        # False means it's AI's calculation
        situations.append(self.calculateDir(row, column,  'west', 4, False))
        situations.append(self.calculateDir(row, column,  'north', 4, False))
        situations.append(self.calculateDir(row, column,  'northwest', 4, False))
        situations.append(self.calculateDir(row, column,  'northeast', 4, False))
        situations.append(self.calculateDir(row, column,  'west', 4, True))
        situations.append(self.calculateDir(row, column,  'north', 4, True))
        situations.append(self.calculateDir(row, column,  'northwest', 4, True))
        situations.append(self.calculateDir(row, column,  'northeast', 4, True))

        # some conditions that can dramatically increase the score
        score1000 = 0
        score100 = 0

        enemyscore1000 = 0
        enemyscore100 = 0


        # add scores for four directions
        totalscore = 0
        enemyscore = 0
        for situation in situations:
            currentscore = 0
            for score in self.scores:
                for s in self.scores[score]:
                    if s in situation:
                        currentscore = score
                
            if currentscore == 1000:
                score1000 += 1

            if currentscore == 100:
                score100 += 1

            for score in self.enemyscores:
                for s in self.enemyscores[score]:
                    if s in situation:
                        enemyscore = score

            if enemyscore == 1000:
                enemyscore1000 += 1

            if enemyscore == 100:
                enemyscore100 += 1

            totalscore += (currentscore + enemyscore)

        # increase total score under some circumstances
        if score1000 >= 2:
            totalscore *= 5

        if enemyscore1000 >= 2:
            totalscore *= 5

        if score100 >= 1 and score1000 >= 1:
            totalscore *= 4

        if enemyscore100 >= 1 and enemyscore1000 >= 1:
            totalscore *= 4

        return totalscore

    # explore from different directions
    def calculateDir(self, row, column, direction, level, enemy):
        s = '1'
        # set in the middle if it's AI's turn
        if enemy == False:
            s = '2'

        i = 1

        while level > 0:
            if direction == 'north':
                if row - i >= 0:
                    s = str(self.board[row - i][column]) + s
                if row + i < len(self.board):
                    s += str(self.board[row + i][column])
                level -= 1
                i += 1
            
            elif direction == 'west':
                if column - i >= 0:
                    s = str(self.board[row][column - i]) + s
                if column + i < len(self.board[0]):
                    s += str(self.board[row][column + i])
                level -= 1
                i += 1
                
            elif direction == 'northwest':
                if row - i >= 0 and column - i >= 0:
                    s = str(self.board[row - i][column - i]) + s
                if column + i < len(self.board[0]) and row + i < len(self.board):
                    s += str(self.board[row + i][column + i])
                level -= 1
                i += 1

            elif direction == 'northeast':
                if row - i >= 0 and column + i < len(self.board[0]):
                    s = str(self.board[row - i][column + i]) + s
                if row + i < len(self.board) and column - i >= 0:
                    s += str(self.board[row + i][column - i])
                level -= 1
                i += 1

        return s

