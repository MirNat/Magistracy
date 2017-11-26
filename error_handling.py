from contextlib import contextmanager
import sys
import traceback

# lab 6
def error_handling(exc_type, re_raise, log_traceback):
    if log_traceback:
        traceback.print_exc()
    if re_raise:
        raise exc_type

def handle_error(re_raise=True, log_traceback=True, exc_type=Exception):
    def inner_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exc_type as e:
                error_handling(e, re_raise, log_traceback)
        return wrapper
    return inner_decorator

@contextmanager
def handle_error_context(re_raise=True, log_traceback=True, exc_type=Exception):
    try:
        yield
    except exc_type as e:
        error_handling(e, re_raise, log_traceback)