#!/usr/bin/lua

local GPIO=require "GPIO"

GPIO.setmode(GPIO.BOARD)

GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)

GPIO.output(3, 1)
os.execute(2)

GPIO.output(3, 0)

GPIO.cleanup()
