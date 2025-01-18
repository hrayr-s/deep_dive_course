import time


def execution_time(func):
    def wrapper(*args, **kwargs):
        start = None
        if kwargs.pop('time', True):
            start = time.time()
        result = func(*args, **kwargs)
        if start is not None:
            print('Execution time:', time.time() - start, 's')
        return result

    return wrapper
