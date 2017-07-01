import serial
import time

def tty_config():
    as_maxrange = 6
    as_numfound = 0
    as_tp_active = False
    
    debugmode = False
    def debugprint(s):
        if debugmode:
            print s
        
    for x in range (0, as_maxrange):
        # determines weather a port is open
        as_tp_active = False
        try:
            testport = serial.Serial('/dev/ttyACM%d' %x, 9600, timeout=3)
            as_tp_active = True
        except serial.SerialException:
            pass
        if as_tp_active:
            debugprint(x)
            # tests if found active testport is a tlc
            try:
                tlc_canidate = serial.Serial('/dev/ttyACM%d' %x,
                baudrate=9600, timeout=10)
                tlc_canidate.write("\r\n\r\n")
                time.sleep(2)
                tlc_canidate.reset_input_buffer()
                tlc_canidate.write("55")
                testcan = tlc_canidate.read(5)
       #         print testcan, " >done>"
                if testcan == '00000':
                    #confirms tlc
                    as_numfound += 1
                    tlc_canidate.close()
                    global tlc
                    tlc = serial.Serial('/dev/ttyACM%d' %x, 9600, timeout=3)
                    print "tlc  @ ttyACM%d" % x, "@ 9600"
                    as_tp_active = False
            except serial.SerialException:
                tlc_canidate.close()
                pass
        
        if as_tp_active:
            #tests if found active testport is a grbl
            try:
                grbl_canidate = serial.Serial('/dev/ttyACM%d' %x,
                baudrate=115200, timeout = 3)
                # WAKES up da grbl and waits for init post script
                grbl_canidate.write('\r\n\r\n')
                time.sleep(2)
                grbl_canidate.reset_input_buffer()
                grbl_canidate.write("M119\r\n\r\n")
                testcan = grbl_canidate.read(5)
                debugprint(">")
                debugprint(testcan)
                if testcan == '99999':
                    #confirms grbl life 3
                    as_numfound += 1
                    grbl_canidate.close()
                    global grbl
                    grbl = serial.Serial('/dev/ttyACM%d' %x,
                    baudrate = 115200)
                    print "grbl @ ttyACM%d" % x, "@ 115200" 
                    as_tp_active == False
            except serial.SerialException:
                grbl_canidate.close()
                pass