from functools import wraps
import logging

def library_logger(original_function):
    """
    Decorator. Records the original function in the log.

    :Usage:
        @library_logger
        def check_equal(a,b)
    :Returns:
        NA
    """
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(original_function.__module__) 
        logger.info(
            'method: {} args: {}, and kwargs: {}'.format(original_function.__qualname__, args, kwargs))
        return original_function(*args, **kwargs)

    return wrapper
    