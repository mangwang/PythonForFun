#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Define a Unix-like tail command.

Usage: python tail.py [OPTION] <FILE>
Print the last 10 lines of each FILE to standard output.
With more than one FILE, precede each with a header giving the file name.

Mandatory arguments to long options are mandatory for short options too.
-h, --help    display this help and exit
-n, --lines=K    output the last K lines, instead of the last 10;
                or use -n +K to output starting with the Kth line

-----------------------------------
Created on Mon Jan 25
@author: mangwang
-----------------------------------
"""

from __future__ import print_function

import sys
import getopt


# define a Usage() exception which can catch in an except clause at the end of main()
class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=sys.argv):
    # parse command line options
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hn:", ["help", "lines="])
        except getopt.error as msg:
            raise Usage(msg)
    except Usage, err:
        print(err, file=sys.stderr)
        print("for help use --help", file=sys.stderr)
        return 2
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print(__doc__)
            return 0
        elif o in ("-n", "--lines"):
            if a.startswith("+"):
                try:
                    fromLine = int(a[1:])
                except ValueError as msg:
                    print(msg, file=sys.stderr)
                    return 2
                else:
                    if len(args) == 1:
                        # input one file
                        fileName = args[0]
                        tail(fileName, fromLine=fromLine)
                    else:
                        # input more than one files
                        for arg in args:
                            fileName = arg
                            print("==> " + fileName + " <==")
                            tail(fileName, fromLine=fromLine)
                            print()
            else:
                try:
                    showLines = int(a)
                except ValueError as msg:
                    print(msg, file=sys.stderr)
                    return 2
                else:
                    if len(args) == 1:
                        # input one file
                        fileName = args[0]
                        tail(fileName, showLines=showLines)
                    else:
                        # input more than one files
                        for arg in args:
                            fileName = arg
                            print("==> " + fileName + " <==")
                            tail(fileName, showLines=showLines)
                            print()
    # if no options
    if len(opts) == 0:
        if len(args) == 1:
            # input one file
            fileName = args[0]
            tail(fileName)
        else:
            # input more than one files
            for arg in args:
                fileName = arg
                print("==> " + fileName + " <==")
                tail(fileName)
                print()

def tail(fileName, showLines=10, fromLine=None):
    try:
        with open(fileName) as fp:
            # count lines in this file
            nLines = 0;
            while fp.readline():
                nLines += 1
            if fromLine is not None:
                fp = open(fileName)
                counter = 0;
                for line in fp:
                    counter += 1
                    if counter >= fromLine:
                        print(line, end='')
            else:
                fp = open(fileName)
                counter = 0;
                for line in fp:
                    counter += 1
                    if counter > nLines - showLines:
                        print(line, end='')
    except IOError, msg:
        print(msg, file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    sys.exit(main())