def split(s, n):
    """
    Like str.split(), but always return a list with n+1 values
    """
    splitted = s.split(' ', n)
    splitted.extend([''] * (n + 1 - len(splitted)))
    return splitted
