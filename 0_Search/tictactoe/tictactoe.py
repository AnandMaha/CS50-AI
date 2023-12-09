"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math

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
    """
    cnt = 0 # cnt = 0, X turn (X goes first so default 0), cnt = -1, O turn
    for r in board:
        for s in r:
            if s == O:
                cnt += 1
            elif s == X:
                cnt -= 1
    if cnt == 0:
        return X
    return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    ans = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                ans.add((i,j))
    return ans


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] is not EMPTY:
        raise Exception("Action not possible!")
    else: # the space is EMPTY
        move = player(board)
        boardNew = deepcopy(board)
        boardNew[i][j] = move
        return boardNew


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def allSame(list):
        return all(i == list[0] for i in list)
    # vertical
    for row in board:
        if allSame(row):
            return row[0]

    # horizontal
    for j in range(3):
        col = [board[i][j] for i in range(3)]
        if allSame(col):
            return col[0]
    
    # diagonal
    diag1 = [board[i][i] for i in range(0, 3)]
    diag2 = [board[i][~i] for i in range(0, 3)]
    if allSame(diag1):
        return diag1[0]
    elif allSame(diag2):
        return diag2[0]
    
    return None # no winner
                  

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # no actions remain or there's a winner
    return len(actions(board)) == 0 or winner(board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    playWin = winner(board)
    if playWin == X:
        return 1
    elif playWin == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def maxValue(board):
        bestMove = ()
        if terminal(board):
            return bestMove, utility(board)
        else:
            score = float('-inf')
            for action in actions(board):
                minVal = minValue(result(board, action))[1]
                if minVal > score:
                    bestMove = action
                    score = minVal
            return bestMove, score 

    def minValue(board):
        bestMove = ()
        if terminal(board):
            return bestMove, utility(board)
        else:
            score = float('inf')
            for action in actions(board):
                maxVal = maxValue(result(board, action))[1]
                if maxVal < score:
                    bestMove = action
                    score = maxVal
            return bestMove, score

    move = player(board)
    if terminal(board):
        return None
    if move == X:
        return maxValue(board)[0]
    else:
        return minValue(board)[0]
