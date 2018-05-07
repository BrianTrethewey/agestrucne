import ntpath

import sys

import re

setDict = {'25':[],'50':[],'100':[]}
filenames = sys.argv[1:]
base_path = ""
re_pattern  = "\S*?\t\S*?\t\S*?\t\\S*?\t(\d*).*?\t.*?\t.*?\t.*?\t.*?\t.*?\t.*?\t.*?\t.*?\t.*?\t.*?\t.*?\t.*?\t.*?\t.*?\t.*?\t.*?\t.*?.*"
re_obj = re.compile(re_pattern)
for filename in filenames:
    setDict = {'25': [], '50': [], '100': []}
    base_path, base_filename_full = ntpath.split(filename)
    base_filename = base_filename_full.split(".")[0] 
    print(base_filename_full)
    file = open(filename,"r")
    header = file.readline()
    for line in file:
        if re_obj.match(line) is not None:
            re_match = re_obj.match(line)
            pop_val = re_match.group(1)
            setDict[pop_val].append(line)
    out_file_base = base_path+'/'+base_filename
    for key in setDict.keys():
        ident = key+'I'
        outfilename = out_file_base+"_"+ident+".tsv"
        outFile = open(outfilename,"w")
        outFile.write(header)
        print key
        for record in setDict[key]:
            outFile.write(record)
        print outfilename
        print len(setDict[key])
        outFile.close()
