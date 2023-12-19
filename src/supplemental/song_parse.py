import requests
import uuid
import urllib
import base64
import re
import signal
import os
from fragile import fragile

lines = []
index = 0
sessionIndex = 0
firstWrite = True
saved = False
restore = False

def get_link(song, artist):
    print(song, artist)

# write rest of file if program exits early 
def restore_rest():
    with open('../../songs.txt', 'a+') as songs:
        if not firstWrite and not saved:
            songs.write('\n')
            songs.write(lines[sessionIndex])
        elif not saved:
            songs.write(lines[sessionIndex])

        for num, line in enumerate(lines):
            if num >= index:
                songs.write(line)

def prompt(str):
    try:
        return input(str)
    except KeyboardInterrupt:
        print('\nNOTE: To EXIT the program enter \'exit\'\n')
        return None
    
def force_prompt(str):
    task = None
    while task is None:
        task = prompt(str)
    return task

# load song file (if it exists)
with open('../../songs.txt', 'r') as songs:
    # store all lines
    lines = songs.readlines()

with fragile(open('../../songs.txt', 'w+')) as songs:
    if len(lines) == 0:
        print('Song history is empty! Listen to some tracks!')
        exit(0)

    print('\nNOTE: For each of the following tracks you have the choice to delete it from your song history file or keep it for future reference.\n')
    
    for num, line in enumerate(lines):
        index = num
        
        if 'Session started on' in line:
            sessionIndex = num
            saved = False
            print(line)
            continue

        if line.strip() != '':
            print(line)
            
            # Fetch link to song and print
            song, artist = re.match('^\"(.+)\" by (.+)$', line).groups()
            # print(get_link(song, artist))

            # Get user input for how to edit file
            choice = ''
            while choice.strip().upper() not in ('D', 'K', 'EXIT'):
                choice = force_prompt('(D)elete or (K)eep? ')
            print()

            choice = choice.strip().upper()

            if choice == 'EXIT':
                restore = True
                raise fragile.Break

            if choice == 'K':
                if not firstWrite and not saved:
                    songs.write('\n')
                    songs.write(lines[sessionIndex])
                    firstWrite = False
                elif not saved:
                    songs.write(lines[sessionIndex])

                saved = True
                songs.write(line)
                
if restore:
    restore_rest()