#!/usr/bin/env perl
#
# Rainer Größlinger <rainer@melodax.de>
# converts a DVB-S channels.conf to a xspf playlist file
# 
# usage: ./channels2xspf channels.conf > playlist.xspf
# 


use strict;
use XML::Writer;


my @channels;
my $index = 0;


# converts channels.conf data to data needed for the xspf playlist
sub prepare_channel {
  if ( @_ != 8 ) {
    die("input not a valid dvb-s channels.conf")
  }


  # h/v to voltage
  if ( $_[2] eq "h" ) {
    $_[2] = 18;
  } else {
    $_[2] = 13;
  }


  # pad strings to certain lengths
  $_[1] = $_[1] . "0" x ( 8 - length($_[1]));
  $_[4] = $_[4] . "0" x ( 8 - length($_[4]));
  push(@_, sprintf("%04d", $index+1));


  $_[7] =~ s/\s+$//;
 
  @_;
}


##################################################


foreach my $file (@ARGV) {
  open(FILE, $file);
  push(@channels, <FILE>);
  close(FILE);
}


my $writer = new XML::Writer(OUTPUT      => "STDOUT",
                             ENCODING    => "utf-8",
                             DATA_MODE   => 1,
                             DATA_INDENT => 4);
$writer->xmlDecl("UTF-8");


$writer->startTag("playlist",
                  "version"   => "1",
                  "xmlns"     => "http://xspf.org/ns/0/",
                  "xmlns:vlc" => "http://www.videolan.org/vlc/playlist/ns/0/");
$writer->startTag("title");
$writer->characters("DVB-S Playlist");
$writer->endTag("title");
$writer->startTag("trackList");


foreach (@channels) {
  my @channel = &prepare_channel(split(/:/));
  $writer->startTag("track");
  $writer->startTag("title");
  $writer->characters("$channel[8]. $channel[0]");
  $writer->endTag("title");
  $writer->startTag("location");
  $writer->characters("dvb-s://satno=1,frequency=$channel[1],voltage=$channel[2],srate=$channel[4]");
  $writer->endTag("location");
  $writer->startTag("extension",
                    "application" => "http://www.videolan.org/vlc/playlist/0");
  $writer->startTag("vlc:id");
  $writer->characters($index);
  $writer->endTag("vlc:id");
  $writer->startTag("vlc:option");
  $writer->characters("program=$channel[7]");
  $writer->endTag("vlc:option");
  $writer->endTag("extension");
  $writer->endTag("track");
  $index++;
}


$writer->endTag("trackList");
$writer->endTag("playlist");
$writer->end();
