"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import json


N: int = 10 # Changed from 3 to 10 to run 10 cycles
sample_ms = 10.0
on_ms = 500


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
    """Writes data to a JSON file.

    Parameters
    ----------

    json_filename: str
        The name of the file to write to. This will overwrite any existing file.

    data: dict
        Dictionary data to write to the file.
    """

    with open(json_filename, "w") as f:
        json.dump(data, f)


def scorer(t: list[int | None]) -> None:
    # %% collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    print(t_good)
    
    oauth_token = "ya29.c.c0ASRK0GbKCZpCudtNl5nwt453RIDiI-MRdg0sIVDDdFXdF5pp8CC3C_HJvCZQLclz4hrzUtb62p1sDqBj4Y2Nk1VXEEI0iCGla62v5Atb02hgMbn461GgEEYlD6V7hUSg1PWDvS7T5NfikSrQdK32e7OhmtRfv42cBIWXBzc8gTXRjeh3VMZR7XRLVy53m91Pf5HtljQxqq8dpW9zQqnGdaOSkaN1BtVbmnYn1KBhzb-k5nKI6glzHfhfgQTPh4_Lv_opog5QW1q5zUF1tUR8YAVuUVLayRPgUzX09T8b4_-l-LdN6DoZuXOAuGo0IfM5cloW7qwpX1-eAhKbW9Bw53bmKAJb0YVuZOXjGKLOw1RVNv4yf9dQybe0N385P_fZIcZ75uUo1ws_c8ebIkpX4pwR6XWkzXrUV4kV2xejmY10XWdxujS513XcuOu91h2O-o6i--zjdRo_ccp0nuUOnS33yrunXkFoQxxZUiaWiVU1BwX16nikR5mpXQp1JWFMSfRq5XbQ21obay26S16f-0dzi2jJSQwietoJ2l3Vve9gckQm0bVSb9pR-mcJMQRI48kxJdwdWx4k5ObajvogsQafmxacMtol46nYd1stsQxbfUaXvy0Rt5eU9W1kB4aWOYJyW8kp2Ozo6rd3dUy11mraJQr_IyhFJ6Mcx-m_6c8tg4_cUeVjjgczf9fnpncdbgJv8q2m4ZUdX0Ymtjrltf-rRn7jxqjd99m6gJXUi-fc0-I_SZnxjQeahtcaktRYxzuSjW1BVwo7z--SJ-5isZjnO4_k27Wm-i4QXdbh9BU0nc-vY041hkt8F1zlqdBjrbeo-XdI3RYiOZscFupb3o6pRqfSZ4a86RRtx8amMOeQWIcM_X58Ve4SgpxMtrSZ-vS6xYpfptIJ_V9ZS2wnXbX-QRIWd5rXb3mV0nmx-fu5Q_nWqiQJ4nsxupn3Xh70jkoscUicgeZcZI660o36FB_bXdmdd3jlutgb9347osqVZpkiFJId6fn"
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

    now: tuple[int] = time.localtime()

    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"

    print("write", filename)

    write_json(filename, data)


if __name__ == "__main__":
    # using "if __name__" allows us to reuse functions in other script files

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
