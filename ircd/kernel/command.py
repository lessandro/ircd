commands = {}


def split(s, n):
    """
    Like str.split(), but always return a list with n+1 values
    """
    splitted = s.split(' ', n)
    splitted.extend([''] * (n + 1 - len(splitted)))
    return splitted


def command(f):
    arity = f.func_code.co_argcount
    name = f.func_name.split('_')[1].upper()
    commands[name] = (f, arity - 2)
    return f


def dispatch(server, user, message):
    cmd, args = split(message, 1)
    cmd = cmd.upper()

    if cmd in commands:
        f, arity = commands[cmd]
        f(server, user, *split(args, arity - 1))
    else:
        return cmd


def load_commands():
    import os
    import glob
    import importlib

    modules = glob.glob(os.path.dirname(__file__) + "/irc_*.py")
    for fullpath in modules:
        name = os.path.basename(fullpath)[:-3]
        importlib.import_module('ircd.kernel.' + name)
