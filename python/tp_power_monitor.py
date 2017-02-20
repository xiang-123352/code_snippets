#!/usr/bin/python

# COPYRIGHT (C) 2006 Matthew Garman
# matthew (dot) garman (at) gmail (dot) com
# License: MIT <http://www.opensource.org/licenses/mit-license.php>

import sys, time, getopt, os, re


class tpPowerMonitorDataSource:

    # The name of the file to parse for needed data (data_source_file) OR
    # the name of a command whose output will be read as a file
    # (os.popen(shell_command)).
    #
    # Typically, data_source_file will be something from /proc (or
    # possibly /sys), and shell_command will be a utility+arguments such
    # as "iwconfig eth1 power".
    #
    # Note that you should set EITHER data_source_file OR shell_command,
    # but not both.
    data_source_file    = None
    shell_command       = None

    # The line number of the data file containing our data OR the string
    # that marks the beginning of the line in which we're interested
    # (startswith_string) OR a regular expression to key the data for
    # which we're looking (regexp_pattern).
    line_number         = None
    startswith_string   = None
    regexp_pattern      = None

    # The string that delimits the line containing our data.  This will be
    # used as the parameter to split().  Note that you can leave this as
    # None to split on whitespace.
    split_string        = None

    # A mapping of data names to indices in the split string.
    name_index_map      = {}

    def __init__(self, file, cmd, line, swstr, pat, splstr, map):
        self.data_source_file    = file
        self.shell_command       = cmd
        self.line_number         = line
        self.startswith_string   = swstr
        self.regexp_pattern      = pat
        self.split_string        = splstr
        self.name_index_map      = map

    def printMembers(self):
        print "\t" + 'self.data_source_file = ' + str(self.data_source_file)
        print "\t" + 'self.shell_command = ' + str(self.shell_command)
        print "\t" + 'self.line_number = ' + str(self.line_number)
        print "\t" + 'self.startswith_string = ' + str(self.startswith_string)
        print "\t" + 'self.regexp_pattern = ' + str(self.regexp_pattern)
        print "\t" + 'self.split_string = ' + str(self.split_string)
        print "\t" + 'self.name_index_map = ' + str(self.name_index_map)

    def readData(self, d):
        # open the data source file or run the command that will produce
        # the data
        file = None
        if self.data_source_file:
            file = open(self.data_source_file, 'r')
        elif self.shell_command:
            file = os.popen(self.shell_command)
        else:
            print 'error: no data source defined'
            self.printMembers()
        # read the contents of the file into a list and close the file
        lines = None
        if file:
            lines = file.readlines()
            file.close()
        else:
            print 'error: data file not opened'
            self.printMembers()
        # now get the line in the file with our data
        line = None
        if lines:
            if None != self.line_number:
                line = lines[self.line_number]
            elif self.startswith_string:
                for l in lines:
                    if l.startswith(self.startswith_string):
                        line = l
                        break
            elif self.regexp_pattern:
                for l in lines:
                    if re.compile(self.regexp_pattern).match(l):
                        line = l
                        break
        else:
            print 'error: no lines in data file'
            self.printMembers()
        # now get the data we want from the line itself
        if line:
            fields = line.split(self.split_string)
            for key, value in self.name_index_map.items():
                d[key] = fields[value].strip()
        else:
            print 'error: could not find line with data in file'
            self.printMembers()

# END --- class tpPowerMonitorDataSource


tp_data_sources = [

    tpPowerMonitorDataSource(
        '/proc/cpuinfo',             # data file
        None,                        # shell command
        None,                        # line index
        'cpu MHz',                   # startswith() string
        None,                        # regexp pattern
        ':',                         # split string
        {'proc_cpuinfo_cpu_mhz': 1}  # name-to-index map
    ),

    # http://thinkwiki.org/wiki/Ipw2200#Power_Management
    tpPowerMonitorDataSource(
        None,                          # data file
        '/sbin/iwpriv eth1 get_power', # shell command
        0,                             # line index
        None,                          # startswith() string
        None,                          # regexp pattern
        ':',                           # split string
        {'iwpriv_get_power': 2}        # name-to-index map
    ),

    # http://forums.gentoo.org/viewtopic-t-447841.html
    # see post from ruben on Wed Mar 29, 2006 4:09 am
    tpPowerMonitorDataSource(
        None,
        '/usr/bin/sudo /sbin/hdparm -C /dev/sda',
        None,
        ' drive state is',
        None,
        ':',
        {'hard_drive_power_state': 1}
    ),

    # http://thinkwiki.org/wiki/Thermal_sensors
    tpPowerMonitorDataSource(
        '/proc/acpi/ibm/thermal',
        None,
        0,
        None,
        None,
        None,
        {'ibm_thermal_cpu':     1,
         'ibm_thermal_hdaps':   2,
         'ibm_thermal_pmcia':   3,
         'ibm_thermal_gpu':     4,
         'ibm_thermal_batt_fl': 5,
         'ibm_thermal_batt_br': 7 }
    ),

    # http://mailman.linux-thinkpad.org/pipermail/linux-thinkpad/2006-July/034738.html
    tpPowerMonitorDataSource(
        '/proc/acpi/processor/CPU/power',
        None,
        None,
        'bus master activity',
        None,
        ':',
        {'bus_master_activity': 1}
    ),

    tpPowerMonitorDataSource(
        '/proc/acpi/battery/BAT0/state',
        None,
        None,
        'present rate:',
        None,
        None,
        {'battery0_state_present_rate': 2}
    ),

    tpPowerMonitorDataSource(
        None,
        '/usr/bin/sudo /usr/sbin/radeontool dac',
        0,
        None,
        None,
        None,
        {'radeontool_dac_ext_vga': -1}
    ),

    tpPowerMonitorDataSource(
        None,
        '/usr/bin/sudo /usr/sbin/radeontool light',
        0,
        None,
        None,
        None,
        {'radeontool_light_lcd': -1}
    ),

    # http://forums.gentoo.org/viewtopic-t-343029-highlight-rovclock.html
    tpPowerMonitorDataSource(
        None,
        '/usr/bin/sudo /usr/sbin/rovclock -i',
        None,
        'Core: ',
        None,
        None,
        {'rovclock_gpu_clock': 1,
         'rovclock_mem_clock': 4 }
    ),

    tpPowerMonitorDataSource(
        None,
        '/sbin/iwconfig eth1',
        None,
        None,
        '.*Power Management.*',
        ':',
        {'wireless_power_mgmt_state': 1}
    ),

    tpPowerMonitorDataSource(
        '/proc/loadavg',
        None,
        0,
        None,
        None,
        None,
        {'proc_loadavg_1min': 0,
         'proc_loadavg_5min': 1,
         'proc_loadavg_15min': 2 }
    ),
]
log_data = list()
poll_freq_hz = 1
run_time_sec = 60*60
logfile = None


def collectPowerData():
    global run_time_sec
    global poll_freq_hz
    global log_data
    global logfile
    global tp_data_sources

    log = None
    if logfile:
        log = open(logfile, 'w')
        log.write("time, data\n")
    end_t = time.time()+run_time_sec
    while time.time() < end_t:
        datum = {}
        for dsrc in tp_data_sources:
            dsrc.readData(datum)
        log_data.append(datum)
        if log: log.write(str(time.time()) + ', ' + str(datum) + "\n")
        time.sleep(1.0/float(poll_freq_hz))
    if log: log.close()


def createStats():
    global log_data
    global logfile
    log = None
    if logfile:
        log = open(logfile, 'a')
    if log: log.close()


def usage():
    print 'Usage: ' + sys.argv[0] + \
        '[-h] [-f freq_hz] [-t time_min] [-l logfile]'
    print "\t-h            Display this help"
    print "\t-f freq_hz    The polling frequency in Hertz, default=" \
        + str(poll_freq_hz)
    print "\t-t time_min   Total poll time in minutes, default=" \
        + str(run_time_sec/60)
    print "\t-l logfile    Write poll data to indicated log file"


def main():
    global poll_freq_hz
    global run_time_sec
    global logfile

    # parse options
    # see: http://docs.python.org/lib/module-getopt.html
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:t:l:")
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for o, a in opts:
        if '-h' == o:
            usage()
            sys.exit()
        if '-f' == o:
            poll_freq_hz = int(a)
        if '-t' == o:
            run_time_sec = int(a)*60
        if '-l' == o:
            logfile = a

    # do stuff
    print 'running for ' + str(run_time_sec/60) + ' minutes'
    print 'poll rate:  ' + str(poll_freq_hz) + ' Hz'
    print 'logfile:    ' + str(logfile)
    collectPowerData()
    print '...done!'
    print 'Data points collected: ' + str(len(log_data))
    sum = 0
    for d in log_data:
        sum += int(d['battery0_state_present_rate'])
    avg = float(sum) / float(len(log_data))
    print 'Average power draw:    ' + str(avg)
    if logfile:     log = open(logfile, 'a')
    if log:
        log.write('Average power draw:    ' + str(avg))
        log.close()


if __name__ == '__main__':
    main()

