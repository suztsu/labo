import socket
import string
import time
import subprocess
import bluepy
from bluepy import btle

# サブプロセスでJuliusをmoduleモードで起動する
p = subprocess.Popen("./julius.sh",
                     stdout=subprocess.PIPE, shell=True)
pid = str(p.pid)
time.sleep(1)
print("julius を起動しました")

# micro:bitとのBluetooth接続情報（LEDサービスを使用）
uuid_uart_service = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
uuid_uart_rx = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
device_addr = "d5:8a:b3:87:c2:22"
per = btle.Peripheral(device_addr, btle.ADDR_TYPE_RANDOM)
uartsvc = per.getServiceByUUID(uuid_uart_service)
uartrx = uartsvc.getCharacteristics(uuid_uart_rx)[0]

# JuliusとのSocket接続を開く
host = 'localhost'
port = 10500
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
print("Juliusとのソケット接続を確立しました")

try:
    recvdata = ""
    commanddict = {
        "とまれ": "ST",
        "すすめ": "FW",
        "もどれ": "BK",
        "みぎ": "TR",
        "ひだり": "TL",
        "いそげ": "HL",
        "ゆっくり": "SL",
    }

    while True:
        while (recvdata.find("\n.") == -1):
            recvdata = recvdata + sock.recv(1024).decode("utf-8")

        # 受信データを解析し、認識した文字列を取り出す
        word = ""
        for line in recvdata.split('\n'):
            i = line.find('WORD="')
            if i != -1:
                line = line[i + 6:line.find('"', i + 6)]
                if line != "[s]" and line != "[/s]":
                    word += line

        # フォロへ送信するコマンド文字列に変換する
        try:
            command = commanddict[word] += "#"
            # フォロへコマンド文字列を送信する
            print(command)
            uartrx.write(bytearray(command.encode("utf-8")))
        except KeyError:

        recvdata = ""

except KeyboardInterrupt:
    p.kill()
    sock.close()
