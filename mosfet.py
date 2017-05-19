# this module is created for the relay controlling the power supply.
# class version

try:
    from setup import grbl
except ImportError:
    pass

from termcolor import colored

from gops import commit

class mosfet:
    instances = []
    def __init__ (self, name, pin):
        self.name = name
        self.pin = pin
        self.status = False

        mosfet.instances.append(self)

    def mos_on(self):   
        grbl.write("M42 P%d S0" %pin)
        commit()
        status[ x ] = True
            
    def mos_off(self):
        grbl.write("M42 P%d S255" %pin)
        commit()
        status[ x ] = False

mosfet("test0", 11)
mosfet("test1", 6)
mosfet("test2", 5)
mosfet("test3", 4)

def mos_init():
    for x in mosfet.instances:
        x.mos_off()

def mos_p_long():
    s_init = False
    for x in mosfet.instances:
        if s_init == False:
            s_init = True
            print "power state: "
        print x.name, 
        if x.status == True:
            print colored("[ON]", "green", attrs=['bold'])
        else:
            print colored("[OFF]", "red", attrs=['bold'])

def mos_p_aline():
    s_init = False
    for x in mosfet.instances:
        if s_init == False:
            s_init = True
            print "POWER: ",
        print ">",
        print x.name, 
        if x.status == True:
            print colored("[ON]", "green", attrs=['bold']),
        else:
            print colored("[OFF]", "red", attrs=['bold']),
    print "\n"

def mos_p_short():
    s_init = False
    s_exist = False
    for x in mosfet.instances:
        if x.status == True:
            if s_init == False:
                s_init = True
            print colored("120vAC POWER", "green", attrs=['bold'])
            print x.name
    if s_init == False:
        print colored("\n[MASTER - NO POWER]", "red", attrs=['bold'])
