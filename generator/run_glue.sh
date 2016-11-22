#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

GLUE=/home/debjit/Documents/hiwi-pace/generator/randomly_glue_graphs.py

echo "Finding all *.gr* files in task5_input..."
INFILES=`find -L task5_input -name '*.gr*'`
tmpdir=$(mktemp --directory --tmpdir=/dev/shm $(basename $0)-XXXXXXXX)
trap "rm -rf $tmpdir" EXIT


echo "Creating the tasks..."
for grfile in $INFILES;
do
  INDIR=$(dirname $grfile)
  OUTDIR=$(echo $INDIR | sed 's/task5_input/task5_output/')

  # Create directory structure in task5_output
  if [ ! -d $OUTDIR ]
  then
    mkdir -p $OUTDIR
  fi

  # Get just the filename without directory
  FILENAME=$(basename $grfile)  
  if [[ "$FILENAME" == *.gr ]];
  then
    GRFILE=$FILENAME
    for c in 10 20 30 40 50 60 70 80 90 100;
    do
      STEM=${GRFILE%.gr}
      echo "echo $FILENAME; python3 $GLUE --C $c $INDIR/$GRFILE > $OUTDIR/"$STEM"_C$c.gr"
    done
  fi
done > $tmpdir/tasks

JOBS=1
echo "Running tasks3 with JOBS=$JOBS (a total of `wc -l $tmpdir/tasks` tasks)"

# Simply output the commands that should be run (for debugging):
#cat $tmpdir/tasks

# Actually run the commands
< $tmpdir/tasks xargs --delimiter='\n' -n1 -P$JOBS sh -c
