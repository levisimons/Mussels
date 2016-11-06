import sys
import os
import csv
import re
from collections import Counter
import numpy as np
import pandas as pd
import gzip

#Read in Blastout files and output likeliest gene sequence match and its
# frequency
namelist = []
filename = []
match=[]
genuslist=[]
genusMatch = []

# Search for likely Genbank hits within each file and tally their totals
def GenbankCount(file):
    f = gzip.open(file,"rU")
    line = f.read()
    ID = re.findall(r'>(.*?)Length=',line,re.DOTALL)
    ID = [i.replace('\n',' ') for i in ID]
    ID = [i.replace('"', '') for i in ID]
    hits = Counter(ID).most_common()
    print "There are ", len(hits), " unique sequence matches in sample ", file
    match.append(hits)
    for i in range(0,len(ID)):
        namelist.append(ID[i])
        genuslist.append(ID[i].split('|')[2].split(' ')[1])
    genusHits = Counter(genuslist).most_common()
    print "There are ", len(genusHits), " unique genus matches in sample ", file
    genusMatch.append(genusHits)
                   
# Store the list of filenames
for file in os.listdir(os.getcwd()):
    if file.endswith(".gz"):
        filename.append(file)
filename.sort()

# Iterate GenbankCount over each input file
for i in range(0,len(filename)):
    file = filename[i]
    GenbankCount(file)
    
# match[file index][hit name][hit count]
# Store Genbank matches as rows and the frequency for matches within each file
# as a column.
unique = list(set(namelist))
final = np.zeros((len(unique),len(match)))
for i in range(0,len(match)):
    for j in range(0,len(unique)):
        for k in range(0,len(match[i])):
            if unique[j] == match[i][k][0]:
                final[j][i] = match[i][k][1]

# Store data array into dataframe for later manipulation
data = pd.DataFrame(final,index=unique,columns=filename)

# Get unique prefixes for filename
fileprefix = set(filename)

# Combine columns which have file names with the same prefix
sumData = data.T.groupby([s.split('.')[0] for s in data.T.index.values]).sum().T
sumData.index.name = 'Genbank Hits'
sumData.to_csv('GenbankHits.txt', sep='\t')

###################################################################################

# match[file index][hit name][hit count]
# Store Genbank matches as rows and the frequency for matches within each file
# as a column.
unique = list(set(genuslist))
final = np.zeros((len(unique),len(genusMatch)))
for i in range(0,len(genusMatch)):
    for j in range(0,len(unique)):
        for k in range(0,len(genusMatch[i])):
            if unique[j] == genusMatch[i][k][0]:
                final[j][i] = genusMatch[i][k][1]

# Store data array into dataframe for later manipulation
data = pd.DataFrame(final,index=unique,columns=filename)

# Get unique prefixes for filename
fileprefix = set(filename)

# Combine columns which have file names with the same prefix
sumData = data.T.groupby([s.split('.')[0] for s in data.T.index.values]).sum().T
sumData.index.name = 'Genbank Hits'
sumData.to_csv('GenbankGenusHits.txt', sep='\t')
