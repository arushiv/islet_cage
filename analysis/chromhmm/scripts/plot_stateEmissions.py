import pandas
import numpy
import seaborn as sns
import pandas
import numpy
import seaborn as sns
import subprocess as sp
import matplotlib
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import argparse

matplotlib.rcParams['pdf.fonttype'] = 42

def makeHeatmap(filename, outputfile):
    dm = pandas.read_csv(filename,header=None, names=['result','state','marknum','mark','yes-no','prob'], sep="\t")
    dm = dm[(dm['result']=="emissionprobs") & (dm['yes-no']==1.0)][['state','mark','prob']]
    newdm = dm.pivot(index='state',columns='mark', values='prob')
    plt.figure(figsize=(6, 7))
    sns.heatmap(newdm, cmap="Blues", linecolor="black", linewidths=0.3)
    plt.tight_layout()
    plt.savefig(outputfile)



def getOpts():
    parser = argparse.ArgumentParser(description="""Plot emission heatmaps from ChromHMM model.txt""")
    parser.add_argument('model', help="""model file""")
    parser.add_argument('figure', help="""figure filename""")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    
    args = getOpts()
    makeHeatmap(args.model, args.figure)
