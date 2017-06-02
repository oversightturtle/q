import time

try:
    from setup import grbl
except ImportError:
    pass



def commit():
    "commit w/o changes"
    try:
        grbl.write(b"\r\n\r\n")
    except NameError:
        pass
    return

def dcommit():
    "Delay and commit changes"
    commit()
    time.sleep(8)
    return

def homex ():
    grbl.write(b"G28 Y")
    dcommit()

def homez ():
    grbl.write(b"G28 Z")
    dcommit()

def movex_old ( int ):
    grbl.write(b"G1 Y%f" %int)
    print (b"G1 Y%f" %int)
    dcommit()
    return

gloc_x = 0
gloc_z = 0
gloc_tran = 1
gloc_acc = 0.5
gloc_acc_fast = 0
gloc_rate = 0.34

def movez_instant( new ):
    grbl.write(b"G1 Z%f" %new)
    print (b"G1 Z%f" %new)

    commit()

    return

def movex_instant( new ):
    grbl.write(b"G1 Y%f" %new)
    print (b"G1 Y%f" %new)

    commit()

    return 

def movex_ins_del( new , delay ):
    grbl.write(b"G1 Y%f" %new)
    print (b"G1 Y%f" %new)

    commit()
    time.sleep(delay)

    return 

def movez_ins_del( new , delay ):
    "test docstring"
    grbl.write(b"G1 Z%f" %new)
    print (b"G1 Z%f" %new)

    commit()
    time.sleep(delay)

    return

def movex ( new ):
    commit()
    grbl.write(b"G1 Y%f" %new)
    print (b"g_mx << G1 Y%f" %new)

    wait = gloc_tran + (2 * gloc_acc) + (gloc_rate *  abs(gloc_x - new))

    commit()
    time.sleep( wait )
    return

def movez ( new ):
    grbl.write(b"G1 Z%f" %new)
    print (b"g_mz << G1 Z%f" %new)

    wait = gloc_tran + (2 * gloc_acc) + (gloc_rate * abs(gloc_z - new))

    commit()
    time.sleep( wait )
    return

def movez_fast( new ):
    grbl.write(b"G1 Z%f" %new)
    print (b"G1 Z%f" %new)

    wait = (2 * gloc_acc_fast) + (gloc_rate * abs(gloc_z - new))

    commit()
    time.sleep( wait )
    return

def movex_fast( new ):
    grbl.write(b"G1 Y%f" %new)
    print (b"G1 Y%f" %new)

    wait = (2 * gloc_acc_fast) + (gloc_rate * abs(gloc_x - new))

    commit()
    time.sleep( wait )
    return

def movez_direct( new ):
    grbl.write(b"G1 Z%f" %new)
    print (b"G1 Z%f" %new)

    commit()

    return
    
def movez_old ( int ):
    grbl.write(b"G1 Z%f" %int)
    print (b"G1 Z%f" %int)
    dcommit()    
    return   


 
def movexz (x, y):
    grbl.write(b"G1 Y%f Z%f" %(x, y))
    print (b"g_mxz >> G1 Y%f Z%f" %(x, y))
    time.sleep(2)
    commit()
    return

def mv (axis, location):
    if axis == ('x' or 'y'):
        movex(location)
    elif axis == ('z'):
        movez(location)
    else:
        print " >> CODE ERROR !!! INVALID INPUT "

def mv (axis, location, axis2, location2):
    if (axis == ('x' or 'y')) or (axis2 == z):
        movexz(location, location2)
    elif (axis == ('z')) or (axis2 == ('x' or 'y')):
        movexz(location2, location)
    else:
        print " >> CODE ERROR !!! INVALID INPUT "


def safez():
    grbl.write(b"G1 Z10")
    dcommit()
    return

def vac_on():
    grbl.write(b"M42 P4 S255")
    commit()
    return

def vac_off():
    grbl.write(b"M42 P4 S0")
    commit()
    return
