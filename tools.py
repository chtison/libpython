def pgcd(a, b):
    while a % b != 0:
        a, b = b, a % b
    return b
