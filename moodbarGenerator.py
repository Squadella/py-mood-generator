#!/usr/bin/env python3
# coding: utf-8
import os
from hashlib import md5
from shlex import quote
from os.path import join

# Getting the variables from the environment variables
MOOD_OUTPUT_FOLDER = os.environ['MOOD_OUTPUT_FOLDER']
LIBRARY_FOLDER = os.environ['LIBRARY_FOLDER']


# Generates the moodbars for all the files in a folder.
def genMoodbars():
    for root, _, files in os.walk(LIBRARY_FOLDER):
        for name in files:
            if name.endswith('mp3') or name.endswith('flac'):
                processFile(join(root, name))


# Process a file to generate the moodbar.
def processFile(filePath):
    # Generating the MD5 of the file and the moodbar path.
    filename_md5 = md5(filePath.encode("ascii", "ignore")).hexdigest()
    moodbarPath = join(MOOD_OUTPUT_FOLDER, '{}.mood'.format(filename_md5))
    # Check if the moodbar was generated previously
    if os.path.exists(moodbarPath):
        return
    # Launching the moodbar rendering
    os.system('python3 moodtool.py {} {}'.format(quote(filePath), quote(moodbarPath)))


if __name__ == '__main__':
    genMoodbars()