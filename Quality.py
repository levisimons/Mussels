import sys
import os
import csv
import re
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import gzip
import pylab

# This function reads in gzipped FASTQ files and calculates the average and
# standard deviation on the Phred read quality score for each read position
# for a given individual.  Each output file is in tsv format with the first
# column the mean quality score, the second column the standard deviation on
# the mean, and the row number the read position along the fragment length.
def QualityOutput(SequenceLength,QualityData,filename):
    QualityString = "!\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    QualityChar = list(QualityString)
    Quality = np.zeros(shape=(SequenceLength,len(QualityData)))       
    for i in range(0,len(QualityData)):
        QualityNum = list(QualityData[i])
        for j in range(0,len(QualityNum)-1):
            Quality[j][i] = QualityString.index(QualityNum[j])
    QDF = pd.DataFrame(Quality)
    QDF_Out = pd.concat([QDF.mean(axis=1),QDF.std(axis=1)], axis=1)
    QDF_Out.columns = ['Quality Score Mean','Quality Score Standard Deviation']
    QDF_Out.index.name = 'Base pair read position'
    fileOut = "".join([filename,'average.txt'])
    QDF_Out.to_csv(fileOut, sep='\t')
    x = QDF_Out.index.values
    y = QDF_Out['Quality Score Mean']
    plt.figure()
    plt.errorbar(x,y,xerr=0,yerr=QDF_Out['Quality Score Standard Deviation'])
    plt.title(filename)
    plt.xlabel('Read position (bp)')
    plt.ylabel('Average quality score')
    imageOut = ''.join([filename,'plot.png'])
    plt.savefig(imageOut)

# This loop iterates the QualityOutput function through a directory containing
# all of the FASTQ files of interest.  The only data read in from each of these
# files is the quality score as a function of read position for each of the
# fragments read in a given individual.
for file in os.listdir(os.getcwd()):
    if file.endswith(".gz"):
        print file
        filename = file[:-7]
        print filename
        f = gzip.open(file,"rU")
        i=0
        QualityData = []
        for line in f:
            i=i+1
            if i%4 == 0:
                QualityData.append(list(line))
                SequenceLength = len(list(line))
        QualityOutput(SequenceLength,QualityData,filename)
