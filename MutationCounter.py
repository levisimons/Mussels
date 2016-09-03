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
        j=0
	for i in range(0, len(line)):
            if i not in (0,1,2,3,4,5,6,7,8,9,20,21,32,33,44):
                if line[i].split(':')[0] != "./.":
                    j=j+1
                genotype.append(line[i].split(':')[0])
                haplotype.append(line[i].split(':')[0].split('/')[0])
                haplotype.append(line[i].split(':')[0].split('/')[1])
        if j >= 15:
            for k in range(0,3):
                if haplotype.count(str(k)) == 1:
                    Index = int(haplotype.index(str(k))/2)
                    mutationCount[Index] = mutationCount[Index]+1
                if haplotype.count(str(k)) == 2:
                    seq = str(k),'/',str(k)
                    homozygote = str(''.join(seq))
                    if homozygote in genotype:
                        Index = int(genotype.index(str(homozygote)))
                        mutationCount[Index] = mutationCount[Index]+1
        genotype=[]
        haplotype=[]
print mutationCount
