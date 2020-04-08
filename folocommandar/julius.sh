#!/usr/bin/bash

julius -C ~/julius/dict-kit/dictation-kit-4.5/command.jconf -module　> /dev/null &
echo $!
sleep 1
