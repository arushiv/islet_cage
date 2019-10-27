#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pandas
import numpy
import math
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import glob
import time
from scipy import stats
import pybedtools
import subprocess as sp
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams.update({'font.size': 12})
matplotlib.rcParams['font.sans-serif'] = "DejaVu Sans"
import random


# In[37]:


mdir = "/lab/work/arushiv/cage/work/tc_enrichment_in_annotations/figures/"

def gp(name):
    return os.path.join(mdir, name)

def rot(g):
    for i, ax in enumerate(g.fig.axes):   ## getting all axes of the fig object
        ax.set_xticklabels(ax.get_xticklabels(), rotation = 90)

def save(name):
    plt.savefig(gp(name), bbox_inches="tight")


# In[38]:


rename = {
 'UTR 5 (UCSC)': "5' UTR (UCSC)" ,
 'atac peaks': "ATAC-seq peaks",
 'UTR 3 (UCSC)': "3' UTR (UCSC)"}

in_parantheses = ['Trynka','LindbladToh','Hoffman','Andersson','Hnisz', 'UCSC']

def significance(x, N):
    if x > 0.05:
        return "non-significant"
    elif x <= 0.05/N:
        return "Significant (Bonferroni)"
    elif x <= 0.05 and x > 0.05/N:
        return "Nominally significant"


gat_results = "/lab/work/arushiv/cage/work/tc_enrichment_in_annotations/results_GAT.dat"
d = pandas.read_csv(gat_results, sep='\t')
d['annotation_info'] = d['annotation']
d['annotation'] = d['annotation'].str.replace("Islets.","" )

d['annotation'] = d['annotation'].str.replace("_", " ")
for string in in_parantheses:
    d['annotation'] = d['annotation'].str.replace(string, f"({string})")

d['annotation'] = d['annotation'].map(lambda x: rename[x] if x in rename.keys() else x)
d.sort_values('fold', inplace=True, ascending=False)

n = len(d.index)
d['significance'] = d['pvalue'].map(lambda x: significance(x, n))
d.head()


# In[39]:


# full sorted figure
plt.figure(figsize=(5,10))
g1 = sns.barplot(data=d, x='l2fold', y='annotation', hue='significance', dodge=False,
                palette = {"Significant (Bonferroni)":"#ff7f00",
                           'Nominally significant': "#4daf4a",
                    'non-significant': "#377eb8"
                      })
g1.axes.axvline(x=0.0, **{'linestyle':'--', 'color':'black'})
plt.xlabel("Tag cluster overlap log2(Fold Enrichment)")
plt.ylabel("Annotation")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
save("fig.full_annotation_enrichment_log2fold.pdf")


# In[41]:


# Ordered figure
order_all = ['Active TSS',
              'ATAC-seq peaks',
              'Flanking TSS',
              'Genic enhancer',
              'Bivalent poised TSS',
              'Active enhancer',
              'Strong transcription',
              'Weak TSS',
               'Weak enhancer',
 'Weak transcription',
 'Repressed polycomb',
              'Quiescent low signal',
 "5' UTR (UCSC)",
 'TSS (Hoffman)',
 'Coding (UCSC)',
 'Promoter (UCSC)',
 'H3K4me3 peaks (Trynka)',
 'H3K9ac peaks (Trynka)',
 'FetalDHS (Trynka)',
 'Conserved (LindbladToh)',
 'TFBS ENCODE',
 'H3K9ac (Trynka)',
 'DHS peaks (Trynka)',
 'H3K4me3 (Trynka)',
 'DHS (Trynka)',
 "3' UTR (UCSC)",
 'DGF ENCODE',
  'Enhancer (Hoffman)',
 'H3K27ac PGC2',
 'SuperEnhancer (Hnisz)',
 'H3K27ac (Hnisz)',
 'H3K4me1 (Trynka)',
 'H3K4me1 peaks (Trynka)',
 'PromoterFlanking (Hoffman)',
 'Enhancer (Andersson)',
 'WeakEnhancer (Hoffman)',
'Intron (UCSC)',
 'CTCF (Hoffman)',
  'Transcribed (Hoffman)',
'Repressed (Hoffman)',
 ]


dselect = d[d['annotation'].isin(order_all)].set_index('annotation')
plotdf = dselect.loc[order_all,:]
plt.figure(figsize=(5,10))
g1 = sns.barplot(data=plotdf, x='l2fold', y=plotdf.index, hue='significance', dodge=False,
                palette = {"Significant (Bonferroni)":"#ff7f00",
                           'Nominally significant': "#4daf4a",
                    'non-significant': "#377eb8"
                      })
g1.axes.axvline(x=0.0, **{'linestyle':'--', 'color':'black'})
plt.xlabel("Tag cluster overlap log2(Fold Enrichment)")
plt.ylabel("Annotation")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
save("fig.ordered_annotation_enrichment_log2fold.pdf")


# In[42]:


# save to files
dselect.reset_index().to_csv("/lab/work/arushiv/cage/work/tc_enrichment_in_annotations/results_GAT_formatted.dat",
              sep='\t', index=False, na_rep="NA")
dselect.reset_index().to_excel("/lab/work/arushiv/cage/work/tc_enrichment_in_annotations/results_GAT_formatted.xlsx",
            index=False, na_rep="NA")
dselect.head()


# In[43]:


# subset figure
select = ['Active TSS',
              'ATAC-seq peaks',
              'Flanking TSS',
              'Genic enhancer',
              'Bivalent poised TSS',
              'Active enhancer',
              'Strong transcription',
              'Weak TSS',
               'Weak enhancer',
 'Weak transcription',
 'Repressed polycomb',
              'Quiescent low signal',
 "5' UTR (UCSC)",
 'Coding (UCSC)',
 'Promoter (UCSC)',
 'H3K4me3 peaks (Trynka)',
 'H3K9ac peaks (Trynka)',
 'Conserved (LindbladToh)',
 'TFBS ENCODE',
 'DHS peaks (Trynka)',
 'H3K4me3 (Trynka)',
 "3' UTR (UCSC)",
 'SuperEnhancer (Hnisz)',
 'H3K4me1 peaks (Trynka)',
 'Enhancer (Andersson)',
 'Intron (UCSC)',
 ]

dselect = d[d['annotation'].isin(select)].set_index('annotation')
plotdf = dselect.loc[select,:]
plt.figure(figsize=(5,10))
g1 = sns.barplot(data=plotdf, x='l2fold', y=plotdf.index, hue='significance', dodge=False,
                palette = {"Significant (Bonferroni)":"#ff7f00",
                           'Nominally significant': "#4daf4a",
                    'non-significant': "#377eb8"
                      })
g1.axes.axvline(x=0.0, **{'linestyle':'--', 'color':'black'})
plt.xlabel("Tag cluster overlap log2(Fold Enrichment)")
plt.ylabel("Annotation")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
save("fig.selected_annotation_enrichment_log2fold.pdf")


# In[ ]:




