import phwd
import cleanup as c

phwdm = phwd.getweatherdata("dbg")
print("Testing getting all data")
data = phwdm.getalldata(72551594947, supressoutput=True)
phwdm.cscreen()
print("Sucess")
c.clean()
print("cleaned all downloaded data")
print("Testing getting data from range")
data = phwdm.getdatafromrange(72551594947, 2017, 2020)
phwdm.cscreen()
print("Sucess")
c.clean()
print("Getting data from year")
data = phwdm.getdatafromyear(72551594947, 2020)
phwdm.cscreen()
print("Sucess")
c.clean()



