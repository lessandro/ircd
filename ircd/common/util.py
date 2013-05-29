def split(s, n):
    """
    Like str.split(), but always return a list with n+1 values
    """
    splitted = s.split(' ', n)
    splitted.extend([''] * (n + 1 - len(splitted)))
    return splitted


def colon(s):
    """
    Prefix strings with :
    """
    return s if s[0:1] == ':' else ':' + s


def decolon(s):
    """
    Remove an optional : prefix
    """
    return s[1:] if s[0:1] == ':' else s
