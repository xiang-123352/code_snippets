#!/bin/sh
# restart any process
#
# usage: bl-restart [decimal] command arg1 arg2...
# The process matching the exact command line will be restarted after 1s,
# or by other number if passed before command.

help='usage: bl-restart [decimal] command arg1 arg2...
bl-restart -h|--help

Kills process matching full command line
and restarts after 1 sec, or "decimal" seconds if supplied.
(Floating-point is supported.)'

[ "$1" = '-h' ] || [ "$1" = '--help' ] && { echo "$help"; exit 0;}

delay=1

#type "$1" >/dev/null 2>&1 || {
command -v "$1" >/dev/null 2>&1 || {
    case "$1" in
    *[!0-9.]*)
        echo "$1 is not a command and not an integer.

$help"
        exit 1
        ;;
    *)
        delay=$1
        shift
        ;;
    esac
}

pkill -fx "$*" && sleep $delay
(setsid "$@" & )

exit 0
