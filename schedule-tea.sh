#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

((!$#)) && echo No arguments supplied! && exit 1

echo "Will schedule the following command (test before running):"
echo "(cd \"$DIR\"; ./gtea.py $@)"

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
  echo "(cd \"$DIR\"; ./gtea.py $@ -s 'WILL SPAM SOON: ')" | at 9:35am $MONDAY
  echo "(cd \"$DIR\"; ./gtea.py $@ send)" | at 10am $MONDAY
fi

if [[ ! -v no_wednesday ]]; then
  echo "(cd \"$DIR\"; ./gtea.py -s 'WILL SPAM SOON: ' $@)" | at 9am $WEDNESDAY
  echo "(cd \"$DIR\"; ./gtea.py -s 'Reminder: ' $@ send)" | at 10am $WEDNESDAY
  echo "(cd \"$DIR\"; ./gtea.py -s 'STARTING NOW: ' $@ send)" | at 2:00pm $WEDNESDAY
fi

