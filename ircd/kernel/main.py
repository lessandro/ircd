import logging
import kernel


def main(config):
    logging.getLogger().setLevel(logging.DEBUG)
    server = kernel.Kernel(config)
    server.loop()
