from collections import OrderedDict
from datetime import date


def decode(d, f):
    m = OrderedDict()
    if f in formats:
        for field in formats[f].fields:
            desc = field.desc
            n = (d[desc.word] >> (desc.bit or 0)) & ((1 << (desc.width or 16)) - 1)
            if desc.text:
                for k, v in desc.text.items():
                    if v == n:
                        m[field.name] = k
                        break
            else:
                m[field.name] = n * (desc.factor or 1)
        return m


def encode(m, f, log):
    err = "Значение '{}' поля '{}' невозможно преобразовать в float"
    log("Генерация массива")
    d = [0] * 32
    if f in formats:
        for field in formats[f].fields:
            desc = field.desc
            if desc.text:
                n = desc.text[m[field.name]]
            else:
                try:
                    x = float(m[field.name])
                except:
                    log(err.format(m[field.name], field.name), log.ERROR)
                    return
                n = round(x / (desc.factor or 1)) & ((1 << (desc.width or 16)) - 1)
            d[desc.word] = d[desc.word] | (n << (desc.bit or 0))
        return tuple(d)


def formats_list():
    return tuple(map(lambda x: x.description, formats.values()))


def new(f):
    ret = Container()
    m = OrderedDict()
    if f in formats:
        for field in formats[f].fields:
            desc = field.desc
            m[field.name] = next(iter(desc.text)) if desc.text else "0"
        return Container(
            codename=f,
            date=date.today().strftime("%Y-%m-%d"),
            desc="",
            fields=m,
            changed=True
        )


def addresses(s, f):
    if f in formats:
        return formats[f].address.get(s, None)


class Container(dict):
    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)

    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            return super(Container, self).__getattr__(name)
        return self.get(name, None)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

'''
Description of all availiable formats
factor:
    real number = array number * factor
if omitted:
    factor = 1
    width = 16
    bit = 0
'''

formats = Container(
    kant3=Container(
        codename="kant3",
        description="КАНТ-3",
        address=OrderedDict((
            ("Практический", 28),
            ("Боевой", 27)
        )),
        fields=(
            Container(
                name="Режим работы",
                desc=Container(word=0, bit=13, width=3,
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
                desc=Container(word=0, bit=11, width=2,
                    text=OrderedDict((
                        ("Левый", 1),
                        ("Правый", 2)
                    ))
                )
            ),
            Container(
                name="Ледовые условия",
                desc=Container(word=0, bit=9, width=2,
                    text=OrderedDict((
                        ("Не лёд", 1),
                        ("Лёд", 2)
                    ))
                )
            ),
            Container(
                name="Шифр изделия",
                desc=Container(word=0, bit=6, width=3,
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
                desc=Container(word=0, bit=3, width=3,
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
            ),
            Container(
                name="Вид стрельбы",
                desc=Container(word=0, bit=2, width=1,
                    text=OrderedDict((
                        ("Одиночная", 0),
                        ("Залп", 1)
                    ))
                )
            ),
            Container(
                name="Знак циркуляции",
                desc=Container(word=1, bit=15, width=1,
                    text=OrderedDict((
                        ("Право", 0),
                        ("Лево", 1)
                    ))
                )
            ),
            Container(
                name="Признак носителя",
                desc=Container(word=1, bit=13, width=2,
                    text=OrderedDict((
                        ("ПЛ с осевыми ТА", 0),
                        ("НК первого типа", 2),
                        ("НК второго типа", 3)
                    ))
                )
            ),
            Container(
                name="Режим движения",
                desc=Container(word=1, bit=12, width=1,
                    text=OrderedDict((
                        ("Vmax", 0),
                        ("Vmin", 1)
                    ))
                )
            ),
            Container(
                name="Признак ТА",
                desc=Container(word=1, bit=11, width=1,
                    text=OrderedDict((
                        ("Не ПЛ с боковым расположением ТА", 0),
                        ("ПЛ с боковым расположением ТА", 1)
                    ))
                )
            ),
            Container(
                name="Признак «677»",  # a-0171, a0187
                desc=Container(word=1, bit=10, width=1,
                    text=OrderedDict((
                        ("не ПЛ 677", 0),
                        ("ПЛ 677", 1)
                    ))
                )
            ),
            Container(
                name="Признак «грунт»",
                desc=Container(word=1, bit=9, width=1,
                    text=OrderedDict((
                        ("Не грунт", 0),
                        ("Грунт", 1)
                    ))
                )
            ),
            Container(
                name="Признак «прилёд»",
                desc=Container(word=1, bit=8, width=1,
                    text=OrderedDict((
                        ("Не прилёд", 0),
                        ("Прилёд", 1)
                    ))
                )
            ),
            Container(
                name="Восстановление блокировки",
                desc=Container(word=1, bit=7, width=1,
                    text=OrderedDict((
                        ("Разрешено", 0),
                        ("Запрещено", 1)
                    ))
                )
            ),
            Container(
                name="Маневрирование в ВП",
                desc=Container(word=1, bit=6, width=1,
                    text=OrderedDict((
                        ("Разрешено", 0),
                        ("Запрещено", 1)
                    ))
                )
            ),
            Container(
                name="Признак «МС ССН»",
                desc=Container(word=1, bit=5, width=1,
                    text=OrderedDict((
                        ("МС ССН не используется", 0),
                        ("МС ССН используется", 1)
                    ))
                )
            ),
            Container(name="Номер широтного пояса", desc=Container(word=2, bit=10, width=6)),
            Container(
                name="Включение ТУ",
                desc=Container(word=2, bit=9, width=1,
                    text=OrderedDict((
                        ("Не включено", 0),
                        ("Включено", 1)
                    ))
                )
            ),
            Container(
                name="Борт ТА",
                desc=Container(word=2, bit=8, width=1,
                    text=OrderedDict((
                        ("Правый", 0),
                        ("Левый", 1)
                    ))
                )
            ),
            Container(
                name="Вид конечной траектории",
                desc=Container(word=2, bit=6, width=2,
                    text=OrderedDict((
                        ("Вниз", 0),
                        ("Вверх", 1),
                        ("Прямо", 2)
                    ))
                )
            ),
            Container(
                name="Ранг цели (НК / ПЛ)",
                desc=Container(word=2, bit=4, width=2,
                    text=OrderedDict((
                        ("Авианос / АПРЛ", 0),
                        ("Крейсер / АПЛ", 1),
                        ("Эсминец / ДПЛ", 2),
                        ("Корвет / СМПЛ", 3)
                    ))
                )
            ),
            Container(name="Дα", desc=Container(word=3)),
            Container(name="Др", desc=Container(word=4)),
            Container(name="Дω1", desc=Container(word=5)),
            Container(name="Дсн", desc=Container(word=6)),
            Container(name="Дω2", desc=Container(word=7)),
            Container(name="ДΔφ", desc=Container(word=8)),
            Container(name="Дкр", desc=Container(word=9)),
            Container(name="Дω3", desc=Container(word=10)),
            Container(name="Да", desc=Container(word=11)),
            Container(name="Дhб", desc=Container(word=12)),
            Container(name="Дпр", desc=Container(word=13)),

            Container(name="ω1", desc=Container(word=16, factor=360 / 32768)),
            Container(name="ω2", desc=Container(word=17, factor=360 / 32768)),
            Container(name="ω3", desc=Container(word=18, factor=360 / 32768)),

            Container(name="h акватории", desc=Container(word=19)),
            Container(name="h слоя скачка", desc=Container(word=20)),
            Container(name="h маршевая", desc=Container(word=21)),
            Container(name="h поиска", desc=Container(word=22)),
            Container(name="h боевая", desc=Container(word=23)),
            Container(name="h ограничения верха", desc=Container(word=24)),
            Container(name="h ограничения низа", desc=Container(word=25)),
            Container(name="h отведедния", desc=Container(word=26)),

            Container(name="ω", desc=Container(word=27, factor=360 / 32768)),
            Container(name="ω + α", desc=Container(word=28, factor=360 / 32768)),
            Container(name="ω + Δφ", desc=Container(word=29, factor=360 / 32768)),

            Container(name="θ0", desc=Container(word=30, factor=180 / 32768)),
            Container(name="γ0", desc=Container(word=31, factor=360 / 32768))
        )
    )
)
