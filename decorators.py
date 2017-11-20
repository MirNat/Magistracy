import time

def convolve(k):
    assert isinstance(k, (int, long))
    assert k > 0

    def inner_decorator(function):
        def wrapper(argument):
            for x in xrange(k):
                argument = function(argument)
            return argument
        return wrapper
    return inner_decorator

def memorize(f):
    class MemoDict(dict):
        def __init__(self, f):
            self.f = f

        def __call__(self, *args):
            return self[args]

        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret

    return MemoDict(f)

def profile(f):
    def wrapper(*args, **kw):
        start_time = time.time()
        result = f(*args, **kw)
        end_time = time.time()
        print end_time - start_time
        return result

    return wrapper
