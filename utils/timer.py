from typing import Callable


def with_timer(fn: Callable) -> Callable:
    import time

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = fn(*args, **kwargs)
        end_time = time.time()
        print(f"Function {fn.__name__} took {end_time - start_time:.4f} seconds")
        return result

    return wrapper