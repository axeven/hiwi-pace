#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

MAKE_CLEAN=./make_clean.py
IS_CLEAN=./is_clean.py
echo "Finding all *.gr* files in task3_input..."
INFILES=`find -L task3_input -name '*.gr*'`
tmpdir=$(mktemp --directory --tmpdir=/dev/shm $(basename $0)-XXXXXXXX)
trap "rm -rf $tmpdir" EXIT


echo "Creating the tasks..."
for grfile in $INFILES;
do
  INDIR=$(dirname $grfile)
  OUTDIR=$(echo $INDIR | sed 's/task3_input/task3_output/')

  # Create directory structure in task3_output
  if [ ! -d $OUTDIR ]
  then
    mkdir -p $OUTDIR
  fi

  # Get just the filename without directory
  FILENAME=$(basename $grfile)
  if [[ "$FILENAME" == *.bz2 ]];
  then
    GRFILE=${FILENAME%.bz2}
    STEM=${GRFILE%.gr}
    echo "echo $FILENAME; bzcat $INDIR/$FILENAME > $tmpdir/$GRFILE; python3 $MAKE_CLEAN $tmpdir/$GRFILE > $OUTDIR/"$STEM".gr;python3 $IS_CLEAN $OUTDIR/"$STEM".gr > $OUTDIR/"$STEM".gr.clean;tar -czvf $OUTDIR/"$STEM".tar.gz $OUTDIR/"$STEM".gr; rm $OUTDIR/"$STEM".gr;rm $tmpdir/$GRFILE"
    
  fi
  if [[ "$FILENAME" == *.xz ]];
  then
    GRFILE=${FILENAME%.xz}
    STEM=${GRFILE%.gr}
    echo "echo $FILENAME; xzcat $INDIR/$FILENAME > $tmpdir/$GRFILE; python3 $MAKE_CLEAN $tmpdir/$GRFILE > $OUTDIR/"$STEM".gr;python3 $IS_CLEAN $OUTDIR/"$STEM".gr > $OUTDIR/"$STEM".gr.clean;tar -czvf $OUTDIR/"$STEM".tar.gz $OUTDIR/"$STEM".gr; rm $OUTDIR/"$STEM".gr;rm $tmpdir/$GRFILE"
  fi
  if [[ "$FILENAME" == *.gr ]];
  then
    GRFILE=$FILENAME    
    STEM=${GRFILE%.gr}
    echo "echo $FILENAME; $MAKE_CLEAN $INDIR/$GRFILE > $OUTDIR/"$STEM".gr;python3 $IS_CLEAN $OUTDIR/"$STEM".gr > $OUTDIR/"$STEM".gr.clean;tar -czvf $OUTDIR/"$STEM".tar.gz $OUTDIR/"$STEM".gr; rm $OUTDIR/"$STEM".gr"
   
  fi
done > $tmpdir/tasks

JOBS=44
echo "Running tasks3 with JOBS=$JOBS (a total of `wc -l $tmpdir/tasks` tasks)"

# Simply output the commands that should be run (for debugging):
#cat $tmpdir/tasks

# Actually run the commands
< $tmpdir/tasks xargs --delimiter='\n' -n1 -P$JOBS sh -c
