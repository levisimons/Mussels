import os,sys,re
import csv

fileInput = "SOL_MYTILUS.VF.SNP.vcf"
GenotypeNum = 30

#Open the vcf file containing all the loci where potential SNPs are located.
#Filter out the headers.
#Filter out the adults genome columns as well as the loci metadata columns.
#Filter out loci with less than half of the individuals counted.
#Check for individuals with a unique haplotype at that loci.
#Check for individuals with a unique homozygotic genotype at that loci.
#Count up each instance for each individual.
f = csv.reader(open(fileInput,"rU"), delimiter='\t')
genotype = []
haplotype = []
mutationCount = [0]*GenotypeNum

for line in f:
    if line[0].startswith('#') == False:
	for i in range(0, len(line)):
		outline = []*len(line)
		outline[i] = line[i]
		DP = line[i].split(':')[2]
		if DP != '.':
			if int(DP) < 4:
				outline[i] = './.:.:.:.:.'
	print line
	print outline
                
