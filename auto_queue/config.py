import json
import os
import re

with open("config.json", 'r', encoding='UTF-8') as cfg_file:
    cfg_data = json.load(cfg_file)

    # Minecraft log
    MINECRAFT_LOG_ENCODING = cfg_data["minecraft_log"]["encoding"]
    preset = cfg_data["minecraft_log"]["preset"]
    path = cfg_data["minecraft_log"]["presets"][preset]["path"]
    MINECRAFT_LOG_FILE = os.path.expanduser(path) + "\\latest.log"

    # log
    LOG_FILE = "auto_queue.log"

    # queue
    QUEUE_COMMANDS = []
    for category, commands in cfg_data['queue']['commands'].items():
        for command, is_enabled in commands.items():
            if is_enabled:
                QUEUE_COMMANDS.append(command)
    TIMEOUT = cfg_data["queue"]["timeout"]

    # shout
    # Hypixel will kick you if you shout more than 100 characters even if you are on 1.11+
    ENABLE_SHOUT = cfg_data['shout']['enabled']
    SHOUT_MESSAGES = []
    for message in cfg_data['shout']['messages']:
        SHOUT_MESSAGES.append(message)

    # key
    GAME_STARTS_SOON_KEY = cfg_data['keys']['game_starts_soon']
    GAME_STARTS_KEY = cfg_data['keys']['game_starts']
    IS_MUTED_KEY = cfg_data['keys']['is_muted']
    COMMAND_KEY = cfg_data['keys']['command']
    STOP_KEY = re.sub("%s", "--stop", COMMAND_KEY)  # type "/w --stop" to stop queue
    REQUEUE_KEY = re.sub("%s", "--rq", COMMAND_KEY)  # type "/w --rq" to re-queue
