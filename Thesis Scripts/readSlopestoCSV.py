import FileIO

import ntpath

import sys

import re


filenames = sys.argv[1:]
base_path = ""

ident_seperator = re.compile("(\d+).*")
pVal_seperator = re.compile("(\d+\.\d+).*")
write_header = "Species,Nb,Loci Count,Individual Count,P Value,Cycles,Decline,Slope,Intercept,P-Value"
out_string = write_header+'\n'
for filename in filenames:
    out_string = write_header + '\n'
    base_path, base_filename_full = ntpath.split(filename)
    base_filename = base_filename_full.split(".")[0]
    print(base_filename_full)

    param_array = base_filename_full.split("_")
    print param_array
    species = param_array[0]
    Nb = param_array[1]
    loci = param_array[2]
    decline_match = ident_seperator.match(param_array[3])
    decline = decline_match.group(1)
    indiv_match = ident_seperator.match(param_array[4])
    individual = indiv_match.group(1)
    cycle_match = ident_seperator.match(param_array[5])
    cycle = cycle_match.group(1)
    pVal_match= pVal_seperator.match(param_array[6])
    p_val = pVal_match.group(1)

    slopes_dict, compiled_dict = FileIO.scrapeSlopes(filename)




    out_filename = base_path+'/'+base_filename+'.'+'slopes.csv'

    for entry in slopes_dict:
        out_string+=species+","+str(Nb)+","+str(loci)+","+str(individual)+","+str(p_val)+","+str(cycle)+","+str(decline)+","+str(entry['slope'])+","+str(entry['intercept'])+","+str(entry['p_val'])+'\n'


    out_file = open(out_filename,"w")
    out_file.write(out_string)
    out_file.close()

