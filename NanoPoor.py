import sys
import glob
import os
import subprocess
from Bio import SeqIO
import numpy as np
import time

folder=sys.argv[1].strip()
reference=sys.argv[2].strip()

used_files=[]
coverage={}

starttime=time.time()

##### BUILD dictionary
inF=open(reference,"r")

for i in SeqIO.parse(inF,"fasta"):
        contig=str(i.id)
        if len(str(i.seq))>500:################################# MIN LENGTH OF INDEXED CONTIGS
                for x in range(1,len(str(i.seq))+1):
                        index="%s_%i" %(contig,x)
                        coverage[index]=0

cmd="makeblastdb -in %s -dbtype nucl" %(reference)
os.system(cmd)

ITIT=0



while 1==1:
        ITIT+=1
        os.system("rm -rf workfolder")
        os.system("mkdir workfolder")
        cmd="ls %s/*/fast5/*.fast5" %(folder)
        statfiles=subprocess.getoutput(cmd)
        statfiles=statfiles.strip().split("\n")
        c=0
        for x in statfiles:
                if x not in used_files:
                        c+=1
                        if c==65:################################# MAX NUMBER OF FAST5 FILES TO ANALYZE AT EACH ITERATION
                                break
                        used_files.append(x)
                        cmd="cp %s workfolder" %(x)
                        os.system(cmd)
        os.system("deepnano2_caller.py --output out.fasta --directory workfolder --network-type 48 --beam-size 1 --threads 15") #NUMBER OF THREADS TO USE FOR BLAST ANALYSIS
        cmd="blastn -query out.fasta -db %s -num_threads 15 -outfmt '6 pident length sstart send sseqid' | awk '$1>90' | awk '$2>1000' | cut -f3,4,5" %(reference)#################
######## MIN LENGTH LONG READS TO ADD TO THE COVERAGE/DEPTH ANALYSIS // NUMBER OF THREADS TO USE FOR BLAST ANALYSIS
        output = subprocess.getoutput(cmd)
        os.system("rm out.fasta")
        output=output.strip().split("\n")
        for x in output:
                x=x.strip().split()
                LL=[int(x[0]),int(x[1])]
                #print(LL)
                START=min(LL)
                END=max(LL)
                RR=[i for i in range(START,END+1)]
                #print(RR)
                for y in RR:
                        #print(y)
                        CC=x[2]+"_"+str(y)
                        coverage[CC]+=1
                        #print(CC)
                        #print(coverage[CC])
        #print(coverage)
        cc=list(coverage.values())
        logname="LOG_#%i.txt" %(ITIT)
        log=open(logname,"w")
        log.write("==============\n")
        log.write("ITERATION:%i\n" %(ITIT))
        log.write("MAX:%i\n" %(max(cc)))
        log.write("MIN:%i\n" %(min(cc)))
        log.write("AVG:%f\n" %(sum(cc)/float(len(cc))))
        P05=np.percentile(cc, 5)
        P95=np.percentile(cc,95)
        log.write("P05:%i\n" %(P05))
        log.write("P95:%i\n" %(P95))
        check_folder = subprocess.getoutput("ls workfolder/ | wc -l")
        log.write("CHECK FOLDER:%s\n" %(check_folder.strip()))
        log.write("CHECK USED_FILES:%i\n" %(len(used_files)))
        log.write("==============\n")
        cc.sort()


        #if ITIT==10:
                #break
        log.close()
        ################### ADD FUNCTION send mail with log?
        
        schedtime=starttime+(ITIT*3600) ########################### REPEAT THE ANALYSIS EVERY 3600 SECONDS (1 HOUR)
        while time.time() < schedtime:
                time.sleep(60)
        
os.system("rm -rf workfolder")
