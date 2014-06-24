import os
import plistlib
import csv
 
infile = '/users/mike/documents/ap.csv'
outfile = '/users/mike/documents/ap.plist'
i = 0
 
alist = []
blist = []
 
csvr = csv.reader(open(infile, 'rb'), delimiter=',')
 
for row in csvr:
 
    if(i>0):
        for col in row:
            alist.append(col)
 
        pl = dict(
                apid = alist[0],
                aptype = alist[1],
                apname = alist[2],
                aplat = alist[3],
                aplon = alist[4],
                apelev = alist[5],
                apreg = alist[6],
                apmuni = alist[7]
                )
        
        blist.append(pl)
        alist = []
 
    i+=1
 
plistlib.writePlist(blist, outfile)