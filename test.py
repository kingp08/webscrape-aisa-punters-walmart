from contextlib import contextmanager

@contextmanager
def Indenter():
    try:
        new_Indenter = Indenter()
        yield new_Indenter
    finally:
        print("error")

    def print1(str):
        print(str)

with Indenter() as indent:
    indent.print1('hi!')