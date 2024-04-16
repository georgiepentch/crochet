from urllib.request import Request, urlopen
import os
from sys import argv


def hl(s): return f"\033[48;5;15m\033[38;5;0m{s}\033[0m"
def red(s): return f"\033[38;5;9m{s}\033[0m"


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


'''
STANDARD PATTERN FORMATTING:
    Comma/newline-separated string of instructions
'''


stitch_count = {
    'inc': 2,
    'dec': 1,
    'sc': 1,
    'dec2': 1,
    'inc2': 3
}


def view(pattern=None, max_size=5):
    if pattern is None:
        pattern = input("Enter a pattern:\n")
    array = [[i.strip() for i in row.split(',')] for row in pattern.split('\n')]
    current_row = 0
    current_item = 0
    while True:
        cls()
        for row_ind in range(len(array)):
            instructions = list(array[row_ind])
            total = 0
            for i in instructions:
                if i in stitch_count.keys():
                    total += stitch_count.get(i)
                elif i.isnumeric():
                    total += int(i)
            if row_ind == current_row:
                instructions[current_item] = hl(instructions[current_item])
            print(f"{str(row_ind + 1)} ({red(total)}):  " + ', '.join(instructions))
        cmd = input()
        if (current_row == len(array) - 1 and current_item == len(array[current_row]) - 1) or cmd == 'stop':
            break
        elif cmd == 'back':
            if current_item == 0:
                current_row -= 1
                current_item = len(array[current_row]) - 1
            else:
                current_item -= 1
        elif current_item == len(array[current_row]) - 1:
            current_item = 0
            current_row += 1
        else:
            current_item += 1


def sphere(n):
    req = Request("https://avtanski.net/projects/crochet/cgi-bin/sphere.cgi?cir=" + str(n))
    req.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, '
                                 'like Gecko) Chrome/103.0.0.0 Safari/537.36')
    raw = str(urlopen(req).read()).split("pre>")[1:][0]
    raw = [i.split(':')[1] for i in raw.split('\\n')[2:-2]]
    initial = raw[0].count(',') + 1
    return str(initial) + '\n' + '\n'.join(raw)


# RUNNING SPHERE FOR NOW
view(sphere(int(argv[1])))
