#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

import machine
import utime

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))


def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(1000)
    speaker.freq(frequency)
    utime.sleep(duration)


def quiet():
    speaker.duty_u16(0)


freq: float = 30
duration: float = 0.1  # seconds

print("Playing frequency (Hz):")

# for i in range(64):
#    print(freq)
#    playtone(freq, duration)
#    freq = int(freq * 1.1)


playtone(370,.4)
playtone(440,.4)
playtone(554,.5)
playtone(440,.6)
playtone(370,.4)
playtone(294,.3)
playtone(15,.05)
playtone(294,.3)
playtone(15,.05)
playtone(294,.3)


playtone(554,.5)
playtone(294,.3)
playtone(370,.4)
playtone(440,.4)
playtone(554,.5)
playtone(440,.4)
playtone(370,.4)
playtone(330,.4)
playtone(311,.4)
playtone(294,.3)





# Turn off the PWM
quiet()
