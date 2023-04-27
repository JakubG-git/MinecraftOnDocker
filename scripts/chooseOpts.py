#!/usr/bin/python

import sys
import subprocess
from os import path

def _help():
    """
    Show help message.
    """

    print("""Usage: python chooseOpts.py [options]
    Options:
        -h, --help: Show this help message.
        -s, --start: Start the server.
        -q, --quit: Stop the server.
        -o, --options: Configure the server properties.
        -c, --console: Open the server console.
    If no options are specified, the server will be started.""")

def _switch(option: str):
    """
    Switcher function to call the correct function based on the option passed as parameter.

    Parameters
    ----------
    option : str
        Option to be executed.
    
    Returns
    -------
    function
        Function to be executed.
    """

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
    if subprocess.run('docker container inspect minecraft', stdout=subprocess.DEVNULL, stderr=subprocess.PIPE).returncode != 0:
        print('Server not found. Creating new server.')
        subprocess.run('docker-compose up -d')
    elif not (subprocess.check_output('docker container inspect minecraft  -f \'{{.State.Running}}\'')
                .strip()
                .decode()
                .replace('\'', '') == 'true'):
        subprocess.run('docker-compose up -d')
    else:
        print('Server already running.')

def _quit():
    """
    Stop the server.
    """
    subprocess.run('docker-compose down')

def _options(file_path='server.properties'):
    """
    Change the server properties.
    Parameters
    ----------
    file_path : str, optional
        Path to the server properties file.
    """

    # Get the absolute path to the server properties file
    script_dir = path.dirname(__file__)
    files_dir = path.join(script_dir, '..', 'files')
    file_path = path.join(files_dir, file_path)

    # Load the properties file
    if not path.isfile(file_path):
        print('Server properties not found. Loading default properties.')
        props = _load_properties(path.join(files_dir, 'server.properties.default'))
    else:
        props = _load_properties(file_path)

    print('Current server properties:')
    for key, value in props.items():
        print(f'{key}={value}')
    print("Enter the new properties:")
    print("Enter number of options to change (0 to keep current):")

    try:
        n = int(input())
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    # Change the properties
    for i in range(n):
        print(f'Enter key {i+1}:')
        key = input()
        print(f'Enter value {i+1}:')
        value = input()
        props[key] = value

    final_file_path = path.join(files_dir, 'server.properties')
    # Save the properties to the file
    with open(final_file_path, 'w') as f:
        for key, value in props.items():
            f.write(f'{key}={value}\n')

    # Copy the properties file to the container
    print("Copying properties to the container...")
    subprocess.run(f"docker cp {final_file_path} minecraft:/opt/minecraft/server.properties")
    
    print("Properties changed successfully.")
    print("Remember to restart/reload the server for the changes to take effect.")
    
def _console():
    """
    Open the server console.
    """
    subprocess.run('docker attach minecraft')


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
        try:
            _switch(sys.argv[1])()
        except TypeError:
            print('Invalid option. Use -h or --help for help.')
    else:
        print('Invalid number of arguments. Use -h or --help for help.')
if __name__ == '__main__':
    main()
