import os

config_path = os.path.normpath(os.path.dirname(__file__))

# ircd config

server_name = 'lessandro.com'

# socket server

tcp_port = 5556

# socket.io server

socketio_port = 8001

flash_policy_port = 10843
flash_policy_file = os.path.join(config_path, 'policy.xml')
