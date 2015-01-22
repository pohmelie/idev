import functools
import sys

if sys.platform == "linux":

    import ltmk as tmk

elif sys.platform == "win32":

    import WDMTMKv2 as tmk

from time import sleep


class Tmk:

    CONTROL, GOOD, BAD, PREPARE, READY, ERROR = tuple(map(lambda x: (1 << x), (0, 1, 2, 3, 4, 9)))
    SEND, RECEIVE = range(2)

    def __init__(self, ntmk, log=print):
        self.log = log
        self.ntmk = ntmk

        self.logfun(tmk.TmkOpen, 0)
        self.logfun(tmk.tmkconfig, 0, self.ntmk)
        self.logfun(tmk.bcreset, 0)
        self.logfun(tmk.bcdefbus, 0, 0)
        self.logfun(tmk.bcdefbase, 0, 0)

    def release(self):
        self.logfun(tmk.tmkdone, 0, self.ntmk)
        tmk.TmkClose()

    def logfun(self, fun, ecode, *args):
        rcode = fun(*args)
        if rcode != ecode:
            self.log(
                "Ошибка: {}{} = {:x}, ожидалось {:x}".format(
                    fun.__name__,
                    args,
                    rcode,
                    ecode
                ),
                self.log.ERROR
            )

    def send_block(self, code_word, data):
        tmk.bcputw(0, code_word)
        for i in range(len(data)):
            tmk.bcputw(i + 1, data[i])
        tmk.bcputw(len(data) + 1, 0xffff)
        self.logfun(tmk.bcstart, 0, 0, tmk.DATA_BC_RT)
        sleep(0.01)
        #self.logfun(tmk.bcgetw, (code_word >> 11) << 11, len(data) + 1)

    def get_block(self, code_word, count):
        d = []
        tmk.bcputw(0, code_word)
        for i in range(count):
            tmk.bcputw(i + 1, 0)
        self.logfun(tmk.bcstart, 0, 0, tmk.DATA_RT_BC)
        sleep(0.01)
        for i in range(count):
            d.append(tmk.bcgetw(i + 2))
        return tuple(d)

    def make_code_word(self, direction, address, subaddress, length):
        return (address << 11) | (direction << 10) | (subaddress << 5) | length

    def test_kant3(self, address, tdata=(0x5555, 0xaaaa, 0xff00, 0x00ff)):
        lines = [False, False]

        for i in range(2):
            self.logfun(tmk.bcdefbus, 0, i)
            for attempt in range(2):
                self.send_block(self.make_code_word(Tmk.SEND, address, 18, 4), tdata)
                sleep(0.1)
                rdata = self.get_block(self.make_code_word(Tmk.RECEIVE, address, 19, 4), 4)

                if tdata == rdata:
                    self.log("МПИ {} исправен".format(("осн.", "рез.")[i]))
                    lines[i] = True
                    break

                if attempt == 0:
                    self.send_block(self.make_code_word(Tmk.SEND, address, 18, 1), (0x00aa,))
                else:
                    self.log("Отказ МПИ {}".format(("осн.", "рез.")[i]), self.log.ERROR)
                    self.log("Отправлено:\n{}".format(self.phex(tdata)), self.log.BORRING)
                    self.log("Принято:\n{}".format(self.phex(rdata)), self.log.BORRING)

        if not any(lines):
            self.log("Отказ БЗ", self.log.ERROR)
            return

        working_line = lines.index(True)
        self.log("Используется МПИ {}".format(("осн.", "рез.")[working_line]))
        self.logfun(tmk.bcdefbus, 0, working_line)
        self.log("Идёт контроль")

        status = 0
        for _ in range(80):
            sleep(0.1)
            status = self.get_block(self.make_code_word(Tmk.RECEIVE, address, 1, 1), 1)[0]
            if status != Tmk.CONTROL:
                break

        if status != Tmk.GOOD:
            if status == Tmk.CONTROL:
                self.log("Отсутствие сообщения «Исправно»", self.log.ERROR)
            elif status == Tmk.BAD:
                self.log("Неисправно (брак МЧ)", self.log.ERROR)
            elif status == Tmk.READY:
                self.log("Блокировки сняты", self.log.ERROR)
            elif status == Tmk.ERROR:
                self.log("Заливка БОД", self.log.ERROR)
            else:
                self.log("status = {x:} ({x:0>16b})".format(x=status), self.log.BORRING)
            self.log("Отказ БЗ", self.log.ERROR)
        else:
            self.log("Изделие исправно")
            self.log("БЗ готов")

    def upload_kant3(self, data, address):
        up = False

        for i in range(2):
            if up:
                break
            self.logfun(tmk.bcdefbus, 0, i)
            self.log("Передача по МПИ {}".format(("осн.", "рез.")[i]))

            for attempt in range(2):
                sleep(0.1)
                self.send_block(self.make_code_word(Tmk.SEND, address, 2, 0), data)
                sleep(0.1)
                self.send_block(self.make_code_word(Tmk.SEND, address, 1, 1), (0xff,))
                sleep(0.1)
                rdata = self.get_block(self.make_code_word(Tmk.RECEIVE, address, 2, 0), 32)

                if data == rdata:
                    up = True
                    break

                if attempt == 0:
                    sleep(0.1)
                    self.send_block(self.make_code_word(Tmk.SEND, address, 18, 1), (0x00aa,))
                sleep(0.1)
                self.send_block(self.make_code_word(Tmk.SEND, address, 1, 1), (0xcece,))
                if attempt == 1:
                    self.log("Контроль не прошёл", self.log.ERROR)
                    self.log("Отправлено:\n{}".format(self.phex(data)), self.log.BORRING)
                    self.log("Принято:\n{}".format(self.phex(rdata)), self.log.BORRING)
                    if i == 1:
                        self.log("Отказ БЗ", self.log.ERROR)
                        return

        self.log("Контроль прошёл")
        sleep(0.1)
        self.send_block(self.make_code_word(Tmk.SEND, address, 18, 1), (0xecec,))

        status = 0
        once = True
        for _ in range(10):
            sleep(0.1)
            status = self.get_block(self.make_code_word(Tmk.RECEIVE, address, 1, 1), 1)[0]
            if once and status == (Tmk.PREPARE | Tmk.GOOD):
                once = False
                self.log("Исправно. Идёт подготовка.")
            elif status != 0 and status != (Tmk.PREPARE | Tmk.GOOD):
                break

        if status == (Tmk.READY | Tmk.GOOD):
            self.log("Исправно. Блокировки сняты")
            self.log("Пуск разрешён")
        elif status == (Tmk.PREPARE | Tmk.GOOD):
            self.log("Блокировки не сняты", self.log.ERROR)
            self.log("Отказ БЗ", self.log.ERROR)
        elif status == Tmk.ERROR:
            self.log("Заливка БОД", self.log.ERROR)
            self.log("Отказ БЗ", self.log.ERROR)
        else:
            self.log("Отказ рабочего МПИ", self.log.ERROR)
            self.log("Отказ БЗ", self.log.ERROR)
            self.log("status = {x:} ({x:0>16b})".format(x=status), self.log.BORRING)

    def checksum(self, data, count=None):
        if count:
            data = map(data.__get__, range(count))
        return functools.reduce(lambda s, x: ((s + x) + ((s + x) >> 16)) & 0xffff, data)


    def upload_plavun(self, data, address):
        up = False
        crc = 0xffff
        for i in range(12):
            crc ^= data[i]  & 0xff
            for _ in range(8):
                crc = (crc >> 1) & 0x7fff
                if crc & 1:
                    crc = crc ^ 0xa001
                else:
                    crc = (crc >> 1) & 0x7fff

        data = data[:12] + (crc,)
        for i in range(2):
            if up:
                break
            self.logfun(tmk.bcdefbus, 0, i)
            self.log("Передача по МПИ {}".format(("осн.", "рез.")[i]))

            for attempt in range(2):
                sleep(0.1)
                self.send_block(self.make_code_word(Tmk.SEND, address, 3, 13), data)
                sleep(0.1)
                aw = tmk.bcgetw(14)
                if aw != 0:
                    self.log("Неправильное ОС(0x{:x})".format(aw), self.log.ERROR)
                    break

                rdata = self.get_block(self.make_code_word(Tmk.RECEIVE, address, 6, 1), 1)
                if rdata == (0x5555,):
                    self.log("Получена решётка 0x{:x}".format(rdata[0]), self.log.BORRING)
                elif rdata == (0xaaaa,):
                    up = True
                    break
                else:
                    self.log("Получена неправильная решётка 0x{:x}".format(rdata[0]), self.log.ERROR)
                    break
        if up:
            self.log("Ввод прошёл")
        else:
            self.log("Ввод не прошёл", self.log.ERROR)

    def phex(self, data):
        return " ".join(map("{:0>4x}".format, data))
