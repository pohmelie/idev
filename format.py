from collections import OrderedDict


class Container(dict):
    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)

    def __getattr__(self, name):
        return self.get(name, None)

'''
Description of all availiable formats
factor:
    real number = array number * factor
if omitted:
    factor = 1
    width = 16
    bit = 0
'''

#TODO: words - 1

formats = Container(
    kant3=Container(
        codename="kant3",
        description = "КАНТ-3",
        address={
            "Практический":28,
            "Боевой":27
        },
        fields=(
            Container(
                name="Режим работы",
                desc=Container(word=1, bit=13, width=3,
                    text=OrderedDict((
                            ("НК-КС", 0),
                            ("ПХ", 1),
                            ("ПЛ", 2),
                            ("НК-корп", 3),
                            ("ИЦ", 4)
                    ))
                )
            ),
            Container(
                name="Борт цели",
                desc=Container(word=1, bit=11, width=2,
                    text=OrderedDict((
                        ("Левый", 1)
                        ("Правый", 2)
                    ))
                )
            ),
            Container(
                name="Ледовые условия",
                desc=Container(word=1, bit=9, width=2,
                    text=OrderedDict((
                        ("Не лёд", 1),
                        ("Лёд", 2)
                    ))
                )
            ),
            Container(
                name="Шифр изделия",
                desc=Container(word=1, bit=6, width=3,
                    text=OrderedDict((
                        ("1-я в залпе", 0),
                        ("2-я в залпе", 1),
                        ("3-я в залпе", 2),
                        ("4-я в залпе", 3),
                        ("Одиночная с КМВ", 4)
                    ))
                )
            ),
            Container(
                name="Кратность цели",
                desc=Container(word=1, bit=3, width=3,
                    text=OrderedDict((
                        ("Первый КС", 0),
                        ("Второй КС", 1),
                        ("Третий КС", 2),
                        ("Четвёртый КС", 3),
                        ("Выбор первого КС", 4),
                        ("Выбор из двух КС", 5),
                        ("Выбор из трёх КС", 6),
                        ("Выбор из четырёх КС", 7)
                    ))
                )
            )
            Container(
                name="Вид стрельбы",
                desc=Container(word=1, bit=2, width=1,
                    text=OrderedDict((
                        ("Одиночная", 0),
                        ("Залп", 1)
                    ))
                )
            )
            Container(
                name="Знак циркуляции",
                desc=Container(word=2, bit=15, width=1,
                    text=OrderedDict((
                        ("Право", 0),
                        ("Лево", 1)
                    ))
                )
            )
            Container(
                name="Признак носителя",
                desc=Container(word=2, bit=13, width=2,
                    text=OrderedDict((
                        ("ПЛ с осевыми ТА", 0),
                        ("НК первого типа", 2),
                        ("НК второго типа", 3)
                    ))
                )
            )
            Container(
                name="Режим движения",
                desc=Container(word=2, bit=12, width=1,
                    text=OrderedDict((
                        ("Vmax", 0),
                        ("Vmin", 1)
                    ))
                )
            )
            Container(
                name="Признак ТА",
                desc=Container(word=2, bit=11, width=1,
                    text=OrderedDict((
                        ("Не установлен", 0),
                        ("Установлен", 1)
                    ))
                )
            )
            Container(
                name="Признак «677»", #  a-0171, a0187
                desc=Container(word=2, bit=10, width=1,
                    text=OrderedDict((
                        ("Не установлен", 0),
                        ("Установлен", 1)
                    ))
                )
            )
            Container(
                name="Признак «грунт»",
                desc=Container(word=2, bit=9, width=1,
                    text=OrderedDict((
                        ("Не установлен", 0),
                        ("Установлен", 1)
                    ))
                )
            )
            Container(
                name="Признак «прилёд»",
                desc=Container(word=2, bit=8, width=1,
                    text=OrderedDict((
                        ("Не установлен", 0),
                        ("Установлен", 1)
                    ))
                )
            )
            Container(
                name="Восстановление блокировки",
                desc=Container(word=2, bit=7, width=1,
                    text=OrderedDict((
                        ("Разрешено", 0),
                        ("Запрещено", 1)
                    ))
                )
            )
            Container(
                name="Маневрирование в ВП",
         desc = {word = 2, bit = 6, width = 1,
             text = {
                 ["Разр."] = 0,
                 ["Запр."] = 1
             }
         }
        },
        {name = "МС ССН",
         desc = {word = 2, bit = 5, width = 1,
             text = {
                 ["Не исп."] = 0,
                 ["Исп."] = 1
             }
         }
        },
        {name = "Шир. пояс", desc = {word = 3, bit = 10, width = 6}},
        {name = "ВТУ",
         desc = {word = 3, bit = 9, width = 1,
             text = {
                 ["Не вкл."] = 0,
                 ["Вкл."] = 1
             }
         }
        },
        {name = "Борт ТА",
         desc = {word = 3, bit = 8, width = 1,
             text = {
                 ["ПБ"] = 0,
                 ["ЛБ"] = 1
             }
         }
        },
        {name = "ВКТ",
         desc = {word = 3, bit = 6, width = 2,
             text = {
                 ["Вниз"] = 0,
                 ["Вверх"] = 1,
                 ["Прямо"] = 2
             }
         }
        },
        {name = "РЦ",
         desc = {word = 3, bit = 4, width = 2,
             text = {
                 ["Авианос"] = 0,
                 ["Крейсер"] = 1,
                 ["Эсминец"] = 2,
                 ["Корвет"] = 3
             }
         }
        },
        {name = "Дalpha", desc = {word = 4}},
        {name = "Драб", desc = {word = 5}},
        {name = "Дw1", desc = {word = 6}},
        {name = "Дсн", desc = {word = 7}},
        {name = "Дw2", desc = {word = 8}},
        {name = "Дdphi", desc = {word = 9}},
        {name = "Дкр", desc = {word = 10}},
        {name = "Дw3", desc = {word = 11}},
        {name = "Да", desc = {word = 12}},
        {name = "Дhб", desc = {word = 13}},
        {name = "Дпр", desc = {word = 14}},

        {name = "w1", desc = {word = 17, factor = 360 / 32768}},
        {name = "w2", desc = {word = 18, factor = 360 / 32768}},
        {name = "w3", desc = {word = 19, factor = 360 / 32768}},

        {name = "h акв.", desc = {word = 20}},
        {name = "h ск.", desc = {word = 21}},
        {name = "h марш.", desc = {word = 22}},
        {name = "h поиска", desc = {word = 23}},
        {name = "h боевая", desc = {word = 24}},
        {name = "hов", desc = {word = 25}},
        {name = "hон", desc = {word = 26}},
        {name = "h отвед.", desc = {word = 27}},

        {name = "w", desc = {word = 28, factor = 360 / 32768}},
        {name = "w + alpha", desc = {word = 29, factor = 360 / 32768}},
        {name = "w + dphi", desc = {word = 30, factor = 360 / 32768}},

        {name = "theta0", desc = {word = 31, factor = 180 / 32768}},
        {name = "gamma0", desc = {word = 32, factor = 360 / 32768}}
    )
)

print(formats)
'''
