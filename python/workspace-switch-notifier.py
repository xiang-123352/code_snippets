#!/usr/bin/env python3

from gi.repository import Wnck, Gtk, Notify
import signal, time

class Kludge:
    def __init__(self):
        self.first = True
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.screen = Wnck.Screen.get_default()
        Notify.init("Workspace Switch Notifier")

    def fire_the_kludge(self, data_a, data_b):
        time.sleep(.1)
        try:
            workspace_num = str(self.screen.get_active_workspace().get_number())
        except:
            workspace_num = "Some error happened"
        popup = Notify.Notification.new("Workspace: " + workspace_num)
        popup.show()
        time.sleep(1)
        popup.close()

    def main(self):
        self.screen.connect("active-workspace-changed", self.fire_the_kludge)
        Gtk.main()

if __name__ == '__main__':
    print("Here comes the kludge")
    kludge = Kludge()
    kludge.main()
