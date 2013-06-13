from ..common.util import split

commands = {}


def is_op(user_data):
    if not user_data:
        return False

    has_q = 'q' in user_data['modes']
    has_o = 'o' in user_data['modes']

    return has_q or has_o


def validate(name, server, user, args, params):
    if 'chan' in params:
        params['auth'] = True
        params['args'] = params.get('args', 1)

    if 'auth' in params:
        if 'auth' not in user:
            server.send_reply(user, 'ERR_NOTREGISTERED')
            return False

    if 'args' in params:
        num = params['args']
        if not args[num - 1]:
            server.send_reply(user, 'ERR_NEEDMOREPARAMS', name)
            return False

    if 'chan' in params:
        chan_name = args[0]
        chan = args[0] = server.find_chan(chan_name)

        if not chan:
            server.send_reply(user, 'ERR_NOSUCHCHANNEL', chan_name)
            return False

        if not server.user_in_chan(user, chan):
            server.send_reply(user, 'ERR_NOTONCHANNEL', chan_name)
            return False

    return True


def command(f_=None, **kwargs):
    def decorator(f):
        name = f.func_name.split('_')[1].upper()

        def new_func(server, user, *args):
            args = list(args)
            if not validate(name, server, user, args, kwargs):
                return
            return f(server, user, *args)

        arity = f.func_code.co_argcount
        commands[name] = (new_func, arity - 2)

        return new_func
    return decorator(f_) if f_ else decorator


def dispatch(server, user, message):
    cmd, args = split(message, 1)
    cmd = cmd.upper()

    if cmd not in commands:
        server.send_reply(user, 'ERR_UNKNOWNCOMMAND', cmd)
        return

    f, arity = commands[cmd]
    f(server, user, *split(args, arity - 1))


def load_commands():
    import os
    import glob
    import importlib

    modules = glob.glob(os.path.dirname(__file__) + "/irc_*.py")
    for fullpath in modules:
        name = os.path.basename(fullpath)[:-3]
        importlib.import_module('ircd.kernel.' + name)
