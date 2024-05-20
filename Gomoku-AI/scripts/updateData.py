from gameData import GameManager

# set black, white and empty in every cell of the board
EMPTY = 0
BLACK = 1
WHITE = 2

# AI's patterns: Focus on indicating both threat creation and blockage potential
ai_patterns = {
    'minor_opportunity': ['011200', '001120', '002110', '021100', '001010', '010100', '00100', '010000', '000010'],
    'moderate_opportunity': ['001112', '010112', '011012', '211100', '211010', '001100', '011000', '000110'],
    'major_opportunity': ['001110', '011100', '010110', '011010', '11110', '01111', '10111', '11011', '11101'],
    'critical_open': ['011110'],
    'win_sequence': ['11111']
}

# Enemy's patterns: Focus on indicating the enemy's threat levels and the AI's blocking needs
enemy_patterns = {
    'minor_threat': ['022100', '002210', '001220', '012200', '002020', '020200', '00200', '020000', '000020'],
    'moderate_threat': ['002221', '020221', '022021', '122200', '122020', '002200', '022000', '000220'],
    'major_threat': ['002220', '022200', '020220', '022020', '22220', '02222', '20222', '22022', '22202'],
    'critical_threat': ['022220'],
    'lose_sequence': ['22222']
}


def count_local_stones(board, row, column, radius=3, ai_stone=1, enemy_stone=2):
    ai_count = 0
    enemy_count = 0
    start_row = max(0, row - radius)
    end_row = min(len(board), row + radius + 1)
    start_col = max(0, column - radius)
    end_col = min(len(board[0]), column + radius + 1)

    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if board[r][c] == ai_stone:
                ai_count += 1
            elif board[r][c] == enemy_stone:
                enemy_count += 1

    return ai_count, enemy_count


def calculateFeatures(move_record):
    row, column = move_record['position']  # Directly use the tuple
    player = move_record['player']

    ai_stones, enemy_stones = count_local_stones(move_record['board_state'], row, column)
    move_record['local_ai_stones'] = ai_stones
    move_record['local_enemy_stones'] = enemy_stones

    # Initialize feature counts for the move_record
    for feature in ai_patterns.keys():
        move_record[feature] = 0
    for feature in enemy_patterns.keys():
        move_record[feature] = 0

    # Adding overall opportunities and threats
    move_record['total_opportunities'] = 0
    move_record['total_threats'] = 0
        
    # save all strings from four directions
    situations = []
    # Evaluate 4 moves from each 8 directions
    directions = ['west', 'north', 'northwest', 'northeast']
    situations.extend(calculateDir(row, column, direction, 4, False, move_record['board_state']) for direction in directions)
    situations.extend(calculateDir(row, column, direction, 4, True, move_record['board_state']) for direction in directions)

    # Process each situation and update feature counts
    for situation in situations:
        for feature, patterns in ai_patterns.items():
            if any(s in situation for s in patterns):
                move_record[feature] += 1
                move_record['total_opportunities'] += 1

        for feature, patterns in enemy_patterns.items():
            if any(s in situation for s in patterns):
                move_record[feature] += 1
                move_record['total_threats'] += 1

    
    # old_keys = ['position_x', 'position_y', 'aggressive_sequence', 'defensive_pressure', 'ai_minor_threat_or_block', 'ai_moderate_threat_or_block', 'ai_major_threat_or_block', 'ai_critical_open', 'ai_win_sequence',
    #         'enemy_minor_threat_or_block', 'enemy_moderate_threat_or_block', 'enemy_major_threat_or_block', 'enemy_critical_open', 'enemy_win_sequence', 'major_opportunity_counter']

    # for key in old_keys:
    #     if key in move_record:
    #         del move_record[key]



def calculateDir(row, column, direction, depth, enemy, board):
    # This function should return the string pattern based on the board and direction
    # This setting assumes that the AI is the black stone
    s = '2' if enemy else '1'  # Set in the middle if it's AI's turn (black stone by default)

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

if __name__ == "__main__":
    manager = GameManager.load_state()
    for game in manager.games:
        for move_record in game.moves:
            calculateFeatures(move_record)

    manager.save_state()
