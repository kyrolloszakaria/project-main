# hello xinyu
# from xinyu pc

import inspect

def print_function_name():
    frame = inspect.currentframe()
    try:
        caller_name = inspect.getframeinfo(frame.f_back).function
        print("The name of the calling function is:", caller_name)
    finally:
        del frame  # Make sure to clean up the frame

def foo():
    print_function_name()

foo()