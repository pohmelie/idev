import WDMTMKv2 as tmk
from time import sleep


class Tmk:

    CONTROL, GOOD, BAD, PREPARE, READY, ERROR = tuple(map(lambda x: (1 << x), (0, 1, 2, 3, 4, 9)))
    SEND, RECEIVE = range(2)

    def __init__(self, ntmk, log=print):
        self.log = log
        self.ntmk = ntmk

        tmk.TmkOpen()
        tmk.tmkconfig(self.ntmk)
        tmk.bcreset()
        tmk.bcdefbase(0)
        tmk.bcdefbus(0)

    def release(self):
        tmk.tmkdone(self.ntmk)
        tmk.TmkClose()

    def send_block(self, code_word, data):
        tmk.bcputw(0, code_word)
        for i in range(len(data)):
            tmk.bcputw(i, data[i])
        tmk.bcputw(len(data) + 1, 0xffff)
        tmk.bcstart(0, tmk.DATA_BC_RT)
        sleep(0.002)
        return tmk.bcgetw(len(data) + 1)

    def get_block(self, code_word, count):
        d = []
        tmk.bcputw(0, code_word)
        for i in range(count):
            tmk.bcputw(i + 1, 0)
        tmk.bcstart(0, tmk.DATA_RT_BC)
        sleep(0.002)
        for i in range(count):
            d.append(tmk.bcgetw(i + 2))
        return tuple(d)

    def make_code_word(self, direction, address, subaddress, length):
        return (address << 11) | (direction << 10) | (subaddress << 5) | length

    def test(self, address):
        tdata = (0x5555, 0xaaaa, 0xff00, 0x00ff)

        self.log("Тест")
        working = [True, True]
        for i in range(2):
            tmk.bcdefbus(i)
            self.send_block(self.make_code_word(Tmk.SEND, address, 18, 4), tdata)
            sleep(0.1)
            if tdata != self.get_block(self.make_code_word(Tmk.RECEIVE, address, 19, 4), 4):
                log("Отказ {} канала".format(("основного", "резервного")[i]), log.ERROR)
                working[i] = False

        for i in range(2):
            if working[i]:
                tmk.bcdefbus(i)
                break
        else:
            log("Отказ БЗ:МК", log.ERROR)

        log("Идёт контроль")
        status = 0
        for _ in range(80):
            sleep(0.1)
            status = self.get_block(self.make_code_word(Tmk.RECEIVE, address, 1, 1), 1)[0]
            if status != Tmk.CONTROL:
                break

        log("status = {x:} ({x:0>16b})".format(x=status), log.BORRING)
        if status != Tmk.GOOD:
            if status & Tmk.BAD:
                log("Отказ БЗ:ГО")
            elif status & Tmk.READY:
                log("Отказ БЗ:БК")
            elif status & Tmk.ERROR:
                log("Отказ БЗ:БОД")
        else:
            log("Изделие исправно")

    def upload(self, data, address):

        def send():
            self.send_block(self.make_code_word(Tmk.SEND, address, 2, 0), data)
            sleep(0.01)
            self.send_block(self.make_code_word(Tmk.SEND, address, 1, 1), (0xff,))
            sleep(0.015)
            return self.get_block(self.make_code_word(Tmk.RECEIVE, address, 2, 0), 32)

        self.log("Ввод массива")
        tmk.bcdefbus(0)
        sleep(0.1)

        if data != send():
            log("Отказ основного канала", log.ERROR)
            tmk.bcdefbus(1)
            sleep(0.1)
            self.send_block(self.make_code_word(Tmk.SEND, address, 1, 1), (0xcece,))
            sleep(0.1)
            self.send_block(self.make_code_word(Tmk.SEND, address, 18, 1), (0xaa,))
            sleep(0.1)

            if data != send():
                log("Отказ резервного канала", log.ERROR)
                log("Ввод не прошёл")
                log("Отказ БЗ:МК", log.ERROR)
                return

        sleep(0.1)
        self.send_block(self.make_code_word(Tmk.SEND, address, 18, 1), (0xecec,))
        log("Ввод прошёл")

        status = 0
        for _ in range(10):
            sleep(0.1)
            status = self.get_block(self.make_code_word(Tmk.RECEIVE, address, 1, 1), 1)[0]
            if status != 0 and status != (Tmk.PREPARE | Tmk.GOOD):
                break

        log("status = {x:} ({x:0>16b})".format(x=status), log.BORRING)
        if status == (Tmk.READY | Tmk.GOOD):
            log("Блокировки сняты")
        elif status == Tmk.ERROR:
            log("Заливка БОД")
        else:
            log("Отказ БЗ")
