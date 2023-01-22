from mdparser import Mdparser
with open("README.md","r") as f:
    test=f.read()

a = Mdparser(test)
print(repr(a))
print(a)
