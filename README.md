### BeagleBone Black Board Setup

```
sudo ntpdate pool.ntp.org
sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus python-twisted \
python-zmq libzmq-dev python-yaml alsa-base alsa-utils alsa-oss mpg321  libmpg123-0 espeak -y

# Adafruit BBIO needs a newer version of distribute
sudo easy_install -U distribute
sudo pip install Adafruit_BBIO txzmq
```

You must run the app as root due to serial communication.

```
git clone git@github.com:mikemilano/hushbot.git
cd hushbot
cp app/plugins/hushbot/hushbot.default.yml config/hushbot.yml
cp app/plugins/minecraft/minecraft.default.yml config/minecraft.yml
sudo bin/start.sh
```

Logs will be written to the `log` directory and the process ID file will be written to the `run` directory.