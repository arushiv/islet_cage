import argparse

def printline(stuff, offset):
    return f"{offset}{stuff}\n"

def pstanza(outputfile, level=None, track=None, **kwargs):

    offset = '\t'*level
    
    with open(outputfile, 'a+') as f:
        f.write(printline(f"track\t{track}", offset))

        for arg, value in kwargs.items():
            f.write(printline(f"{arg}\t{value}", offset))

        f.write("\n\n")
            
# def getOpts():
#     parser = argparse.ArgumentParser()
        
#     parser.add_argument('filename', help="""The file with hg19 tiles to search for.""")
#     parser.add_argument('-tn','--track', nargs='?', type=str, default="", help="""The track name""")
#     parser.add_argument('-sl','--shortLabel', nargs='?', type=str, default="", help="""The short label. (Default:First column of filename split by '_')""")
#     parser.add_argument('-i','--infoString', nargs='?', type=str, default="chromatin states from ChIP-seq", help="""The long label.""")
#     parser.add_argument('-p','--parent', nargs='?', type=str, default="chromatin_states", help="""The parent. (Default=chromatin_states)""")
#     parser.add_argument('-ft','--filetype', nargs='?', type=str, default="bigBed 9 +.", help="""The file type.(Default=bigBed 9 +.)""")
#     parser.add_argument('-u','--url', nargs='?', type=str, default="", help="""The url.(Default=url constructed from filename path)""")
#     parser.add_argument('outfile', help="""Name of the output file.""")
    
#     args = parser.parse_args()
        
# if __name__ == '__main__':
        
                                                                                                                                                                                                                                        
