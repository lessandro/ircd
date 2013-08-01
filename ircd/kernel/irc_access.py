from command import command, is_op, is_owner
from ..common.util import decolon
import time
import fnmatch

levels = {
    '': (0, ''),
    'DENY': (1, 'b'),
    'GRANT': (2, ''),
    'VOICE': (3, 'v'),
    'HOST': (4, 'o'),
    'OWNER': (5, 'q')
}


@command(chan=True)
def cmd_access(server, user, chan, action, level, mask, timeout, reason):
    user_data = server.chan_nick(chan, user['nick'])
    if not is_op(user_data):
        server.send_reply(user, 'ERR_CHANOPRIVSNEEDED', chan['name'])
        return

    action = action.upper()
    level = level.upper()

    if level not in levels:
        server.send_reply(user, 'ERR_BADLEVEL', 'ACCESS')
        return

    is_owner_ = is_owner(user_data)

    if action in ['ADD', 'DELETE', 'CLEAR']:
        if level == 'OWNER' and not is_owner_:
            server.send_reply(user, 'ERR_NOACCESS', 'ACCESS')
            return

    if action == 'ADD':
        if not mask:
            server.send_reply(user, 'ERR_NEEDMOREPARAMS', 'ACCESS')
            return

        if server.access_list_count(chan) >= server.config.max_acl_entries:
            server.send_reply(user, 'ERR_TOOMANYACCESSES')
            return

        mask = parse_mask(mask)
        timeout = parse_timeout(timeout)
        reason = decolon(reason)
        server.access_list_add(chan, level, mask, timeout, user, reason)
        timeout = timeout_minutes(timeout)

        server.send_reply(user, 'RPL_ACCESSADD', chan['name'], level, mask,
                          timeout, user['id'], reason)

    elif action == 'DELETE':
        mask = parse_mask(mask)
        server.access_list_del(chan, level, mask)

        server.send_reply(user, 'RPL_ACCESSDELETE', chan['name'], level, mask)

    elif action == 'CLEAR':
        for level_, mask, _, _, _ in get_access_list(server, chan):
            if level and level != level_:
                continue
            if level_ == 'OWNER' and not is_owner_:
                continue

            server.access_list_del(chan, level_, mask)

        server.send_reply(user, 'RPL_ACCESSCLEAR', chan['name'], level)

    elif action == 'LIST':
        server.send_reply(user, 'RPL_ACCESSSTART', chan['name'])

        acl = get_access_list(server, chan)
        for level_, mask, timeout, userid, reason in acl:
            if level and level != level_:
                continue

            timeout = timeout_minutes(timeout)

            server.send_reply(user, 'RPL_ACCESSLIST', chan['name'], level_,
                              mask, timeout, userid, reason)

        server.send_reply(user, 'RPL_ACCESSEND', chan['name'])

    else:
        server.send_reply(user, 'ERR_BADCOMMAND', 'ACCESS')
        return


def parse_mask(mask):
    part_syms = {'!': 1, '@': 2, '$': 3}
    parts = ['', '', '', '']
    cur = 0

    for c in mask:
        if c in part_syms:
            cur = part_syms[c]
            parts[cur] = ''
        else:
            parts[cur] += c

    parts = [part or '*' for part in parts]
    return '{0}!{1}@{2}'.format(*parts)


def parse_timeout(timeout):
    try:
        minutes = int(timeout)
        return int(minutes * 60 + time.time())
    except:
        return 0


def timeout_minutes(timeout):
    if timeout > 0:
        return int((timeout - time.time()) / 60)
    return timeout


def get_access_list(server, chan):
    now = time.time()
    for entry in server.access_list_all(chan):
        level, mask, timeout, _, _ = entry
        if timeout > 0 and timeout < now:
            server.access_list_del(chan, level, mask)
        else:
            yield entry


def check_user_access(server, chan, user):
    acl = get_access_list(server, chan)
    best_level = levels['']

    for level, mask, _, _, _ in acl:
        if fnmatch.fnmatch(user['id'], mask):
            if levels[level] > best_level:
                best_level = levels[level]

    return best_level[1]
