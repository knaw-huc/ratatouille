#! /usr/bin/env python3

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Merge multiple Elastic indices to a unified index')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')
    args = parser.parse_args()

    if args.quiet:
        verbosity = -1
    elif args.verbose:
        verbosity = 1
    else:
        verbosity = 0

    print(f'Verbosity: {verbosity}')

if __name__ == '__main__':
    main()
