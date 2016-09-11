import os,re,sys
import csv
import subprocess

#Get all of the position files in all of the first-level subdirectories.
filenames = []
for subdir, dirs, files in os.walk('.'):
    for file in files:
        if file[-3:] == 'pos':
            filenames.append(os.path.join(subdir, file))

#Initialize the first comparison file from the first position file.
comparison = "CallableSites.tsv"
f0 = open(comparison, "w")
output = csv.writer(f0, delimiter='\t')
header = ['#CHROM and POS','COUNT']
output.writerow(header)
sites = []
fileInput = filenames[0]
f1 = csv.reader(open(fileInput,"rU"), delimiter ='\t')
for line in f1:
    if line[0].startswith('#') == False:
        row = line[0],line[1]
        loci = ''.join(row)
        sites.append(loci)
unique = list(set(sites))
for i in range(0,len(unique)):
    row = unique[i],sites.count(unique[i])
    output.writerow(row)
f0.close()
sites = []

#Function reads in a comparison file as a reference.  Then it reads
#in the next position file.  If the next position file has an entry
#not seen in the reference then the reference is expanded with the
#new entry with a count of 1.  If the entry is seen in the reference
#then the count for the reference containing that entry is iterated up
#by 1.  This new list, with a count of all positions and their count
#values, is then outputted as the new comparison file.
def fileRead(index):
    referenceName = []
    referenceNum = []
    #Read in comparison file.
    fileInput = open(comparison,"rU")
    f1 = csv.reader(fileInput, delimiter='\t')
    for line in f1:
        if line[0].startswith('#') == False:
            referenceName.append(line[0])
            referenceNum.append(line[1])
    fileInput.close()
    
    #Read in position file.
    fileInput = open(filenames[index],"rU")
    f1 = csv.reader(fileInput, delimiter='\t')
    for line in f1:
        if line[0].startswith('#') == False:
            row = ''.join(line)
            if referenceName.count(row) == 0:
                referenceName.append(row)
                referenceNum.append(1)
            if referenceName.count(row) > 0:
                j = referenceName.index(row)
                referenceNum[j] = int(referenceNum[j])+int(referenceName.count(row))
    fileInput.close()

    #Output the new comparison file.
    #The format is #CHROM and POS, Count.
    f0 = open(comparison, "w")
    output = csv.writer(f0, delimiter='\t')
    for j in range(0,len(referenceName)):
        row = referenceName[j],referenceNum[j]
        output.writerow(row)
    f0.close()


#Call the fileRead function and loop through all position files.
for i in range(1,len(filenames)):
    index = i
    fileRead(index)
    print index,filenames[index]
