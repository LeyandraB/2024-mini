"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import json
import sys
import urequests
import network


N: int = 10 # Changed from 3 to 10 to run 10 cycles
sample_ms = 10.0
on_ms = 500

DB_url = "https://miniproject-7042f-default-rtdb.firebaseio.com/"


def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    # %% let user know game started / is over

    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
    jason = json.dumps(data)
    
    """Writes data to a JSON file.

    Parameters
    ----------

    json_filename: str
        The name of the file to write to. This will overwrite any existing file.

    data: dict
        Dictionary data to write to the file.
    """
    request = urequests.put(DB_url + json_filename, headers = {}, data = jason)  #Sends file 
    print(request.text) #Prints what was sent
    

    with open(json_filename, "w") as f:
        json.dump(data, f)


def scorer(t: list[int | None]) -> None:
    # %% collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    print(t_good)
    
    # add key, value to this dict to store the minimum, maximum, average response time
    # and score (non-misses / total flashes) i.e. the score a floating point number
    # is in range [0..1]
    data = {
        "MinRespTime": min(t_good),
        "MaxRespTime": max(t_good),
        "AvgRespTime": (sum(t_good) / len(t_good)),
        "Score": 1- misses / len(t)
    }

    # %% make dynamic filename and write JSON
    print(data)

    now: tuple[int] = time.localtime()

    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"

    print("write", filename)

    write_json(filename, data)
    
def connect():  #Checks for connection or connects
    ssid="Ley"
    password="BlueBlackPurple"
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    max_wait = 100
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >=3:
            print(str(wlan.status()))
            break
        max_wait -= 1
        print('waiting for connection')
        time.sleep(1)

     # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )

        
               

if __name__ == "__main__":
    # using "if __name__" allows us to reuse functions in other script files

    connect() #Make sure its connected to the internet
    
    led = Pin("LED", Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []

    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5, led)

    scorer(t)




