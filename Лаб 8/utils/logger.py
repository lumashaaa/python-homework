import sys
import functools
import logging


def logger(func=None, *, handle=sys.stdout):
    """декоратор для логирования вызовов функций."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            is_logging = isinstance(handle, logging.Logger)

            start_msg = f"INFO: calling {fn.__name__} args={args} kwargs={kwargs}\n"
            if is_logging:
                handle.info(start_msg.rstrip())
            else:
                handle.write(start_msg)
                handle.flush()

            try:
                result = fn(*args, **kwargs)

                end_msg = f"INFO: finished {fn.__name__} result={result}\n"
                if is_logging:
                    handle.info(end_msg.rstrip())
                else:
                    handle.write(end_msg)
                    handle.flush()

                return result

            except Exception as e:
                err_msg = f"ERROR: {type(e).__name__}: {e}\n"
                if is_logging:
                    handle.error(err_msg.rstrip())
                else:
                    handle.write(err_msg)
                    handle.flush()
                raise

        return wrapper

    return decorator if func is None else decorator(func)