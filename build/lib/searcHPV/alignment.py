from searcHPV.generate_alignment import *
import subprocess
from searcHPV.general import *

#####################
#pipeline of alignment
#Function:
#1. customize reference genome
#2. generate alignment bash script
#3. run alignment script
#fq1: paired-end raw sequencing data, fastq1
#fq2: paired-end raw sequencing data, fastq2
#humRef: human reference genome
#outputDir: output directory
#rmdup: = True: remove duplicate = False : don't remove duplicate, default = TRUE
def alignment(fq1, fq2, humRef, virRef, outputDir, rmdup = True):
    #make output dir
    mkdir(outputDir)
    scriptDir = f'{outputDir}/alignment'
    mkdir(scriptDir)

    #catenate humRef and virRef
    ref = catRef(humRef,virRef, outputDir)

    #generate alignment bash

    alignmentFile = scriptDir + "/orignal.alignment.sh"
    indelFile = scriptDir + "/indel.alignment.sh"
    generate_alignment_bash(alignmentFile,ref,fq1,fq2,outputDir)
    generate_indel_alignment_bash(indelFile,ref,outputDir)
    check_file(alignmentFile)
    check_file(indelFile)

    #rmdup for alignment results
    
    bashFile = scriptDir + f"/alignment.sh"
    if not rmdup:
    ##generate indel alignment bash file
        with open(bashFile,'w') as output:
            output.write(f'''bash {alignmentFile};
bash {indelFile};''')
    else:
        generate_mkdup_bash(indelFile,outputDir)


        with open(bashFile,'w') as output:
            output.write(f'''bash {alignmentFile};
bash {indelFile};''')

    #run scripts
    check_file(bashFile)
    os.system(f'chmod +x {bashFile}')
    subprocess.call(bashFile)
