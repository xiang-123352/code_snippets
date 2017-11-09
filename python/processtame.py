import os
import sys
import win32process
import win32api
import subprocess
import win32con
def setpriority(pid=None,priority=1):
	priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
	win32process.BELOW_NORMAL_PRIORITY_CLASS,
	win32process.NORMAL_PRIORITY_CLASS,
	win32process.ABOVE_NORMAL_PRIORITY_CLASS,
	win32process.HIGH_PRIORITY_CLASS,
	win32process.REALTIME_PRIORITY_CLASS]
	if pid == None:
	        pid = win32api.GetCurrentProcessId()
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
        win32process.SetPriorityClass(handle, priorityclasses[priority])
if (len(sys.argv) == 0):
    print("usage: processtame.exe ")
else:
    if (os.path.exists(sys.argv[1])):
    app = subprocess.Popen(sys.argv[1])
    pid = app.pid
    setpriority(pid, 0)
    app.wait()
