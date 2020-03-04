import argparse
import re


def max_nargs(x):
    class RequiredLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if not len(values) <= x:
                msg = 'argument "{f}" requires maximum 2 arguments!Check if you not passed positional argument after --gc_bounds'.format(
                    f=self.dest)
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, values)

    return RequiredLength


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
args = parser.parse_args()


def gc_content(x):
    c = x.count('c') + x.count('C')
    g = x.count('g') + x.count('G')
    return (c + g) / len(x) * 100


if args.output_base_name is not None:
    output_name = args.output_base_name
else:
    output_name = args.reads.replace('.fq', '')

trash_list = []
filtered_list = []
new_list = []
Pass = True
with open(args.reads, 'r') as f:
    for line in f:
        line = line.rstrip()
        new_list.append(line)
        if len(new_list) == 4:
            if len(new_list[1]) < args.min_length:
                Pass = False
            elif args.gc_bounds is not None:
                if len(args.gc_bounds) == 2:
                    if gc_content(new_list[1]) < int(args.gc_bounds[0]) or gc_content(new_list[1]) > int(
                            args.gc_bounds[1]):
                        Pass = False
                elif len(args.gc_bounds) == 1:
                    if gc_content(new_list[1]) < int(args.gc_bounds[0]):
                        Pass = False
            if not Pass and args.keep_filtered:
                trash_list.append(new_list)
            if Pass:
                filtered_list.append(new_list)
            new_list = []
            Pass = True

if args.keep_filtered:
    if not trash_list:
        print('Attention! All reads are passed and "{}__failed.fastq" file will be empty!'.format(output_name))
    with open(output_name + '__failed.fastq', "w") as f:
        for el in trash_list:
            for x in el:
                f.write(x + '\n')

with open(output_name + '__passed.fastq', "w") as f:
    for el in filtered_list:
        for x in el:
            f.write(x + '\n')
