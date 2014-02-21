#from app.globals import config
from subprocess import Popen, PIPE


class Espeak:
    def __init__(self, config):
        self.config = config["app"]
        pass

    def say(self, str, block=True):
        p1 = Popen(['espeak', str, '--stdout'], stdout=PIPE)
        p2 = Popen(['aplay', '-D', self.config['audio_device']], stdin=p1.stdout)
        p1.stdout.close()
        #output = p2.communicate()[0]
        if block:
            p2.wait()