#!/bin/bash

VALIDATE=./td-validate/td-validate

NUM_PASSED=0
NUM_ALL=0

do_test()
{
for uaifile in test/*.uai;
do
  python3 translate.py "$uaifile" > "$uaifile.out.gr";
done
for grfile in test/*.out.gr;
do
  file="${grfile%%.out.gr}"
  NUM_ALL=$[$NUM_ALL + 1]
  $VALIDATE "$grfile" &> /dev/null;
  STATE=$?
  if [ "0$STATE" -eq "0$1" ]
  then
    diff "$grfile" "$file.gr" &> /dev/null;
    STATEDIFF=$?
    if [ "0$STATEDIFF" -eq "00" ]
    then
      tput setaf 2;
      echo "ok  " "$file" "(valid gr + translation)"
      NUM_PASSED=$[$NUM_PASSED + 1]
    else
      tput setaf 1;
      echo "FAIL" "$file" "(invalid translation)"
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
