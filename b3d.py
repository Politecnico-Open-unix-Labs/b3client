#!/usr/bin/env python3
from sys import argv


def print_help():
    print("")


def start():
    pass


def stop():
    pass


def main():
    if len(argv) != 2:
        print_help()
    else:
        if argv[1] == "start":
            start()
        elif argv[1] == "stop":
            stop()
        elif argv[1] == "reload":
            start()
        else:
            print_help()
