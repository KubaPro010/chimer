import datetime
import time
import subprocess
import arrow, ntplib
import pytz
import sys
DEVICE = "2"

def get_time():
    return arrow.now(tz=pytz.timezone("Europe/Warsaw")).timestamp()

def new_hr(hr: int, hh: bool):
    if not hh:
         command = f"mpg123 -o pulse -a {DEVICE} -q --mono gts.mp3"
         subprocess.run(command, shell=True)
    else:
         subprocess.run(f"mpg123 -o pulse -a {DEVICE} -q --mono gts_4pips.mp3", shell=True)

if len(sys.argv) > 1:
    try:
        OFFSET = int(sys.argv[1])
    except ValueError:
        print("Invalid offset. Using the default offset of 0.")
        OFFSET = 0
else:
    OFFSET = 0

print(f"Beeps should run at {55 + OFFSET} and {56 + OFFSET} (offset: {OFFSET})")
def get_ntp_time(server="tempus1.gum.gov.pl"):
    client = ntplib.NTPClient()
    response = client.request(server)
    return response.tx_time
print(f"Time Diffrence: {get_ntp_time() - datetime.datetime.fromtimestamp(get_time()).timestamp()}")
while True:
    now = datetime.datetime.fromtimestamp(get_time())
    hr = now.hour
    min = now.minute
    sec = now.second

    if (min == 59 and sec == (55 + OFFSET)) or (min == 29 and sec == (56 + OFFSET)):
        print(f"Time Diffrence: {get_ntp_time() - now.timestamp()}")
        print(f"################################".replace("#", " "), end="\r")
        print("beeping...",end="\r")
        new_hr((hr + 1) % 24, (min == 29))
        print(f"beep {hr} {min}")
    print(f"################################".replace("#", " "), end="\r")
    print(f"{hr:02d}:{min:02d}:{sec:02d}.{(now.microsecond // 1000):03d}", end="\r")

    time.sleep(0.001)  # Sleep for a second to avoid a busy wait
