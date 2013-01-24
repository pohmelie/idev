from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from time import strftime


class HorizontalButtons(Frame):
    def __init__(self, *args, **kw):
        buttons = kw.pop("buttons", ())

        Frame.__init__(self, *args, **kw)

        self.rowconfigure(0, weight=1)
        for i, data in enumerate(buttons):
            text, action = data
            btn = Button(self, text=text, command=action)
            btn.grid(column=i, row=0, sticky=(N, W, E, S))
            self.columnconfigure(i, weight=1)


class Logger(Frame):
    def __init__(self, *args, **kw):
        Frame.__init__(self, *args, **kw)

        self.txt = ScrolledText(self, wrap=WORD, state=DISABLED, relief=SUNKEN, height=10)
        self.txt.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)

    def __call__(self, string):
        self.txt["state"] = NORMAL
        self.txt.insert(END, "\n[{}] {}".format(strftime("%H:%M:%S"), string))
        self.txt["state"] = DISABLED

if __name__ == "__main__":
    root = Tk()

    HorizontalButtons(root, buttons=(
        ("one", lambda: print("one")),
        ("two", lambda: print("two")),
        ("three", lambda: print("three")))
    ).grid(column=0, row=0, sticky=(N, W, E, S))

    log = Logger()
    log.grid(column=0, row=1, sticky=(N, W, E, S))

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    log("yoba")
    log("here")
    root.mainloop()
