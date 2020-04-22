import argparse


# function for checking number of values in gc_bounds argument
def max_nargs(x):
    class RequiredLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if not len(values) <= x:
                msg = 'argument "{f}" requires maximum 2 arguments!Check if you not passed positional argument after --gc_bounds'.format(
                    f=self.dest)
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, values)

    return RequiredLength

#define arguments
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min_length", type=int,
                        help="minimum appropriate length of read")
    parser.add_argument("--keep_filtered", action='store_true',
                        help="If you want to keep filtered reads in *__failed.fastq file")
    parser.add_argument("--gc_bounds", nargs="+", action=max_nargs(2),
                        help="range of GC percent(only minimum or minimum and maximum) "
                             "USE MAXIMUM TWO VALUES AND DON'T USE POSITIONAL ARGUMENTS AFTER THIS!!!",
                        )
    parser.add_argument("--output_base_name",
                        help="Name for output file/files")
    parser.add_argument("reads",
                        help="File with reads in fastq format. Please, pass it as the last argument!")
    parser.add_argument("--leading", type=int,
                        help="Specifies the minimum quality required to keep a base")
    parser.add_argument("--trailing", type=int,
                        help="Specifies the minimum quality required to keep a base from the start")
    parser.add_argument("--headcrop", type=int,
                        help="The number of bases to remove from the start of the read from the end")
    parser.add_argument("--crop", type=int,
                        help="The number of bases to keep, from the start of the read")
    parser.add_argument("--print_stat", action='store_true',
                        help="Print statistics after reads processing")
    parser.add_argument("--slidingwindow", nargs=2, type=int,
                        help="The slidingwindow will cut the leftmost position in the window where the average quality drops below the threshold and remove")
    return parser.parse_args()


# count GC content of sequence in percentage, two digits after dot
def gc_content(x):
    c = x.count('c') + x.count('C')
    g = x.count('g') + x.count('G')
    return round(((c + g) / len(x) * 100), 2)


# checking if read length more than minimal appropriate
def min_length_check(arg, from_list):
    return arg <= len(from_list)


# check if new name for file is passed or we should use name of files with reads
def check_name(arg_output, arg_read):
    if arg_output is not None:
        output_name = arg_output
    else:
        output_name = arg_read.replace('.fastq', '')
    return output_name


# check if list len equal 4, that means all rows for one read are passed and we can continue
def len_list_equal_four(somelist):
    if len(somelist) == 4:
        return True


# Create dictionary with ascii label for quality
phred = {}
for x in range(0, 94):
    phred[str((chr(x + 33).encode('ascii')).decode("utf-8"))] = x


# Function to remove bases with quality below treshhold from the start
def leading(seq, qual, treshold):
    if seq:
        for el in range(len(seq)):
            if el == len(seq) - 1:
                seq = ''
            if phred[str(qual[el])] < treshold:
                continue
            if phred[str(qual[el])] >= treshold:
                seq = seq[el:]
                break
    return seq


# Function to remove bases with quality below treshold from the end
def trailing(seq, qual, treshold):
    if seq:
        for el in range(len(seq) - 1, 1, -1):
            if el == 1:
                seq = ''
            if phred[str(qual[el])] < treshold:
                continue
            if phred[str(qual[el])] >= treshold:
                seq = seq[:el + 1]
                break
    return seq


# Function The to cut the leftmost position in the window where the average quality drops below the threshold and remove the rest of the read
def slidingwindow(seq, qual, size, treshold):
    sum_list = []
    for el in range(len(seq) - size):
        for pos in qual[el:el + size]:
            sum_list.append(phred[str(pos)])
        if sum(sum_list) / len(sum_list) < treshold:
            seq = seq[:el + size]
            break
        else:
            sum_list = []
    return seq


def cut_quality_string(length, qual, direction):
    if direction == 'start':
        qual = qual[len(qual) - length:]
    elif direction == 'end':
        qual = qual[:length]
    return qual


# Function to remove "len" bases from the start of the read
def headcrop(seq, len):
    seq = seq[len:]
    return seq


# Function to keep "len" number of bases from the start of the read
def crop(seq, len):
    seq = seq[:len]
    return seq


# if args.gc_bounds is not None we can compare gc_cont of read with defined limits
def gc_bounds_all_in_one_maker(gc_arg, gc_cont):
    length = len(gc_arg)
    if length == 2:
        if gc_cont < int(gc_arg[0]) or gc_cont > int(gc_arg[1]):
            return False
        else:
            return True
    elif length == 1:
        if gc_cont < int(gc_arg[0]):
            return False
        else:
            return True


#list to store dropped and filtered reads
trash_list = []
filtered_list = []
# variable to store number of reads with unapropriate GC content
dropped_gc = 0
# variable to store number of reads with len less then min_lenth
dropped_len = 0


# check if reads in file is ok
def reading(reads, dropped_gc, dropped_len):
    new_list = []
    Pass_len = True
    Pass_gc = True
    with open(reads) as f:
        for line in f:
            line = line.rstrip()
            new_list.append(line)
            # Check length and GC content
            if len_list_equal_four(new_list):
                if args.gc_bounds is not None:
                    Pass_gc = gc_bounds_all_in_one_maker(args.gc_bounds, gc_content(new_list[1]))
                    if not Pass_gc:
                        dropped_gc += 1

                # make headcrop if defined
                if args.headcrop is not None:
                    new_list[1] = headcrop(new_list[1], args.headcrop)
                    new_list[3] = headcrop(new_list[3], args.headcrop)

                # make crop if defined
                if args.crop is not None:
                    new_list[1] = crop(new_list[1], args.crop)
                    new_list[3] = crop(new_list[3], args.crop)

                # make slingwindow if defined
                if args.slidingwindow is not None:
                    new_list[1] = slidingwindow(new_list[1], new_list[3], args.slidingwindow[0], args.slidingwindow[1])
                    new_list[3] = cut_quality_string(len(new_list[1]), new_list[3], 'end')

                # make leading and trailing if defined
                if args.leading is not None:
                    new_list[1] = leading(new_list[1], new_list[3], args.leading)
                    new_list[3] = cut_quality_string(len(new_list[1]), new_list[3], 'start')
                if args.trailing is not None:
                    new_list[1] = trailing(new_list[1], new_list[3], args.trailing)
                    new_list[3] = cut_quality_string(len(new_list[1]), new_list[3], 'end')

                # Check if length is OK after all trimming operations
                if args.min_length is not None:
                    Pass_len = min_length_check(args.min_length, new_list[1])
                    if not Pass_len:
                        dropped_len += 1

                if not Pass_len and args.keep_filtered or not Pass_gc and args.keep_filtered:
                    trash_list.append(new_list)
                if Pass_len and Pass_gc:
                    filtered_list.append(new_list)
                new_list = []
                Pass_len = True
                Pass_gc = True
        reading_result_dict = {'gc': dropped_gc, 'len': dropped_len, 'filtered': filtered_list, 'trash': trash_list}
        return reading_result_dict


def write_trash(output_name, result):
    if args.keep_filtered:
        if not trash_list:
            print('Attention! All reads are passed and "{}__failed.fastq" file will be empty!'.format(output_name))
        with open(output_name + '__failed.fastq', "w") as f:
            for el in result['trash']:
                for x in el:
                    f.write(x + '\n')


def write_passed(output_name, result):
    with open(output_name + '__passed.fastq', "w") as f:
        for el in result['filtered']:
            for x in el:
                f.write(x + '\n')


def print_output(result):
    if args.print_stat:
        print('Total number of processed reads:{}'.format(len(result['filtered']) + len(result['trash'])))
        print('{} reads was dropped out from the file'.format(len(result['trash'])))
        print(
            '{} reads was dropped out due to inappropriate GC-content and {} was dropped out due to low length'.format(
                result['gc'], result['len']))
        if args.keep_filtered:
            print('Dropped reads were saved in {}__failed.fastq file'.format(output_name))
        else:
            print('Dropped reads were NOT stored due to the absence of keep_filtered argument')


if __name__ == '__main__':
    args = parse_args()
    output_name = check_name(args.output_base_name, args.reads)
    res = reading(args.reads, dropped_gc, dropped_len)
    write_passed(output_name, res)
    write_trash(output_name, res)
    print_output(res)
