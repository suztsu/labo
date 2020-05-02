import bluepy

scanner = bluepy.btle.Scanner(0)
devices = scanner.scan(3)

for device in devices:
    print('addr: %s' % device.addr)
    for (adtype, desc, value) in device.getScanData():
        print('%s : %s' % (desc, value))