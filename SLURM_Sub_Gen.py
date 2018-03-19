import os

wavedict = {}
filelist = os.listdir(os.curdir)
filelist.sort()
for filename in filelist:
        wavefunction = filename.split('.wfn')[0]
        if filename.endswith(".wfn"):
                wavedict.update({wavefunction: []})
        if filename.endswith(".inp") and filename.startswith(wavefunction) and wavefunction in wavedict:
                wavedict[wavefunction].append(filename)
for wavefunction, inputfiles in wavedict.items():
        for filename in inputfiles:
                with open(filename + 'sub.pbs', 'w') as subscript:
                        subscript.write('#!/bin/bash\n#SBATCH --time=60:00:00\n#SBATCH --mem=2048m\n\n')
                        filenamesplit = filename.split('.')
                        extension = filenamesplit[1]
                        subscript.write('for (( i = 1; i <= 10; i++))\ndo\n  ./proaimv.out ' + wavefunction + '.' + extension + ' ' + wavefunction + '\n\n  if [ $(grep -c "NORMAL TERMINATION OF PROAIMV" ' + wavefunction + '.' + extension + '.int) -gt 0 ]\n  then\n    break\n  fi\n\ndone')
