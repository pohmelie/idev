from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from time import strftime
from formats import Container


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


LoggerColors = Container(
    default=Container(
        selectbackground='#505254',
        bg='#293134',
        fg='#E0E2E4',
        font=('courier new', 12)
    ),
    tags=Container(
        error=Container(
            foreground='#ff7f7f'
        ),
        borring=Container(
            foreground='#909294'  # blue -> '#ADD8E6'
        ),
        time=Container(
            foreground='#93c763'
        )
    )
)


class Logger(Frame):

    ERROR, BORRING, NORMAL = "error", "borring", None

    def __init__(self, *args, **kw):
        Frame.__init__(self, *args, **kw)

        self.txt = ScrolledText(self, wrap=WORD, state=DISABLED, relief=SUNKEN, height=25)
        self.txt.grid(column=0, row=0, sticky=(N, W, E, S))
        self.txt.configure(LoggerColors.default)
        for k, v in LoggerColors.tags.items():
            self.txt.tag_configure(k, v)

        self.columnconfigure(0, weight=1)

    def __call__(self, obj, tag=None):
        self.txt["state"] = NORMAL
        self.txt.insert(END, "\n[{}] ".format(strftime("%H:%M:%S")), "time", obj, tag)
        self.txt.yview(END)
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
    log("normal")
    log("borring", Logger.BORRING)
    log("error", Logger.ERROR)
    root.mainloop()
