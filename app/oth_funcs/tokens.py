import random

def get_rnd_hex():
    return random.choice('0123456789abcdef')

def get_token(leng=20):
    s = ''
    for c in range(leng):
        s += get_rnd_hex()

    return s
