#!/usr/bin/python
#
# mythtv-mouse2kbd.py - Convert mouse movements into key presses
#
# Roman Yepishev <roman.yepishev@ubuntu.com>
# Public domain. Feel free to do whatever you want with the code.
#
# USAGE: Run this script in the session where MythTV is running.
#
# See http://rtg.in.ua/2012/10/19/mythtv-and-mce-remote-mouse-emulation/

import sys
try:
    from Xlib import display, X, XK
    from Xlib.ext.xtest import fake_input
    from Xlib.error import BadWindow
except ImportError:
    print "This script requires python-xlib package to run."
    sys.exit(1)

import time
import select

class App(object):
    """Application for translating mouse movements into keypresses"""
    DEFAULT_POINTER_X = 320
    DEFAULT_POINTER_Y = 240
    REPEAT_DELAY = 0.2 # in seconds

    def __init__(self):
        print "Initializing..."
        self.display = display.Display()
        self.screen = self.display.screen()

        self.root_window = self.screen.root

        self.is_grabbed = False

        self.last_event_x = 0
        self.last_event_y = 0

        self.last_keysym = None
        self.last_event_time = 0

        self.key_codes = {
            'XK_Up': None,
            'XK_Down': None,
            'XK_Left': None,
            'XK_Right': None,
            'XK_Return': None,
            'XK_Escape': None,
        }

        for key in self.key_codes.keys():
            code = self.display.keysym_to_keycode(getattr(XK, key))
            self.key_codes[key] = code

    def grab_pointer(self):
        if not self.is_grabbed:
            self.root_window.grab_pointer(1,
                    X.ButtonPressMask | X.ButtonReleaseMask | X.PointerMotionMask,
                    X.GrabModeAsync,
                    X.GrabModeAsync,
                    X.NONE, X.NONE,
                    X.CurrentTime)
            print "Pointer grabbed"
            self.is_grabbed = True

    def ungrab_pointer(self):
        if self.is_grabbed:
            self.display.ungrab_pointer(X.CurrentTime)
            print "Pointer released"
            self.is_grabbed = False

    def fake_press(self, keysym):
        """Perform fake KeyPress"""
        current_time = time.time()
        if self.last_keysym == keysym:
            if (current_time - self.last_event_time) < App.REPEAT_DELAY:
                return

        self.last_keysym = keysym
        self.last_event_time = current_time

        fake_input(self.display, X.KeyPress, self.key_codes[keysym])
        fake_input(self.display, X.KeyRelease, self.key_codes[keysym])

        self.display.sync()

    def reset_pointer(self):
        """Reset pointer so that it does not run away"""
        self.root_window.warp_pointer(App.DEFAULT_POINTER_X,
                                      App.DEFAULT_POINTER_Y)
        self.display.sync()

    def handle_event(self, event):
        """Handle actual X event"""
        if event.type == X.ButtonPress:
            key = event.detail
            if key == 1:
                self.fake_press('XK_Return')
            elif key == 3:
                self.fake_press('XK_Escape')
        elif event.type == X.ButtonRelease:
            pass
        elif event.type == X.MotionNotify:
            current_event_x = event.event_x
            current_event_y = event.event_y

            # Our default coordinates, can be ignored
            if (current_event_x == App.DEFAULT_POINTER_X and
                    current_event_y == App.DEFAULT_POINTER_Y):
                return

            delta_y = abs(current_event_y - App.DEFAULT_POINTER_Y)
            delta_x = abs(current_event_x - App.DEFAULT_POINTER_X)

            if delta_y > delta_x:
                if current_event_y > App.DEFAULT_POINTER_Y:
                    self.fake_press("XK_Down")
                elif current_event_y < App.DEFAULT_POINTER_Y:
                    self.fake_press("XK_Up")
            else:
                if current_event_x < App.DEFAULT_POINTER_X:
                    self.fake_press("XK_Left")
                elif current_event_x > App.DEFAULT_POINTER_X:
                    self.fake_press("XK_Right")

            self.reset_pointer()

    def run(self):
        print "Ready to process events"
        while True:
            try:
                readable, w, e = select.select([self.root_window.display],
                                            [], [], 1)

                if not readable:
                    # Timeout, time to check for a foreground window
                    prop = self.root_window.get_full_property(
                            self.display.intern_atom('_NET_ACTIVE_WINDOW'),
                            X.AnyPropertyType)

                    if prop is None:
                        # No active window
                        continue

                    window_id = prop.value[0]
                    window = self.display.create_resource_object('window', window_id)
                    if window.get_wm_name() == "MythTV Frontend":
                        self.grab_pointer()
                    else:
                        self.ungrab_pointer()
                    continue
                elif self.root_window.display in readable:
                    i = self.root_window.display.pending_events()
                    for e in range(i):
                        event = self.root_window.display.next_event()
                        self.handle_event(event)
            except BadWindow:
                pass 
            except Exception, e:
                print >> sys.stderr, "Exiting on %s" % (e, )
                break

if __name__ == "__main__":
    app = App()
    app.run()
