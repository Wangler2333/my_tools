#!/usr/bin/python

import sys, os


def tokenize(stream):
    x = ""
    level = 0
    for i in stream:
        if i == "{":
            if level == 0:
                yield x
                x = ""
            level += 1
            x += i
        elif i == "}":
            x += i
            level -= 1
            if level == 0:
                yield x
                x = ""
        else:
            x += i


def main():
    for i in tokenize(sys.stdin.read()):
        print i


if __name__ == "__main__":
    main()



