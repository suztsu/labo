import socket
import string
import time
import subprocess
import bluepy
from bluepy import btle

res = subprocess.run(["julius", "-C", "~/julius/dict-kit/dictation-kit-4.5/command.jconf", "-module"], stdout=subprocess.PIPE, shell=True)
time.sleep(5)

# micro:bitとのBluetooth接続情報（LEDサービスを使用）
# uuid_led_service = "E95DD91D-251D-470A-A062-FA1922DFA9A8"
# uuid_led_text = "e95d93ee-251d-470a-a062-fa1922dfa9a8"
uuid_uart_service ="6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
uuid_uart_rx = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
device_addr = "d5:8a:b3:87:c2:22"
per = btle.Peripheral(device_addr, btle.ADDR_TYPE_RANDOM)
# ledsvc = per.getServiceByUUID(uuid_led_service)
# ledsvcchar = ledsvc.getCharacteristics(uuid_led_text)[0]
uartsvc = per.getServiceByUUID(uuid_uart_service)
uartrx = uartsvc.getCharacteristics(uuid_uart_rx)[0]

# JuliusとのSocket接続を開く
host = 'localhost'
port = 10500
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

recvdata = ""

while True:
    while (recvdata.find("\n.") == -1):
        recvdata = recvdata + sock.recv(1024).decode("utf-8")
    
    word = ""
    for line in recvdata.split('\n'):
        i = line.find('WORD="')
        if i != -1:
            line = line[i + 6:line.find('"', i + 6)]
            if line != "[s]" and line != "[/s]":
                word += line
    
    # print("結果:" + word)

    command = ""
    if word == "とまれ":
        command = "S"
    elif word == "すすめ":
        command = "G"
    elif word == "もどれ":
        command = "B"
    elif word == "みぎ":
        command = "R"
    elif word == "ひだり":
        command = "L"

    if command != "":
        # ledsvcchar.write(command.encode("utf-8"))
        uartrx.write(bytearray(command))

    recvdata = ""
