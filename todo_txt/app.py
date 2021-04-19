import sys


def run():
    for i in range(len(sys.argv)):
        print(f'argv[{i}] = "{sys.argv[i]}"')
    print("That's all folks!")
