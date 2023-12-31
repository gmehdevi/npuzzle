import numpy as np

def manhattan_distance(board, goal_board) -> int:
    n = len(board)
    goal_positions = {}
    total_distance = 0

    for i in range(n):
        for j in range(n):
            tile_value = goal_board[i][j]
            if tile_value != 0:
                goal_positions[tile_value] = (i, j)

    for i in range(n):
        for j in range(n):
            if board[i][j] != 0:
                tile_value = board[i][j]
                goal_position = goal_positions[tile_value]
                distance = abs(i - goal_position[0]) + abs(j - goal_position[1])
                total_distance += distance

    return total_distance


def hamming_distance(board, goal_board) -> int:
    misplaced = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != goal_board[i][j]:
                misplaced += 1
    return misplaced


def linear_conflict(board, goal_board) -> int:
    manhattan = manhattan_distance(board, goal_board)
    n = len(board)
    conflict_count = 0

    for i in range(n):
        for j in range(n):
            if board[i][j] != 0:
                tile_value = board[i][j]
                goal_position = np.argwhere(goal_board == tile_value)[0]

                if goal_position[0] == i:
                    for k in range(j + 1, n):
                        if board[i][k] != 0 and goal_board[i][k] != 0 and board[i][k] < tile_value:
                            conflict_count += 1

                if goal_position[1] == j:
                    for k in range(i + 1, n):
                        if board[k][j] != 0 and goal_board[k][j] != 0 and board[k][j] < tile_value:
                            conflict_count += 1

    return manhattan + (2 * conflict_count)
