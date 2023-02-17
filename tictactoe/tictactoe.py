"""
Tic Tac Toe Player
"""

from copy import deepcopy
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    It is O's turn if number of EMPTY cells is even else X
    """
    return O if sum([row.count(EMPTY) for row in board]) % 2 == 0 else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # check if move is valid
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid move")

    # make move on copy of original board
    new_board = deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check rows and cols in one go by rotating board
    rotated = list(zip(*board[::-1]))
    for row in board + rotated:
        if len(set(row)) == 1 and all(row):
            return row[0]

    # check diagonals
    if len(set(diagonal := [board[i][i] for i in range(3)])) == 1 and all(diagonal):
        return diagonal[0]
    if len(set(diagonal := [board[i][2-i] for i in range(3)])) == 1 and all(diagonal):
        return diagonal[0]

    # game is a tie or still in progress
    return None


def terminal(board):
    """
    Returns True if game is over (someone won or all cells are filled), False otherwise.
    """
    return True if winner(board) or not actions(board) else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    victor = winner(board)
    return 1 if victor == X else -1 if victor == O else 0


def min_value(board):
    # base condition, board has winner or tie
    if terminal(board):
        return utility(board)

    # return the lowest utility, given optimal play by the maximising player
    v = 10
    for move in actions(board):
        v = min(v, max_value(result(board, move)))
    return v


def max_value(board):
    # base condition, board has winner or tie
    if terminal(board):
        return utility(board)

    # return the highest utility, given optimal play by the minimising player
    v = -10
    for move in actions(board):
        v = max(v, min_value(result(board, move)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    Does not yet (!) include alpha-beta pruning.
    """
    if terminal(board):
        return None

    # calculate each move's utility and store them as utility-move pair in dictionary
    moves = dict()
    for move in actions(board):
        if player(board) == X:
            moves[min_value(result(board, move))] = move
        else:
            moves[max_value(result(board, move))] = move

    # return move with highest/lowest utility
    return moves[max(moves)] if player(board) == X else moves[min(moves)]
