#!/usr/bin/env python
from numbers import Integral

class Curry(type):
    """Metaclass that allows a function to support currying by dynamically creating new
    Curried class objects which can be called with the function's arguments to curry it
    through object instances that operate perfectly independently, essentially becoming
    a curried function factory.
    """
    def __new__(cls, func, minargs=None, unique=True):
        if minargs is not None:
            if not isinstance(minargs, Integral):
                raise TypeError('minargs must be an integer')
            elif minargs < 0:
                raise ValueError('minargs must not be negative')
        curried = type(f'_Curried_{id(func)}', (object,), {
            '__doc__': (
                f'Proxy object that stores an argument tuple and dictionary for'
                f'the curried function {func.__name__}.'
                ),
            '__slots__': ('_args', '_kwargs'),
            '__init__': cls.__init,
            '__call__': cls.__call,
            '__getattr__': cls.__get,
            '_func': staticmethod(func), '_minargs': minargs, '_unique': unique,
            })
        return curried

    def __init(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def __get(self, name):
        if name == 'func':
            return self._func
        elif name == 'args':
            return self._args
        elif name == 'kwargs':
            return self._kwargs.copy()

    def __call(self, *args, **kwargs):
        """If called with no arguments, attempts to call the curried function using the
        currently stored set of arguments. Otherwise, it will add the arguments provided
        to the argument list and return another instance with the total argument list
        stored. If minargs has been defined and the total argument count now exceeds its
        minimum, attempt to call the function with the total argument list.
        """
        if args or kwargs:
            newargs = self._args + args
            if self._unique and not self._kwargs.keys().isdisjoint(kwargs):
                raise TypeError('keyword argument collision on curried function')
            newkwargs = {**self._kwargs, **kwargs}
            if (self._minargs is not None
                and self._minargs <= len(newargs) + len(newkwargs)
                ):
                return self._func(*newargs, **newkwargs)
            return type(self)(*newargs, **newkwargs)
        return self._func(*self._args, **self._kwargs)

if __name__ == '__main__':
    # Run unit tests here
    pass
