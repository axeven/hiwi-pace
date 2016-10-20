#!/bin/bash

VALIDATE=./td-validate/td-validate

NUM_PASSED=0
NUM_ALL=0

IFS=""
TESTTASKS=(test/BlanusaSecondSnarkGraph.gr\ -c\ 6\ -r\ 0\ \>\ test/BSSG_6_0.out.gr
test/BlanusaSecondSnarkGraph.gr\ -c\ 6\ -r\ 1\ \>\ test/BSSG_6_1.out.gr
test/BlanusaSecondSnarkGraph.gr\ -c\ 6\ -r\ 2\ \>\ test/BSSG_6_2.out.gr
test/BlanusaSecondSnarkGraph.gr\ -c\ 6\ -r\ 3\ \>\ test/BSSG_6_3.out.gr
test/BlanusaSecondSnarkGraph.gr\ -c\ 6\ -r\ 4\ \>\ test/BSSG_6_4.out.gr
test/BlanusaSecondSnarkGraph.gr\ -c\ 6\ -r\ 5\ \>\ test/BSSG_6_5.out.gr
)
IFS=""

do_test()
{
IDX=0
echo "Performing BFS on test instances ...";
for ttask in "${TESTTASKS[@]}"
do
  eval "python3 BFS.py "$ttask;
done
python3 BFS.py test/BAY.gr -c 6 -r 20 > test/BAY.out.gr;
echo "Validating output ...";
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
      echo "ok  " "$file" "(valid gr + result)";
      NUM_PASSED=$[$NUM_PASSED + 1]
    else
      if [ "$file" = "test/BAY" ]; then
        tput setaf 2;
        echo "ok  " "$file" "(valid gr)";
        NUM_PASSED=$[$NUM_PASSED + 1]
      else
        tput setaf 1;
        echo "FAIL" "$file" "(invalid result)";
      fi
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
