### BeagleBone Black Board Setup

```
# As root
sudo ntpdate pool.ntp.org
sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus python-twisted -y
# Adafruit BBIO needs a newer version of distribute
sudo easy_install -U distribute
sudo pip install Adafruit_BBIO
```
