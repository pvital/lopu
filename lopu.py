#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# lopu - LOg Parsing Utility
# Copyright (c) 2020 Paulo Vital <pvital@gmail.com>
#

import argparse
import re
import sys


REGEX_RULES = {
    'timestamp': r'(([01]\d|2[0123]):([012345]\d):([012345]\d))',
    'ipv4': r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
    'ipv6': r'\b(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)\b',
}


def DEBUG(content):
    '''
    Prints DEBUG messages with given content.

    Args:
        content: str   string to print as DEBUG message

    Returns:
        None
    '''
    print(f'---> \033[1;33;40mDEBUG\033[m - {content}')


def init_argparse():
    '''
    Initialize the argument parsing.

    Returns:
        argparse.ArgumentParser
    '''
    parser = argparse.ArgumentParser(
        prog='util.py',
        usage='%(prog)s [OPTION]... [FILE]',
        description='log parsing utility.'
    )

    parser.add_argument(
        '-f', '--first', action='store', type=int, metavar='NUM',
        help='Print first NUM lines' , dest='head_val'
    )

    parser.add_argument(
        '-l', '--last', action='store', type=int, metavar='NUM',
        help='Print last NUM lines', dest='tail_val'
    )

    parser.add_argument(
        '-t', '--timestamps', action='store_true',
        help='Print lines that contain a timestamp in HH:MM:SS format'
    )

    parser.add_argument(
        '-i', '--ipv4', action='store_true',
        help='Print lines that contain an IPv4 address, matching IPs \
              are highlighted'
    )

    parser.add_argument(
        '-I', '--ipv6', action='store_true',
        help='Print lines that contain an IPv6 address, (standard \
              notation), matching IPs are highlighted'
    )

    parser.add_argument(
        '-v', '--version', action='version',
        version = f'{parser.prog} version 0.1'
    )

    parser.add_argument('FILE', nargs='?')

    return parser


def read_file(file):
    '''
    Read a give file and returns a list with it's lines content.

    Args:
        file: str   path of the file to be read

    Returns:
        list containing the lines of file
    '''
    file_content = []

    with open(file) as f:
        for line in f:
            file_content.append(line.rstrip())

    return file_content


def search_pattern(content, pattern):
    '''
    Print all lines containing one of the patterns format.
    Patterns can be: timestamp, ipv4, ipv6

    Args:
        content: list  log content to analyse
        pattern: str        pattern to search for

    Returns:
        list containing the lines to display
    '''
    ret = []

    if pattern not in REGEX_RULES.keys():
        return ret

    for line in content:
        # Set regex to look for the pattern HH:MM:SS
        regex = re.compile(REGEX_RULES[pattern], re.M|re.I)
        match = regex.search(line)
        if match:
            if pattern in ['ipv4', 'ipv6']:
                ret.append(line.replace(match.group(),
                            '\033[1;33;44m{}\033[m'.format(match.group())))
            else:
                ret.append(line)

    return ret


def check_intersection(args, fargv = False):
    '''
    Check sys.argv to create a FIFO sequence to inteserction execution.

    This is a 'workarround' solution to get the exact sequence of arguments
    passed, since argparse doens't perserve/store it.

    Args:
        args: argparse.Namespace    arguments read from command line
        fargv: list                 fake argv for unittests - Default is False

    Returns:
        list of sequential actions
    '''
    argv_seq = []

    for arg in (fargv if fargv else sys.argv[1:]):
        # Do not consider the following argument options
        if arg in [args.FILE, '-h', '--help', '-v', '--version']:
            continue

        # check arg with startswith() method since the argument can be passed
        # with space, together (like -f2) or with = (--first=2)
        if arg.startswith('-f') or arg.startswith('--first'):
            argv_seq.append('head')
        elif arg.startswith('-l') or arg.startswith('--last'):
            argv_seq.append('tail')
        elif arg.startswith('-t') or arg.startswith('--timestamps'):
            argv_seq.append('timestamp')
        elif arg.startswith('-i') or arg.startswith('--ipv4'):
            argv_seq.append('ipv4')
        elif arg.startswith('-I') or arg.startswith('--ipv6'):
            argv_seq.append('ipv6')
        else:
            continue

    return argv_seq


def parse_log(args, fargv = False):
    '''
    Parse log

    Args:
        args: argparse.Namespace    arguments read from command line
        fargv: list                 fake argv for unittests - Default is False

    Returns:
        list containing the output
    '''
    # Create a list to store the output lines
    log_content = []

    # If there's no file to parse as argument, capture from STDIN
    if not args.FILE:
        for line in sys.stdin:
            log_content.append(line.rstrip())
    else:
        # Read file
        try:
            log_content = read_file(args.FILE)
        except (FileNotFoundError, IsADirectoryError) as err:
            print(f'{sys.argv[0]}: {args.FILE}: {err.strerror}')
            return sys.exit(1)

    # Check the arguments passed and execute the actions based on the sequence
    for action in check_intersection(args, fargv):
        if action == 'head':
            # Print from {log_content} the {args.head_val} first lines.
            log_content = log_content[:args.head_val]
        if action == 'tail':
            # Print from {log_content} the {args.head_val} last lines.
            log_content = log_content[-args.tail_val:]
        if action in ['timestamp', 'ipv4', 'ipv6']:
            # Search for {action} pattern in {log_content}
            log_content = search_pattern(log_content, action)

    # return the output of the actions as list
    return log_content


def main():
    '''
    Main function.
    '''
    # Parse the arguments
    parser = init_argparse()
    args = parser.parse_args()

    # Print the output of the actions
    for line in parse_log(args):
        print(f'{line}')


if __name__ == '__main__':
    main()
    sys.exit(0)
