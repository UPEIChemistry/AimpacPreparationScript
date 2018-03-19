import os

wavedict = {}
filelist = os.listdir(os.curdir)
filelist.sort()
for file in filelist:
        rootname = file.split('.wfn')
        if file.endswith(".wfn"):
                wavedict.add({rootname: []})
        if file.endswith(".inp") and file.startswith(rootname) and rootname in wavedict:
                wavedict[rootname].append(file)

for key, inputfiles in wavedict.items():
        for filename in inputfiles:
                with open(filename + 'sub.pbs', 'w') as subscript:
                        subscript.write('#!/bin/bash\n#SBATCH --time=60:00:00\n#SBATCH --mem=2048m\n\n')
                        atomsplit = filename.split('.')
                        subscript.write('for (( i = 1; i <= 10; i++))\ndo\n  ./proaimv.out ' + atomsplit[0] + '.' + atomsplit[1] + ' ' + key[0] + '\n\n  if [ $(grep -c "NORMAL TERMINATION OF PROAIMV" ' + atomsplit[0] + '.' + atomsplit[1] + '.int) -gt 0 ]\n  then\n    break\n  fi\n\ndone')
