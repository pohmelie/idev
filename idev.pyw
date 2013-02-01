import pickle
import os.path
from copy import deepcopy
from datetime import date
from threading import Thread
from tkinter import *
from tkinter.ttk import *

import formats
from blocks import *
from milstd import Tmk


class Idev:
    def __init__(self):
        self.formats_list = formats.formats_list()
        self.current_array = None

        self.root = Tk()
        self.root.title("idev")
        self._make_widgets()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.tmk = Tmk(0, self.log)
        self.read_file()
        self.mainloop = self.root.mainloop

    def clear_edit(self):
        self.edit_value.state(("!readonly",))
        self.edit_value["values"] = ()
        self.edit_value.set("")

    def clear_tdata(self):
        self.tdata.delete(*self.tdata.get_children())
        self.clear_edit()

    def clear_tarrays(self):
        self.tarrays.delete(*self.tarrays.get_children())
        self.clear_tdata()

    def fill_arrays(self):
        self.current_array = None
        self.clear_tarrays()

        for i, d in enumerate(self.data):
            name = formats.formats[d.codename].description
            txt = d.date
            if d.changed:
                txt = "[*] " + txt
            self.tarrays.insert("", "end", text=txt, values=(name, d.desc), tag=i)

    def fill_data(self, d):
        self.clear_tdata()

        for k in d.fields:
            self.tdata.insert("", "end", text=k, values=(d.fields[k],))

    def choose_array(self):
        self.clear_tdata()

        iid = self.tarrays.focus()
        if iid:
            i = int(self.tarrays.item(iid, "tag")[0])
            name = formats.formats[self.data[i].codename].description
            self.entry_type.set(name)
            self.entry_desc.set(self.data[i].desc)
            self.current_array = i
            self.fill_data(self.data[i])

    def choose_data(self):
        iid = self.tdata.focus()
        if iid:
            it = self.tdata.item(iid)
            d = self.data[self.current_array]
            t = it["text"]
            v = it["values"][0]
            for field in formats.formats[d.codename].fields:
                if field.name == t:
                    desc = field.desc
                    if desc.text:
                        self.edit_value.state(("readonly",))
                        self.edit_value["values"] = tuple(desc.text)
                        self.edit_value.set(v)
                    else:
                        self.edit_value.state(("!readonly",))
                        self.edit_value["values"] = ()
                        self.edit_value.set(v)

    def edit_value_on_change(self, e):
        iid = self.tdata.focus()
        s = self.edit_value_v.get()
        if iid:
            it = self.tdata.item(iid)
            d = self.data[self.current_array]
            t = it["text"]
            self.tdata.item(iid, values=[s])
            d.fields[t] = s

            iid = self.tarrays.focus()
            if not d.changed:
                self.tarrays.item(iid, text="[*] " + d.date)
            d.changed = True

    def entry_desc_on_change(self, e):
        if self.current_array is not None:
            s = self.entry_desc_v.get()

            d = self.data[self.current_array]
            d.desc = s

            iid = self.tarrays.focus()
            vals = (formats.formats[d.codename].description, s)
            self.tarrays.item(iid, values=vals)
            if not d.changed:
                self.tarrays.item(iid, text="[*] " + d.date)
            d.changed = True

    def entry_type_on_change(self, e):
        if self.current_array is not None:
            s = self.entry_type_v.get()

            d = self.data[self.current_array]
            if formats.formats[d.codename].description != s:
                for form in formats.formats.values():
                    if form.description == s:
                        self.data[self.current_array] = formats.new(form.codename)
                        self.data[self.current_array].changed = True
                        self.fill_arrays()
                        break

    def new_array(self):
        self.data.append(formats.new(next(iter(formats.formats))))
        self.fill_arrays()

    def copy_array(self):
        if self.current_array is not None:
            self.data.append(deepcopy(self.data[self.current_array]))
            self.data[-1].changed = True
            self.fill_arrays()

    def delete_array(self):
        if self.current_array is not None:
            self.data.pop(self.current_array)
            self.fill_arrays()

    def save_all(self):
        for d in self.data:
            if d.changed:
                d.changed = False
                d.date = date.today().strftime("%Y-%m-%d")
        self.save_file()
        self.fill_arrays()

    def read_file(self, fname="data.pickle"):
        succ = "Файл '{}' прочитан"
        fail = "Файл '{}' отсутствует или не может быть открыт"

        if os.path.isfile(fname):
            with open(fname, "rb") as f:
                self.data = pickle.load(f)
            self.log(succ.format(fname), self.log.BORRING)
        else:
            self.data = []
            self.log(fail.format(fname), self.log.BORRING)

        self.fill_arrays()

    def save_file(self, fname="data.pickle"):
        succ = "Файл '{}' сохранён"
        fail = "Файл '{}' не может быть сохранён"

        try:
            with open(fname, "wb") as f:
                pickle.dump(self.data, f)
            self.log(succ.format(fname), self.log.BORRING)
        except:
            self.log(fail.format(fname), self.log.ERROR)

    def test(self):
        if self.current_array is not None:
            address = formats.addresses(
                ("Практический", "Боевой")[self.address.current()],
                self.data[self.current_array].codename
            )
            Thread(target=self.tmk.test, args=(address,)).start()

    def upload(self):
        if self.current_array is not None:
            d = self.data[self.current_array]
            rawd = formats.encode(d.fields, d.codename, self.log)
            if rawd is not None:
                address = formats.addresses(
                    ("Практический", "Боевой")[self.address.current()],
                    d.codename
                )
                Thread(target=self.tmk.upload, args=(rawd, address)).start()

    def _make_widgets(self):
        pn = PanedWindow(self.root, orient=HORIZONTAL)
        pn.grid(column=0, row=0, sticky=(N, W, E, S))

        lf1 = LabelFrame(pn, text="Массивы")
        lf1.columnconfigure(0, weight=1)
        lf1.rowconfigure(0, weight=1)
        pn.add(lf1)

        lf2 = LabelFrame(pn, text="Данные")
        lf2.columnconfigure(0, weight=1)
        lf2.rowconfigure(0, weight=1)
        pn.add(lf2)

        cols = (
            ("Дата", dict(stretch=0, width=120)),
            ("Тип", dict(stretch=0, width=100)),
            ("Описание", {})
        )
        self.tarrays = Table(lf1, columns=cols, padding=(0, 0, 0, 4), callback=self.choose_array)
        self.tarrays.grid(column=0, row=0, sticky=(N, W, E, S))

        f, self.entry_type = LabelCombo(lf1, "Тип:")
        self.entry_type.state(("readonly",))
        self.entry_type["values"] = self.formats_list
        f.grid(column=0, row=1, sticky=(N, W, E, S))
        self.entry_type_v = StringVar()
        self.entry_type["textvar"] = self.entry_type_v
        self.entry_type.bind("<<ComboboxSelected>>", self.entry_type_on_change)

        f, self.entry_desc = LabelCombo(lf1, "Описание:")
        f.grid(column=0, row=2, sticky=(N, W, E, S))
        self.entry_desc_v = StringVar()
        self.entry_desc["textvar"] = self.entry_desc_v
        self.entry_desc.bind("<KeyRelease>", self.entry_desc_on_change)

        btns = (
            ("Новый", self.new_array),
            ("Копировать", self.copy_array),
            ("Удалить", self.delete_array),
            ("Сохранить", self.save_all)
        )
        HorizontalButtons(lf1, buttons=btns).grid(column=0, row=3, sticky=(N, W, E, S))

        cols = (
            ("Параметр", {}),
            ("Значение", {})
        )
        self.tdata = Table(lf2, columns=cols, padding=(0, 0, 0, 4), callback=self.choose_data)
        self.tdata.grid(column=0, row=0, sticky=(N, W, E, S))

        f, self.edit_value = LabelCombo(lf2, "Значение:")
        f.grid(column=0, row=1, sticky=(N, W, E, S))
        self.edit_value_v = StringVar()
        self.edit_value["textvar"] = self.edit_value_v
        self.edit_value.bind("<KeyRelease>", self.edit_value_on_change)
        self.edit_value.bind("<<ComboboxSelected>>", self.edit_value_on_change)

        f = Frame(self.root, padding=(0, 5, 0, 5))
        f.columnconfigure(0, weight=1)
        f.grid(column=0, row=1, sticky=(N, W, E, S))
        Separator(f, orient=HORIZONTAL).grid(column=0, row=0, sticky=(W, E))

        f, self.address = LabelCombo(self.root, "Режим:")
        self.address.state(("readonly",))
        self.address["values"] = ("Практический", "Боевой")
        self.address.current(0)
        f.grid(column=0, row=2, sticky=(N, W, S))

        btns = (
            ("Ввод", self.upload),
            ("Тест", self.test)
        )
        HorizontalButtons(self.root, buttons=btns).grid(column=0, row=3, sticky=(N, W, E, S))

        self.log = Logger(self.root, text_height=10)
        self.log.grid(column=0, row=4, sticky=(N, W, E, S))

idev = Idev()
idev.mainloop()
idev.tmk.release()
