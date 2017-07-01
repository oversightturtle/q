import serial
import time

def config():
    setup = False
    while setup == False:
        try:
            setup = intconfig()
        except serial.SerialException:
            print " >>>>> Port not found >>>>>"
            print " "

def intconfig():
    print "initating the serial ports:"
    print "0 >> grbl at acm0 && tlc at acm1"
    print "1 >> grbl at acm1 && tlc at acm0"
    print "2 >> grbl at acm0"
    print "3 >> grbl at acm1"
    print "4 >> tlc  at acm0"
    print "5 >> tlc  at acm1"
    print "6 >> tlc  at usb0"
    print "7 >> tlc  at usb1"
    com = input(' >>> ')
    if int(com) == 0:
        grbl = serial.Serial('/dev/ttyACM0', 115200)
        tlc = serial.Serial('/dev/ttyACM1', 9600)

    elif int(com) == 1:
        grbl = serial.Serial('/dev/ttyACM1', 115200)
        tlc = serial.Serial('/dev/ttyACM0', 9600)

    elif int(com) == 2:
        grbl = serial.Serial('/dev/ttyACM0', 115200)
    
    elif int(com) == 3:
        grbl = serial.Serial('/dev/ttyACM1', 115200)

    elif int(com) == 4:
        tlc = serial.Serial('/dev/ttyACM0', 9600)

    elif int(com) == 5:
        tlc = serial.Serial('/dev/ttyACM1', 9600)

    elif int(com) == 6:
        tlc = serial.Serial('/dev/ttyUSB0', 9600)

    elif int(com) == 7:
        tlc = serial.Serial('/dev/ttyUSB1', 9600)


    try:
        global grbl
    except NameError:
        pass

    try:
        global tlc
    except NameError:
        pass

    return True

