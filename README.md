# NanoPoor
Monitor tool for nanopore sequencing runs. It is used to estimate the long read coverage on a short reads assembly while sequencing

#### WARNING
THIS IS THE ALPHA VERSION. It is published as it was used for the first test. A beta version will soon be released

#### Dependencies
* Python3.6
* Deepnano-blitz (it is run in a conda environment with Python 3.6 and the Rust compiler)
* blast+
* biopython
* numpy


#### How to run NanoPoor

`conda activate deepnanoblitz`

`python NanoPoor.py {folder_name} {reference_assembly}`

the {folder_name} is the same as the one set in the MinKNOW software

{reference_assembly} needs to be in fasta format


#### How it works
* NanoPoor uses deepnano-blitz to perform a quick-and-dirty basecall
* the output fasta file is used as query in a blast-search against the short-read assembly
* this process is run every few minutes (default: every hour) on newly generated fast5 files and updates a dictionary containing the covarege for each base in the draft assembly

* NanoPoor performance is optimal when run using 10+ threads in a RAMdisk folder

###### Some issues still need to be addressed:
- needs a better implementation of the deepnano-blitz basecaller
- needs parameter settings and a help menu
- needs a graphical output
- needs to automatically detect an ongoing nanopore run
