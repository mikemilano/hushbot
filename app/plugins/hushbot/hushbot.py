from twisted.internet import reactor
import Adafruit_BBIO.ADC as ADC
import random
import time

ADC.setup()


class HushBot():
    def __init__(self, config, plugins):
        self.config = config["hushbot"]
        self.minecraft = plugins["minecraft"]
        self.playback = plugins["playback"]
        self.espeak = plugins["espeak"]

        # hushbot config vars
        self.debug = self.config["debug"]
        self.input_pin = self.config["input_pin"]
        self.autostart = self.config["autostart"]
        self.pause = not self.autostart
        self.delay = int(self.config["sample_delay"])
        self.sample_size = int(self.config["sample_size"])
        self.sample_count = int(self.config["sample_count"])
        self.punish_threshold_1 = float(self.config["punish_threshold_1"])
        self.punish_threshold_2 = float(self.config["punish_threshold_2"])
        self.reward_time_1 = int(self.config["reward_time_1"])
        self.reward_time_2 = int(self.config["reward_time_2"])
        self.reward_time_3 = int(self.config["reward_time_3"])
        self.punishments = self.config["punishments"]
        self.rewards = self.config["rewards"]
        # state vars
        self.loud_count = 0
        self.loud_threshold = 0
        self.quiet_since = time.time()
        self.last_reward_level = 0

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
        deliver_reward_level = None;
        deliver_punishment_level = None;

        # Last sample was below threshold 1
        if value <= self.punish_threshold_1:
            if self.debug:
                print('Level acceptable: ' + str(value))

            #reset loud count and threshold
            self.loud_count = 0
            self.loud_threshold = 0

            since = time.time() - self.quiet_since
            if self.last_reward_level < 1:
                if since >= self.reward_time_1:
                    deliver_reward_level = 1
                    self.last_reward_level = 1

            elif self.last_reward_level < 2:
                if since >= self.reward_time_2:
                    deliver_reward_level = 2
                    self.last_reward_level = 2
            else:
                if since >= self.reward_time_3:
                    deliver_reward_level = 3
                    # reset quiet since time
                    self.quiet_since = time.time()
                    self.last_reward_level = 0

        # Last sample was above threshold 1
        else:
            # reset quiet since time
            self.quiet_since = time.time()
            self.last_reward_level = 0

            # test/set loud count
            self.loud_count += 1
            punishment_level = 0

            # set top threshold achieved for this set
            if value < self.punish_threshold_2:
                punishment_level = 1
                if self.debug:
                    print('Level 1 threshold exceeded: %r' % value)
                if self.loud_threshold < 1:
                    self.loud_threshold = 1
            else:
                punishment_level = 2
                if self.debug:
                    print('Level 2 threshold exceeded: %r' % value)

                if self.loud_threshold < 2:
                    self.loud_threshold = 2

            # collect another sample if the sample_count hasn't been reached
            if self.loud_count < self.sample_count:
                if self.debug:
                    print('Sample count not yet met: %r of %r' % (self.loud_count, self.sample_count))
            else:
                deliver_punishment_level = punishment_level

        # set default delay
        delay = self.delay

        if deliver_reward_level is not None:
            # deliver the reward
            delay = self.deliver_reward(deliver_reward_level)

        elif deliver_punishment_level is not None:
            # deliver the pain
            delay = self.deliver_punishment(deliver_punishment_level)
            self.loud_count = 0

        if not self.pause:
            reactor.callLater(delay, self.sample)

    def deliver_reward(self, level):
        level = 'level'+str(level)
        data = self.rewards[level][random.choice(self.rewards[level].keys())]
        self.issue_commands(data)
        if 'delay' in data:
            return int(data['delay'])
        return 30

    def deliver_punishment(self, level):
        level = 'level'+str(level)
        data = self.punishments[level][random.choice(self.punishments[level].keys())]
        self.issue_commands(data)
        if 'delay' in data:
            return int(data['delay'])
        return 30

    def issue_commands(self, data):
        if 'say' in data:
            self.minecraft.rcon.send('/say "' + data['say'])
            self.espeak.say(data['say'])
        if 'rcon' in data:
            for cmd in data['rcon']:
                self.minecraft.rcon.send(cmd)
        if 'sounds' in data:
            for file in data['sounds']:
                self.playback.play(file)

if __name__ == '__main__':
    hb = HushBot()
    hb.start()
    reactor.run()