import sys

def checkpoint(message, args):
    if not args.get("interactive", False):
        return

    answer = input("{}".format(message))
    if answer=="n":
        sys.exit(1)

