import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

with open('out.gdepth') as f:
    v = np.loadtxt(f, delimiter="\t", dtype='float', comments="#", skiprows=1, usecols=[4])
v_hist = np.ravel(v)   # 'flatten' v
fig = plt.figure()
fig.suptitle('12x10_J01', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)

n, bins, patches = ax.hist(v_hist, bins=100, normed=1, facecolor='green')
ax.set_xlabel('Read depth')
ax.set_ylabel('Relative abundance')
ax.set_xlim(0, 20)
plt.show()
pp = PdfPages('foo.pdf')
pp.savefig(fig)
pp.close()
