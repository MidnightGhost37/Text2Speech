import random, string


def random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))
