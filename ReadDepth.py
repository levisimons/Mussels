import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

#This function reads in the read depth profile for a population.  The first two columns are the 
#chromosome and position and the remaining columns are the read depth at those sites for each
#individual.  The output histograms are in pdf format.
def depthGraph(index):
    with open('out.gdepth') as f:
        v = np.loadtxt(f, delimiter="\t", dtype='float', comments="#", skiprows=1, usecols=[index])
    v_hist = np.ravel(v)   # 'flatten' v
    fig = plt.figure()
    fig.suptitle(header[index], fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)

    n, bins, patches = ax.hist(v_hist, bins=100, normed=1, facecolor='green')
    ax.set_xlabel('Read depth')
    ax.set_ylabel('Relative abundance')
    ax.set_xlim(0, 20)
    plt.show()
    filename = header[index],'pdf'
    filename = '.'.join(filename)
    pp = PdfPages(filename)
    pp.savefig(fig)
    pp.close()
    f.close()

header = ['CHROM','POS','12x10_FP','12x10_J01','12x10_J02','12x10_J03','12x10_J04','12x10_J05','12x10_J06','12x10_J07','12x10_J08','12x10_J09','12x10_J10','12x10_MP','14x12_FP','14x12_J01','14x12_J02','14x12_J03','14x12_J04','14x12_J05'$

#Iterate through all of the individuals.
for i in range(2,len(header)):
    print i,header[i]
    index = i
    depthGraph(index)
