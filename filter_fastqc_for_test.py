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
    return parser.parse_args()


# count GC content of sequence in percentage, two digits after dot
def gc_content(x):
    c = x.count('c') + x.count('C')
    g = x.count('g') + x.count('G')
    return round(((c + g) / len(x) * 100), 2)


# checking if read length more than minimal permitted
def min_length_check(arg, from_list):
    if arg > len(from_list):
        return False


# check if new name for file is passed or we should use name of files with reads
def check_name(arg_output, arg_read):
    if arg_output is not None:
        output_name = arg_output
    else:
        output_name = arg_read.replace('.fastq', '')
    return output_name


# in case of need for print smth
def filtered(arg):
    print(arg)


# check if list len equal 4, that means all rows for one read are passed and we can continue
def len_list_equal_four(somelist):
    if len(somelist) == 4:
        return True


# if args.gc_bounds is not None we can compare gc_cont of read with passed limits
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



trash_list = []
filtered_list = []


# check if reads in file is ok
def reading(reads):
    new_list = []
    Pass = True
    with open(reads) as f:
        for line in f:
            line = line.rstrip()
            new_list.append(line)
            if len_list_equal_four(new_list):
                if args.min_length is not None:
                    Pass = min_length_check(args.min_length,new_list[1])
                elif args.gc_bounds is not None:
                    Pass = gc_bounds_all_in_one_maker(args.gc_bounds, gc_content(new_list[1]))
                if not Pass and args.keep_filtered:
                    trash_list.append(new_list)
                if Pass:
                    filtered_list.append(new_list)
                new_list = []
                Pass = True
        return filtered_list


def write_trash(output_name):
    if args.keep_filtered:
        if not trash_list:
            print('Attention! All reads are passed and "{}__failed.fastq" file will be empty!'.format(output_name))
        with open(output_name + '__failed.fastq', "w") as f:
            for el in trash_list:
                for x in el:
                    f.write(x + '\n')


def write_passed(output_name):
    with open(output_name + '__passed.fastq', "w") as f:
        for el in reading(args.reads):
            for x in el:
                f.write(x + '\n')


if __name__ == '__main__':
    args = parse_args()
    output_name = check_name(args.output_base_name, args.reads)
    write_passed(output_name)
    write_trash(output_name)
    reading(args.reads)
