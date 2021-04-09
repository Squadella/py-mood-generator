#!/usr/bin/env python3
# coding: utf-8
import os
from hashlib import md5
from multiprocessing import Pool
from os.path import join
from shlex import quote
import time

# Getting the variables from the environment variables
MOOD_OUTPUT_FOLDER = os.environ['MOOD_OUTPUT_FOLDER']
LIBRARY_FOLDER = os.environ['LIBRARY_FOLDER']
METADATA_OUTPUT_FOLDER = os.environ['METADATA_FOLDER']


# Return the list of all the path of the songs.
def scanLibrary():
    for root, _, files in os.walk(LIBRARY_FOLDER):
        for name in files:
            if name.endswith('mp3') or name.endswith('flac'):
                yield join(root, name)


# Generates the moodbars for all the files in a folder.
def genMoodbars():
    # Creating the outputs folders.
    if not os.path.exists(join(METADATA_OUTPUT_FOLDER, 'ld')):
        os.mkdir(join(METADATA_OUTPUT_FOLDER, 'ld'))
    if not os.path.exists(join(METADATA_OUTPUT_FOLDER, 'std')):
        os.mkdir(join(METADATA_OUTPUT_FOLDER, 'std'))
    if not os.path.exists(join(METADATA_OUTPUT_FOLDER, 'hd')):
        os.mkdir(join(METADATA_OUTPUT_FOLDER, 'hd'))
    # Iterate over files to generates moodbar only for .mp3/.flac files
    processNumber = os.cpu_count() - 2

    with Pool(processes=processNumber) as p:
        p.map(processFile, scanLibrary())


# Process a file to generate the moodbar.
def processFile(filePath):
    # Generating the MD5 of the file and the moodbar path.
    md5Filename = md5(filePath.encode('ascii', 'ignore')).hexdigest()

    rawmoodFile = '{}.rawmood'.format(md5Filename)
    # .rawmood is basically a txt file with an array of width * 3, for each RGB sample value
    metadataPathSmall = join(METADATA_OUTPUT_FOLDER, 'ld', rawmoodFile)
    metadataPathNormal = join(METADATA_OUTPUT_FOLDER, 'std', rawmoodFile)
    metadataPathLarge = join(METADATA_OUTPUT_FOLDER, 'hd', rawmoodFile)
    # Check if the moodbar was generated previously
    if os.path.exists(metadataPathNormal):
        return

    command = 'python3 moodtool.py -i {} -o {} -w {} -s'
    # Launching the moodbar rendering for low definition, standard definition and high definition
    os.system(command.format(quote(filePath), metadataPathSmall, 500))
    os.system(command.format(quote(filePath), metadataPathNormal, 1000))
    os.system(command.format(quote(filePath), metadataPathLarge, 2000))


if __name__ == '__main__':
    while True:
        genMoodbars()
        time.sleep(3600)
