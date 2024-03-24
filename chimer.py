import datetime
import time
import subprocess
import arrow, ntplib
import pytz
import sys
DEVICE = "2"
TIMESERVER = "tempus1.gum.gov.pl" #polish goverment ntp
COMMAND = "mpg123 -o pulse -a {} -q --mono {}"

def get_time(): return arrow.now(tz=pytz.timezone("Europe/Warsaw")).timestamp()

def new_hr(hr: int, hh: bool):
    if not hh: subprocess.run(COMMAND.format(DEVICE, "5sec.mp3"), shell=True)
    else: subprocess.run(COMMAND.format(DEVICE, "4sec.mp3"), shell=True)

if len(sys.argv) > 1:
    try:
        OFFSET = int(sys.argv[1])
        _OFFSET = int(sys.argv[1])
    except ValueError:
        print("Invalid offset. Using the default offset of 0.")
        OFFSET = 0
        _OFFSET = 0
else:
    OFFSET = 0
    _OFFSET = 0

print(f"Beeps should run at {55 + OFFSET} and {56 + OFFSET} (offset: {OFFSET})")
def get_ntp_req(server): 
    return ntplib.NTPClient().request(server)
leapsec = get_ntp_req(TIMESERVER)
if leapsec == 0:
    print("We have no leap seconds today.")
elif leapsec == 1:
    print("Today's last minute has 61 seconds.")
elif leapsec == 2:
    print("Today's last minute has 59 seconds.")
print(f"Time Diffrence: {get_ntp_req(TIMESERVER).tx_time - datetime.datetime.fromtimestamp(get_time()).timestamp()}")
while True:
    now = datetime.datetime.fromtimestamp(get_time())
    hr = now.hour
    min = now.minute
    sec = now.second
    if hr == 0 and min == 0 and sec == 1: #new day
        leapsec = get_ntp_req(TIMESERVER)
        if leapsec == 0:
            OFFSET = _OFFSET
            print(f"We have no leap seconds today. Adjusting offset to {OFFSET}")
        elif leapsec == 1:
            OFFSET = _OFFSET + 1
            print(f"Today's last minute has 61 seconds. Adjusting offset to {OFFSET}")
        elif leapsec == 2:
            OFFSET = _OFFSET - 1
            print(f"Today's last minute has 59 seconds. Adjusting offset to {OFFSET}")
        else:
            OFFSET = _OFFSET
            print(f"Don't know about the leap sec, adjusting offset to {OFFSET}")
    elif now.day == 31 and now.month == 12 and hr == 23 and min == 59 and sec == (30 + OFFSET):
        print("Happy new year, operator!")
        print(f"Time Diffrence: {get_ntp_req(TIMESERVER).tx_time - now.timestamp()}")
        print(f"################################".replace("#", " "), end="\r")
        print("beeping...",end="\r")
        subprocess.run(COMMAND.format(DEVICE, "30sec.mp3"), shell=True)
        print(f"beep {hr} {min}")
    elif (min == 59 and sec == (55 + OFFSET)) or (min == 29 and sec == (56 + OFFSET)):
        print(f"Time Diffrence: {get_ntp_req(TIMESERVER).tx_time - now.timestamp()}")
        print(f"################################".replace("#", " "), end="\r")
        print("beeping...",end="\r")
        new_hr((hr + 1) % 24, (min == 29))
        if min == 29: print(f"beep {hr} {min+1} 4 pips")
        else min == 0: print(f"beep {hr} {min} 5 pips")
    print(f"################################".replace("#", " "), end="\r")
    print(f"{hr:02d}:{min:02d}:{sec:02d}", end="\r")
    time.sleep(0.2)
