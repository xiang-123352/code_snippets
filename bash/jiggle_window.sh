#!/bin/bash
#
# jiggle_window [Jiggle_Option] [Window_Selection]
#
# Jiggle an X window in some way to indicate to user about some action or
# problem to do with that window.  For example shake a window when some input
# error has occurred, or the window contents has been captured into an image
# or sent to printer.
#
# Jiggle Options
#   -t style       Type or syle of 'jiggle' to apply can be any one of...
#                        bounce (default)  shake  circle  jump
#   -n count       Number of 'jiggles'  (default varies with style)
#
# Window Selection (as per xwit)
#   -current             The currently active window (default)
#   -id window_id        The windows ID  (the normal method)
#   -names class|title   First window matching given string
#   -select              User selection (for testing)
#
# This specific version uses xwit to do its task.
#
####
#
# Examples...
#
# Just bounce the currently active window
#
#   jiggle_window
#
# Make a user selected window circle 3 times
#
#   jiggle_window -t circle -n 3 -select
#
# Shake the launching terminal window, when previous command terminates,
# regardless of where pointer is at the time.
#
#   sleep 5;  jiggle_window -t shake -id $WINDOWID
#
# WARNING...
#
# Can fail if two or more 'jiggles' are applied to the same window at the same
# time.  Basically the moves are not 'atomic' operations, and updates between
# the read/write will generate positional errors.
#
# Window moves will also fail unexpectantally with some applications.
# For example "xmessage" with a "-center" option.  Perhaps due to the
# applications own 'placement' handling at the same time that the window is
# being 'jiggled'.
#
# Caution is recommended
#
####
#
# Anthony Thyssen  6 April 2010
#
PROGNAME=`type $0 | awk '{print $3}'`  # search for executable on path
PROGDIR=`dirname $PROGNAME`            # extract directory of program
PROGNAME=`basename $PROGNAME`          # base name of program
Usage() {                              # output the script comments as docs
  echo >&2 "$PROGNAME:" "$@"
  sed >&2 -n '/^###/q; /^#/!q; s/^#//; s/^ //; 3s/^/Usage: /; 2,$ p' \
          "$PROGDIR/$PROGNAME"
  exit 10;
}

style="bounce"

while [  $# -gt 0 ]; do
  case "$1" in
  --help|--doc*) Usage ;;

  -t) shift; style="$1" ;;
  -n) shift; loop="$1" ;;

  -id)      shift; id="$1" ;;
  -name)    shift; id=`xwit -print -names "$1" | sed -n '1s/:.*//p'` ;;
  -current) id=`xprop -root _NET_ACTIVE_WINDOW | sed 's/.* //'` ;;
  -select)  id=`xwit -print -select | sed -n '3s/:.*//p'` ;;

  --) shift; break ;;    # forced end of user options
  -*) Usage "Unknown option \"$1\"" ;;
  *)  break ;;           # unforced  end of user options

  esac
  shift   # next option
done

[ $# -gt 0 ] && Usage "Too many Arguments"

if [ "X$id" = 'X' ]; then
  #id=`xwit -print -current | sed '1s/:.*//p'`  -- fails for firefox windows!
  id=`xprop -root _NET_ACTIVE_WINDOW | sed 's/.* //'`
fi

# -----------------------------------------------------------------------

trap "i=0" 1 2 3 15  # just complete the loop and finish - do not just exit

case "$style" in
bounce) # bounce like a ball - new window needs input
  : ${loop:=4}
  let loop++           # ignores low bounce
  delay=4000   # delay adjustment
  for (( i=2**loop; i > 1; i/=2 )); do
    let d=delay*i
    let j=i*3/4
    let k=i-j
    xwit -rmove  0  -$j  -id "$id"
    usleep $d
    xwit -rmove  0  -$k  -id "$id"
    usleep $d
    xwit -rmove  0  +$k  -id "$id"
    usleep $d
    xwit -rmove  0  +$j  -id "$id"
    usleep $d
  done
  ;;
shake) # fast left and right shake - error condition
  : ${loop:=5}   # how many times to 'cycle' the window
  size=3         # how big is the shake
  delay=25000    # delay adjustment
  for (( i=loop; i > 0; i-- )); do
    xwit -rmove  -$size 0  -id "$id"
    usleep $delay
    xwit -rmove   $size 0  -id "$id"
    usleep $delay
    xwit -rmove   $size 0  -id "$id"
    usleep $delay
    xwit -rmove  -$size 0  -id "$id"
    usleep $delay
  done
  ;;
circle) # circle window -- hey look at me
  : ${loop:=5}  # how many times to 'cycle' the window
  delay=30000   # delay adjustment
  for (( i=loop; i > 0; i-- )); do
    xwit -rmove   1 -2  -id "$id"
    usleep $delay
    xwit -rmove   2 -1  -id "$id"
    usleep $delay
    xwit -rmove   2  1  -id "$id"
    usleep $delay
    xwit -rmove   1  2  -id "$id"
    usleep $delay
    xwit -rmove  -1  2  -id "$id"
    usleep $delay
    xwit -rmove  -2  1  -id "$id"
    usleep $delay
    xwit -rmove  -2 -1  -id "$id"
    usleep $delay
    xwit -rmove  -1 -2  -id "$id"
  done
  ;;
jump) # jump side to side -- happy happy happy
  : ${loop:=3}  # how many times to 'cycle' the window
  delay=70000  # delay adjustment
  # initial half jump
  xwit -rmove  -2 -2  -id "$id"
  usleep $delay
  xwit -rmove  -2 +2  -id "$id"
  usleep $delay
  let loop--
  for (( i=loop; i > 0; i-- )); do
    xwit -rmove  +3 -3  -id "$id"
    usleep $delay
    xwit -rmove  +2  0  -id "$id"
    usleep $delay
    xwit -rmove  +3 +3  -id "$id"
    usleep $delay
    xwit -rmove  -3 -3  -id "$id"
    usleep $delay
    xwit -rmove  -2  0  -id "$id"
    usleep $delay
    xwit -rmove  -3 +3  -id "$id"
    usleep $delay
  done
  # one final jump to the other side
  xwit -rmove  +3 -3  -id "$id"
  usleep $delay
  xwit -rmove  +2  0  -id "$id"
  usleep $delay
  xwit -rmove  +3 +3  -id "$id"
  usleep $delay
  # half jump back to start
  xwit -rmove  -2 -2  -id "$id"
  usleep $delay
  xwit -rmove  -2 +2  -id "$id"
  usleep $delay
  ;;
*) # this type is not known
  echo >&2 "jiggle_window:  Unknown jiggle style"
  exit 10
  ;;
esac

exit 0

