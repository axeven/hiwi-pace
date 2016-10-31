#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'
IS_CLEAN=/home/debjit/Documents/hiwi-pace/cleaner
echo "Finding all *.tar.gr* files in task3_output..."
INFILES=`find -L task3_output -name '*.tar.gz*'`
tmpdir=$(mktemp --directory --tmpdir=/dev/shm $(basename $0)-XXXXXXXX)
trap "rm -rf $tmpdir" EXIT
echo "Creating the tasks..."
for tarfile in $INFILES;
do
  INDIR=$(dirname $tarfile)
  # Get just the filename without directory
  FILENAME=$(basename $tarfile)
  if [[ "$FILENAME" == *.tar.gz ]];
  then
    GRFILE=${FILENAME%.tar.gz}
    STEM=${GRFILE%.gr}
    echo "echo $FILENAME; tar -xOf $IS_CLEAN/$INDIR/$FILENAME > $IS_CLEAN/$INDIR/$GRFILE; xz $IS_CLEAN/$INDIR/$GRFILE; rm $IS_CLEAN/$INDIR/$GRFILE.tar.gz"
  fi 
done > $tmpdir/tasks

JOBS=44
echo "Running tasks3 with JOBS=$JOBS (a total of `wc -l $tmpdir/tasks` tasks)"

# Simply output the commands that should be run (for debugging):
#cat $tmpdir/tasks

# Actually run the commands
< $tmpdir/tasks xargs --delimiter='\n' -n1 -P$JOBS sh -c
