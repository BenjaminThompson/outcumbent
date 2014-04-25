#!/usr/bin/python

import os
import sys
import httplib
import xmltodict
from pymongo import MongoClient

logfile=open(os.getcwd()+"/SenateVotes.log", 'a')

def GetData(vote):
    dir = "/vote{0}{1}".format(str(vote['congress']),str(vote['session']))
    xml = "/vote_{0}_{1}_{2}.xml".format(str(vote['congress']),str(vote['session']),str(vote['number']).zfill(5))
    h = httplib.HTTPConnection('www.senate.gov')
    h.request('GET', '/legislative/LIS/roll_call_votes'+dir+xml)
    r = h.getresponse()
    data=r.read()
    data.index('<roll_call_vote>')
    return data

def LogResult(vote,success):
    row=str(vote['congress'])+"\t"+str(vote['session'])+"\t"+str(vote['number'])+"\t"
    if success:
        print(row+"Imported")
        logfile.write(row+"Imported")
    else:
        print(row+"Aborted")
        logfile.write(row+"Aborted")

def Increment(vote,success):
    if success == True:
        vote['number'] += 1         # If success, just keep counting up to the next vote.
    else:                           # Otherwise, we need to find out what to do next.
        if vote['number']==1:
            return                      # If failed on vote #1, assume the whole session/congress is bad. Finish.
        else:
            vote['session'] +=1        # If the vote wasn't #1, try going to the next session.
            vote['number'] = 1         # Start counting from the first vote of that session.

        if vote['session'] > 2:     # If you just incremented to session 3, you went too far.
            vote['congress'] += 1       # Increment to the next Congress.
            vote['session'] = 1         # And set Session to the first one.
            vote['number'] = 1          # And the vote Number too.
    return vote

####Main body of program#####
def main(argv):
    try:
        vote=dict(congress=int(argv[0]),session=int(argv[1]),number=int(argv[2]))
    except:
        print("You didn't provide the correct arguments. Aborting.")
        return
    client=MongoClient()
    db=client.Outcumbent
    SenateVotes=db['SenateVotes']

    while True:

        try:
            data = GetData(vote)
            record = xmltodict.parse(data)
            SenateVotes.insert(record)
            success = True
        except:
            success = False

        LogResult(vote,success)
        vote = Increment(vote,success)



if __name__ == "__main__":
    main(sys.argv[1:])
