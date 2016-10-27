#!/bin/bash

VALIDATE=./td-validate/td-validate

NUM_PASSED=0
NUM_ALL=0

IFS=""
TESTTASKS=(test/dirty/test1.gr\ \>\ test/dirty/test1.out.gr
test/dirty/test2.gr\ \>\ test/dirty/test2.out.gr
test/clean/test3.gr\ \>\ test/clean/test3.out.gr
test/clean/test4.gr\ \>\ test/clean/test4.out.gr
)
IFS=""

do_test_make_clean()
{
IDX=0
echo "Performing make_clean on test instances ...";
for ttask in "${TESTTASKS[@]}"
do
  eval "python3 make_clean.py "$ttask;
done
echo "Validating output ...";
for grfile in test/$2/*.out.gr;
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

do_test_is_clean()
{
IDX=0
echo "Performing is_clean on test instances ...";

for grfile in test/$1/*.clean.gr;
do
  file="${grfile%%.clean.gr}"
  NUM_ALL=$[$NUM_ALL + 1]
  python3 is_clean.py $file.gr > $file.gr.out;
  STATE=$?
  if [ "0$STATE" -eq "0$2" ]
  then
    diff "$grfile" "$file.is_clean.out" &> /dev/null;
    STATEDIFF=$?
    if [ "0$STATEDIFF" -eq "00" ]
    then
      tput setaf 2;
      echo "ok  " "$file" "(valid exitcode + result)";
      NUM_PASSED=$[$NUM_PASSED + 1]
    else
      tput setaf 1;
      echo "FAIL" "$file" "(different result)";
    fi
  else
    tput setaf 1;
    echo "FAIL" "$file" "(invalid exitcode)"
  fi
done
}

do_test_make_clean 0 dirty
tput sgr0;

do_test_make_clean 0 clean
tput sgr0;

do_test_is_clean dirty 1
tput sgr0;

do_test_is_clean clean 0
tput sgr0;

echo
echo "$NUM_PASSED of $NUM_ALL tests passed."
echo

test $NUM_PASSED = $NUM_ALL
