#!/bin/bash

VALIDATE=./td-validate/td-validate

NUM_PASSED=0
NUM_ALL=0

IFS=""
TESTTASKS=(test/test1.gr\ \>\ test/test1.out.gr
test/test2.gr\ \>\ test/test2.out.gr
test/test3.gr\ \>\ test/test3.out.gr
test/test4.gr\ \>\ test/test4.out.gr
)
IFS=""

do_test()
{
IDX=0
echo "Performing clean on test instances ...";
for ttask in "${TESTTASKS[@]}"
do
  eval "python3 make_clean.py "$ttask;
done
echo "Validating output ...";
for grfile in test/*.out.gr;
do
  file="${grfile%%.out.gr}"
  NUM_ALL=$[$NUM_ALL + 1]
  $VALIDATE "$grfile" &> /dev/null;
  STATE=$?
  if [ "0$STATE" -eq "0$1" ]
  then
    diff "$grfile" "$file.clean.gr" &> /dev/null;
    STATEDIFF=$?
    if [ "0$STATEDIFF" -eq "00" ]
    then
      tput setaf 2;
      echo "ok  " "$file" "(valid gr + result)";
      NUM_PASSED=$[$NUM_PASSED + 1]
    else
      tput setaf 1;
      echo "FAIL" "$file" "(different result)";
    fi
  else
    tput setaf 1;
    echo "FAIL" "$file" "(invalid gr)"
  fi
done
}

do_test 0

tput sgr0;

echo
echo "$NUM_PASSED of $NUM_ALL tests passed."
echo

test $NUM_PASSED = $NUM_ALL
