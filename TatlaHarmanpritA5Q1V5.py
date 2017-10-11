# -*- coding: utf-8 -*-
"""TatlaHarmanpritA5Q1
￼￼

COMP 1012 SECTION A01
INSTRUCTOR Terrance H. Andres
ASSIGNMENT: A5 Question 1
AUTHOR Harmanprit Tatla
VERSION 2015 - March - 27

PURPOSE: To compute several properties of specified curves, and their solids made by
rotating about an axis. 
"""
import time
import numpy as np

#Tuple of the solids that the user will pick from, and will be analyzed for 
#the required properties.
SOLIDS = ('0earth: evaluate properties of the planet earth:',
          '1bowlingPin: evaluate attributes of a bowling pin',
          '2saucePan: evaluate size of the inside of a sauce pan')

def main():
    """When called, executes the solid analyzing program."""
    
    print 'PROPERTIES OF SOLIDS OF REVOLUTION' #Prints program title
    
    HEADING = 'Select a solid of revolution to analyze:\n' #heading for menu
    STOP_CODE = 'Q' #stop code to quit program.
    
    #Min and Max num of points to use to approximate curve and solid properties
    MIN_P, MAX_P = 5, 6000 
    
    userChoice = getChoice(HEADING, SOLIDS, STOP_CODE) #gets user input.
    
    #Loops until user enters stop code to quit program.
    while userChoice != STOP_CODE:
        
        #Prints table of values of the properties of user selected solid;
        #1:SOLIDS[userChoice].index(':'), is slice of solid name.
        #Return value ignored.
        analyzeSolid(SOLIDS[userChoice][1:SOLIDS[userChoice].index(':')], 
                     MIN_P, MAX_P) 
        
        userChoice = getChoice(HEADING, SOLIDS, STOP_CODE) #asks user for input
   
    theEnd() #prints termination output.
    
    return
     
def analyzeSolid(fncName, minPoints, maxPoints):
    """Given fncName, the name of a solid of revolution as a string, minPoints 
    and maxPoints as positive integers. This function prints a table of 
    approximations of the properties of the solid of revolution and its curve, 
    and returns the last best estimate of those properties as a 4 element tuple
    """
    silhouetteFnc = eval(fncName) #converts fncName to a pre-defined function
    #units of measure for solid; 0 arbitrary arg, units in pos 2 in return
    units = silhouetteFnc(0)[2] 
    
    #Message indicating program is analyzing the selected solid.
    print "\nAnalyzing a solid obtained from the silhouette function '%s'\n" %(
           fncName) 
    
    #Lines needed to construct table headings where results will be printed.
    LINE1 = '%6s|%8sSILHOUETTE%6s|%10sSOLID\n' % ('', '', '', '')
    LINE2 = ' # OF |%2sPERIMETER%5sAREA%4s|%3sSURFACE%6sVOLUME\n' % ('', '', 
            '','', '')
    LINE3 = 'POINTS|%5s[%s]%6s[%s^2]%3s|%4s[%s^2]%6s[%s^3]\n' % ('', units, '', 
            units, '', '', units, '', units) 
    LINE4 = ('-' * 6) + '+' + ('-' * 24) + '+' + ('-' * 24) 
    print  LINE1 + LINE2  + LINE3 + LINE4 #Prints table headings
    
    #Loops until minPoints >= maxPoints
    while minPoints < maxPoints:
        
        #Send x and y vals for solid, and get computed properties for it.
        properties = solidSizes(silhouetteFnc(minPoints)[0], 
                                silhouetteFnc(minPoints)[1])
        
        #prints recently calculated properties for solid
        print '%5d |%10.5g%12.5g%2s|%11.5g%12.5g' % (minPoints, properties[0], 
              properties[1], '', properties[2], properties[3])
       
        minPoints *= 2 #double minPoints,more points used to compute properties
        
    return properties #last best estimate of properties for selected solid.

def bowlingPin(numPoints):
    """This function represents the curve for a 15-inch bowling pin. Given an 
    integer > 1 for numPoints, the number of equally spaced points to be placed 
    along the bowling pin curve, which extends from x = 0 to x = 15 on the 
    x-axis. Returns a 3 element tuple with an array for x-values, y-values, 
    and a character string for the unit of measure that is in inches.  """
  
    #Coefficients of polynomial needed to compute the y-values for curve.
    COEFS = np.array([1.27731344, 0.85418707, 0.032282353, 0.127018447,
                     -5.1957538e-2, 6.718114e-3, -3.61828e-4, 7.025e-6])
    
    #numPoints x-values of curve equally spaced from x = 0 to x = 15 
    xVals = np.linspace(0, 15, numPoints)
    
    #evalPoly and np.sqrt to get y-values for given x-values of curve 
    yVals = np.sqrt(evalPoly(COEFS, xVals))
    
    return  (xVals, yVals, 'in') #x & y values, and unit of measure.

def earth(numPoints):
    """This function represents earth as a solid sphere with radius 6371 km. 
    Given an integer > 1 for numPoints, the number of equally spaced points to 
    be placed along the semi-circle curve for earth, which extends from 
    x = -6371 to x = 6371 on the x-axis. Returns a 3 element tuple with an 
    array for x-values, y-values, and a character string for the unit of 
    measure that is in kilometres."""
    
    EARTH_RADIUS = 6371 #Radius of sphere representing earth [km]
    
    #numPoints x-values, equally spaced from x = -6371 to x = 6371 for curve.
    xEarth = np.linspace(-6371, 6371, numPoints)
    
    #Computes the y-values for the corresponding x-values for curve.
    yEarth = np.sqrt((EARTH_RADIUS**2) - (xEarth**2))
      
    return (xEarth, yEarth, 'km') #x & y values, and unit of measure.

def evalPoly(coefs, xs):
    """This function uses Horner’s method to evaluate polynomials of degree 
    n >= 0, with COEFS, the list or array of the coefficients of the polynomial 
    arranged a0, a1, …, an, for either an array or list of values xs. 
    Returns, an array of the results. """
    
    result = 0.0 #holds result of evaluating polynomial with COEFS at xs 
    
    #Evaluates polynomial at xs using the given coefs, and Horner's method.
    for coef in reversed(coefs):
        result  = result * xs + coef

    return np.array(result) 
    
def getChoice(heading, choices, stopCode):
    """Given character strings for heading and stopCode, and a tuple/list of 
    character strings for choices. This function prints a menu of choices, asks 
    user for input, and then returns the user's choice."""
    
    MAX_CHOICE = len(choices) - 1 #max digit a choice can have.
    CHOICE_PROMPT = 'Enter a choice number, or enter %s to quit\n' % stopCode
    warning = '\b' #displays a message when user enters invalid input.
    
    #Loops until len(warning) == 0, occurs once user enters valid input.
    while len(warning) > 0:
        print warning  #prints warning if user enters invalid input
        print heading, #prints heading of menu
        for loc, choice in enumerate(choices): #prints menu of choices
            print (' %d) ' % loc) + choice[1:] 
        
        userInput = raw_input(CHOICE_PROMPT).strip() #Prints prompt, gets input
        warning = ''
        
        #if user entry is stop code assign it to userInput then return.
        if userInput.upper() == stopCode.upper():
            userInput = stopCode
        
        #Invalid choice if len(userInput) > 1, or not between '0' and 
        #str(MAX_CHOICE)
        elif len(userInput) > 1 or not ('0' <= userInput <= str(MAX_CHOICE)):
            #warning message if input too long
            warning += ("Invalid length of input '%s'.\n" % userInput) * (
                        len(userInput) > 1) 
            
            #warning message if not a valid choice
            warning += 'You entered %s; enter a number from 0 to %d.\n' % (
                        userInput, MAX_CHOICE) 
        
        #user input is a valid choice; convert to integer then return
        else:
            userInput = int(userInput)
    
    return userInput

def saucePan(numPoints):
    """This function represents the curve of a 2-litre sauce pan, oriented 
    vertically with its handle omitted, and axis of symmetry directed to the 
    right. The base radius of the sauce pan is 1.5 cm, radius of its inner 
    cavity is 8.7 cm, and lip radius is  0.8 cm. Additionally, its height from 
    its base to lip is 8.5 cm. Given numPoints, the number of equally spaced 
    points to be placed along the sauce pan curve, which extends from x = 0 to 
    x = 8.5 on the x-axis. Returns a 3 element tuple with an array of x-values, 
    y-values, and a character string for the unit of measure that is in 
    centimetres."""
    
    #Measurements of 2-litre pan
    rPan = 8.7 #radius of cavity of pan [cm]
    rBase = 1.5 #radius of the base of the pan [cm]
    rLip = 0.8 #radius of the lip of the pan [cm]
    h_ = 8.5  #height of pan from its base to lip [cm]
    
    #numPoints x-values equally spaced from 0 to h_, and numPoints 0's for
    #y-values.
    xs, ys = np.linspace(0, h_, numPoints), np.zeros(numPoints)
    
    #Refer to x values in xs that make up btm, side, and top of sauce pan curve
    btmCurve = (xs <= rBase)
    sideCurve = (rBase < xs)
    topCurve = ((h_ - rLip) < xs)

    #computes y-values corresponding to given x-values, using mathematical 
    #formulas for btm, side, and top of sauce pan curve.
    ys[btmCurve] = rPan - rBase + np.sqrt(xs[btmCurve] * (2*rBase - 
                                                          xs[btmCurve]))
    ys[sideCurve] = rPan 
    ys[topCurve] = rPan + rLip - np.sqrt(rLip**2 - (h_ - rLip - 
                                                    xs[topCurve])**2)
    
    return (xs, ys, 'cm') #x & y values, and unit of measure.
   
def solidSizes(xs, ys):
    """Given a sequence of x and y values of a curve as arrays/lists, let x’ 
    and x’’ equal the first and last values in the list/array for x. This 
    function adds two line segments to the curve by adding the point (x’, 0) to 
    the front and (x’’, 0) to the end of the curve, so it begins and ends at 
    the x-axis. Thereafter, it computes the perimeter of the curve, area under 
    the curve and above x-axis; area and volume of the solid of revolution, 
    obtained from rotating the curve about x-axis. Returns a 4 entry tuple 
    containing the results of the four properties mentioned above."""
    
    #Adds x’ to front, the first x value in sequence, and x’’ to end, the last 
    #x value in x-value sequence.
    xs = np.array([list(xs)[0]] + list(xs) + [list(xs)[-1]])
    
    #Adds [0] to the front and end in y-value sequence.
    ys = np.array([0] + list(ys) + [0])
    
    #Arrays needed to calculate properties for curve 
    xj, xj0 = xs[1:], xs[:-1]
    yj, yj0 = ys[1:], ys[:-1]
    
    #Computes properties of curve and its solid of revolution, using 
    #mathematical formulas. 
    perimeter = np.sum(np.sqrt((xj - xj0)**2 + (yj - yj0)**2))
    
    areaUnderCurve = (0.5) * np.sum((xj - xj0) * (yj + yj0))
    
    areaOfSolid = np.pi * np.sum((yj + yj0) * np.sqrt((xj - xj0)**2 + 
                                                      (yj - yj0)**2))
    
    volumeOfSolid = (np.pi/4.) * np.sum((xj - xj0) * (yj + yj0)**2)
         
    return (perimeter, areaUnderCurve, areaOfSolid, volumeOfSolid)      
    
def theEnd():
    """Prints termination message to indicate succesful completion of 
       program."""
    
    print '\nProgrammed by Harmanprit Tatla'
    print 'Date:', time.ctime()
    print 'End of processing...' 
    
    return   

main() #Call needed to start program

