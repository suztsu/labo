#!/usr/bin/bash

gnome-terminal --tab --active -- julius -C ~/julius/dict-kit/dictation-kit-4.5/command.jconf -module
sleep 5
/usr/bin/python3 /home/pi/dev/labo/folocommandar/commandar.py
