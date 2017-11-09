#!/opt/bin/bash
# Rotate a directory backup using hard links. Specify the rootpath this script
# should operate on, and a specific directory.
#
# Arguments:
#    rootpath    - The root path this script operates in.
#    dir         - Target directory in the rootpath to backup.
#    type        - String to differentiate multiple backups. Daily, weekly,
#                  etc. This gets appended to the new directory we create.
#
# Usage: rotate_dir_file_date.sh <rootpath> <dir> <type> <maxnumber>
#
# Example:
#    > rotate_dir_file_date.sh /home/ user daily 5
#    Creates /home/user.daily.20130813
#    Deletes oldest /home/user/daily.* directory if more than 5 exist
#
 
ROOTPATH=$1
DIR=$2
TYPE=$3
MAXNUMBER=$4
 
if [ -z "$ROOTPATH" ]; then
        echo "Missing argument #1: rootpath to $0" >&2
        exit 1
fi
 
if [ ! -d "$ROOTPATH" ]; then
        echo "Missing directory '$ROOTPATH' for: rootpath to $0" >&2
        exit 1
fi
 
if [ ! -d "$ROOTPATH$DIR" ]; then
        echo "Missing directory '$ROOTPATH$DIR' for: rootpath and dir to $0" >&2
        exit 1
fi
 
if [ -z "$DIR" ]; then
        echo "Missing argument #2: dir to $0" >&2
        exit 1
fi
 
if [ -z $TYPE ]; then
        echo "Missing argument #3: type to $0" >&2
        exit 1
fi
 
if [ -z $MAXNUMBER ]; then
        echo "Missing argument #4: maxnumber to $0" >&2
        exit 1
fi
 
 
# Create a new directory appended with date
NEWDIR=@${DIR}.${TYPE}.`date +\%Y\%m\%d`
rm -rf ${ROOTPATH}${NEWDIR} 2>/dev/null
cp -al ${ROOTPATH}${DIR} ${ROOTPATH}${NEWDIR}
 
# Touch directory to make sure of correct sorting
touch ${ROOTPATH}${NEWDIR}
 
# Delete the oldest directories (on a system with buggy tail +n command)
SAVEDIRS=`ls -1dt ${ROOTPATH}@${DIR}.${TYPE}.* | head -${MAXNUMBER}`
SAVERX=`echo ${SAVEDIRS} | sed -e 's/ /|/g'`
rm -rf `ls -1dtr ${ROOTPATH}@${DIR}.${TYPE}.* | egrep -v "${SAVERX}"`

