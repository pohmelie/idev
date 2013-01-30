import formats
from blocks import *
from tkinter import *
from tkinter.ttk import *
from milstd import Tmk


from collections import OrderedDict
data = (0x0b08, 0x00c0, 0x10a0, 0xc350, 0xc350, 0x015e, 0x0514, 0x0000, 0x047e,
    0xc350, 0x0000, 0xc350, 0x04b0, 0x1f40, 0x0000, 0x0000, 0x0000, 0x0000,
    0x0000, 0x00fa, 0x0032, 0x0014, 0x0000, 0x000a, 0x0000, 0x0000, 0x0000,
    0x6000, 0x6000, 0x7000, 0x0000, 0x0000)

udata = OrderedDict([
    ('Режим работы', 'НК-КС'),
    ('Борт цели', 'Левый'),
    ('Ледовые условия', 'Не лёд'),
    ('Шифр изделия', 'Одиночная с КМВ'),
    ('Кратность цели', 'Второй КС'),
    ('Вид стрельбы', 'Одиночная'),
    ('Знак циркуляции', 'Право'),
    ('Признак носителя', 'ПЛ с осевыми ТА'),
    ('Режим движения', 'Vmax'),
    ('Признак ТА', 'Не установлен'),
    ('Признак «677»', 'Не установлен'),
    ('Признак «грунт»', 'Не установлен'),
    ('Признак «прилёд»', 'Не установлен'),
    ('Восстановление блокировки', 'Запрещено'),
    ('Маневрирование в ВП', 'Запрещено'),
    ('Признак «МС ССН»', 'Не установлен'),
    ('Номер широтного пояса', 4.0),
    ('Включение ТУ', 'Не включено'),
    ('Борт ТА', 'Правый'),
    ('Вид конечной траектории', 'Прямо'),
    ('Ранг цели', 'Эсминец / ДПЛ'),
    ('Дα', 50000.0),
    ('Др', 50000.0),
    ('Дω1', 350.0),
    ('Дсн', 1300.0),
    ('Дω2', 0.0),
    ('ДΔφ', 1150.0),
    ('Дкр', 50000.0),
    ('Дω3', 0.0),
    ('Да', 50000.0),
    ('Дhб', 1200.0),
    ('Дпр', 8000.0),
    ('ω1', 0.0),
    ('ω2', 0.0),
    ('ω3', 0.0),
    ('h акватории', 250.0),
    ('h слоя скачка', 50.0),
    ('h маршевая', 20.0),
    ('h поиска', 0.0),
    ('h боевая', 10.0),
    ('h ограничения верха', 0.0),
    ('h ограничения низа', 0.0),
    ('h отведедния', 0.0),
    ('ω', 270.0),
    ('ω + α', 270.0),
    ('ω + Δφ', 315.0),
    ('θ0', 0.0),
    ('γ0', 0.0)
])


class Idev:
    def __init__(self):
        self.root = Tk()
        self.root.title("idev")
        self._make_widgets()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.mainloop = self.root.mainloop

    def _make_widgets(self):
        #"edit" frame
        self.edit = Frame(self.root)
        self.edit.columnconfigure(0, weight=1)
        self.edit.rowconfigure(0, weight=1)
        self.edit.grid(column=0, row=0, sticky=(N, W, E, S))

        #"edit" choose array side (left)
        tmp = Frame(self.edit, padding=(5, 5, 5, 5))
        tmp.columnconfigure(0, weight=1)
        tmp.columnconfigure(1, weight=1)
        tmp.rowconfigure(0, weight=1)
        tmp.grid(column=0, row=0, sticky=(N, W, E, S))

        cols = (
            ("Дата", dict(stretch=0, width=100)),
            ("Тип", dict(stretch=0, width=100)),
            ("Описание", {})
        )
        Table(tmp, columns=cols).grid(column=0, row=0, sticky=(N, W, E, S))

        lc = LabelCombo(tmp, text="Тип:")
        self.entry_type = lc.combo
        lc.grid(column=0, row=1, sticky=(N, W, E, S))

        le = LabelEntry(tmp, text="Описание:")
        self.entry_desc = le.entry
        le.grid(column=0, row=2, sticky=(N, W, E, S))

        btns = (
            ("Новый", None),
            ("Копировать", None),
            ("Удалить", None)
        )
        HorizontalButtons(tmp, buttons=btns).grid(column=0, row=3, sticky=(N, W, E, S))

        #"edit" parameters  side (right)
        cols = (
            ("Параметр", {}),
            ("Значение", {})
        )
        Table(tmp, columns=cols).grid(column=1, row=0, sticky=(N, W, E, S))

        lc = LabelCombo(tmp, text="Значение:", cs=(N, W, E, S))
        self.edit_value = lc.combo
        self.edit_value.state(("readonly",))
        lc.columnconfigure(0, weight=0)
        lc.grid(column=1, row=1, sticky=(N, W, E, S), pady=1)

        btns = (
            ("Ввод", None),
            ("Тест", None)
        )
        HorizontalButtons(self.edit, buttons=btns).grid(column=0, row=1, sticky=(N, W, E, S))

        #logger
        self.log = Logger(self.root, text_height=10)
        self.log.grid(column=0, row=2, sticky=(N, W, E, S))

Idev().mainloop()

'''from threading import Thread


def test():
    Thread(target=tmk.test, args=(28,)).start()

def upload():
    Thread(target=tmk.upload, args=(encode(udata, "kant3"), 28)).start()

root = Tk()

HorizontalButtons(root, buttons=(
        ("Тест", test),
        ("Ввод", upload),
    )
).grid(column=0, row=0, sticky=(N, W, E, S))

log = Logger()
log.grid(column=0, row=1, sticky=(W, E, S))

tmk = Tmk(0, log)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.mainloop()

tmk.release()
'''
