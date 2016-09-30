import os,sys,re
import csv

fileInput = "SOL_MYTILUS.VF.SNP.vcf"
fileOutput = "SOL_MYTILUS.VF.SNP.Filtergt4.vcf"

#Open the vcf file containing all the loci where potential SNPs are located.
#Filter out the headers.
#Filter out the adults genome columns as well as the loci metadata columns.
#Filter out loci with less than half of the individuals counted.
#Check for individuals with a unique haplotype at that loci.
#Check for individuals with a unique homozygotic genotype at that loci.
#Count up each instance for each individual.
f = csv.reader(open(fileInput,"rU"), delimiter='\t')

for line in f:
    if line[0].startswith('#') == False:
	outline = []
	for i in range(0, len(line)):
		outline.append(line[i])
	for i in range(0,len(outline)):
		if i not in (0,1,2,3,4,5,6,7,8,9,20,21,32,33,44):
			DP = line[i].split(':')[2]
			if DP != '.':
				if int(DP) < 4:
					blank = './.:.:.:.:.'
					outline[i] = blank
	print line
	print outline
                
