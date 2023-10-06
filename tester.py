#!/usr/bin/env python3
#run npuzzle-solve.py with different options and check the output
import sys
import subprocess
from subprocess import PIPE
from pathlib import Path

def all_files(dir_path):
    return [str(p) for p in Path(dir_path).iterdir() if p.is_file()]

def main():

    choices = ["hamming", "manhattan", "linear_conflict"]
    cmd =  ['./npuzzle-solve.py']
    files = all_files('./tests')
    solveable = [f for f in files if 'unsolvable' not in f]
    unsolveable = [f for f in files if 'unsolvable' in f]
    
    # print(f"Running {' '.join(cmd)}")
    # p = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    # stdout, stderr = p.communicate()
    # print(stdout.decode('utf-8'))
    # print(stderr.decode('utf-8'))
    
    for f in unsolveable:
        print(f"Running {' '.join(cmd)} {f}")
        p = subprocess.Popen(cmd + [f], stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        print(stdout.decode('utf-8'))
        print(stderr.decode('utf-8'))
        print('------------------')
        input('Press enter to continue...')
    
    for f in solveable:
        for c in choices:
            print(f"Running {' '.join(cmd)} -m {c} {f}\n")
            p = subprocess.Popen(cmd + ['-m',c, f], stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
            print(stdout.decode('utf-8'))
            print(stderr.decode('utf-8'))
            print('------------------')
            input('Press enter to continue...')


if __name__ == '__main__':
    main()