import time

from auto_queue.auto_queue import auto_queue, LOG_FILE

if __name__ == '__main__':
    time.sleep(2)
    try:
        with open(LOG_FILE, 'r+', encoding='utf-8') as file:
            content = file.read()
            if content.strip():
                file.seek(0, 2)
                file.write("\n\n")
    except Exception as e:
        log(e)
    auto_queue()
