import os,sys,re
import csv

fileInput = "SOL_MYTILUS.VF.SNP.vcf"
IndividualNum = 30

#Open the vcf file containing all the loci where potential SNPs are located.
#Filter out the headers.
#Filter out the adults genome columns as well as the loci metadata columns.
#Filter out loci with less than half of the individuals counted.
#Check for individuals with a unique genotype at that loci.
#Count up each instance for each individual.
f = csv.reader(open(fileInput,"rU"), delimiter='\t')
genotype = []
mutationCount = [0]*IndividualNum
for line in f:
    if line[0].startswith('##') == False:
        for i in range(0, len(line)):
            if i not in (0,1,2,3,4,5,6,7,8,9,20,21,32,33,44):
                if line[i].split(':')[0] != "./.":
                    genotype.append(line[i].split(':')[0])
        genotypeFreq = dict((j, genotype.count(j)) for j in genotype)
        if len(genotype) >= IndividualNum/2:
            rareGenotype = [x for x in genotype if genotype.count(x) == 1]
            if len(rareGenotype) > 0:
                for i in range(0,len(rareGenotype)):
                    mutationIndex = genotype.index(rareGenotype[i])
                    mutationCount[mutationIndex] = mutationCount[mutationIndex]+1
        genotype = []
print mutationCount
