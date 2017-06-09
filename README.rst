=======================================================
mka -- easy bootstrap of ATAC-seq and RNA-seq pipelines
=======================================================

``mka`` (short for "make analysis") is a tool we use to create ATAC-seq
and RNA-seq pipelines in the Parker Lab at the University of Michigan.

Features
========

* Its output is a ready-to-go analysis: just run ``make run`` to start
  it. The Makefile also includes targets for cleaning your work
  directories and creating a GitHub repository for the analysis.

* Generates Python scripts that in turn generate your pipeline. These
  scripts tend to be more robust and easier to customize than shell
  scripts written by hand, particularly if you have a lot of input
  data.

* You can supply your own pipeline templates, if you don't like our
  choice of tools or the settings we use.

* Works with any FASTQ input files; while there's specific support for
  data from the UM DNA Sequencing Core, we routinely use it for public
  data or when collaborating on data sequenced at other institutions.

* Can handle input from more than one organism.

* Creates read group information from the metadata you supply, making
  it easier to track libraries throughout the pipeline.

Shortcomings
============

* It's not very general -- it does what we want and not much else. If
  you want to use bowtie instead of bwa, or cutadapt instead of our
  adapter trimmer, you'll need to provide your own templates.

* You can't currently start from BAM files.

Requirements
============

Python requirements
-------------------

These should automatically be installed by pip when you ``pip install
https://github.com/ParkerLab/mka/``:

* Jinja2
* python-dateutil

Pipeline requirements
---------------------

* `FASTQC`_
* `cta`_, our C++ version of Jason Buenrostro's adapter trimmer
* `bwa`_
* `MACS2`_
* `bedtools`_
* `samtools`_
* `drmr`_, our tool for working with resource managers like Slurm or
  PBS

Other requirements
------------------

* `hub`_, if you want to create a GitHub repository for your analysis

Installation
============

   ``pip install git+https://github.com/ParkerLab/mka``

Examples
========

ATAC-seq
--------

For this example, I'm using data from ATAC-seq assays we performed on
human skeletal muscle for [Scott2016]_. I downloaded that data into a
local directory, ``Run_1398``. The files relevant to ``mka`` were:

* ``Run_1398_parker.csv``
* ``parker/``

  * ``Sample_53252/``

    * ``53252_CTCTCTAC_S1_L002_R1_001.fastq.gz``
    * ``53252_CTCTCTAC_S1_L002_R2_001.fastq.gz``

  * ``Sample_53253/``

    * ``53253_CAGAGAGG_S2_L002_R1_001.fastq.gz``
    * ``53253_CAGAGAGG_S2_L002_R2_001.fastq.gz``

Working in that directory, I used the ``screname`` script to create
specially-named symlinks to those FASTQ files, using the run
information provided by the UM DNA Sequencing Core in
``Run_1398_parker.csv``::

    $ screname -v Run_1398_parker.csv parker Scott2016
    Looking for FASTQ files in parker/Sample_53252
    Linking ../parker/Sample_53252/53252_CTCTCTAC_S1_L002_R1_001.fastq.gz -> Scott2016/53252___53252___L002___13-human-atac-k5-10mg.1.fq.gz
    Linking ../parker/Sample_53252/53252_CTCTCTAC_S1_L002_R2_001.fastq.gz -> Scott2016/53252___53252___L002___13-human-atac-k5-10mg.2.fq.gz
    Looking for FASTQ files in parker/Sample_53253
    Linking ../parker/Sample_53253/53253_CAGAGAGG_S2_L002_R1_001.fastq.gz -> Scott2016/53253___53253___L002___14-human-atac-k5-2mg.1.fq.gz
    Linking ../parker/Sample_53253/53253_CAGAGAGG_S2_L002_R2_001.fastq.gz -> Scott2016/53253___53253___L002___14-human-atac-k5-2mg.2.fq.gz
    ...

The ``mka`` file naming scheme is
``sample___library___readgroup___description.pair_index.fq.gz``. The
triple underscores make for cumbersome names, but allow easy parsing
and more freeform descriptions. Since the sequencing core doesn't
provide more than one library per sample name, the above files have
the same values for each.

To use the file name parsing with third-party data, you'll have to
rename the files without the aid of ``screname``. The files from
[Buenrostro2013]_ could look like this::

    GSM1155957___SRR891268___GM12878_ATACseq_50k_Rep1___1.fastq.gz
    GSM1155957___SRR891268___GM12878_ATACseq_50k_Rep1___2.fastq.gz
    GSM1155958___SRR891269___GM12878_ATACseq_50k_Rep2___1.fastq.gz
    GSM1155958___SRR891269___GM12878_ATACseq_50k_Rep2___2.fastq.gz
    ...

You don't have to use the file name parsing at all; running ``mka``
with the ``--interactive`` flag lets you provide or override all the
library metadata for arbitrary input files. The special file names are
just a way to save time.

With the input files set up, I ran ``mka``. Because there were
actually additional files in Run 1398 containing data not used in the
paper, I'm selecting a subset here, in samples 53252 and 53253::

    $ mka -v --run-info Run_1398_parker.csv -t atac-seq -d "ATAC-seq of human skeletal muscle" -a ~/analyses/scott2016 ~/control/scott2016 Scott2016/5325[23]*
    Reading sequencing run information from Run_1398_parker.csv
      Please specify the reference genome: hg19

    Libraries: {
        "53252": {
            "analysis_specific_options": {},
            "description": "13-human-atac-k5-10mg",
            "library": "53252",
            "readgroups": {
                "L002": [
                    "/nfs/turbo/parkerlab1/lab/data/seqcore/Run_1398/Scott2016/53252___53252___L002___13-human-atac-k5-10mg.1.fq.gz",
                    "/nfs/turbo/parkerlab1/lab/data/seqcore/Run_1398/Scott2016/53252___53252___L002___13-human-atac-k5-10mg.2.fq.gz"
                ]
            },
            "reference_genome": "hg19",
            "sample": "53252",
            "sequencing_center": "UM DNA Sequencing Core",
            "sequencing_date": "2015-10-23",
            "sequencing_platform": "ILLUMINA",
            "sequencing_platform_model": "",
            "url": ""
        },
        "53253": {
            "analysis_specific_options": {},
            "description": "14-human-atac-k5-2mg",
            "library": "53253",
            "readgroups": {
                "L002": [
                    "/nfs/turbo/parkerlab1/lab/data/seqcore/Run_1398/Scott2016/53253___53253___L002___14-human-atac-k5-2mg.1.fq.gz",
                    "/nfs/turbo/parkerlab1/lab/data/seqcore/Run_1398/Scott2016/53253___53253___L002___14-human-atac-k5-2mg.2.fq.gz"
                ]
            },
            "reference_genome": "hg19",
            "sample": "53253",
            "sequencing_center": "UM DNA Sequencing Core",
            "sequencing_date": "2015-10-23",
            "sequencing_platform": "ILLUMINA",
            "sequencing_platform_model": "",
            "url": ""
        }
    }

    Your analysis is ready in /home/hensley/control/scott2016
    $

At this point, I can change directory to ``~/control/scott2016`` and
type ``make run`` to submit the pipeline with ``drmr``. I'll be mailed
when it finishes, or if any job encounters an error.


.. [Scott2016] `The genetic regulatory signature of type 2 diabetes in
               human skeletal muscle, Scott et al., Nature
               Communications 2016`_
.. [Buenrostro2013] `Transposition of native chromatin for fast and
                    sensitive epigenomic profiling of open chromatin,
                    DNA-binding proteins and nucleosome position,
                    Buenrostro et al., Nature Methods 2013`_

.. _FASTQC: http://www.bioinformatics.babraham.ac.uk/projects/fastqc/
.. _cta: https://github.com/ParkerLab/cta/
.. _bwa: http://bio-bwa.sourceforge.net/
.. _MACS2: https://github.com/taoliu/MACS
.. _bedtools: http://bedtools.readthedocs.io/en/latest/
.. _samtools: http://samtools.sourceforge.net/
.. _drmr: https://github.com/ParkerLab/drmr/
.. _hub: https://github.com/github/hub
.. _The genetic regulatory signature of type 2 diabetes in human skeletal muscle, Scott et al., Nature Communications 2016: https://doi.org/10.1038/ncomms11764
.. _Transposition of native chromatin for fast and sensitive epigenomic profiling of open chromatin, DNA-binding proteins and nucleosome position, Buenrostro et al., Nature Methods 2013: https://doi.org/10.1038/nmeth.2688
