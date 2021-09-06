import dataclasses
import datetime

from typing import Tuple

@dataclasses.dataclass
class Date:
    day:int
    hour:int
    minutes:int
    seconds:int

import time
t0 = time.time()
def get_cpu_temp() -> Tuple[str, float]:
    cpu_temp_file = '/sys/class/thermal/thermal_zone0/temp'
    try:
        with open(cpu_temp_file, 'r') as f:
            temp = int(f.readline()) / 1000
    except FileNotFoundError as e:
        temp = 10
    now = datetime.datetime.now()
    #return  dataclasses.asdict(Date(now.date, now.hour, now.minute, now.second)), temp
    return time.time()-t0, temp
