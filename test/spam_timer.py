import threading

import time

count = 0

def loop():
    while True:
        time.sleep(0.1)
        print(threading.get_ident())

for i in range(0, 100):
    threading.Thread(target=loop).start()

print("Starting timer spam")
while True:
    count += 1
    try:
        threading.Timer(0.3, lambda: None).start()
    except:
        print("Hier fout", count)
        raise Exception("kaput")