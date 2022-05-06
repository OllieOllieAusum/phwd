import phwd
import textbox
box = textbox.box()
phwdm = phwd.getweatherdata("dbg")
box.addtext("Testing getting all data")
box.print()
data = phwdm.getalldata(1087699999)
phwdm.cscreen()
box.addtext(data)
box.print()

