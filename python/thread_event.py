import time
import threading

one = threading.Event()
two = threading.Event()
done = threading.Event()

def longProcess():
    for i in range(10000):
        time.sleep(0.001)
        if i > 3333:
            one.set()
        if i > 6666:
            two.set()
    done.set()

threadWork = threading.Thread(target=longProcess)
threadWork.start()

# Wait for various events
one.wait()
print('One done!')

two.wait()
print('Two done!')

done.wait()
print('Done!')
