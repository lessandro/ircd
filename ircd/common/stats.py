from socket import socket, AF_INET, SOCK_DGRAM
import time
import resource
import gc


statsd_addr = ("127.0.0.1", 8125)
udp_sock = socket(AF_INET, SOCK_DGRAM)


def send(data):
    udp_sock.sendto(data, statsd_addr)


def gauge(name, n):
    send('%s:%d|g\n' % (name, n))


def count(name):
    send('%s:1|c\n' % name)


def timing(f):
    def new_f(*args, **kwargs):
        t0 = time.time()
        result = f(*args, **kwargs)
        t1 = time.time()
        ms = (t1 - t0) * 1000
        send('%s:%f|ms\n' % (f.func_name, ms))
        return result
    return new_f


def stats(name):
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    mem_kb = float(mem) / 1024
    gauge(name + '-mem', mem_kb)
    gauge(name + '-gc', sum(gc.get_count()))
