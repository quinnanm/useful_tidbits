#copy eos files from lpc to lxplus

import subprocess
import os
import argparse
import sys
import math
import numpy as np
import random

parser = argparse.ArgumentParser(description='copy eos files from lpc to lxplus') 
#parser.add_argument("-i", "--indir", dest="indir", default='/eos/uscms/store/user/cmantill/bbVV/input/Jan19/2017') 
parser.add_argument("-i", "--indir", dest="indir", default='/eos/uscms/store/user/cmantill/bbVV/input/Jan19_Validation/2017') 
parser.add_argument("-o", "--outdir", dest="outdir", default='/eos/user/m/mequinna/hwwtraining/AK8_Jan19') 
parser.add_argument("-d", "--dirsmade", dest="dirsmade", action='store_true')
parser.set_defaults(dirsmade=False) 
args = parser.parse_args()

split_frac = 0.15

print 'split_frac', split_frac
print 'have you made the lxplus eos dirs yet? option set to ', args.dirsmade
print 'NOTE: this is the lxplus eos directory', args.outdir

cmd=''
cmd2=''

if not args.dirsmade:
    print 'Need to make dirs: Do this on lxplus first:'
    for subdir, dirs, files in os.walk(args.indir):
        if dirs == ['pickles', 'root'] :
            proc = subdir.replace(args.indir,'')
            print 'mkdir ', args.outdir+'/test'+proc 
            if 'Validation' not in args.indir:
                print 'mkdir ', args.outdir+'/train'+proc 

else:
    print 'DIRS MADE: COPYING FILES'
    for subdir, dirs, files in os.walk(args.indir):
        # print 'START'
        if dirs == ['pickles', 'root'] :
            proc = subdir.replace(args.indir,'')

        #print 'files', files
        if len(files)<1 or '.pkl' in files:
            continue
        
        random.shuffle(files)
        split_index = math.ceil(len(files)*split_frac)
        print 'split index:', split_index, 'total N files', len(files)

        #print files
        # print 'len(files[:split_index])',len(files[:split_index])
        # print 'len(files[split_index:])', len(files[split_index:])

        for i,file in enumerate(files):
            # f=file
            inf=subdir+'/'+file
            inf=inf.replace('/eos/uscms','root://cmseos.fnal.gov/')
            if '.root' in inf:
                
                print 'file',i+1, 'of', len(files) 
                
                outf_test = args.outdir+'/test'+proc+'/'+file
                outf_train = args.outdir+'/train'+proc+'/'+file

                if 'Validation' in args.indir:
                    test_cmd='\nsubprocess.call(\' xrdcp '+inf+' '+outf_test+'\',shell=True)'
                    print test_cmd
                    cmd+=test_cmd

                else:
                    if i<split_index: #small piece
                        print 'TEST'
                        test_cmd='\nsubprocess.call(\' xrdcp '+inf+' '+outf_test+'\',shell=True)'
                        print test_cmd
                        cmd+=test_cmd

                    elif i>=split_index: #big piece
                        print 'TRAIN'
                        train_cmd='\nsubprocess.call(\' xrdcp '+inf+' '+outf_train+'\',shell=True)'
                        print train_cmd
                        cmd2+=train_cmd
                print '\n'
# cmd+='\''
print cmd                
with open("copy_cmd4test.py",'w') as cmdfile:
    cmdfile.write('import subprocess\n')
    cmdfile.write(cmd)
    # cmdfile.write('\nsubprocess.call(cmd, shell=True)')
    print 'wrote copy_cmd4test.py'

if 'Validation' not in args.indir:
    # cmd2+='\''
    print cmd2
    with open("copy_cmd4train.py",'w') as cmdfile:
        cmdfile.write('import subprocess\n')
        cmdfile.write(cmd2)
        # cmdfile.write('\nsubprocess.call(cmd, shell=True)')
        print 'wrote copy_cmd4train.py'
