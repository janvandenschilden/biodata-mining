from blast import blast
#from uniprotRetrieve import uniprotRetrieve
#from uniprotGroupId import uniprotGroupId
from clustalOmega import clustalOmega

sequences=list()
with open("./coronavirus.fasta") as f:
    for line in f.readlines():
        if line.startswith(">"):
            sequences.append(line)
        else:
            sequences[-1]+=line
 
for seq in sequences:
    name = seq.split("|")[1]
    print(name)
    format="fasta"
    BlastFile = name+"."+format
    BlastFile = blast(seq, 
                      output=BlastFile ,
                      database="UniRef90", 
                      eValue=0.0001, 
                      hits=1000, 
                      format=format)
    
    ClustalOmegaFasta, ClustalOmegaPim = clustalOmega(BlastFile, 
                                                      outputFormat="Pearson/FASTA")