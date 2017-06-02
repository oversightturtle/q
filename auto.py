import time
from gops import *
from tops import operatestage



tstage = operatestage

pickuplevel = 0

try:
    from setup import grbl
except ImportError:
    pass

try:
    from setup import tlc
except ImportError:
    pass

def tlc_initsafe():
    global safeloc
    safeloc = True
    tlc.write(b"98")


def stage( sval ):
    print("Stage: %d" %sval)
    return

def pulse(mx):
    def movex( xval ):
        movex_ins_del( xval , 1)
    def movez( zval ):
        movez_ins_del( zval, 1.5)
    upper = mx - 8
    movex(35)
    movez(mx)
    movez(upper)
    movex(36)
    movez(mx)
    movez(upper)
    movex(37)
    movez(mx)
    movez(upper)
    movex(38)
    movez(mx)
    movez(upper)
    movex(38.5)

def pulse_concat(mx):
    def movex( xval ):
        movex_ins_del( xval , 1)
    def movez( zval ):
        movez_ins_del( zval, 1.5)
    upper = mx - 8
    movex(35.5)
    movez(mx)
    movez(upper)
    movex(36)
    movez(mx)
    movez(upper)
    movex(37)
    movez(mx)
    movez(upper)
    movex(38)
    movez(mx)
    movez(upper)
    movex(38.5)

def read_pps():
    while True:
        tlc.reset_input_buffer()
        stringo = tlc.read(5)
        print stringo
        if stringo == '11111':
            print "obstruction"
            return 1
        elif stringo == '00000':
            print "no obs."
            return 0
        else:
            print "conflicting values > too noisy" , stringo

def autoposition( initial, offset, limit, inc):
    
    __delay = 3
    escape = False
    current = initial

    while (escape == False) and (current != limit):
        movez_direct(current)
        time.sleep( __delay )
        movez_direct(current - offset)
        time.sleep( __delay )
        tlc.write("5")
        det = read_pps()
        if det == False:
            print "no obs"
        else:
            print "obs found"
            escape = True
            global pickuplevel
            pickuplevel = (current - inc)
        current += inc


def autotest():
    grbl.write("G28 Z")
    dcommit()
    vac_off() ###
    autoposition(
        offset = 28,
        initial = 245,
        limit = 267,
        inc = 1
    )
        
def autoset(initial, offset, limit, inc):
    time.sleep(1)
    vac_on()
    escape = False
    current = initial
    while escape == False:
        movez_direct(current)
        try: 
            a = input(" press enter to continue >> (type any key to halt) >> ")
            print "uhoh!"
            vac_off()
            return ( current - inc)
        except SyntaxError:   
            current += inc
        except NameError:
            vac_off()
            return ( current - inc)

def pri_init():

    tlc_initsafe()
    movex(3)
    #######################################
    vac_on()
    initialx = autoset(
        initial = 243,
        offset = 0,
        limit = 267,
        inc = 4)

    movez_direct(240)

    initialxx = autoset(
        initial = initialx,
        offset = 0,
        limit = 267,
        inc = 1)

    movez_direct(240)
    
    vac_on()
    autoposition(
        initialxx,
        offset = 28,
        limit = 267,
        inc = 0.25
    )
    #######################################

def pri_loop():

    movex(3)
    global pickuplevel
    vac_on()
    autoposition(
        initial = pickuplevel,
        offset = 28,
        limit = 267,
        inc = 0.25
    )
    

def primary():
    tstage(19)
    movex(6)
    movez(50) ## calibrate

    g_old = 50
    g_new = 49
    g_c_escape = False
    while g_c_escape == False:
        while g_old != g_new:
            a = raw_input("manually calibrbate the z value >> ")
            movez_instant(float(a))
            g_old = g_new
            g_new = a
        vac_on()
        time.sleep(1)
        movez_instant(40)
        a = raw_input("type 40 to confirm >> ")
        if int(a) == 40:
            g_c_escape = True
        g_old = 50
        g_new = 49

    vac_on()
    time.sleep(1)
    movez(30)
    movex(19)
    movez(48)
    vac_off()
    time.sleep(1)
    movexz(13, 35)
    tstage(20)
    time.sleep(1)
    movexz(14, 45)
    movex(19)
    movez_ins_del(51, 2)
    movez_ins_del(48, 2)
    movex(21)
    movez_ins_del(51, 2)
    movez_ins_del(48, 2)
    movex(14)
    tstage(25)
    for x in range (0, 30):
        time.sleep(1)
        print "waiting > ", x
    movex(19)
    movez_ins_del(52, 2)
    vac_on()
    time.sleep(1)
    tstage(26)
    movez_ins_del(45, 2)
    movexz(14, 32)
    movez(15)
    movex(32)
    vac_off()
    time.sleep(1)

def primary_OLD():

    tstage(19)###
    movez(150)
    movex(32.83)
    movez(263)
    movex(32.75)
    vac_off()
    time.sleep(1)

    movexz(35.5, 120)

    tstage(20)###

    pulse_concat(269) # >>

    movez(100)
    tstage(25)###
    movex(32.5)
    pulse(267) # >>
    movez(120)
    movex(34.5)
    vac_on()
    movez(267)
    tstage(26)###
    movez(263)
    tstage(27)###
    movexz(27, 200)
    movez(150)
    movex(40)
    vac_off()
    


def home():
#startup and homing sequence
    tlc_initsafe()
    time.sleep(2)
    print "Automation Started"
    print "Homing Z axis"
#    grbl.write("G28 Z\r\n".encode())
    grbl.write("G28 Z")
    commit()
    try:
        a = input(" push any key to continue >> ")
    except SyntaxError:
        pass

# you need to manually tell computer when homing is done
    print "Homing Y axis"
#    grbl.write("G28 Y\r\n".encode())
    grbl.write("G28 Y")
    commit()
    try:
        a = input(" push any key to continue >> ")
    except SyntaxError:
        pass
        
isHomed = False

def looper(h = True):

    global isHomed
    if (isHomed == False )and h:
        home()
        isHomed = True
    init = False
    while True:
        primary()
'''
    while True:
        if init == False:
            pri_init()
            init = True
        else :
            pri_loop()
        primary()
'''




