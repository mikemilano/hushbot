from twisted.internet import reactor
import Adafruit_BBIO.ADC as ADC

ADC.setup()


class Listener():
    def __init__(self):
        self.listening = False
        self.delay = 1
        self.sample_size = 50

    def start(self):
        self.listening = True
        self.listen()

    def stop(self):
        self.listening = False

    def listen(self):
        if not self.listening:
            return

        min = 1.0
        max = 0
        for x in range(1, self.sample_size):
            value = ADC.read("P9_39")
            if value > max:
                max = value
            elif value < min:
                min = value

        diff = max - min
        self.process(diff)

    def process(self, value):
        print(value)

        if self.listening:
            reactor.callLater(self.delay, self.listen)


if __name__ == '__main__':
    l = Listener()
    l.start()
    reactor.run()