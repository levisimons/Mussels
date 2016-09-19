import os, re, sys
import csv

#Get all of the position files in all of the first-level subdirectories.
filenames = []
for subdir, dirs, files in os.walk('.'):
    for file in files:
        if file[-3:] == 'pos':
            filenames.append(os.path.join(subdir, file))

#Store the list of high quality sites for the juvenile mussel population
# into a nested dictionary.  Sites called in more than a certain number of
# juveniles are ultimately stored in memory.
referenceName = {}
referenceInput = open('covered.sites','rU')
f1 = csv.reader(referenceInput,delimiter='\t')
for line in f1:
    if int(line[2]) >= 15:
        chrom = line[0]
        pos = int(line[1])
        if chrom not in referenceName:
            referenceName[chrom] = referenceName.get(chrom,{})
        else:
            if pos not in referenceName[chrom]:
                referenceName[chrom][pos] = referenceName[chrom].get(pos)
referenceInput.close()

#This function compares each juvenile positions file against the dictionary.
#If a position is called in a juvenile and is also in the dictionary then the
# count for callable sites for that individual is incremented up by 1.
def fileRead(index,referenceName):
    fileInput = open(filenames[index],"rU")
    f1 = csv.reader(fileInput, delimiter='\t')
    j=0
    for line in f1:
        if line[0].startswith('#') == False:
            chrom = line[0]
            pos = int(line[1])
            if chrom in referenceName:
                if pos in referenceName[chrom]:
                    j=j+1
    fileInput.close()
    print index,filenames[index],j

#Call the fileRead function and loop through all position files.
for i in range(0,len(filenames)):
    index = i
    fileRead(index,referenceName)

