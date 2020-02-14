def spread(x):
    if x < 0 or x > 1:
        print(x)
        raise ValueError
    if x <= .5:
        result = x ** (1.5 - x)
    elif .5 < x <= 1:
        result = 1 - (1 - x) ** (.5 + x)
    return result

def narrow(x):
    if x < 0 or x > 1:
        print(x)
        raise ValueError
    if x <= .5:
        result = x ** (.5 + x)
    elif .5 < x <= 1:
        result = 1 - (1 - x) ** (1.5 - x)
    return result
