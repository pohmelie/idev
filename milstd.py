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
        self.logfun(tmk.bcgetw, (code_word >> 11) << 11, len(data) + 1)

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

    def test(self, address, tdata=(0x5555, 0xaaaa, 0xff00, 0x00ff)):

        self.log("Тест", self.log.EVENT)

        self.send_block(self.make_code_word(Tmk.SEND, address, 18, 4), tdata)
        sleep(0.1)
        rdata = self.get_block(self.make_code_word(Tmk.RECEIVE, address, 19, 4), 4)

        if tdata != rdata:
            self.log("Отказ канала", self.log.ERROR)
            self.log("Отправлено:\n{}".format(self.phex(tdata)), self.log.BORRING)
            self.log("Принято:\n{}".format(self.phex(rdata)), self.log.BORRING)
            return

        self.log("Идёт контроль")

        status = 0
        for _ in range(80):
            sleep(0.1)
            status = self.get_block(self.make_code_word(Tmk.RECEIVE, address, 1, 1), 1)[0]
            if status != Tmk.CONTROL:
                break

        if status != Tmk.GOOD:
            if status & Tmk.BAD:
                self.log("Отказ БЗ:ГО", self.log.ERROR)
            elif status & Tmk.READY:
                self.log("Отказ БЗ:БК", self.log.ERROR)
            elif status & Tmk.ERROR:
                self.log("Отказ БЗ:БОД", self.log.ERROR)
            self.log("status = {x:} ({x:0>16b})".format(x=status), self.log.BORRING)
        else:
            self.log("Изделие исправно")

    def upload(self, data, address):

        self.log("Ввод", self.log.EVENT)

        self.send_block(self.make_code_word(Tmk.SEND, address, 2, 0), data)
        sleep(0.01)
        self.send_block(self.make_code_word(Tmk.SEND, address, 1, 1), (0xff,))
        sleep(0.01)
        rdata = self.get_block(self.make_code_word(Tmk.RECEIVE, address, 2, 0), 32)

        if data != rdata:
            self.log("Отказ канала", self.log.ERROR)
            self.log("Отправлено:\n{}".format(self.phex(data)), self.log.BORRING)
            self.log("Принято:\n{}".format(self.phex(rdata)), self.log.BORRING)
            return

        sleep(0.1)
        self.send_block(self.make_code_word(Tmk.SEND, address, 18, 1), (0xecec,))

        self.log("Ввод прошёл")

        status = 0
        for _ in range(10):
            sleep(0.1)
            status = self.get_block(self.make_code_word(Tmk.RECEIVE, address, 1, 1), 1)[0]
            if status != 0 and status != (Tmk.PREPARE | Tmk.GOOD):
                break

        if status == (Tmk.READY | Tmk.GOOD):
            self.log("Блокировки сняты")
        elif status == Tmk.ERROR:
            self.log("Отказ БЗ:БОД")
        elif status == (Tmk.PREPARE | Tmk.GOOD):
            self.log("Отказ БЗ:БК")
        else:
            self.log("Отказ БЗ")
            self.log("status = {x:} ({x:0>16b})".format(x=status), self.log.BORRING)

    def phex(self, data):
        return " ".join(map("{:0>4x}".format, data))
