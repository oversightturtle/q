import serial
import time

nopen = 0
global nopen

def config():
    global nopen
    nlist = [0,0,0,0,0,0,0,0]
    def search( recall = False ):
        for x in range (0, 8):
            try:
                testport = serial.Serial('/dev/ttyACM%d' %x, 9600)
          #      debugtest = serial.Serial('/dev/ttyUSB%d' %x, 9600)
                nlist[x] = 1
                nopen += 1
                print "port " + str(x) + " [ACTIVE]"
                testport.close()
       #         debugtest.close()
            except serial.SerialException :
                print "port " + str(x) + " [NOT ACTIVE]"
        if recall == True:
            setSer()

    def cleanports():
        # removes all but the last 2 ports
        for x in range (0,8):
            if ((nopen - 2) != 0) and (nlist[x] == 1):
                nlist[x] == 0

    def setSer():
        # safety check for the numbers()
        if int(nopen) > 2:
            print "ERROR FOUND MORE THEN 2 PORTS"
            print "wiping all but the last 2 ports"
            cleanports()
            setSer()
        if int(nopen) == 0:
            a = raw_input("no ports found >> 0 to override, 1 to retry >> ")
            if int(a) == 1:
                search(recall = True)
                return 1
            if int(a) == 0:
                return 0
        if int(nopen) == 1:
            print "set the port to (g)rbl or (t)lc?"
            a = raw_input(" >> ")
            if a == ( "g" or "grbl" ):
                for x in range(0,8):
                    if nlist[x] == 1:
                        grbl = serial.Serial('/dev/ttyACM%d' %x, 115200)
            elif a == ( "t"or "tlc" ):
                for x in range(0,8):
                    if nlist[x] == 1:
                        tlc = serial.Serial('/dev/ttyACM%d' %x, 9600)
            else:
                print "invalid choice"
                setSer()
        if int(nopen) == 2: 
            print "0 >> grbl to 0, tlc to 1"
            print "1 >> grbl to 1, tlc to 0"
            a = raw_input(" >> ")
            isFirst = True
            for x in range(0, 8):
                if (nlist[x] == 1) and (isFirst == True):
                    port1 = serial.Serial('/dev/ttyACM%d' %x, 115200)
                    isFirst = False
                if (nlist[x] == 1) and (isFirst == False):
                    port2 = serial.Serial('/dev/ttyACM%d' %x, 9600)
            if int(a) == 0:
                g, x = port1, port2
            elif int(a) == 1:
                g, x = port2, port1
            else:
                print "invalid choice"
                setSer()

    try:
        global grbl
    except NameError:
        pass

    try:
        global tlc
    except NameError:
        pass
    search()
    setSer()

