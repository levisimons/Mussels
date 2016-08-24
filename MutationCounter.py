import os,sys,re
import csv

#Open a file containing the allele frequencies at various SNP sites.
fileInput = "Juveniles.frq"
genomeNum = 60
fileOutput = ("JuvenileOutliers.tsv")
header = ["CHROM","POS","N_ALLELES","N_CHR","ALLELE_FREQ1","ALLELE_FREQ2","ALLELE_FREQ3","ALLELE_FREQ4"]
output = csv.writer(open(fileOutput, "w"),delimiter='\t')
output.writerow(header)

# Look for SNPs where at least half of the individuals are present, scan the relative frequency of the
# alleles, then select the SNPs where one of the alleles is only present at a frequency at or below a
# certain threshold.
with open(fileInput, "rU") as f:
    f = csv.reader(f, delimiter="\t")
    next(f, None)
    for line in f:
        if [] == line: break
        if float(line[3]) >= float(genomeNum/2):
            alleleNum = int(line[2])
            threshold = 1/float(line[3])
            for i in range (0, alleleNum):
                if float(line[4+i].split(":")[1]) <= threshold and float(line[4+i].split(":")[1]) > 0:
                    output.writerow(line)
