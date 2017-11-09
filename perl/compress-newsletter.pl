#!/bin/sh
#  -*-Perl-*-
# ====================================================================== #
# Run the right perl version:
if [ -x /usr/local/bin/perl ]; then
  perl=/usr/local/bin/perl
elif [ -x /usr/bin/perl ]; then
  perl=/usr/bin/perl
else
  perl=`which perl| sed 's/.*aliased to *//'`
fi

exec $perl -x -S $0 "$@"     # -x: start from the following line
# ====================================================================== #
#! /Good_Path/perl -w
# line 17

# Name:   compress-newsletter
# Author: wd (Wolfgang [.] Dobler [at] kis.uni-freiburg.de)
# Date:   03-Oct-2005
# Description:
#   Use ghostscript's pdfwrite device (à la ps2pdf) to reduce the
#   Newsletter's PDF file size, and add meta information like author,
#   date, etc.
#   The preferred route is currently:
#                 [scribus>=1.2.3]
#                        |
#                    file.pdf
#                        |
#                 [pdftops>=3.00]
#                        |
#                     file.ps
#                        |
#            [pstopdf14 (gs-gnu-8.16 or higher)]
#                        |
#                        V
#                    final.pdf
# Usage:
#   compress-newletter [-i col:gray:mono] Newsletter_big.pdf
# Options:
#   -i col:gray:mono
#   --imgres=col:gray:mono   Set resolution for downsampling color,
#                            grayscale and black-and-white images
#                            (default is 144:300:300)
#   -d
#   --dont-touch-images      Try to not resample images
#
#   -q
#   --quiet                  Be less verbose
#
#   --debug                  Be more verbose and keep temporary files around
use strict;
use File::Temp qw/ :mktemp /;

use Getopt::Long;
# Allow for `-Plp' as equivalent to `-P lp' etc:
Getopt::Long::config("bundling");

my (%opts);			# Options hash for GetOptions
my $doll='\$';			# Need this to trick CVS

## Process command line
GetOptions(\%opts,
	   qw( -h   --help
	       -i=s --imgres=s
	       -d   --dont-touch-images
	            --debug
	       -q   --quiet
               -v   --version ));

my $debug = ($opts{'debug'} ? 1 : 0 ); # undocumented debug option
if ($debug) {
    printopts(\%opts);
    print "\@ARGV = `@ARGV'\n";
}

if ($opts{'h'} || $opts{'help'})    { die usage();   }
if ($opts{'v'} || $opts{'version'}) { die version(); }

my $quiet      = ($opts{'q'} || $opts{'quiet'}             || ''           );
my $imgres     = ($opts{'i'} || $opts{'imgres'}            || '144:300:300');
my $dont_touch = ($opts{'d'} || $opts{'dont-touch-images'} || 0);
my $resample_imgs = ! $dont_touch; # easier to check for

my ($gs,      @gsargs     ) = ('gs'     );
my ($pdftops, @pdftopsargs) = ('pdftops');
my ($pdfopt,  @pdfoptargs ) = ('pdfopt' );

my $infile = shift or die usage();
(my $root=$infile) =~ s/\.(pdf|ps).*//;
(my $outfile=$infile) =~ s/(.*)(\.(pdf|ps))/${1}_new${2}/;
my $tmpfile = mktemp("${root}.tmp_XXXXXX");


## 0. Extract all sorts of information

# Extract Scribus version, creation date, bookmarks from original PDF:
print "Running pdftk ...\n";
print STDERR "pdftk $infile dump_data output\n" if ($debug);
my $meta = `pdftk $infile dump_data output -`;
my ($creator) = ( $meta =~
		  m{InfoKey: Creator\s+InfoValue:\s*(.+)$}m
		);
$creator = 'Scribus 1.2.3' unless defined($creator);
my $datestring = extract_CreationDate($meta);
my @bookmarks = extract_bookmarks($meta);

# Extract desired image resolutions
my ($colres,$grayres,$monores) = ($imgres =~ /([0-9]+):([0-9]+):([0-9]+)/);
die "Image resolution must be of form `col:gray:mono'\n"
    unless defined($monores);

## 1. Run pdftops
push @pdftopsargs, "-level3";
my $psfile1 = mktemp("${root}.ps_XXXXXX");
my $psfile2 = mktemp("${root}.ps_XXXXXX");
push @pdftopsargs, $infile, $psfile1;
print "Running pdftops ...\n";
print STDERR "$pdftops @pdftopsargs\n" if ($debug);
system($pdftops,@pdftopsargs);
# Avoid setting /Duplex as this upsets EPS ghostscript 8.15.1
system("sed 's:{ /Duplex true def }:{ }:' < $psfile1 > $psfile2");

## 2. Run gs
# a) Prepare options
push @gsargs, qw{-q -dNOPAUSE -dBATCH};
push @gsargs, '-sDEVICE=pdfwrite';
push @gsargs, '-dCompatibilityLevel=1.3';
push @gsargs, '-dEmbedAllFonts=true';
push @gsargs, '-dSubsetFonts=true';

# Image downsampling. Resolution is not continuous, but [for images of a
# certain resolution] is the same within each of the following intervals
# (GNU ghostscript 8.16):
# ??--49
# 50--74
# 75--?? (for the sample used for testing, 75 was the same as 1200)
if ($resample_imgs) {
    # One of /printer, /screen, /prepress, /ebook, /default; see Ps2pdf.htm:
    push @gsargs, '-dPDFSETTINGS=/screen';

    push @gsargs, '-dDownsampleColorImages=true';
    push @gsargs, '-dColorImageDownsampleType=/Bicubic';
    push @gsargs, "-dColorImageResolution=$colres";
    #
    push @gsargs, '-dDownsampleGrayImages=true';
    push @gsargs, '-dGrayImageDownsampleType=/Bicubic';
    push @gsargs, "-dGrayImageResolution=$grayres";
    #
    push @gsargs, '-dDownsampleMonoImages=true';
    push @gsargs, '-dMonoImageDownsampleType=/Bicubic';
    push @gsargs, "-dMonoImageResolution=$monores";
    # the following is default for /screen
    push @gsargs, '-dColorConversionStrategy=/sRGB';
} else {
    # One of /printer, /screen, /prepress, /ebook, /default; see Ps2pdf.htm:
    push @gsargs, '-dPDFSETTINGS=/printer';
    # (or JPEG images will get re-sampled even if they have 72 dpi, which
    # makes InDesign's PDF look worse).
    #
    # I haven't found a way to specify this through the options that
    # follow. Most likely, setting the /QFactor in /ColorACSImageDict
    # would do the job (see http://electron.mit.edu/~gsteele/pdf/)
    push @gsargs, '-dDownsampleColorImages=false';
    push @gsargs, '-dDownsampleGrayImages=false';
    push @gsargs, '-dDownsampleMonoImages=false';
    #
    push @gsargs, '-dColorConversionStrategy=/LeaveColorUnchanged';
}

push @gsargs, "-sOutputFile=$tmpfile";
push @gsargs, "-c .setpdfwrite";

# b) Write meta information to temporary file
#my $metafile = mktemp("metainfo.tmp_XXXXXX");
my $metafile = "${root}.meta";
open(META, "> $metafile");
print META <<"DEAD_PARROT";
% Document information
[%
 /CreationDate (D:$datestring)
 /ModDate (D:$datestring)
 /Creator ($creator)
 /Title ([Insert your document title here])
 /Subject ([Insert the Subject here])
 /Keywords ([Insert key words here])
 /Author ([Insert author' name here])
 /DOCINFO pdfmark

% Initial view on opening the document
[/View [/Fit] % Fit page in window
 /Page 1
 % /PageMode /UseOutlines % /UseNone /UserOutlines /UseThumbs /FullScreen
 /DOCVIEW pdfmark

DEAD_PARROT

## Bookmarks. [Commented out for acroread 7.0 has problems] Currently at
## the mercy of the original bookmarks (and Scribus 1.2.2 does not allow
## to edit the bookmark names) and the encoding that pdftk understands
## (most quotation marks get mapped to `?').
## Ideally, one would write out the meta information file with
## `compress-newsletter -m CC.pdf' and use it then with
## `compress-newsletter CC.pdf'.
## % Bookmarks: @bookmarks


push @gsargs, '-f', $psfile2, $metafile;
print "Running gs ...\n";
print STDERR "$gs @gsargs\n" if ($debug);
system($gs,@gsargs);

## 3. Run pdfopt
print "Running pdfopt ...\n";
print STDERR "$pdfopt @pdfoptargs $tmpfile $outfile\n" if ($debug);
system($pdfopt,@pdfoptargs,$tmpfile,$outfile);

# Some diagnostics:
system('ls', '-l', $infile, $psfile2, $tmpfile, $outfile);

END {
    # Clean up even in case of an error:
    unless ($debug) {
        foreach my $file ($psfile1,$psfile2,$tmpfile) {
            unlink $file if (defined($file) && -f $file);
        }
    }
}


# ---------------------------------------------------------------------- #
sub extract_CreationDate {

    use POSIX qw(strftime);

    my $meta = shift;

    my ($cdate) = ( $meta =~
		    m{InfoKey: CreationDate\s+InfoValue:\s*(?:D:)?(.+)$}m
		  );
    # Time string: need to splice in "'" after hours and minutes of time zone
    # definition. To me this looks like the technical documentation was taken
    # too literally and now applications (and Acroread 7) insist on these
    # stupid markers.
    my $datestring;
    if ($cdate =~ /[0-9]{14}/) { # managed to extract CreationDate from $meta
	$datestring = "$cdate-06'00'";
    } else {		         # Creation date unknown -- use current date
	my $tz = strftime "%z", localtime();
	$tz =~ s/([0-9][0-9])([0-9][0-9])/$1'$2'/;
	$datestring = strftime "%Y%m%d%H%M%S$tz", localtime();
    }

    $datestring;
}
# ---------------------------------------------------------------------- #
sub extract_bookmarks {

    my $meta = shift;

    my @bm;

    while ($meta =~ /^BookmarkTitle:      \s* (.*) \n
                      BookmarkLevel:      \s* (.*) \n
                      BookmarkPageNumber: \s* (.*) /xmg) {
	my ($title,$level,$page) = ($1,$2,$3);
	push @bm, "[/Title ($title /Page $page /OUT pdfmark\n";
    }

}
# ---------------------------------------------------------------------- #
sub printopts {
# Print command line options
    my $optsref = shift;
    my %opts = %$optsref;
    foreach my $opt (keys(%opts)) {
	print STDERR "\$opts{$opt} = `$opts{$opt}'\n";
    }
}
# ---------------------------------------------------------------------- #
sub usage {
# Extract description and usage information from this file's header.
    my $thisfile = __FILE__;
    local $/ = '';              # Read paragraphs
    open(FILE, "<$thisfile") or die "Cannot open $thisfile\n";
    while (<FILE>) {
	# Paragraph _must_ contain `Description:' or `Usage:'
        next unless /^\s*\#\s*(Description|Usage):/m;
        # Drop `Author:', etc. (anything before `Description:' or `Usage:')
        s/.*?\n(\s*\#\s*(Description|Usage):\s*\n.*)/$1/s;
        # Don't print comment sign:
        s/^\s*# ?//mg;
        last;                        # ignore body
    }
    $_ or "<No usage information found>\n";
}
# ---------------------------------------------------------------------- #
sub version {
# Return CVS data and version info.
    my $doll='\$';		# Need this to trick CVS
    my $cmdname = (split('/', $0))[-1];
    my $rev = '$Revision: 1.14 $';
    my $date = '$Date: 2007/07/12 17:12:28 $';
    $rev =~ s/${doll}Revision:\s*(\S+).*/$1/;
    $date =~ s/${doll}Date:\s*(\S+).*/$1/;
    "$cmdname version $rev ($date)\n";
}
# ---------------------------------------------------------------------- #

# End of file compress-newsletter
