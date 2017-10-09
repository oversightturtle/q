import sys
import time
from gops import *
from tops import operatestage, operateservo
from config import con_VIRTUAL

from config import workingtime

tstage = operatestage

pickuplevel = 0


### 62.0 >> 50.5

# 99.5 >> 46.5
# Z OFFSET -> + 53

ZOFFSET = 11.6

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

def head_overload():
#    operateservo(19, 480)
    operateservo(19, 470)

def head_down():
    operateservo(19, 470)

def head_down_right():
    operateservo(19, 465)

def head_down_right_right():
    operateservo(19, 462)

def head_up():
    operateservo(19, 270)

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

def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()


    
def verbose_wait(delaytime):
    global workingtime
    workingtime += delaytime
    for x in range (0, delaytime):
        time.sleep(1)
        print " waiting > ", x , "/", delaytime,
        restart_line()
        if x+1 == delaytime:
            print " "

def primary():
    ''' >>>>>>>>>>>>>>>>>>>>>>> # change ZOFFSET before uncomment <<<<<<<<<<<<<<<<<<<<<<<<
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
    
    head_down()

    movex(14)
    movez(ZOFFSET + 50.5 - 5)
    movex(18.1)
    tstage(26)
    verbose_wait(2)
    vac_on()
    verbose_wait(2)
    movez(ZOFFSET + 50.5)
    vac_on()
    verbose_wait(3)
    movez(ZOFFSET + 40)
    tstage(27)
    verbose_wait(3)
    movex(17.5)
    movez(ZOFFSET + 25)
    movex(10)
#    head_up()    # up to 14 ASSUMED DONE ON STAGE 29
    verbose_wait(3)
    tstage(29) # closes and fold safe
    verbose_wait(10)

    movex(60)
 
    #STAGE 3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #105.35 END
     
    movex(60) #moves way out to prevent conflict
    tstage(30) # open upplace and load
    movez(ZOFFSET + 40)
    movex(53.5)

    head_down_right()

    movez(ZOFFSET + 52)
    movex(51)

    tstage(305)
 
    verbose_wait(4) # 44.3 below3
 
 #   movex(45.5)

    grbl.write("G0 Y45.6 F200") #45.45
    commit()
 #   head_down() <<< IMPLICIT IN TLC
    verbose_wait(2)
 
 #   tstage(31) # CLOSE LOAD
    time.sleep(4)
     
    grbl.write("G0 Z63.3  F9999") #CHECK DIS NUMBER
    commit()
 
    time.sleep(2) ##
 
    vac_off()
 
    verbose_wait(2)

    movez(ZOFFSET + 40)
    verbose_wait(2)
    
    head_up()
    movex(55)
    verbose_wait(3)
    tstage(32) # upplace close
    verbose_wait(8)
    head_down()
    movex(48)
    movez(ZOFFSET + 52.3)
    tstage(33) # set to safe

    verbose_wait(6)

    movez(ZOFFSET + 40) # HEAD UP
    movex(55)

    verbose_wait(6)
    tstage(36) # folds actual paper
    verbose_wait(23)
    movex(45.45) #offert by .1 FIX DIS NUMBRO CONFIRM MATCH ON F100
    movez(ZOFFSET + 52) # CHECK THIS NUMBER MATCH WITH PREZ NUM
    vac_on()
 
    verbose_wait(2)
    tstage(37)
    verbose_wait(5)

    movex(53.75)

    head_up()
    movez(1)

    #STAGE 4  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    movex(77.75)
    head_overload()
    verbose_wait(4)
    tstage(40)
    verbose_wait(7)
    movez(ZOFFSET + 25)
    movex(76.25)
    movez(ZOFFSET + 30.45)
    verbose_wait(4)

    grbl.write("G0 Y74.4 F180")
    commit()
    time.sleep(2)

    vac_off()

    time.sleep(4)
    
    grbl.write("G0 Z18.3  F9999") #CHECK DIS NUMBER
    commit()
    verbose_wait(4)
    head_up()
    verbose_wait(4)

    movex(65) ## VAC OFF

    tstage(45) # <<<<<<< <<< <<< flips 
 #   movez(22)
    verbose_wait(5)
    head_down()
    verbose_wait(7)


    movex(74.4) ###
    verbose_wait(5)
    movez(ZOFFSET + 18.4)## CHANGE TO Z18.2 !!!!!!!!!!!!!
    vac_on()
    verbose_wait(4)
    movex(77) ###
    movez(2)
    verbose_wait(2)
#    head_up()
#    verbose_wait(4)
    head_up()


    #STAGE 3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #105.35 END  DO NOT OVERWRITE
     
    movex(60) #moves way out to prevent conflict
    tstage(30) # open upplace and load
    movez(ZOFFSET + 40)
    movex(53.5)

    head_down_right()

    movez(ZOFFSET + 52)
    movex(51)

    tstage(305)
 
    verbose_wait(4) # 44.3 below3
 
 #   movex(45.5)

    grbl.write("G0 Y45.45 F200")
    commit()
 #   head_down() <<< IMPLICIT IN TLC
    verbose_wait(2)
 
 #   tstage(31) # CLOSE LOAD
    time.sleep(4)
     
    grbl.write("G0 Z63.3  F9999") #CHECK DIS NUMBER
    commit()
 
    time.sleep(2) ##
 
    vac_off()
 
    verbose_wait(2)

    movez(ZOFFSET + 40)
    verbose_wait(2)
    
    head_up()
    movex(55)
    verbose_wait(3)
    tstage(32) # upplace close
    verbose_wait(8)
    head_down()
    movex(48)
    movez(ZOFFSET + 52.3)
    tstage(33) # set to safe

    verbose_wait(6)

    movez(ZOFFSET + 40) # HEAD UP
    movex(55)

    verbose_wait(6)
    tstage(36) # folds actual paper
    verbose_wait(23)
    movex(45.45) #offert by .1 FIX DIS NUMBRO CONFIRM MATCH ON F100
    movez(ZOFFSET + 52) # CHECK THIS NUMBER MATCH WITH PREZ NUM
    vac_on()
 
    verbose_wait(2)
    tstage(37)
    verbose_wait(5)

    movex(53.75)
 
    #PUTDOWN
    vac_off()
 
    #ENDSTATE
    tstage(99)
    verbose_wait(5)
    movez(40)
    head_up()
 
    ##################################
    #ASSUME
    print " ***** >> END OF SEQUENCE << ***** "
    print colored(workingtime, "yellow")

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
        '''

#vac on/off
con_VAC = True

    
#   this part creates the initial value of the vac
    movex_fast(6)

    # initial z

#vac on/off
con_VAC = True
 value for homing
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
    
        hip_last = hip_initis
        '''
isHomed = False


def looper(h = True):
    global isHomed
    if (isHomed == False):
        home()
        isHomed = True
    init = False
    while True:
        primary()
