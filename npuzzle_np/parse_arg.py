import sys
import re
import numpy as np

def parse_initial_state(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        sys.exit(1)

    lines = [line.strip() for   line in lines if not line.startswith("#") and line.strip()]

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