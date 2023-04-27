#!/usr/bin/python

import sys
import os
import subprocess


def _help():
    print("""Usage: python chooseOpts.py [options]
    Options:
        -h, --help: Show this help message.
        -s, --start: Start the server.
        -q, --quit: Stop the server.
        -o, --options: Configure the server properties.
        -c, --console: Open the server console.
    If no options are specified, the server will be started.""")


def _switch(option: str):
    switcher = {
        '-h': _help,
        '--help': _help,
        '-s': _start,
        '--start': _start,
        '-q': _quit,
        '--quit': _quit,
        '-o': _options,
        '--options': _options,
        '-c': _console,
        '--console': _console
    }
    return switcher.get(option)


def _start():
    """
    Start the server.
    """
    if not (subprocess.check_output('docker container inspect minecraft  -f \'{{.State.Running}}\'')
                .strip()
                .decode()
                .replace('\'', '') == 'true'):
        os.system('docker-compose up -d')
    else:
        print('Server already running.')


def _quit():
    """
    Stop the server.
    """
    os.system('docker-compose down')

def _options():
    props = _load_properties('server.properties')
    print('Current server properties:')
    for key, value in props.items():
        print(f'{key}={value}')
    print("Enter the new properties:")
    print("Enter number of options to change (0 to keep current):")
    n = int(input())
    for i in range(n):
        print(f'Enter key {i+1}:')
        key = input()
        print(f'Enter value {i+1}:')
        value = input()
        props[key] = value
    with open('server.properties', 'w') as f:
        for key, value in props.items():
            f.write(f'{key}={value}\n')
    os.system("docker cp server.properties minecraft:/opt/minecraft/server.properties")
    print("Properties changed successfully.")
    print("Remember to restart the server for the changes to take effect.")
    
def _console():
    """
    Open the server console.
    """
    os.system('docker attach minecraft')


def _load_properties(file_path, sep='=', comment_char='#') -> dict:
    """
    Read the file passed as parameter as a properties file.

    Parameters
    ----------
    file_path : str
        Path to the file to be read.
    sep : str, optional
        Separator character between key and value in the properties file.
    comment_char : str, optional
        Character used to indicate the start of a comment line.

    Returns
    -------
    props : dict
        Dictionary containing the key-value pairs in the properties file.
    """
    props = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line[0] == comment_char:
                continue
            key, value = line.split(sep, 1)
            props[key] = value.strip()
    return props


def main():
    n = len(sys.argv)
    if n == 1:
        _start()
    elif n == 2:
        _switch(sys.argv[1])()


if __name__ == '__main__':
    main()
