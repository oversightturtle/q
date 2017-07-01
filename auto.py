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

import config

if config.con_VIRTUAL == True:
    from virtual import grbl, tlc

def tlc_initsafe():
    global safeloc
    safeloc = True
    tlc.write(b"98")

def stage( sval ):
    print("Stage: %d" %sval)

def read_pps():
    "reads the IR sensor to detect paper pickup. Returns 1 for pickup. 0 for not pickup"
    while True:
        tlc.write("5\r\n\r\n")
        time.sleep(2)
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
            return 2

hip_last = None

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
    
def verbose_wait(delaytime):
    for x in range (0, delaytime):
        time.sleep(1)
        print "waiting > ", x

def primary():
    tstage(19)
    movex(6)
    cali_escape = False
    while cali_escape == False:
        movez_fast(hip_last)
        movez_fast(hip_last - 10)
        tmp_esc = read_pps()
        if int(tmp_esc) == 1:
            cali_escape = True
        elif int(tmp_esc) == 0:
            hip_last == hip_last + 0.02

    print " ***** >> START OF AUTOSEQ << ***** "
    time.sleep(1)
    movez(30)
    movex(19)
    movez(48)
    vac_off()
    time.sleep(1)
    movez(43)
    movexz_instant(13, 35)
    time.sleep(5)
    tstage(20)
    verbose_wait(7)
    movexz_instant(14, 45)
    time.sleep(5)

    tstage(25)
    verbose_wait(42)# 40 + e

    movex(19)
    movez_ins_del(52, 2)
    vac_on()
    time.sleep(1)
    # stage 27 >
    tstage(26)
    movez_ins_del(45, 2)
    movexz_instant(14, 32)
    time.sleep(6)
    movez(15)
    # END HERE -- DELETE AFTER
    movex(1)
    vac_off()
    time.sleep(1)
    # stage 29??? >
    print " ***** >> END OF SEQUENCE << ***** "

    '''
    movex(###)
    movez(###)
    movex()
    vac off
    movez()
    stage33
    movez
    stage36
    movez
    stage37ish
    movez down
    vac on
    movex
    movez
    movex roller
    vac off
    movez
    movex
    movexz out
    stage roll
    move xz
    vac on
    movex off
    movez up

    # REPEAT
    # END REPEAT
    
    movez up
    movex 999...
    vac off
    '''

def home():
#startup and homing sequence
    tlc_initsafe()
    time.sleep(2)
    print "Automation Started"

# you need to manually tell computer when homing is done
    print "Homing Z axis"
    grbl.write("G28 Z")
    commit()
    try:
        a = input(" push any key to continue >> ")
    except SyntaxError:
        pass

    print "Homing Y axis"
    grbl.write("G28 Y")
    commit()
    try:
        a = input(" push any key to continue >> ")
    except SyntaxError:
        pass
    
#   this part creates the initial value of the vac
    movex_fast(6)

    # initial z value for homing
    hip_init = 46.4
    # homing increment for each step
    hip_inc_05= 0.6
    hip_inc_0005 = 0.15
    global hip_last
    hip_escape_05 = False
    hip_escape_0005 = False

    vac_on()

#0.02 accuracy
    # obtain hipvalues to 0.6 unit accuracy
    while hip_escape_05 == False:
        movez_instant(hip_init)
        a = raw_input("press enter to continue (no suction), press any key to stop")
        if a == '':
            hip_init = hip_init + hip_inc_05
        else:
            hip_init = hip_init - hip_inc_05
            hip_escape_05 = True
            vac_off()
            
        time.sleep(2)
        movez_instant(hip_init)
        vac_on()
        time.sleep(1)

    #obtain hipvalues to 0.15 unit accuracy
    while hip_escape_0005 == False:
        movez_instant(hip_init)
        a = raw_input("press any key to end. press enter to lower")
        if a == '':
            hip_init = hip_init + hip_inc_0005
        else:
            hip_init = hip_init - hip_inc_0005
            hip_escape_0005 = True

        hip_last = hip_init
        
isHomed = False

def looper(h = True):
    global isHomed
    if (isHomed == False) and h:
        home()
        isHomed = True
    init = False
    while True:
        primary()
