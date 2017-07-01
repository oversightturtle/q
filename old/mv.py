
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

