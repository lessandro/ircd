import time


class Timer(object):
    def __enter__(self):
        self.__start = time.time()

    def __exit__(self, type, value, traceback):
        self.__finish = time.time()

    def duration(self):
        return self.__finish - self.__start

timer = Timer()
