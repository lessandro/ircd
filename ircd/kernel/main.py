import signal
import logging
import kernel


def main(config):
    logging.getLogger().setLevel(logging.DEBUG)
    server = kernel.Kernel(config)

    def sig_handler(sig, frame):
        server.stop()

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    server.loop()
