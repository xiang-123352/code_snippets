#!/bin/env python
# vim:fileencoding=iso-8859-1:ft=python
"""
	Try to guess a network configuration
	Copyright (c) Phillip Berndt, 2006
"""
import gtk, gtk.glade, os, sys, re, threading, random, base64, bz2

# The IP-testing part
def testIP(subnet):
	dev = glade.get_widget("interface").get_active_text()
	time = int(glade.get_widget("time").get_active_text())

	for ipEnding in random.sample(range(5, 254), time + 1):
		ip = ".".join((subnet, str(ipEnding)))
		setStatus(info=ip)
		if os.system("ifconfig %s %s up" % (dev, ip)) is not 0:
			gtk.threads_enter()
			errMessage = "You don't have permission to change the IP of device %s.\n" % dev + \
				"Please run this application as super user. I will now exit..."
			msgBox = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format=errMessage)
			msgBox.show()
			msgBox.run()
			msgBox.destroy()
			gtk.main_quit()
			gtk.threads_leave()
			return True
		for routerEnding in [1, 2]:
			if "doStopScan" in globals():
				return True
			ip = ".".join((subnet, str(routerEnding)))
			if os.system("arping -qfw %d -I %s %s >/dev/null" % (time, dev, ip)) is 0:
				addLog("\nThe subnet %s seems to have a router at %s" % (subnet, ip))
				return True
	return False

def testIPs():
	addLog(None)
	addLog("Warning: This script assumes that you search for a /24 network.")
	# Try some default configurations first
	addLog("Testing for common network configurations")
	defaults = [ "192.168.1", "192.168.0", "192.168.2", "192.168.178", "10.0.0" ]
	for subnet in range(len(defaults)):
		if "doStopScan" in globals():
			addLog("Canceled")
			return
		setStatus(1.0 * subnet / len(defaults), "%s.*" % defaults[subnet])
		if testIP(defaults[subnet]):
			stopScan(None)
			return

	# Try the 192.168.0.0/16 network
	addLog("Testing for 192.168.0.0/16")
	for subnet in range(255):
		if "doStopScan" in globals():
			addLog("Canceled")
			return
		setStatus(1.0 * subnet / 255, "192.168.%s.*" % subnet)
		if testIP("192.168.%s" % subnet):
			stopScan(None)
			return

	# Try the 169.254.0.0/16 network
	addLog("Testing for 169.254.0.0/16 (Windows autoconfiguration standard)")
	for subnet in range(255):
		if "doStopScan" in globals():
			addLog("Canceled")
			return
		setStatus(1.0 * subnet / 255, "169.254.%s.*" % subnet)
		if testIP("169.254.%s" % subnet):
			stopScan(None)
			return

	# Try the 172.16.0.0/12 network
	addLog("Testing for 172.16.0.0/12")
	for subnet1 in range(16, 32):
		for subnet2 in range(255):
			if "doStopScan" in globals():
				addLog("Canceled")
				return
			setStatus(1.0 * ((subnet1 - 16) * 255 + subnet) / (255 * (32-16)), "172.%d.%d.*" % (subnet1, subnet2))
			if testIP("172.%d.%d" % (subnet1, subnet2)):
				stopScan(None)
				return
	
	# Try the 10.0.0.0/8 network
	addLog("Testing for 10.0.0.0/8 (This one is very large and could take you more than 4 and a half day)")
	for subnet1 in range(255):
		for subnet2 in range(255):
			if "doStopScan" in globals():
				addLog("Canceled")
				return
			setStatus(1.0 * (subnet1 * 255 + subnet2) / (255**2), "10.%d.%d.*" % (subnet1, subnet2))
			if testIP("10.%d.%d" % (subnet1, subnet2)):
				stopScan(None)
				return
	
	addLog("\nSorry - I didn't find any networks")
	return False

# Useful GTK functions (Only to be called from a thread)
def setStatus(percent = None, info = None):
	gtk.threads_enter()
	if percent is not None:
		glade.get_widget("progress").set_fraction(percent)
		glade.get_widget("progress").set_text("%.2f%%" % (percent * 100))
	if info is not None:
		glade.get_widget("information").set_text(info)
	gtk.threads_leave()
def addLog(text):
	gtk.threads_enter()
	if text is None:
		glade.get_widget("log").get_buffer().set_text("")
	else:
		glade.get_widget("log").get_buffer().insert(glade.get_widget("log").get_buffer().get_end_iter(), "%s\n" % text)
	gtk.threads_leave()

# Signal handlers for GTK
def quit(window):
	sys.exit(0)
def startScan(widget):
	for widget in ("btnStart", "interface"):
		glade.get_widget(widget).set_sensitive(False)
	glade.get_widget("btnStop").set_sensitive(True)
	global scannerThread
	scannerThread = threading.Thread(target=testIPs)
	scannerThread.setDaemon(True)
	scannerThread.start()
def stopScan(widget):
	global scannerThread, doStopScan
	doStopScan = True
	if threading.currentThread() is not scannerThread:
		scannerThread.join()
	del doStopScan
	for widget in ("btnStart", "interface"):
		glade.get_widget(widget).set_sensitive(True)
	glade.get_widget("btnStop").set_sensitive(False)


# Glade data follows...
def getGladeWindow():
	return bz2.decompress(base64.b64decode("""
		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
		====
	"""))

if __name__ == "__main__":
	# Load main window
	gladeXML = getGladeWindow()
	glade = gtk.glade.xml_new_from_buffer(gladeXML, len(gladeXML))
	glade.signal_autoconnect(globals())
	glade.get_widget("btnStop").set_sensitive(False)
	for interface in re.findall("^\s+([0-9a-z]+):", open("/proc/net/dev").read(), re.M):
		glade.get_widget("interface").append_text(interface)
	for widget in ("interface", "time"):
		glade.get_widget(widget).set_active(0)

	gtk.gdk.threads_init()
	gtk.threads_init()
	gtk.threads_enter()
	gtk.main()
	gtk.threads_leave()
