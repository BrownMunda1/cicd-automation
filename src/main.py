import sys

def testing_func(a):
    print("Enter here")
    return type(a), a

print(testing_func(sys.argv[1]))