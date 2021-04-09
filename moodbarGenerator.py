#!/usr/bin/env python3
# coding: utf-8
import os
from hashlib import md5
from os.path import join
from shlex import quote


# Getting the variables from the environment variables
MOOD_OUTPUT_FOLDER = os.environ['MOOD_OUTPUT_FOLDER']
LIBRARY_FOLDER = os.environ['LIBRARY_FOLDER']
METADATA_OUTPUT_FOLDER = os.environ['METADATA_FOLDER']


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
    for root, _, files in os.walk(LIBRARY_FOLDER):
        for name in files:
            if name.endswith('mp3') or name.endswith('flac'):
                processFile(join(root, name))


# Process a file to generate the moodbar.
def processFile(filePath):
    # Generating the MD5 of the file and the moodbar path.
    md5Filename = md5(filePath.encode('ascii', 'ignore')).hexdigest()
    # .rawmood is basically a txt file with an array of width * 3, for each RGB sample value
    metadataPathSmall = join(METADATA_OUTPUT_FOLDER, 'ld', '{}.rawmood'.format(md5Filename))
    metadataPathNormal = join(METADATA_OUTPUT_FOLDER, 'std', '{}.rawmood'.format(md5Filename))
    metadataPathLarge = join(METADATA_OUTPUT_FOLDER, 'hd', '{}.rawmood'.format(md5Filename))
    # Check if the moodbar was generated previously
    if os.path.exists(metadataPathNormal):
        return
    # Launching the moodbar rendering for low definition, standard definition and high definition
    os.system(
        'python3 moodtool.py -i {} -o {} -w {} -s'.format(quote(filePath), metadataPathSmall, 500))
    os.system(
        'python3 moodtool.py -i {} -o {} -w {} -s'.format(quote(filePath), metadataPathNormal, 1000))
    os.system(
        'python3 moodtool.py -i {} -o {} -w {} -s'.format(quote(filePath), metadataPathLarge, 2000))


if __name__ == '__main__':
    genMoodbars()
