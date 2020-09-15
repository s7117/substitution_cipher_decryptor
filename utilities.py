#!/usr/bin/env python
"""
This python program contains the functions which are somewhat boilerplate to
any program.
"""
################################################################################
# Author: Peyton Chandarana
################################################################################
# Import packages
import argparse
import sys
################################################################################
def file_to_string(file_name):
    """
    This function takes in a filename and then returns its contents as a
    string assuming the file consists of one line of text.
    """
    a_file = open(file_name)
    file_line = a_file.readlines()[0]
    a_file.close()
    return str(file_line).strip('\n')
################################################################################
# Argument handling
def arg_handler():
    """
    This function handles the input parameters for the program.
    """
    parser = argparse.ArgumentParser(description='Decipher a substitution \
                                                  ciphertext.')
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-f', '--filename', metavar='filename',
                               type=str, nargs=1, required=True,
                               help='Substitution ciphertext filename')
    required_args.add_argument('-d', '--dictionary', metavar='dictionary',
                               type=str, nargs=1, required=True,
                               help='File of unique words on each line')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    filename = args.filename
    dictionary = args.dictionary
    return [filename, dictionary]
