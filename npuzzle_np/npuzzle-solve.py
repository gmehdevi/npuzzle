#! /usr/bin/python3
import sys
import argparse
from heuristics import *
import numpy as np
import re
import time
from queue import PriorityQueue
from solvable import is_solvable
from collections import deque
from functools import partial

def board_from_bytes(board_bytes, n):
    return np.frombuffer(board_bytes, dtype=np.uint64).reshape((n, n))

def bytes_from_board(board):
    return board.tobytes()

def possible_actions(board):
    empty_tile = np.argwhere(board == 0)[0]
    actions = []

    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for move in moves:
        new_position = empty_tile + move
        if 0 <= new_position[0] < board.shape[0] and 0 <= new_position[1] < board.shape[1]:
            new_board = board.copy()
            new_board[empty_tile[0], empty_tile[1]] = board[new_position[0], new_position[1]]
            new_board[new_position[0], new_position[1]] = 0
            actions.append(new_board)

    return actions

def reconstruct_path(closed_set, current):
    total_path = [current]
    while current in closed_set:
        current = closed_set[current]
        total_path.append(current)
    return total_path[::-1]

def determine_goal_state(initial_state):
    n = initial_state.shape[0]
    goal_state = np.zeros((n, n), dtype=int)
    x = 0
    y = 0
    dx = 1
    dy = 0
    for i in range(1, n * n):
        goal_state[y, x] = i
        if x + dx == n or y + dy == n or x + dx < 0 or goal_state[y + dy, x + dx] != 0:
            dx, dy = -dy, dx
        x += dx
        y += dy
    goal_state[y, x] = 0
    return goal_state

def parse_initial_state(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        sys.exit(1)

    lines = [line.strip() for line in lines if not line.startswith("#") and line.strip()]

    n = int(lines[0])

    board = np.zeros((n, n), dtype=int)
    if len(lines) == n + 1:
        for i in range(n):
            values = re.findall(r'\d+', lines[i + 1])
            for j, value in enumerate(values):
                board[i, j] = int(value)
    elif len(lines) == n * n + 1:
        for i in range(n * n):
            board[i // n, i % n] = int(lines[i + 1])

    else:
        print("Invalid file format.")
        sys.exit(1)

    return board

def ida_star_search(puzzle, solved, h):
    def search(path, g, bound):
        node = path[-1]
        f = g + h(node, solved)
        if f > bound:
            return f, None
        if np.array_equal(node, solved):
            return True, path
        ret = float("inf")
        moves = possible_actions(node)
        for m in moves:
            if not any(np.array_equal(m, p) for p in path):
                path.append(m)
                t, solution = search(path, g + 1, bound)
                if t is True:
                    return True, solution
                if t < ret:
                    ret = t
                path.pop()
        return ret, None

    bound = h(puzzle, solved)
    path = [puzzle]
    while True:
        t, _ = search(path, 0, bound)
        if t is True:
            path.reverse()
            return path
        elif t == float("inf"):
            return None
        else:
            bound = t

        
def a_star_search(start, goal, h):
    open_set = PriorityQueue()
    start_bytes = bytes_from_board(start)
    open_set.put((h(start, goal), start_bytes))
    came_from = {}
    g_score = {start_bytes: 0}
    max_state = 0

    while not open_set.empty():
        _, current_bytes = open_set.get()
        current = board_from_bytes(current_bytes, goal.shape[0])

        if np.array_equal(current, goal):
            to_map = partial(board_from_bytes, n=goal.shape[0])
            print(f"\nMax state: {max_state}")
            return map(to_map, reconstruct_path(came_from, current_bytes))

        for neighbor in possible_actions(current):
            neighbor_bytes = bytes_from_board(neighbor)
            tentative_g_score = g_score[current_bytes] + 1

            if neighbor_bytes not in g_score or tentative_g_score < g_score[neighbor_bytes]:
                g_score[neighbor_bytes] = tentative_g_score
                f_score = tentative_g_score + h(neighbor, goal)
                open_set.put((f_score, neighbor_bytes))
                came_from[neighbor_bytes] = current_bytes

        max_state = max(max_state, open_set.qsize())

    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python npuzzle_parser.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    initial_state = parse_initial_state(file_path)
    
    print("Initial State:")
    print(initial_state)
    
        
    goal_state = determine_goal_state(initial_state)
    print("\nGoal State:")
    print(goal_state)
    
    if not is_solvable(initial_state, goal_state):
        print("The puzzle is not solvable.")
        sys.exit(1)
    
    heuristic_function = manhattan_distance
    
    time_start = time.time()
    solution = a_star_search(initial_state, goal_state, heuristic_function)
    time_end = time.time()
    
    if solution is not None:
        for step, state in enumerate(solution):
            print(f"Step {step}:\n{(state)}\n")
        print(f"time taken: {((time_end - time_start)):.2f} seconds")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
