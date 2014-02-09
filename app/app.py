from twisted.application import service, internet
from twisted.web.server import Site

import random
from subprocess import Popen
import yaml

from plugins.minecraft.minecraft import Minecraft
from plugins.hushbot.hushbot import HushBot
from webserver import WebServer


def getConfig(filepath):
    with open(filepath, 'r') as f:
        config = yaml.load(f)
    return config


application = service.Application('hushbot')

resource = WebServer()
factory = Site(resource)
internet.TCPServer(8080, factory).setServiceParent(application)



# load main config
app_config = getConfig('../config/config.yml')
plugins = {}

# Play random r2 sound
num = random.randint(1, 14)
p = Popen(['mpg321', '-o', 'alsa', '--audiodevice', app_config["audio_device"], './assets/audio/r2d2/r2_' + str(num) + '.mp3'])
# block
p.wait()

# Manually load plugins for now
mc_config = getConfig('../config/minecraft.yml')
plugins['minecraft'] = Minecraft(mc_config)

hb_config = getConfig('../config/hushbot.yml')
plugins['hushbot'] = HushBot(app_config, hb_config, plugins['minecraft'])


