from time import time

def timeit(method):
    """decorator for timing processes"""
    def timed(*args, **kwargs):
        ts = time()
        result = method(*args, **kwargs)
        te = time()
        print("Process took " + str(round(te-ts,2)) + " seconds")
        return result
    return timed
