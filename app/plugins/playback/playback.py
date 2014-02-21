#from app.globals import config
from subprocess import Popen


class Playback:
    def __init__(self, config):
        self.config = config["app"]

    def play(self, file, block=False):
        p = Popen(['mpg321', '-o', 'alsa', '--audiodevice', self.config["audio_device"], file])
        if block:
            p.wait()