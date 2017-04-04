#!/usr/bin/env python
import i3ipc
from ewmh import EWMH
import subprocess
 
# process all windows on this workspace. hide when leaving and show when entering
# because chrome/ium doesnt consider itself hidden when on an invisible workspace
# this script drops my cpu usage when listening to google music from ~10% to ~3% 
 
MUSIC_WS_INDEX = 6
 
SHOWN = '_NET_WM_STATE_SHOWN'
HIDDEN = '_NET_WM_STATE_HIDDEN'
 
def toggleWindowState(window):
    state = ewmh.getWmState(window, True)
    if SHOWN in state or not state:
        print "HIDING"
         
        subprocess.call(["xprop", "-id", str(window.id), "-f",
        "_NET_WM_STATE", "32a", "-set", "_NET_WM_STATE", HIDDEN])
         
        #ewmh.setWmState(window, 1, HIDDEN)
    if HIDDEN in state:
        print "SHOWING"
         
        subprocess.call(["xprop", "-id", str(window.id), "-f", 
        "_NET_WM_STATE", "32a", "-set", "_NET_WM_STATE", SHOWN])
 
        #ewmh.setWmState(window, 0, HIDDEN)
         
    # ewmh.display.flush()
    # why didnt ewmh work? idk...
 
def process_window(window):
    print "Processing window: %s (%d)" % (window.name, window.window)
    # already hidden?
    w = ewmh.display.create_resource_object('window', window.window)
    toggleWindowState(w)
 
 
def onWorkspace(i3, event):
    if event.change in ['focus']:
        # maybe in the future I will check the workspace event for enter/leave
        windows = i3.get_tree().leaves()
        for window in windows:
            if window.workspace().num == MUSIC_WS_INDEX:
                # maybe in the future I will check the workspace event for enter/leave
                # instead of just toggling the state
                process_window(window)
 
 
ewmh = EWMH()
i3 = i3ipc.Connection()
 
i3.on('workspace', onWorkspace)
i3.main()
