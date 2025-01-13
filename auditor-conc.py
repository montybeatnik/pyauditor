import threading
from auditor import get_software, devices

if __name__ == "__main__":
    threads = list()
    for dev in devices:
        thread = threading.Thread(target=get_software, args=(dev,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()