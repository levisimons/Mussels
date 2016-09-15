import os,re,sys
import csv
import subprocess

#Get all of the position files in all of the first-level subdirectories.
filenames = []
for subdir, dirs, files in os.walk('.'):
    for file in files:
        if file[-3:] == 'pos':
            filenames.append(os.path.join(subdir, file))
print filenames

#Initialize the first comparison file from the first position file.
referenceName = {}
name = []
num = []

#Function reads in a comparison file as a reference.  Then it reads
#in the next position file.  If the next position file has an entry
#not seen in the reference then the reference is expanded with the
#new entry with a count of 1.  If the entry is seen in the reference
#then the count for the reference containing that entry is iterated up
#by 1.  This new list, with a count of all positions and their count
#values, is then outputted as the new comparison file.
def fileRead(index):
    #Read in position file.
    fileInput = open(filenames[index],"rU")
    f1 = csv.reader(fileInput, delimiter='\t')
    print index,filenames[index]
    for line in f1:
        if line[0].startswith('#') == False:
            row = ','.join(line)
            if index == 0:
                referenceName[row] = referenceName.get(row,1)
            if index > 0:
                if row in referenceName:
                    referenceName[row] = referenceName.get(row,0)+1
                else:
                    referenceName[row] = referenceName.get(row,1)
    fileInput.close()

#Call the fileRead function and loop through all position files.
for i in range(0,len(filenames)):
    index = i
    fileRead(index)

#Output the new comparison file.
#The format is #CHROM and POS, Count.
comparison = 'CallableSites.tsv'
f0 = open(comparison, "w")
output = csv.writer(f0, delimiter='\t')
header = ['#CHROM','POS','Count']
output.writerow(header)
for row in referenceName:
    entry = row.split(',')[0],row.split(',')[1],referenceName[row]
    output.writerow(entry)
f0.close()
