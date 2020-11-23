import os
import sys
from searcHPV.general import *


#############
#Function: generate bash script for mapping contigs to human genome
#out_dir:out_dir for searcHPV
#humRef: human reference genome
#return: path of bash script 
def mapToHgRef(out_dir,humRef):
    sitesPath = f'{out_dir}/assemble/'
    listSites = os.listdir(sitesPath)
    outputPath = f'{out_dir}/call_fusion_virus/'
    mkdir(outputPath)
    #if there are sites
    if listSites != ['']:
        with open( f'{outputPath}/alignContigsToGenome.sh','w') as bashFile:
            bashFile.write('#!/bin/bash\n')
            for site in listSites:
                contigPath = f'{sitesPath}/{site}/pearOutput/'            
                outputPath = f'{out_dir}/call_fusion_virus/{site}/'
                mkdir(outputPath)
                bashFile.write( f'''bwa mem -R \'@RG\\tID:hpv\\tSM:hpv\\tLB:hpv\\tPL:ILLUMINA\' -M -t 8 \
    {humRef} \
    {contigPath}/{site}.all.fa.cap.contigs > {outputPath}/{site}.contigToGenome.sam
    samtools view -bhS -@ 8 {outputPath}/{site}.contigToGenome.sam > {outputPath}/{site}.contigToGenome.bam
    samtools sort -@ 8 -o {outputPath}/{site}.contigToGenome.sort.bam {outputPath}/{site}.contigToGenome.bam;
    samtools index {outputPath}/{site}.contigToGenome.sort.bam;
    rm {outputPath}/{site}.contigToGenome.sam''')
    return f'{outputPath}/alignContigsToGenome.sh'

#############
#Function: generate bash script for mapping contigs to hpv genome
#out_dir:out_dir for searcHPV
#virRef: virus reference genome
#return: path of bash script 
def mapToVirRef(out_dir,virRef):
    sitesPath = f'{out_dir}/assemble/'
    listSites = os.listdir(sitesPath)
    outputPath = f'{out_dir}/call_fusion_virus/'
    mkdir(outputPath)
    #if there are sites
    if listSites != ['']:
        with open( f'{outputPath}/alignContigsToHPV.sh','w') as bashFile:
            bashFile.write('#!/bin/bash\n')
            for site in listSites:
                contigPath = f'{sitesPath}/{site}/pearOutput/'
                outputPath = f'{out_dir}/call_fusion_virus/{site}/'
                bashFile.write( f'''bwa mem -R \'@RG\\tID:hpv\\tSM:hpv\\tLB:hpv\\tPL:ILLUMINA\' -M -t 8 \
    {virRef} \
    {contigPath}/{site}.all.fa.cap.contigs > {contigPath}/{site}.contigToHPV.sam
    samtools view -bhS -@ 8 {contigPath}/{site}.contigToHPV.sam >  {contigPath}/{site}.contigToHPV.bam
    samtools sort -@ 8 -o {outputPath}/{site}.contigToHPV.sort.bam {contigPath}/{site}.contigToHPV.bam;
    samtools index {outputPath}/{site}.contigToHPV.sort.bam;
    samtools faidx {contigPath}/{site}.all.fa.cap.contigs;
    rm {outputPath}/{site}.contigToGenome.sam''')
    return f'{outputPath}/alignContigsToHPV.sh'

#############
#Function: count number of supprotive reads for each contig
#out_dir:out_dir for searcHPV
def count_sr(out_dir):
    dirName = f'{out_dir}/assemble/'
    sites = os.listdir(dirName)

    key = ""
    rowList = []
    for site in sites:
        sampleDic = {}
        cap3File = f'{dirName}/{site}/cap3Output/{site}.CAP3'
        with open(cap3File) as eachFile:
            for i in range(0, 5):
                eachFile.readline()

            for row in eachFile:
                if re.match('^\*',row):
                    
                    key = site+"."+\
                        row.rstrip().strip(' ').split(" ")[1]+row.rstrip().strip(' ').split(" ")[2]#contig number
                    rowList = []
                else:
                    rowList.append(row)
                sampleDic[key] = rowList
                if re.match("^DETAILED",row):
                    break

    #         for items in sampleDic.items():
    #            print(items)

        with open(f'{out_dir}/call_fusion_virus/{site}/srNum.txt', "w") as sampleOutput:
            for key, value in sampleDic.items():
                sampleOutput.write(key+"\t"+str(len(value)-1)+'\n')
    return None














