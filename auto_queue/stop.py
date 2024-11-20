import sys
import time

from auto_queue.config import LOG_FILE
from log import log


def stop(start_time, t_sum, success_count, failure_count):
    running_time = time.time() - start_time
    running_hours, remainder = divmod(running_time, 3600)
    running_minutes, running_seconds = divmod(remainder, 60)

    time_str = f"{int(running_hours):02d}h {int(running_minutes):02d}min {int(running_seconds):02d}s"

    t_avg = t_sum / success_count if success_count else 0
    t_avg_str = f"{t_avg:.3f} s"

    log(LOG_FILE, "Stopped queuing")
    log(LOG_FILE, f"Running Time: \x1b[36m{time_str}\x1b[0m")
    log(LOG_FILE, f"Successful Queues: \x1b[36m{success_count}\x1b[0m")
    log(LOG_FILE, f"Failed Queues: \x1b[36m{failure_count}\x1b[0m")
    log(LOG_FILE, f"Average Time of Successful Queues: \x1b[36m{t_avg_str}\x1b[0m")

    sys.exit()
