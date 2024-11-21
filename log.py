import re
import time

from pynput import keyboard

keyboard_controller = keyboard.Controller()


def log(log_file, message):
    timestamp = time.strftime("%y-%m-%d %X", time.localtime())
    log_message = f"[{timestamp}] {message}"
    print(log_message)

    sanitized_message = re.sub(r"\x1b\[[0-9]{,2}m", "", log_message)

    try:
        with open(log_file, 'a', encoding='UTF-8') as log_file:
            log_file.write(sanitized_message + '\n')
    except Exception as e:
        print(e)
