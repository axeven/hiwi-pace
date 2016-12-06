#!/bin/bash

VALIDATE=./td-validate/td-validate

NUM_PASSED=0
NUM_ALL=0

do_test_nice_td()
{
for inp_td in test/*.orig.td;
do
  python3 nice_td.py "$inp_td" > "$inp_td.out";
done
for out_td in test/*.out;
do
  file="${out_td%%.out}"
  stem="${file%%.orig.td}"
  NUM_ALL=$[$NUM_ALL + 1]
  $VALIDATE test/test.gr "$out_td" &> /dev/null;
  STATE=$?
  if [ "0$STATE" -eq "0$1" ]
  then
    diff "$out_td" "$stem.nice.td" &> /dev/null;
    STATEDIFF=$?
    if [ "0$STATEDIFF" -eq "00" ]
    then
      tput setaf 2;
      echo "ok  " "$file" "(valid + nice td)"
      NUM_PASSED=$[$NUM_PASSED + 1]
    else
      tput setaf 1;
      echo "FAIL" "$file" "(may not be a nice td)"
    fi
  else
    tput setaf 1;
    echo "FAIL" "$file" "(invalid td)"
  fi
  tput sgr0;
done
}

do_test_nice_td 0

echo
echo "$NUM_PASSED of $NUM_ALL tests passed."
echo

test $NUM_PASSED = $NUM_ALL
