from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from time import strftime
from formats import Container
from collections import deque


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
            foreground='#909294'
        ),
        time=Container(
            foreground='#93c763'
        ),
        event=Container(
            foreground='#ADD8E6'
        ),
    )
)


class Logger(Frame):

    ERROR, BORRING, EVENT, NORMAL = "error", "borring", "event", None

    def __init__(self, *args, **kw):
        Frame.__init__(self, *args, **kw)

        self.deque = deque()

        self.txt = ScrolledText(self, wrap=WORD, state=DISABLED, relief=SUNKEN, height=25)
        self.txt.grid(column=0, row=0, sticky=(N, W, E, S))
        self.txt.configure(LoggerColors.default)
        for k, v in LoggerColors.tags.items():
            self.txt.tag_configure(k, v)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.after(100, self._toscreen)

    def __call__(self, *args):
        self.deque.appendleft(args)

    def _toscreen(self):
        if len(self.deque):
            self.txt["state"] = NORMAL
            while(len(self.deque)):
                self.txt.insert(
                    END,
                    "\n[{}] ".format(strftime("%H:%M:%S")),
                    "time",
                    *self.deque.pop())
            self.txt.yview(END)
            self.txt["state"] = DISABLED
        self.after(100, self._toscreen)

if __name__ == "__main__":
    root = Tk()

    HorizontalButtons(root, buttons=(
        ("one", lambda: print("one")),
        ("two", lambda: print("two")),
        ("three", lambda: print("three")))
    ).grid(column=0, row=0, sticky=(N, W, E, S))

    log = Logger(root)
    log.grid(column=0, row=1, sticky=(W, E, S))

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    #root.rowconfigure(1, weight=0)
    log("normal")
    log("borring", Logger.BORRING)
    log("error", Logger.ERROR)
    log("event", Logger.EVENT)
    root.mainloop()
