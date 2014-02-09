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
