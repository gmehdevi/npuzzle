#!/usr/bin/python3
import sys
import argparse
from heuristics import *
import re
import time
from parse_arg import *
from queue import PriorityQueue
from solvable import is_solvable
import numpy as np
from heuristics import *

TRANSITION_COST = 1

def possible_actions(board):
    empty_tile = None
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            if tile == 0:
                empty_tile = (i, j)
                break
        if empty_tile:
            break

    actions = []

    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for move in moves:
        new_i = empty_tile[0] + move[0]
        new_j = empty_tile[1] + move[1]

        if 0 <= new_i < len(board) and 0 <= new_j < len(board[0]):
            new_board = [list(row) for row in board]
            new_board[empty_tile[0]][empty_tile[1]] = board[new_i][new_j]
            new_board[new_i][new_j] = 0
            actions.append(tuple(tuple(row) for row in new_board))

    return actions

def reconstruct_path(closed_set, current):
    total_path = [current]
    while current in closed_set:
        current = closed_set[current]
        total_path.append(current)
    return total_path[::-1]

def a_star_search(start, goal, h):
    open_set = PriorityQueue()
    open_set.put((h(start, goal), start))
    came_from = {}
    g_score = {start: 0}

    while not open_set.empty():
        _, current = open_set.get()

        if current == goal:
            print(f"Space complexity: {open_set.qsize() + len(came_from)}")
            print(f"Time complexity: {len(came_from)}")
            return reconstruct_path(came_from, current)

        for neighbor in possible_actions(current):
            tentative_g_score = g_score[current] + TRANSITION_COST

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + h(neighbor, goal)
                open_set.put((f_score, neighbor))
                came_from[neighbor] = current

    return None

def main():
    file_path, h = parse_args()

    h_dict = {"manhattan": manhattan_distance, "hamming": hamming_distance, "linear_conflict": linear_conflict}

    initial_state = parse_initial_state(file_path)
    print(f"Initial State:");print(initial_state);print()

    goal_state = determine_goal_state(initial_state)
    print("Goal State:");print(goal_state);print()
    
    if not is_solvable(initial_state, goal_state):
        print("The puzzle is not solvable.")
        sys.exit(1)

    initial_state = tuple(tuple(row) for row in initial_state)
    goal_state = tuple(tuple(row) for row in goal_state)

    print(f"Using {h} heuristic.")

    time_start = time.time()
    solution = a_star_search(initial_state, goal_state, h_dict[h])
    time_end = time.time()

    if solution is not None:
        with open("solution.txt", "w") as f:
            print(f"Solution of {file_path}:", file=f)
            for step, state in enumerate(solution):
                print(f"Step {step}:\n{np.array(state)}", file=f)

        print(f"time taken: {((time_end - time_start)):.2f} seconds")
        print(f"Solution of length {len(solution) - 1} saved to solution.txt")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
