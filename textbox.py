import os

SINGLEDRAWERS = ["┌", "┐", "└", "┘", "│", "─", "─"]
DOUBLEDRAWERS = ["╔", "╗", "╚", "╝", "║", "═", "═"]
BLOCKDRAWERS = ["█", "█", "█", "█", "█", "█", "█"]
THINDRAWERS = ["▄", "▄", "▀", "▀", "█", "▀", "▄"]
OUTWARDTHINDRAWERS = ["█", "█", "█", "█", "█", "▄", "▀"]
defaultdrawers = DOUBLEDRAWERS


class box:
    def __init__(s, margin=2, full=False, justify="left", drawers=[]):
        s.drawers = drawers
        if len(drawers) == 0:
            s.drawers = defaultdrawers
        s.lines = []
        s.boxlines = []
        s.isfull = full
        s.boxsize = 1
        s.longestline = 0
        s.termsize = [os.get_terminal_size().columns, os.get_terminal_size().lines]
        s.margin = margin

    def addtext(s, text):
        if len(text) > s.longestline and len(text) <= s.termsize[0] - s.margin * 2:
            s.longestline = len(text)
            s.boxsize = len(text)
        if len(text) > s.termsize[0] - s.margin * 2:
            s.wordwrap(text)
            s.longestline = s.termsize[0] - s.margin * 2
            s.boxsize = s.termsize[0] - s.margin * 2
        else:
            s.lines.append(text)

    def wordwrap(s, text):
        if len(text) > s.termsize[0] - 2 * s.margin:
            x = text.split(" ")
            length = len(x)
            y = [len(pars) for pars in x]
            tb = ""
            linelen = 0
            for i in range(len(y)):
                if y[i] + linelen > s.termsize[0] - 2 * s.margin:
                    length = 0

            if length > 1:
                for i in range(len(x)):
                    if linelen + y[i] >= s.termsize[0] - (2 * s.margin):
                        s.lines.append(tb)
                        tb = ""
                        linelen = 0
                    linelen += y[i] + 1
                    tb += str(f"{x[i]} ")
                s.lines.append(tb)
            else:
                x = list(text)
                y = [len(pars) for pars in x]
                for i in range(len(x)):
                    if linelen + y[i] >= s.termsize[0] - (2 * s.margin):
                        s.lines.append(tb)
                        tb = ""
                        linelen = 0
                    linelen += y[i]
                    tb += str(f"{x[i]}")
                s.lines.append(tb)

    def gen(s):
        if s.isfull:
            s.boxsize = s.termsize[0] - s.margin * 2
        s.boxlines = []
        topboarder = s.drawers[0]
        for i in range(s.boxsize):
            topboarder += s.drawers[6]
        topboarder += s.drawers[1]
        s.boxlines.append(topboarder)
        for i in range(len(s.lines)):
            line = s.drawers[4] + str(s.lines[i])
            while len(line) <= s.boxsize:
                line += " "
            line += s.drawers[4]
            s.boxlines.append(line)
        bottomboarder = s.drawers[2]
        for i in range(s.boxsize):
            bottomboarder += s.drawers[5]
        bottomboarder += s.drawers[3]
        s.boxlines.append(bottomboarder)

    def print(s):
        s.gen()
        for i in range(len(s.boxlines)):
            print(s.boxlines[i])
