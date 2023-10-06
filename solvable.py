import numpy as np

def get_taxicab_distance(board, solved):
    pi = np.argwhere(board == 0)[0]
    qi = np.argwhere(solved == 0)[0]
    return abs(pi[0] - qi[0]) + abs(pi[1] - qi[1])

def count_inversions(board, solved):
    size = board.size
    flat_board = board.flatten()
    flat_solved = solved.flatten()
    res = 0
    for i in range(size - 1):
        for j in range(i + 1, size):
            vi = flat_board[i]
            vj = flat_board[j]
            if np.where(flat_solved == vi)[0][0] > np.where(flat_solved == vj)[0][0]:
                res += 1
    return res

def is_solvable(board, solved):
    taxicab_distance = get_taxicab_distance(board, solved)
    num_inversions = count_inversions(board, solved)
    return (taxicab_distance % 2 == 0) == (num_inversions % 2 == 0)  
