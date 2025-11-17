import sys
import functools
import logging

def logger(func=None, *, handle=sys.stdout):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            is_logging = isinstance(handle, logging.Logger)

            #Старт вызова
            start_msg = f"INFO: calling {fn.__name__} args={args} kwargs={kwargs}\n"
            if is_logging:
                handle.info(start_msg)
            else:
                handle.write(start_msg)

            try:
                result = fn(*args, **kwargs)

                #Успешное окончание
                end_msg = f"INFO: finished {fn.__name__} result={result}\n"
                if is_logging:
                    handle.info(end_msg)
                else:
                    handle.write(end_msg)

                return result

            except Exception as e:
                #Ошибка
                err_msg = f"ERROR: {type(e).__name__}: {str(e)}\n"
                if is_logging:
                    handle.error(err_msg)
                else:
                    handle.write(err_msg)

                raise e

        return wrapper

    #Если декоратор без параметров
    if func is not None:
        return decorator(func)

    return decorator