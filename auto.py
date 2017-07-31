import time
from gops import *
from tops import operatestage

tstage = operatestage

pickuplevel = 0

# 99.5 >> 46.5
# Z OFFSET -> + 53

ZOFFSET = 53

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
    
def verbose_wait(delaytime):
    for x in range (0, delaytime):
        time.sleep(1)
        print "waiting > ", x

def primary():
    '''
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
    movez(25 + ZOFFSET)
    movex(19)
    movez(48 + ZOFFSET)
    vac_off()
    time.sleep(1)
    movez(43 + ZOFFSET)

    movexz_instant(13, 35 + ZOFFSET)
    time.sleep(5)
    tstage(25) # 45 SECONEDS
    verbose_wait(25)# 40 + e

    movex(19)
    movez(96.5)
    tstage(26)
    verbose_wait(15)

    movez_ins_del(101)
    vac_on()
    time.sleep(1)
    # stage 27 >
    tstage(27)
    time.sleep(6)
    ### Z40 UP MOVE SX LOW

    movez_ins_del(98, 2)
    movexz_instant(14, 60)
    time.sleep(6)
    movez(15 + ZOFFSET)
    tstage(29) # END HERE
    
    # END HERE -- DELETE AFTER

    print "dead ### INTERVENE HERE"
    verbose_wait(10)
    '''
    
    movex(19)
    movez(97)
    tstage(26)
    verbose_wait(4)
    movez(101)
    vac_on()
    movez(97)
    movexz_instant(9, 50)
    time.sleep(10)
    tstage(29)
    movez(20)
    movex(52)

    #STAGE 3
    
    movex(52)
    tstage(30)
    movez(104.8)
    movex(50.8)
    movex(46.35)
    vac_off()
    movez(100)
    movexz_instant(60, 90)
    verbose_wait(10)
    tstage(31)
    movexz_instant(48, 101) ## CHECK BELOW MOVE Y?!?!?
    verbose_wait(3)
    movez(105)
    tstage(33) # set to safe
    movez(100)
    movexz_instant(60, 90) ### PROBLEM S4 SAFEPLACE PUSHDOWN NOT HIGH ENOUGH
    # REDO THE STAGE +- 5 LINES
    verbose_wait(8) # CHANGE WAITSEQ
    tstage(36)
    verbose_wait(20)
    movexz(46.35, 105)
    verbose_wait(8)
    movex(52.5)

    #STAGE 4

    tstage(40) ### set to open
    movez(30)
    movex(75)
    movez(100)
    movez(80)
    movex(74.5)
    movez(82.3)
    movex(74.3)
    movex(72.8)
    vac_off()
    movez(75)
    movexz_instant(70, 70)
    verbose_wait(8)
    movex(60)
    tstage(45) # flips
    movex(72.8)
    movez(82)
    vac_on()
    movex(75)
    movez(60)
    
    #STAGE 3
    
    movex(52)
    tstage(30)
    movez(104.8)
    movex(50.8)
    movex(46.35)
    vac_off()
    movez(100)
    movexz_instant(60, 90)
    verbose_wait(10)
    tstage(31)
    movexz_instant(48, 101)
    verbose_wait(3)
    movez(105)
    tstage(33) # set to safe
    movez(100)
    movexz_instant(60, 90)
    verbose_wait(8)
    tstage(36)
    verbose_wait(20)
    movexz(46.35, 105)
    verbose_wait(8)
    movex(52.5)

    #PUTDOWN

    movex(53.5)
    vac_off()

    #ENDSTATE
    tstage(99)
    verbose_wait(5)
    movez(40)

    ##################################
    #ASSUME
    print " ***** >> END OF SEQUENCE << ***** "
 

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

    '''
    
#   this part creates the initial value of the vac
    movex_fast(6)

    # initial z value for homing
    hip_init = (46.4 + ZOFFSET)
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
    '''    
isHomed = False

def looper(h = True):
    global isHomed
    if (isHomed == False) and h:
        home()
        isHomed = True
    init = False
    while True:
        primary()
