try:
    from setup import grbl
except ImportError:
    pass

try:
    from setup import tlc
except ImportError:
    pass

import time

from pri import partz

from gops import movez_ins_del, homez, movez, commit, dcommit, vac_on, vac_off, movez_instant

from tops import operateservo, operatestage

from auto import looper, autotest

from mosfet import *

from setup import config

vacstate = False
safeloc = False



def checkloc():
    if safeloc == False:
        print "CAUTION ! YOU HAVE NOT INITALIZED THE INITAL POSITION TO SAFE"



class option:
    instances = []
    def __init__ (self, name, function, loop):
        self.name = name
        self.func = function
        self.loop = loop
        
        option.instances.append(self)

class poption:
    instances = []
    def __init__ (self, upper, name):
        self.name = name
        self.upper = upper
        poption.instances.append(self)

def mos_con():
    # switchboard to all omsfet relatetd functions
    mos_p_long()
    print "mosfet centeral connection >>> commands" ###


def noisetest():
    homez()
    ign = raw_input("press any key after homing is complete")
    while True:
        movez_instant(20)
        time.sleep(7)
        movez_instant(40)
        time.sleep(7)

def vac():
    global vacstate
    if vacstate == False:
        vac_on()
        vacstate = True
    else:
        vac_off()
        vacstate = False

def sen():
    autotest()

zloc = 0
def gtime():
    n = raw_input("enter the num of steps >> ")
    d = raw_input('enter the delay between moves >> ')
    global zloc
    for x in range(0, 4):
        zloc += int(n)
        movez_ins_del(float(zloc), float(d))

def testest():
    pass

def jauto():
    looper(h = True)

def jautom():
    looper(h = False)

def grbl_send():
    st = raw_input('Input your string to send GRBL >> ')
    if st == 'vac':
        vac()
    else:
        grbl.write(st)
    
ss_init = False
def script():
    if ss_init == False:
        ss_init == True
    #    mos_p_aline()
    sc = raw_input('g >> ')
    xs = sc.split()
    if sc == 'vac':
        vac()
    elif xs[0] == 'stage':
        operatestage(int(xs[1]))
    elif xs[0] == 'read':
		pass
    elif xs[0] == 'auto':
        looper(True)
    else:
        print "found"
        grbl.write(sc)
        dcommit()
'''
    elif xs[0] == 'power':
        p_exist = False
        if xs[1] == 'on':
            for x in mosfet.instances:
                if xs[2] == x.name:
                    p_exist == True
                    x.mos_on()

        elif xs[1] == 'off':
            for x in mosfet.instances:
                if xs[2] == x.name:
                    p_exist == True
                    x.mos_off()
    
        else:
            print "unknown syntax (second word on/off)"
            
        if p_exist == False:
            print "could not recognize the name"
'''       



def tlc_send():
    st = raw_input('Input your string to send TLC >> ')
    tlc.write(st)
    commit()

def tlc_stage():   
    checkloc()
    sval = input('ENTER STAGE VALUE >> ')
    operatestage(sval)


def tlc_servo1():
    p1, po1 = raw_input("ENTER PIN1, POS1  >> ").split()
    p1, po1 = [int(p1), int(po1)]
    tlc.write(b"1 %d %d" %(p1, po1) )

def tlc_servo2():
    p1, po1, p2, po2 = raw_input("Enter PIN1, POS1, PIN2, POS2  >> " ).split()
    p1, po1, p2, po2 = [int(p1), int(po1), int(p2), int(po2)]
    tlc.write(b"2 %d %d %d %d" %(p1, po1, p2, po2) )

def tlc_loop1():
    try:
        d, p1, po1, po2 = raw_input("Enter del, PIN1, POS1, PO2  > "  ).split()
        d, p1, po1, po2 = [int(d), int(p1), int(po1), int(po2)]
    except ValueError:
        print " >> You have entered an incorrect value > "
    try: 
        while True:
            tlc.write(b"1 %d %d" %(p1 , po1))
            print(po1)
            time.sleep(d)
            tlc.write(b"1 %d %d" %(p1, po2))
            print(po2)
            time.sleep(d)
    except NameError:
        pass
    except KeyboardInterrupt:
        print " >> halting subprocess"

def tlc_initsafe():
    global safeloc
    safeloc = True
    tlc.write(b"98")

def tlc_setsafe():
    checkloc()
    tlc.write(b"99")

def jpartial():
    partz()    

def tlc_stage5():
    po1, po2 = raw_input("p1(r), p2(l) >> ").split()
#                    p1, po1, p2, po2 = raw_input("Enter PIN1, POS1, PIN2, POS2  >> " ).split()
#                    p1, po1, p2, po2 = [int(p1), int(po1), int(p2), int(po2)]
    po1, po2 = [int(po1), int(po2)]

    tlc.write(b"2 18 210 19 400")
    time.sleep(2)

    tlc.write(b"2 18 %d 19 %d" %(po1, po2) )  

def tlc_stage2():
    print "(130 500) > (478 130)"
    po1, po2 = raw_input("p1(l), p2(r) >> ").split()
    po1, po2 = [int(po1), int(po2)]

    tlc.write(b"2 16 450 17 180 ")
    time.sleep(4)
    tlc.write(b"2 16 %d 17 %d" %(po1, po2) )

def tlc_jointset(delay, servo1pin, servo1safe, servo2pin, servo2safe):
    print "delay:" , delay, "s1", servo1safe, "s2", servo2safe
    servo1target, servo2target = raw_input("v1, v2 >> ").split()
    servo1target, servo2target = [int(servo1target), int(servo2target)]

    tlc.write("2 %d %d %d %d" %(servo1pin, servo1safe, servo2pin, servo2safe) )
    time.sleep(delay)
    tlc.write("2 %d %d %d %d" %(servo1pin, servo1target, servo2pin, servo2target) )

#try:
#    tlc_jointset(3,3,3,3,3)

def opt_print():
    for x in option.instances:
        print x.name,
        
        #list out all aliases below
        exist = False
        for y in poption.instances:
            if y.upper == x.name:
                exist = True
        #lists out all aliases
        if exist == True:
            print "(",
        
        for y in poption.instances:
            if y.upper == x.name:
                print y.name,

        if exist == True:
            print ")",    
