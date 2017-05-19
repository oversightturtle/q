import time
import serial

from proptions import *

from gops import commit, dcommit, vac_on, vac_off

### below functions are not updated
def movex (val):
    grbl.write(b"G1 Y%d" %val)
    print (b"G1 Y%d" %val)
    commit()
    xloc = val
    return

def movez (val):
    grbl.write(b"G1 Z%d" %val)
    print (b"G1 Z%d" %val)
    dcommit()  
    loc = val  
    return  

def movexz (vx, vy):
    grbl.write(b"G1 Y%d Z%d" %(vx, vy))
    print (b"G1 Y%d Z%d" %(vx, vy))
    dcommit()
    xloc, yloc = vx, vy
    return


xloc, zloc = 0, 0

def pront_setup():
    print "init ports"
    print "0 to set grbl at 0"
    print "1 to setup up grbl at 1"
    select = input(" >>> ")
    
    if int(select) == 0:
        g1 = serial.Serial('/dev/ttyACM0', 115200)
    elif int(select) == 1:
        g1 = serial.Serial('/dev/ttyACM0', 115200)

def pront_status():
    print "current x, z position >> ", xloc, zloc

def pront_options():
    print ""

def pront_inputs(inputs):
    input_list = raw_input().split(" ")
    try:
        inputs= [str(a) for a in input_list] 
    except ValueError:
        pass
    input = [x for x in a if x != ' ']
 
    return inputs

def pront_main():
    inputs = []
    proptions_setup(inputs)   
    pront_setup()

    while True:
       pront_status()
       inputs = pront_inputs(inputs)
       pront_command(inputs)

def err():
    print "error detected!"
    raw_input("yup >> ")

def move1(inputs):

    if inputs[2] == 'by':
        if inputs[1] == 'x':
            inputs[3] = xloc + inputs[3]
        elif inputs[1] == 'z':
            inputs[3] = zloc + inputs[3]
        else:
            err()

def move2(inputs):
    if inputs[2] == 'by':
        if inputs[1] == 'x':
            inputs[3] = xloc + inputs[3]          
        elif inputs[1] == 'z':
            inputs[3] = zloc + inputs[3]
        else:
            err()
    if inputs[2] == ('by' or 'to') and inputs[6] == ('by' or 'to'):
        
        
    else:
        err()

def vac(inputs):
    if inputs[1] == 'on':

    elif inputs[1] == 'off':

    else: 
        err()

def home(inputs):
    print "444"

def proptions_setup(inputs):

    x1 = proption(inputs, 'move1', move1)
    x2 = proption(inputs, 'move2', move2)
    x3 = proption(inputs, 'vac', vac)
    x4 = proption(inputs, 'home', home)


def pront_command(inputs):
    c = inputs[0]
    for x in proption.pront_instances:
        if c == x.name:
            print "command rc and exec."
            x.func(inputs)


if __name__ == "__main__":
    # execute only if run as a script
    pront_main()
 
