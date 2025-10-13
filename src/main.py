import sys

def testing_func(a):
    return type(a), a

print(testing_func(sys.argv[1]))
