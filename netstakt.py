#!/usr/bin/env python3

"""Windows netstat without the unfortunate newline when using
the -b flag.

    Usage:

        netstakt.py

    Author: 

        Written by: Evan Ottinger (@OttySec)
"""

import os


def _check_env():
    """Performs a check to reasonably determine whether or not the 
    user is running the script from a Windows Administrator terminal.

        Returns:
            True: if the user has access to an Admin directory
    """
    if os.name == 'nt':
        try:
            temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
            return True
        except:
            print("netstakt must be run as Administrator to use the -b flag.")
            exit()
    else:
        print("This script is intended for use on Windows systems. *nix users can already enjoy this functionality using $ netstat -naop")

        
def run_netstat():
    """Runs netstat -naob and saves the output to netstat.tmp.

    """
    os.system("netstat -naob > netstat.tmp")


def get_content():
    """Reads the content of netstat.tmp to memory.

        Returns:
            content: a list of lines of output from netstat.
    """
    with open("netstat.tmp") as f:
        content = f.readlines()

    return content


def format_output(content):
    """Formats the output such that the CMD is in-line with the related
    network information.

        Args:
            content: a list of lines of output from netstat

        Returns:
            output: a string of grepable netstat output

    """
    buffer = None
    output = ""

    for line in content:
        split_line = line.split()

        # Some lines in netstat are None length and throw
        # index out of bounds errors without this try...except
        try: 
            if split_line[0] == "TCP" or split_line[0] == "UDP":
                buffer = split_line
            elif buffer:
                buffer.append(' '.join(split_line))
                output += ','.join(buffer) + '\n'
                buffer = None
        except:
            pass
    
    return output


def print_output(output):
    """Prints the formatted netstat output to standard out in a columnar format.

        Args: 
            output: a string of grepable netstat output
    """
    header = ['Proto', 'Local Address', 'Foreign Address', 'State', 'PID', 'CMD']
    table_format = "{: <7} {: <40} {: <20} {: <13} {: <7} {: <20}"


    print("Active Connections\n")
    print(table_format.format(*header))

    rows = output.split('\n')
    split_rows = []
    
    for row in rows:
        split_row = row.split(',')
        split_rows.append(split_row)

    for row in split_rows:
        if row[0] == "TCP":
            print(table_format.format(*row))
        elif row[0] == "UDP":
            row.insert(3, " ")
            print(table_format.format(*row))
        

def cleanup_disk():
    """Removes netstat.tmp from the local disk.

    """
    os.remove("netstat.tmp")


def main():
    run_netstat()
    content = get_content()
    output = format_output(content)
    print_output(output)
    cleanup_disk()


if __name__ == '__main__':
    if _check_env():
        main()
    
