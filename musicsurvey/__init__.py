from random import randint

def random_name():
    return '%010d' % randint(1, 10**9)
