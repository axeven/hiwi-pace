#!/bin/bash

VALIDATE=./td-validate/td-validate

NUM_PASSED=0
NUM_ALL=0

do_test()
{
for uaifile in input/$1/*.uai;
do
  if [ ! -d "output/$1" ]
  then
    mkdir "output/$1";
  fi
  temp1=${uaifile%%.uai}
  temp2=${temp1##input}
  echo "Translating $uaifile";
  python3 uai2gr.py "$uaifile" > "output$temp2.gr";
done
echo
echo "Validating outputs ... "
for grfile in output/$1/*.gr;
do
  file="${grfile%%.out.gr}"
  NUM_ALL=$[$NUM_ALL + 1]
  $VALIDATE "$grfile" &> /dev/null;
  STATE=$?
  if [ "0$STATE" -eq "0$2" ]
  then
    diff "$grfile" "$file.gr" &> /dev/null;
    tput setaf 2;
    echo "ok  " "$file" "(valid gr)"
    NUM_PASSED=$[$NUM_PASSED + 1]
  else
    tput setaf 1;
    echo "FAIL" "$file" "(invalid gr)"
  fi
done
tput sgr0;
}

if [ ! -d "output" ] ;
then
  echo "Creating output directory" ;
  mkdir "output";
fi

do_test input1 0
echo 
do_test input2 0
echo
do_test input3 0

tput sgr0;

echo
echo "$NUM_PASSED of $NUM_ALL outputs are valid."
echo

test $NUM_PASSED = $NUM_ALL
