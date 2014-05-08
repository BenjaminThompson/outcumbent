#!/usr/bin/python
from outcumbent.models import *
import xml.etree.ElementTree as ET
import httplib

def getData(year,roll):
    h = httplib.HTTPConnection('clerk.house.gov')
    h.request('GET', '/evs/{0}/roll{0}.xml'.format(str(year),str(roll).zfill(3)))
    return h.getresponse().read()

def increment(year,roll,success):
    if success == True:
        roll += 1           # If success, just keep counting up to the next vote.
    else:                   # Otherwise, we need to find out what to do next.
        if roll == 1:
            return          # If failed on vote #1, assume the whole year is bad. Finish.
        else:
            year +=1        # If the vote wasn't #1, try going to the next year.
            roll = 1        # Start counting from the first vote of that session.
    return year, roll

#Main Program
def getAll(year,roll):
    while True:
        success = False
        try:
            data = getData(year,roll)
            success = True
            rollcall = ET.fromstring(data)
            leg = Legislation(rollCallNum=int(rollcall[0][4].text),
                              congress= int(rollcall[0][1].text),
                              session = int(rollcall[0][2].text[:1]),
                              chamber = Chamber.objects.filter(name='United States House of Representatives'),
                              identifier = ...,
                              title = ...,
                              description = ...,
                              hyperlink = ...)
        except:
            success = False

        year,roll = increment(year,roll,success)