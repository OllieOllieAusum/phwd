import os
def clean():
    x = os.listdir("dbg")
    for i in x:
        os.remove(f"dbg/{i}")