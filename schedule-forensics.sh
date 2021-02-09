#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

((!$#)) && echo No arguments supplied! && exit 1

echo "Will schedule the following command (test before running):"
echo "(cd \"$DIR\"; ./gen.py $@)"

read  -n 1 -p "Have you tried test email (y|n)? " hastested

if [ $hastested != "y" ]; then
  echo "Aborting..."
  exit 1
fi

MONDAY=${MONDAY:-Monday}
WEDNESDAY=${WEDNESDAY:-Wednesday}
FRIDAY=${FRIDAY:-Friday}

# schedule only on Saturday/Sunday; for the next week
if [[ ! -v no_monday ]]; then 
  echo "(cd \"$DIR\"; ./gen.py $@ -s 'WILL SPAM SOON: ')" | at 10:30am $MONDAY
  echo "(cd \"$DIR\"; ./gen.py $@ send)" | at 11am $MONDAY
fi

if [[ ! -v no_wednesday ]]; then
  echo "(cd \"$DIR\"; ./gen.py -s 'WILL SPAM SOON: ' $@)" | at 10:30am $WEDNESDAY
  echo "(cd \"$DIR\"; ./gen.py -s 'Reminder: ' $@ send)" | at 11am $WEDNESDAY
fi

if [[ ! -v no_friday ]]; then
  echo "(cd \"$DIR\"; ./gen.py -s 'WILL SPAM SOON: ' $@)" | at 10:00am $FRIDAY
  echo "(cd \"$DIR\"; ./gen.py -s 'Reminder: ' $@ send)" | at 10:30am $FRIDAY
  echo "(cd \"$DIR\"; ./gen.py -s 'STARTING NOW: ' $@ send)" | at 12:57pm $FRIDAY
fi

