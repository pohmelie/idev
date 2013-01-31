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
        text_height = kw.pop("text_height", 25)

        Frame.__init__(self, *args, **kw)

        self.deque = deque()

        self.txt = ScrolledText(self, wrap=WORD, state=DISABLED, relief=SUNKEN, height=text_height)
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


class Table(Frame):
    def __init__(self, *args, **kw):
        columns = kw.pop("columns", ())
        callback = kw.pop("callback", lambda: None)

        Frame.__init__(self, *args, **kw)

        self.tree = Treeview(
            self,
            columns=tuple(map(lambda x: x[0], columns[1:])),
            selectmode="browse"
        )

        self.tree.bind("<<TreeviewSelect>>", lambda _: callback())

        self.scrollY = Scrollbar(self, orient=VERTICAL, command=self.tree.yview)
        self.scrollX = Scrollbar(self, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(
            yscrollcommand=self.scrollY.set,
            xscrollcommand=self.scrollX.set
        )

        name, opts = columns[0]
        self.tree.column("#0", **opts)
        self.tree.heading("#0", text=name, anchor=(W,))

        for name, opts in columns[1:]:
            self.tree.column(name, **opts)
            self.tree.heading(name, text=name, anchor=(W,))

        self.tree.grid(column=0, row=0, sticky=(N, W, E, S))
        self.scrollY.grid(column=1, row=0, sticky=(N, S))
        self.scrollX.grid(column=0, row=1, sticky=(W, E))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.delete = self.tree.delete
        self.get_children = self.tree.get_children
        self.focus = self.tree.focus
        self.item = self.tree.item
        self.insert = self.tree.insert


def LabelCombo(root, text):
    f = Frame(root)
    f.columnconfigure(1, weight=1)

    Label(f, text=text, anchor=E, width=15).grid(column=0, row=0, sticky=(N, W, E, S))
    c = Combobox(f, exportselection=0)
    c.grid(column=1, row=0, sticky=(N, W, E, S))

    return f, c
