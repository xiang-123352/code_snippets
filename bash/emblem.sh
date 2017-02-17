#!/bin/bash

# change emblem's in Nautilus with nautilus-actions
# add a new action in nautilus-actions-config-tool with
# Path /path/to/this/script.sh
# Parameter %F

# Germar Reitze <germar.reitze(AT)gmx.de> Nov 2011
# 2011-12-12 Germar Reitze - bugfix and new function to remove emblems in multiple files
# 2011-12-14 Germar Reitze - automatic refresh Nautilus after change

emblem="art cool danger default desktop development documents downloads draft favorite important mail marketing money new nowrite \
ohno OK package people personal photos pictures plan presentation readonly shared sound symbolic-link system \
ubuntuone-unsynchronized ubuntuone-updating unreadable urgent videos web"
#debug=1
xsendkeycode=$(which xsendkeycode)

# ask which emblem to add
pick_emblem() {
   emblem_list=""
   for i in $emblem; do
        if [ $(echo "$@" | grep -c $i) -eq 1 ]; then
           emblem_list="$emblem_list TRUE $i"
        else
           emblem_list="$emblem_list FALSE $i"
        fi
   done
   if [ "$multiple_files" == "true" ]; then
        text="Which embleme to add to files?"
        emblem_list="FALSE DELETE_ALL_EMBLEMS $emblem_list"
   else
        text="Which embleme to set?"
   fi
   # if lineakd is not installed remind to press F5
   if ! [ -x "$xsendkeycode" ]; then
      text="$text \nDon't forget to press [F5] after OK"
   fi
   zenity  --list  --text "$text" --checklist  --column "Pick" --column "Emblem" $emblem_list --separator=" " --height=700 --width=300
   return $?
}

# do we already have emblem's?
get_used_emblem() {
   a=$(gvfs-info "$1" -a metadata::emblems)
   err=$?
   b=${a#*[}
   b=${b%]*}
   echo "$b" | sed -e 's/,//g'
   return $err
}

# emblem won't show without
set_icon_view_auto_layout() {
   if [ $(gvfs-info "$1" -a metadata::nautilus-icon-view-auto-layout | grep -c true) -lt 1 ]; then
        [ $debug ] && echo "SET: metadata::nautilus-icon-view-auto-layout true"
        gvfs-set-attribute -t string "$1" metadata::nautilus-icon-view-auto-layout true
        return $?
   else
        [ $debug ] && echo "metadata::nautilus-icon-view-auto-layout already set"
        return 0
   fi
}

set_emblem() {
   file="$1"
   shift
   gvfs-set-attribute -t stringv "$file" metadata::emblems $@
   return $?
}

del_emblem() {
   gvfs-set-attribute -t unset "$1" metadata::emblems
   return $?
}

report_error() {
   zenity --error --text "Failed in $1"
}


multiple_files=false
if [ $# -gt 1 ]; then
   multiple_files=true
fi

if [ "$multiple_files" == "true" ]; then
   add_emblem=$(pick_emblem)
   err=$?
   if [ $err -gt 0 ]; then
        [ $debug ] && echo "cancel"
        exit 1
   fi
   [ $debug ] && echo "embleme to add: $add_emblem"

   # process every file separate
   while [ $# -gt 0 ]; do
        if [ $(echo "$add_emblem" | grep -c DELETE_ALL_EMBLEMS) -eq 1 ]; then
           [ $debug ] && echo "$1: delete emblems"
           del_emblem "$1"
           err=$?
           [ $err -gt 0 ] && report_error "$1" && exit 1
        else
           used_emblem=$(get_used_emblem "$1")
           err=$?
           [ $err -gt 0 ] && report_error "$1" && exit 1
           emblem_list=""
           for i in $emblem; do
                if [ $(echo "$used_emblem $add_emblem" | grep -c $i) -ne 0 ]; then
                   emblem_list="$emblem_list $i"
                fi
           done
           set_icon_view_auto_layout "$1"
           err=$?
           [ $err -gt 0 ] && report_error "$1" && exit 1

           if [ "$emblem_list" != "" ]; then
                [ $debug ] && echo "$1: $emblem_list"
                set_emblem "$1" $emblem_list
                err=$?
                [ $err -gt 0 ] && report_error "$1" && exit 1
           fi
        fi
        shift
   done
else
   # we only have one file
   add_emblem=$(pick_emblem $(get_used_emblem "$1") )
   err=$?
   if [ $err -gt 0 ]; then
        [ $debug ] && echo "cancel"
        exit 1
   fi
   [ $debug ] && echo "embleme to add: $add_emblem"

   set_icon_view_auto_layout "$1"
   err=$?
   [ $err -gt 0 ] && report_error "$1" && exit 1

   if [ "$add_emblem" != "" ]; then
        [ $debug ] && echo "$1: $add_emblem"
        set_emblem "$1" $add_emblem
        err=$?
   else
        [ $debug ] && echo "$1: delete emblem"
        del_emblem "$1"
        err=$?
   fi
   [ $err -gt 0 ] && report_error "$1" && exit 1
fi

# refresh Nautilus if lineakd is installed
if [ -x "$xsendkeycode" ]; then
   $xsendkeycode 71 1
   $xsendkeycode 71 0
fi

