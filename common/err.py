from functools import wraps


def error_handler(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as error:
            print(f'Error: {error}')
    return wrapper

# TODO: add error logging
