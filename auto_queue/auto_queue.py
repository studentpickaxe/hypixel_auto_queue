import random
import time

import pyautogui
import pyperclip
from pynput import keyboard

from auto_queue.config import *
from auto_queue.stop import stop
from log import log

keyboard_ctrl = keyboard.Controller()


def auto_queue():
    def read_mc_log():
        return minecraft_log_file.read()

    def queue():
        minecraft_log_file.seek(0, 2)

        # /
        keyboard_ctrl.press('/')
        time.sleep(0.05)
        keyboard_ctrl.release('/')

        # cmd
        game = random.choice(QUEUE_COMMANDS)
        pyautogui.typewrite(game)

        # enter
        keyboard_ctrl.press(keyboard.Key.enter)
        time.sleep(0.05)
        keyboard_ctrl.release(keyboard.Key.enter)

        time.sleep(0.2)

        for j in range(9):
            new_lines = read_mc_log()
            if STOP_KEY in new_lines:
                stop(start_time, t2, success_count, failure_count)
            if re.findall(r" \[CHAT] \w+ has joined \((\d+)/(\d+)\)!", new_lines):
                matches = re.findall(r" \[CHAT] \w+ has joined \((\d+)/(\d+)\)!", new_lines)
                break
            if j == 8:
                log(LOG_FILE, "Failed to queue a game! Trying again in 3 seconds...")
                for _ in range(6):
                    new_lines = read_mc_log()
                    if STOP_KEY in new_lines:
                        stop(start_time, t2, success_count, failure_count)
                    time.sleep(0.5)
                queue()
                return
            time.sleep(0.2)

        current_players, max_players = matches[-1]
        if int(current_players) * 3 < int(max_players):
            log(LOG_FILE, "Too few players! Trying again in 5 seconds...")
            for _ in range(10):
                new_lines = read_mc_log()
                if STOP_KEY in new_lines:
                    stop(start_time, t2, success_count, failure_count)
                time.sleep(0.5)
            queue()
            return

        log(LOG_FILE, "Successfully auto queued a game")

    log(LOG_FILE, "Started auto queue")

    success_count = 0
    failure_count = 0
    i = 0

    t1 = time.time()
    t2 = 0
    start_time = time.time()

    with open(MINECRAFT_LOG_FILE, 'r', encoding='UTF-8', errors='ignore') as minecraft_log_file:
        minecraft_log_file.seek(0, 2)

        queue()

        while True:
            new_lines = read_mc_log()

            if STOP_KEY in new_lines:
                stop(start_time, t2, success_count, failure_count)

            if GAME_STARTS_SOON_KEY in new_lines:
                i += 1
                log(LOG_FILE, "A game will start soon...")

            if REQUEUE_KEY in new_lines:
                log(
                    LOG_FILE,
                    "(\x1b[36m{0:.3f} s\x1b[0m) Re-queuing...".format(
                        time.time() - t1,
                    )
                )

                queue()
                i = 0
                t1 = time.time()
                continue

            if GAME_STARTS_KEY in new_lines:
                success_count += 1
                log(
                    LOG_FILE,
                    "(\x1b[36m{0:.3f} s\x1b[0m) Game \x1b[36m#{1}\x1b[0m started".format(
                        time.time() - t1,
                        success_count,
                    )
                )
                t2 += time.time() - t1

                if ENABLE_SHOUT:
                    shout(success_count)

                new_lines = read_mc_log()
                if ENABLE_SHOUT and IS_MUTED_KEY in new_lines:
                    log(LOG_FILE, "You have been muted and cannot shout anymore! Stopping...")
                    stop(start_time, t2, success_count, failure_count)
                if STOP_KEY in new_lines:
                    stop(start_time, t2, success_count, failure_count)
                queue()
                i = 0
                t1 = time.time()
                continue

            if time.time() > t1 + TIMEOUT and i != 1:
                failure_count += 1
                log(
                    LOG_FILE,
                    "(\x1b[36m{0:.3f} s\x1b[0m) Timed out! Trying again...".format(
                        time.time() - t1,
                    )
                )

                new_lines = read_mc_log()
                if STOP_KEY in new_lines:
                    stop(start_time, t2, success_count, failure_count)
                queue()
                i = 0
                t1 = time.time()


def shout(i):
    time.sleep(0.3)

    # /
    keyboard_ctrl.press('/')
    time.sleep(0.05)
    keyboard_ctrl.release('/')

    time.sleep(0.05)

    # msg
    msg = f"shout {SHOUT_MESSAGES[(i - 1) % len(SHOUT_MESSAGES)]} #{i}"
    pyperclip.copy(msg)
    keyboard_ctrl.press(keyboard.Key.ctrl)
    keyboard_ctrl.press('v')
    time.sleep(0.05)
    keyboard_ctrl.release('v')
    keyboard_ctrl.release(keyboard.Key.ctrl)

    time.sleep(0.05)

    # enter
    keyboard_ctrl.press(keyboard.Key.enter)
    keyboard_ctrl.release(keyboard.Key.enter)

    time.sleep(0.3)
