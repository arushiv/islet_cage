import pandas
import numpy
import itertools
import os
import sys
import math
import argparse

sys.path.append("/home/arushiv/toolScripts/")
from make_trackdb import pstanza
        
def geturl(x):
    return os.path.join(params.urlstem, x)


def getOpts():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('filename', help="""The file with hg19 tiles to search for.""")
    parser.add_argument('-tn','--track', nargs='?', type=str, default="", help="""The track name""")
    parser.add_argument('-sl','--shortLabel', nargs='?', type=str, default="", help="""The short label. (Default:First column of filename split by '_')""")
    parser.add_argument('-i','--infoString', nargs='?', type=str, default="chromatin states from ChIP-seq", help="""The long label.""")
    parser.add_argument('-p','--parent', nargs='?', type=str, default="chromatin_states", help="""The parent. (Default=chromatin_states)""")
    parser.add_argument('-ft','--filetype', nargs='?', type=str, default="bigBed 9 +.", help="""The file type.(Default=bigBed 9 +.)""")
    parser.add_argument('-u','--url', nargs='?', type=str, default="https://theparkerlab.med.umich.edu/gb/custom-tracks/", help="""The url.(Default=url constructed from filename path)""")
    parser.add_argument('outfile', help="""Name of the output file.""")



    bb = expand(os.path.join(BROWSER_DIR, '{type}', '{tissue}.bb'),
                    type = ['atac_peaks', 'histone_chromatin_states', 'tcs'],
                    tissue = TISSUES),
        bw = expand(os.path.join(BROWSER_DIR, 'atac_seq', '{tissue}.bw'),
                    tissue = TISSUES)
    output:
        db = os.path.join(BROWSER_DIR, "trackdb.txt")


if __name__ == '__main__':

    CELL = {
        'parent': ['Islets','SkeletalMuscle','Adipose','Liver'],
        'atac_seq': ['Islets','SkeletalMuscle','Adipose'],
        'tc': [],
        'atac_peaks': [],
        'chrom_states': []
        }
    
    pstanza(output.db, level=0, track="Islets",
            **{'shortLabel':'Islet data',
               'longLabel' :'Islet CAGE, TCs, ATAC-seq, peaks and RNA-seq',
               'superTrack' : 'on show',
               'priority' : 1})
    
    pstanza(output.db, level=1, track="Islet-CAGE",
            **{'shortLabel':'Islet CAGE',
               'longLabel' :'Islet CAGE data',
               'parent' : "Islets",
               'container': "multiWig",
               'visibility': "full",
               'type': "bigWig",
               'maxHeightPixels' : "100:100:16",
               'aggregate': "transparentOverlay",
               'priority' : 1.1})

    pstanza(output.db, level=2, track="Islet-CAGE-fwd",
            **{'type': 'bigWig',
               'bigDataUrl': geturl("2019-01-02-ATAC-comparisons/atac-comparisons/islet.fwd.bw"),
               'parent': 'Islet-CAGE',
               'color': '85,149,212',})
    
        
    pstanza(output.db, level=2, track="Islet-CAGE-rev",
            **{'type': 'bigWig',
               'bigDataUrl': geturl("2019-01-02-ATAC-comparisons/atac-comparisons/islet.rev.bw"),
               'parent': 'Islet-CAGE',
               'color': '85,149,212',
               'altColor': '85,85,212'})
                                       
    pstanza(output.db, level=1, track="Islet-CAGE-TCs",
            **{'shortLabel':'Islet TCs',
               'longLabel' :'Islet CAGE tag clusters',
               'parent' : "Islets",
               'visibility': "dense",
               'itemRgb' : 'on',
               'type': "bigBed 6 +.",
               'bigDataUrl': geturl("2019_CAGE/tcs/Islets.bb"),
               'priority' : 1.2})
        
    pstanza(output.db, level=1, track="Islet-ATACseq",
            **{'shortLabel':'Islet ATACseq',
               'longLabel' :'Islet ATAC seq track',
               'parent' : "Islets",
               'visibility': "full",
               'color': "255,128,0",
               'maxHeightPixels': "50:50:50",
               'windowingFunction': 'mean',
               'smoothingWindow': 3,
               'type': "bigWig",
               'bigDataUrl':geturl("2019_CAGE/atac_seq/Islets.bw"),
               'priority' : 1.3})
                                                                      
    pstanza(output.db, level=1, track="Islet-ATAC-peaks",
            **{'shortLabel':'Islet ATAC-peaks',
               'longLabel' :'Islet ATAC-seq broad peaks (1% FDR)',
               'parent' : "Islets",
               'visibility': "dense",
               'type': "bigBed",
               'bigDataUrl':geturl("2019_CAGE/atac_peaks/Islets.bb"),
               'priority' : 1.4})

    pstanza(output.db, level=1, track="Islet-states",
            **{'shortLabel':'Islet states',
               'longLabel' :'Islet chromatin states',
               'parent' : "Islets",
               'visibility': "dense",
               'itemRgb' : 'on',
               'type': "bigBed 9 +.",
               'bigDataUrl':geturl("2019_CAGE/histone_chromatin_states/Islets.bb"),
               'priority' : 1.5})
        

        pstanza(output.db, level=1, track="Islet-RNAseq",
                **{'shortLabel':'Islet RNA-seq',
                 'longLabel' :'Islet RNA-seq track',
                 'parent' : "Islets",
                 'container': "multiWig",
                 'visibility': "full",
                 'type': "bigWig -10 10",
                 'maxHeightPixels' : "100:100:16",
                 'aggregate': "transparentOverlay",
                 'priority' : 1.6})

        pstanza(output.db, level=2, track="Islet-RNA-fwd",
                **{'type': 'bigWig',
                'bigDataUrl': geturl('test/track_hub/VDH041_depth.Win2.fwd.bw'),
                'parent': 'Islet-RNAseq',
                'color': '85,149,212',})

        
        pstanza(output.db, level=2, track="Islet-RNA-rev",
                **{'type': 'bigWig',
                'bigDataUrl': geturl('test/track_hub/VDH041_depth.Win2.rev.bw'),
                'parent': 'Islet-RNAseq',
                'color': '85,149,212',
                'altColor': '85,85,212'})
