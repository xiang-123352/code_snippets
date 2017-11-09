import Tkinter as tk
from queue import Queue, Empty

def idle_add(callable, *args):
    '''Call this with a function and optional arguments, and that function
       will be called on the GUI thread via an event.
       
       This function returns immediately.
    '''
    queue.put((callable, args))
    root.event_generate('<<Idle>>', when='tail')
    
def _on_idle(event):
    '''This should never be called directly, it is called via an 
       event, and should always be on the GUI thread
    '''
    while True:
        try:
            callable, args = queue.get(block=False)
        except queue.Empty:
            break
        callable(*args)
        
queue = Queue()
root = tk.Tk()
root.bind('<<Idle>>', _on_idle)
