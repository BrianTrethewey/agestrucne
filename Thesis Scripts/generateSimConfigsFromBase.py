from __future__ import print_function
import glob
import os
import sys
import ntpath

import configparser


if __name__ == "__main__":
#not used but was for creating different values of SNPS
    SNP_array = [400]
#decline values to test
    decline_array = [0.1,0.05,0.15]

    configNames = sys.argv[1:]

    config = configparser.ConfigParser()
    configFile = None
    for configName in configNames:
        print(configName)
        config = configparser.ConfigParser()
        config.read(configName)
        base_path, base_filename_full = ntpath.split(configName)
        base_filename = base_filename_full.split(".")[0]
        print(base_filename)
        for SNP_val in SNP_array:
            SNP_ind = str(SNP_val)
            config.set("genome",'numSNPs',str(SNP_val))
            for decline_val in decline_array:
                start = config.get('sim','startSave')
                end = config.get('sim','gens')
                decline_ind = str(decline_val+100)+"D"
                nbadj_val = "[\'"+str(start)+"-"+str(end)+":"+str(decline_val)+"\']"
                config.set('sim','nbadjustment',nbadj_val)
                configFile  = base_path+'/'+base_filename+'_'+SNP_ind+'_'+decline_ind+'.conf'
                config.write(open(configFile, "w"))

