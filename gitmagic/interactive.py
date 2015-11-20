# Copyright (c) 2015 BalaBit
# All rights reserved.

import sys

def checkpoint(message, args):
    if not args.get("interactive", False):
        return

    answer = input("{}".format(message))
    if answer=="n":
        sys.exit(1)

