import os
x = os.listdir("dbg")
for i in x:
    os.remove(f"dbg/{i}")