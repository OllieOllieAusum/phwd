import os
def clean():
    x = os.listdir("dbg")
    for i in x:
        print(i)
        if i != "gitinclude":
            os.remove(f"dbg/{i}")