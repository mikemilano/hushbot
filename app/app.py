from twisted.application import service, internet
from twisted.web.server import Site
import random
import yaml
from plugins.playback.playback import Playback
from plugins.espeak.espeak import Espeak
from plugins.minecraft.minecraft import Minecraft
from plugins.hushbot.hushbot import HushBot
from webserver import WebServer
import shared


def getConfig(filepath):
    with open(filepath, 'r') as f:
        config = yaml.load(f)
    return config

# initialize globals
shared.init()
config = shared.config
plugins = shared.plugins

# initialize app
application = service.Application('hushbot')

resource = WebServer()
factory = Site(resource)
internet.TCPServer(8080, factory).setServiceParent(application)

# load main config
config["app"] = getConfig('../config/config.yml')

# Manually load plugins for now
plugins['playback'] = Playback(config)
# random r2 sound to know hushbot has started
num = random.randint(1, 14)
plugins['playback'].play('./assets/audio/r2d2/r2_' + str(num) + '.mp3', True)

plugins['espeak'] = Espeak(config)

config['minecraft'] = getConfig('../config/minecraft.yml')
plugins['minecraft'] = Minecraft(config)

config['hushbot'] = getConfig('../config/hushbot.yml')
plugins['hushbot'] = HushBot(config, plugins)
