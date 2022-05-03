import phwd
x = phwd.getweatherdata("dbg")
dinput = x.usrinput()
print(dinput)
x.getdatafromyear(dinput,2021)