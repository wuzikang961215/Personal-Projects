# set black, white and empty in every cell of the board
EMPTY = 0
BLACK = 1
WHITE = 2

class GomokuAI:

    # initialize different scores
    def _init_(self, board):
        # score: situation
        self.enemyscores = {10: ['011200', '001120', '002110', '021100', '001010', '010100', '00100', '010000', '000010'],
                            100: ['001112', '010112', '011012', '211100', '211010', '001100', '011000', '000110'],
                            1000: ['001110', '011100', '010110', '011010', '11110', '01111', '10111', '11011', '11101'],
                            100000000: ['011110'],
                            1000000000: ['11111']}
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
        highestScore = float('-inf')
        dp = []
        for i in range(len(self.board)):
            dp.append([-1] * len(self.board[0]))
        # only evaluate around enemy move to save time
        for i in range(enemyrow - 3, enemyrow + 4):
            for j in range(enemycolumn - 3, enemycolumn + 4):
                if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == EMPTY:
                    # prepare for dfs
                    discovered = set()
                    # predict 3 future moves
                    newScore = self.dfs(i, j, 3, 0, discovered, dp)
                    # update highest score
                    if newScore > highestScore:
                        bestmove = (i, j)
                        highestScore = newScore

        return bestmove

    def dfs(self, row, column, level, totalscore, discovered, dp):

        # dynamic programming
        '''if dp[row][column] > -1:
            if level % 2 == 0:
                return -1 * dp[row][column]
            
            else:
                return dp[row][column]'''

        discovered.add((row, column))

        currentscore = self.calculateScore(row, column)
        # when enemy moves
        if level % 2 == 0:
            currentscore *= -1

        if level == 1:
            discovered.remove((row, column))
            return totalscore + currentscore

        maxscore = float('-inf')
        # backtracking all possible next moves
        for i in range(row - 3, row + 4):
            for j in range(column - 3, column + 4):
                if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == EMPTY and (i, j) not in discovered:
                    # recursive call
                    maxscore = max(maxscore, self.dfs(i, j, level - 1, totalscore + currentscore, discovered, dp))

        discovered.remove((row, column))

        #dp[row][column] = maxscore

        return maxscore

        

        

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
        if score1000 >= 2 or enemyscore1000 >= 2:
            totalscore *= 6

        if score100 >= 1 and score1000 >= 1:
            totalscore *= 2

        if enemyscore100 >= 1 and enemyscore1000 >= 1:
            totalscore *= 2

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

