import importlib
import phwd
"""
    test file to test the getweatherdata class in the python3 environment.

"""
def test():
    importlib.reload(phwd)
    x = phwd.getweatherdata("dbg")
    print(x.usrinput())