import sys

def testing_func(a):
    return type(a), a

testing_func(sys.argv[1])