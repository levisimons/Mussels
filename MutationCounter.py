import os,sys,re
import csv

fileInput = "SOL_MYTILUS.VF.SNP.vcf"
GenotypeNum = 30

#Open the vcf file containing all the loci where potential SNPs are located.
#Filter out the headers.
#Filter out the adults genome columns as well as the loci metadata columns.
#Filter out loci with less than half of the individuals counted.
#Check for individuals with a unique haplotype at that loci.
#Count up each instance for each individual.
f = csv.reader(open(fileInput,"rU"), delimiter='\t')
genotype = []
haplotype = []
mutationCount = [0]*GenotypeNum
genCount=0
hapCount=0

#output = csv.writer(open("JuvenileMutations.vcf","w"), delimiter='\t')

for line in f:
#    if line[0].startswith('#') == True and line[0].startswith('##') == False:
#        output.writerow(line)
    if line[0].startswith('#') == False:
        j=0
	for i in range(0, len(line)):
            if i not in (0,1,2,3,4,5,6,7,8,9,20,21,32,33,44):
                if line[i].split(':')[0] != "./.":
                    j=j+1
                genotype.append(line[i].split(':')[0])
                haplotype.append(line[i].split(':')[0].split('/')[0])
                haplotype.append(line[i].split(':')[0].split('/')[1])
        rareGenotype = [x for x in genotype if genotype.count(x) == 1]
        rareHaplotype = [x for x in haplotype if haplotype.count(x) == 1]
        if len(rareGenotype) > 0:
            for i in range(0,len(rareGenotype)):
                if rareGenotype != ['./.']: Index = int(genotype.index(rareGenotype[i]))
                if j >= 15 and rareGenotype != ['./.']:
                    mutationCount[Index] = mutationCount[Index]+1
                    genCount=genCount+1
                    print 'Single genotype',j,len(genotype),rareGenotype,Index,genotype
                    print mutationCount
        if len(rareHaplotype) > 0 and len(rareGenotype) == 0:
            for i in range(0,len(rareHaplotype)):
                if rareHaplotype != ['./.']: Index = int(haplotype.index(rareHaplotype[i])/2)
                if j >= 15 and rareHaplotype != ['.']:
                    mutationCount[Index] = mutationCount[Index]+1
                    hapCount=hapCount+1
                    print 'Single haplotype',j,len(haplotype),rareHaplotype,Index,haplotype
                    print mutationCount
        print hapCount,genCount
        genotype=[]
        haplotype=[]
print mutationCount
