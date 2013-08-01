import os

config_path = os.path.normpath(os.path.dirname(__file__))

# ircd config

server_name = 'lessandro.com'
ping_timeout = 999999999

hmac_key = 'secret'

max_acl_entries = 300

# socket server

tcp_port = 5556

# sockjs server

sockjs_port = 8002

# redis

redis_db = 7
