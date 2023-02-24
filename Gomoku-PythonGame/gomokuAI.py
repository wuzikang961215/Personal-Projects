# set black, white and empty in every cell of the board
EMPTY = 0
BLACK = 1
WHITE = 2

class GomokuAI:

    # initialize different scores
    def _init_(self):
        # score: situation
        self.scores = {10: ['22000', '02200', '00220', '00022', '002020', '020200', '00200', '020000', '000020'],
                       100: ['02220', '22200', '00222', '02202', '22020', '02022', '20220', '002200', '022000', '000220'],
                       1000: ['002220', '022200', '020220', '022020', '22220', '02222', '20222', '22022', '22202'],
                       10000: ['022220'],
                       100000: ['22222']}
        
    # evaluate every possible moves and return the best
    # board is a 2D matrix
    def evaluate(self, board):
        bestmove = (0, 0)
        highestScore = float('-inf')
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == EMPTY:
                    # update highest score
                    newScore = self.calculateScore(i, j, board)
                    if newScore > highestScore:
                        bestmove = (i, j)
                        highestScore = newScore

        return bestmove

    def calculateScore(row, column, board):
        # save all strings from four directions
        situations = []
        # only evaluate 4 moves from each 8 directions
        situations.append(self.calculateDir(row, column, board, 'west', 4))
        situations.append(self.calculateDir(row, column, board, 'north', 4))
        situations.append(self.calculateDir(row, column, board, 'northwest', 4))
        situations.append(self.calculateDir(row, column, board, 'northeast', 4))

        # add scores for four directions
        totalscore = 0
        for situation in situations:
            currentscore = 0
            for score in self.scores:
                for s in self.scores[score]:
                    if situation.contains(s):
                        currentscore = score

            totalscore += currentscore

        return totalscore

    # explore from different directions
    def calculateDir(self, row, column, board, direction, level):
        # set in the middle
        s = '2'
        i = 1

        while level > 0:
            if direction == 'north':
                if row - i >= 0:
                    s.insert(0, board[row - i][column])
                if row + i < len(board):
                    s.append(board[row + i][column])
                level -= 1
                i += 1
            
            elif direction == 'west':
                if column - i >= 0:
                    s.insert(0, board[row][column - i])
                if column + i < len(board[0]):
                    s.append(board[row][column + i])
                level -= 1
                i += 1
                
            elif direction == 'northwest':
                if row - i >= 0 and column - i >= 0:
                    s.insert(0, board[row - i][column - i])
                if column + i < len(board[0]) and row + i < len(board):
                    s.append(board[row + i][column + i])
                level -= 1
                i += 1

            elif direction == 'northeast':
                if row - i >= 0 and column + i < len(board[0]):
                    s.insert(0, board[row - i][column + i])
                if row + i < len(board) and column - i >= 0:
                    s.append(board[row + i][column - i])
                level -= 1
                i += 1

        return s


                

'''if __name__ == '__main__':
    gomokuAI = GomokuAI()
    gomokuAI._init_(0)
    print(gomokuAI.scores)'''

