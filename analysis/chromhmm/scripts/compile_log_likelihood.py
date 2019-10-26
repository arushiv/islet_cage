
# coding: utf-8

# In[76]:


import pandas 
import numpy
import seaborn as sns
#get_ipython().magic('matplotlib inline')
import glob
import os
import time
import subprocess as sp
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from pathlib import Path

# In[77]:

d = pandas.DataFrame({'filename': snakemake.input.log})

d['feature'] = d['filename'].map(lambda x: os.path.basename(x).replace("log.learnmodel.", "").replace(".txt",""))

def msplit(x):
    return x.rsplit('.', 1)

d['feature'],d['numStates'] = zip(*d['feature'].map(msplit))
d['numStates'] = d['numStates'].astype(int)

def getLastLine(x):
    cmd = f"less {x} | grep -v 'Writing' | grep -v 'Warning' | tail -1"
    return sp.check_output(cmd, shell=True).decode("utf-8")

d.loc[:,'lastline'] = d.filename.map(getLastLine)
d[['iteration','estimated_log_likelihood','change', 'totalTime']] = d.lastline.str.split(expand=True)
d.loc[:,'estimated_log_likelihood'] = d.estimated_log_likelihood.astype(float)

d.loc[:,'change'] = d.change.astype(float)
print(len(d.index))
print(len(d[d['change']==0.001].index))
d1 = d[d['change']==0.001]

for name, grp in d1.groupby("feature"):
    figname = os.path.join(snakemake.params.figdir, f"loglikelohoods.{name}.png")
    s = sns.lmplot(data=grp, x="numStates", y="estimated_log_likelihood", fit_reg=False)
    s.savefig(figname)

    
Path(snakemake.output.fig).touch()
 
