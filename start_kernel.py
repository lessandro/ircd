import logging
import config
from kernel import kernel

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    kernel.start(config)
