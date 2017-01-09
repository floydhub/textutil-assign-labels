from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import random

def str2bool(val):
    """
    Helper method to convert string to bool
    """
    if val is None:
        return False
    val = val.lower().strip()
    if val in ['true', 't', 'yes', 'y', '1', 'on']:
        return True
    elif val in ['false', 'f', 'no', 'n', '0', 'off']:
        return False

def main():
    """
    Simple helper script to assign labels to data in multiple files. All the rows in 
    a single file will be assigned the same label.

    This reads all the data into memory first. It is fast, but unsuitable for large files
    """

    # Parse command line args
    parser = argparse.ArgumentParser(description='Assign labels to input data')

    fileargs = ['input1', 'input2', 'input3', 'input4', 'input5']
    labelargs = ['label1', 'label2', 'label3', 'label4', 'label5']

    for i in range(len(fileargs)):
        parser.add_argument('-i{}'.format(i+1), '--{}'.format(fileargs[i]),
            required=True if i==0 else False,
            help='Path to input file {}'.format(i))
        parser.add_argument('-l{}'.format(i+1), '--{}'.format(labelargs[i]),
            required=True if i==0 else False,
            help='Label for input file {}'.format(i))
    
    parser.add_argument('-o', '--output', required=True, help='Path to output file')
    parser.add_argument('-d', '--delimiter', required=True, default='\t', 
        help='Column delimiter between row and label')
    parser.add_argument('-s', '--shuffle', required=False, type=str2bool,
        default='False', help='Shuffle rows in output?')
    parser.add_argument('-p', '--position', required=False, choices=['start', 'end'],
        default='end', help='Position label at start or end of row? (Default is end)')

    args = parser.parse_args()
    # Unescape the delimiter
    # args.delimiter = args.delimiter.decode('string_escape') # Python 2
    args.delimiter = bytes(args.delimiter, "utf-8").decode('unicode_escape') # Python 3
    # Convert args to dict
    vargs = vars(args)

    print("\nArguments:")
    for arg in vargs:
        print("{}={}".format(arg, getattr(args, arg)))

    # Load data from files
    output = []
    for i in range(len(fileargs)):
        file = vargs[fileargs[i]]
        label = vargs[labelargs[i]]
        if file and label:
            print("\nProcessing Input{}".format(i))
            rows = list(open(file, 'r').readlines())
            if args.position == 'start': # append label to start of row
                rows = [label + args.delimiter + row.strip() for row in rows]
            else: # append label to end of row
                rows = [row.strip() + args.delimiter + label for row in rows]
            output = output + rows

    # Shuffle all rows?
    if args.shuffle == True:
        print("\nShuffling rows")
        random.shuffle(output)

    with open(args.output, "w") as f:
        print("\nDumping to output")
        for row in output:
            f.write("{}\n".format(row))

    print("\nDone. Bye!")

if __name__ == '__main__':
    main()