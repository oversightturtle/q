import time

try:
    from setup import grbl
except ImportError:
    pass

import config

if config.con_VIRTUAL == True:
    from virtual import grbl

def commit():
    "Sends \r\n\r\n to grbl as required for proper functioning"
    try:
        grbl.write(b"\r\n\r\n")
    except NameError:
        pass

def homex ():
    grbl.write(b"G28 Y")
    commit()

def homez ():
    grbl.write(b"G28 Z")
    commit()

gloc_x = 0
gloc_z = 0
gloc_tran = 0.2 # delay time
gloc_acc = 0.5
gloc_acc_fast = 0
gloc_rate_x = 0.143
gloc_rate_z = 0.34

def g_wpcs(axis, location, delay = False):
    '''
    general function to move(g), write,  print, commit, and set
    '''
    if axis == "xz":
        grbl.write("G1 Y%d Z%d" %(location[0], location[1]))

    if axis == "z":
        grbl.write(b"G1 %s%s" %(axis.upper(), location))

    if axis == "x":
        grbl.write(b"G1 Y%s" %(location))

    commit()

    if axis == "xz":
        print ("wpcs >> G1 Y%d Z%d" %(location[0], location[1]))
    elif axis == "z":
        print ("wpcs >> G1 %s%s" %(axis.upper(), location))
    elif axis == "x":
        print ("wpcs >> G1 Y%s" %(location))
    else:
        raise InvalidValueError('an invalid value was set in IVE')

    if delay == True:
        if axis == "x":
            wait = gloc_tran + (2 * gloc_acc) + (gloc_rate_x *  abs(gloc_x - location))
            time.sleep( wait )
        if axis == "z":
            wait = gloc_tran + (2 * gloc_acc) + (gloc_rate_z * abs(gloc_z - location))
            time.sleep( wait )
        print " >> ", wait
            
    global gloc_x, gloc_z
    if axis == "x": ## RESET THE VALS
        gloc_x = location
    elif axis == "z":
        gloc_z = location
    elif axis == "xz":
        gloc_x = location[0]
        gloc_z = location[1]
    else:
        raise InvalidValueError('an invalid value was set in IVE')

def movex_instant( new ):
    g_wpcs("x", new)

def movez_instant( new ):
    g_wpcs("z", new)

def movex_ins_del( new , delay ):
    g_wpcs("x", new)
    time.sleep(delay)

def movez_ins_del( new , delay ):
    g_wpcs("z", new)
    time.sleep(delay)

def movex ( new ):
    g_wpcs("x", new, delay = True)

def movez ( new ):
    g_wpcs("z", new, delay = True)

def movez_fast( new ):
    movez(new)

def movex_fast( new ):
    movex(new)
 
def movexz_instant(x, z): ## DELAYTIME
    g_wpcs("xz", (x, z))

def vac_on():
    if config.con_VAC == True:
        grbl.write(b"M42 P4 S255")
        commit()

def vac_off():
    if config.con_VAC == True:
        grbl.write(b"M42 P4 S0")
        commit()
