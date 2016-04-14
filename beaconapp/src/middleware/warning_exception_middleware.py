__author__ = 'fuiste'

import traceback
import sys
import warnings


class ProcessExceptionMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 200:
            print '\n'.join(traceback.format_exception(*sys.exc_info()))
        return response


def deprecated(func):
    """This is a decorator which can be used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.
    """
    def new_func(*args, **kwargs):
        warnings.warn("Call to deprecated function {}.".format(func.__name__), category=DeprecationWarning)
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func