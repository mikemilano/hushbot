from twisted.internet import reactor
import Adafruit_BBIO.ADC as ADC

ADC.setup()


class HushBot():
    def __init__(self, config, plugins):
        self.config = config['hushbot']
        self.minecraft = plugins['minecraft']
        self.espeak = plugins['espeak']

        self.espeak.say('initialized')

        self.input_pin = self.config["input_pin"]
        self.autostart = self.config["autostart"]
        self.pause = not self.autostart
        self.delay = self.config["sample_delay"]
        self.sample_size = self.config["sample_size"]
        if not self.pause:
            reactor.callLater(self.delay, self.sample)

    def start(self):
        self.pause = False
        self.sample()

    def stop(self):
        self.pause = True

    def sample(self):
        if self.pause:
            return

        min = 1.0
        max = 0
        for x in range(1, self.sample_size):
            value = ADC.read(self.input_pin)
            if value > max:
                max = value
            elif value < min:
                min = value

        diff = max - min
        self.process(diff)

    def process(self, value):
        print(value)

        if not self.pause:
            reactor.callLater(self.delay, self.sample)


if __name__ == '__main__':
    hb = HushBot()
    hb.start()
    reactor.run()