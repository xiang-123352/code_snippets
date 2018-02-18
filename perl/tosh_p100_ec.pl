#!/usr/bin/perl -w

# Version 1.0 (2010-05-27)
#
# *************************************************
# ** Toshiba P100 series GPU fan setup for Linux **
# ** Must be called in init/resume scripts       **
# ** This bypass the need for custom ACPI kernel **
# ** no more possible in latest distros...       **
# *************************************************
#
# Machines used for test (successful users, please update):
#  - p100-114, PSPA3E, bios 4.80
#  - ...
#
# Copyright (C) 2010  YL ; adapted from acer_ec.pl (0.6.1) by these authors:
#
# Copyright (C) 2007  Michael Kurz     michi.kurz (at) googlemail.com
# Copyright (C) 2007  Petr Tomasek     tomasek (#) etf,cuni,cz
# Copyright (C) 2007  Carlos Corbacho  cathectic (at) gmail.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


require 5.004;

use strict;
use Fcntl;
use POSIX;
use File::Basename;

sub initialize_ioports
{
  sysopen (IOPORTS, "/dev/port", O_RDWR)
    or die "/dev/port: $!\n";
  binmode IOPORTS;
}

sub close_ioports
{
  close (IOPORTS)
    or print "Warning: $!\n";
}



sub inb
{
  my ($res,$nrchars);
  sysseek IOPORTS, $_[0], 0 or return -1;
  $nrchars = sysread IOPORTS, $res, 1;
  return -1 if not defined $nrchars or $nrchars != 1;
  $res = unpack "C",$res ;
  return $res;
}

# $_[0]: value to write
# $_[1]: port to write
# Returns: -1 on failure, 0 on success.
sub outb
{
  if ($_[0] > 0xff)
  {
    my ($package, $filename, $line, $sub) = caller(1);
    print "\n*** Called outb with value=$_[1] from line $line\n",
          "*** (in $sub). PLEASE REPORT!\n",
          "*** Terminating.\n";
    exit(-1);
  }
  my $towrite = pack "C", $_[0];
  sysseek IOPORTS, $_[1], 0 or return -1;
  my $nrchars = syswrite IOPORTS, $towrite, 1;
  return -1 if not defined $nrchars or $nrchars != 1;
  return 0;
}

sub wait_write
{
	my $i = 0;
	while ((inb($_[0]) & 0x02) && ($i < 10000)) {
		sleep(0.01);
		$i++;
	}
	return -($i == 10000);
}

sub wait_read
{
	my $i = 0;
	while (!(inb($_[0]) & 0x01) && ($i < 10000)) {
		sleep(0.01);
		$i++;
	}
	return -($i == 10000);
}

sub wait_write_ec
{
	wait_write(0x66);
}

sub wait_read_ec
{
	wait_read(0x66);
}

sub send_ec
{
	if (!wait_write_ec()) { outb($_[0], 0x66); }
	if (!wait_write_ec()) { outb($_[1], 0x62); }
}

sub write_ec
{
	if (!wait_write_ec()) { outb(0x81, 0x66 ); }
	if (!wait_write_ec()) { outb($_[0], 0x62); }
	if (!wait_write_ec()) { outb($_[1], 0x62); }
}

sub read_ec
{
	if (!wait_write_ec()) { outb(0x80, 0x66 ); }
	if (!wait_write_ec()) { outb($_[0], 0x62); }
	if (!wait_read_ec())  { inb(0x62); }
}

sub print_regs
{
	initialize_ioports();

	my @arr = ("00","10","20","30","40","50","60","70","80","90","A0","B0","C0","D0","E0","F0", "");

	my $i = 0;
	my $t = 0;
	print "\n  \t00\t01\t02\t03\t04\t05\t06\t07\t|\t08\t09\t0A\t0B\t0C\t0D\t0E\t0F\n";
	print "  \t__\t__\t__\t__\t__\t__\t__\t__\t|\t__\t__\t__\t__\t__\t__\t__\t__\n";
	print "00 |\t";
	for ($i = 0; $i < 256; $i++)
	{
		$t = read_ec($i);
		print $t;
		print "\t";
		if ((($i + 1) % 8) == 0){
			if ((($i + 1) % 16) == 0) {
				if ($i != 255) { print "\n$arr[(($i-(($i + 1) % 16)) / 16) + 1] |\t"; }
			} else {
				print "|\t";
			}
		}
	}
	
	print "\n";
	
	close_ioports();
}

if (!$ARGV[0]){
        print "wrong arguments!\n";
	print "usage:\n";
	print "\'tosh_p100_ec regs\' \t\t\t\tdumps all ec registers\n";
	print "\'tosh_p100_ec set_gpu_fan_med\' \t\t\tinit GPU fan medium  speed\n";
	print "\'tosh_p100_ec set_gpu_fan_hig\' \t\t\tinit GPU fan high    speed\n";
} elsif ($ARGV[0] eq "regs") {
	print_regs();
} elsif ($ARGV[0] eq "set_gpu_fan_med") {
	# Set VTMP for GPU fan, medium speed : Bios 2.4 pre-Vista hack value
	initialize_ioports();
	write_ec(0x5e, 0x3c);
	close_ioports(); 
} elsif ($ARGV[0] eq "set_gpu_fan_hig") {
	# Set VTMP for GPU fan, highest speed (some higher values seems not always reversible)
	initialize_ioports();
	write_ec(0x5e, 0x4c);
	close_ioports();
} else {
	print "wrong arguments!\n";
}
