DEBUG = False


def dprint(*args):
    if not DEBUG:
        return
    print(*args)
