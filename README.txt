Tool FilterFastq2 was created to filter reads in Fastq format

Several options are avaliable on FilterFastq2:

    • CROP <length> 
length: The number of bases to keep, from the start of the read

    • HEADCROP <length> 
length: The number of bases to remove from the start of the read

    • TRAILING <quality> 
quality: Specifies the minimum quality required to keep a base

    • LEADING <quality>
quality: Specifies the minimum quality required to keep a base

    • MIN_LENGTH <length> 
length: Specifies the minimum length of reads to be kept

    • SLIDINGWINDOW <windowSize> <requiredQuality>
cut the leftmost position in the <windowSize> where the average quality drops below the threshold and remove the rest of the read

    • GC_BOUNDS <minimum_GC_percent> opltional<maximum_GC_percent>
minimum_GC_percent:  Specifies the minimum GC content of reads to be kept
maximum_GC_percent: Specifies the maximum GC content of reads to be kept

    • OUTPUT_BASE_NAME <name>
name : Specifies the name of output file. Name of input file will be used if it is omitted

    • keep_filtered
Flag to keep failed reads in file *__failed.fastq. Inappropriate reads will be irretrievably removes if it is omitted. 

    • print_stat
Flag to print statistics of FilterFastq2 work. It includes number of processed reads, whole number of dropped reads and number of reads dropped due to the low length and inappropriate GC content

Usage example:
python3 FilterFastq2.py [-h] [--min_length MIN_LENGTH]
                                    [--keep_filtered]
                                    [--gc_bounds GC_BOUNDS [GC_BOUNDS ...]]
                                    [--output_base_name OUTPUT_BASE_NAME]
                                    [--leading LEADING] [--trailing TRAILING]
                                    [--headcrop HEADCROP] [--crop CROP]
                                    [--print_stat]
                                    [--slidingwindow SLIDINGWINDOW SLIDINGWINDOW]
                                    reads


Attention! IMPORTANT INFORMATION!
    • Simultaneous using CROP/HEADCROP and LEADING/TRAILING/SLIDINGWINDOW is depricated, but if you want to use it in a such way HEADCROP/CROP operations will be implemented in the first place
    • FilterFastq2 is only compatible with FASTQ reads where Phred33 scale is used for quality
    • FilterFastq2 was created for Python3 (version > 3.6) and usage of other Python version may cause errors
    • Checking for appropriate GC content is implemented before CROP/HEADCROP/LEADING/TRAILING/SLIDINGWINDOW operations because this feature is organism characteristic and it is highly depends on reads length. Checking for read length is implemented after trimming procedure.


General statistic of FilterFastq2 includes all information about number of processed reads, number of dropped reads and their destination. Also it includes information about the reason why it was dropped(GC-content or length)

In this branch you can also find file FilterFastq2_tests.py which includes tests for all functions which are involved in processing of reads inside FilterFastq2.py. 
