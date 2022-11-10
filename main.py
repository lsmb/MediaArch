#!/bin/python3

import clipboard
import subprocess
import os
import sys

confLoc = os.path.dirname(os.path.realpath(__file__)) + '/gdl.conf'
destDir = '~/Pictures/PicArch/'
blink = clipboard.paste()
subdir = sys.argv[1]

def runGalleryDL(subfolder, link):
    try:
        sp = subprocess.run(['gallery-dl', '-c', confLoc, '--verbose', '-d', destDir + subfolder, link], check=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with open('output.log', 'a') as file:
            file.write(sp.stdout)
            if '✔ ' in sp.stdout:
                notify('Saved!', f'{subfolder}: {blink}')
            else:
                notify('Save failed!', f'{subfolder}: {blink}')
        with open('error.log', 'a') as file:
            file.write(sp.stderr)
    except:
        print("Stuff failed!")
        print("Unexpected error:", sys.exc_info()[0])
        notify("Error!", f'{subfolder}: {blink}')



def notify(header, message):
    subprocess.run(['notify-send', header, message])

def yt_dlp(subfolder, link):
    try:
        sp = subprocess.run(['yt-dlp', '-o', destDir + subfolder + '/%(id)s - %(title)s.%(ext)s', link], check=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(sp.stderr)
        print(sp.stdout)
        if '100% of' in sp.stdout:
            notify('Saved!', f'{subfolder}: {blink}')
        else:
            notify('Save failed!', f'{subfolder}: {blink}')
    except:
        print("Stuff failed!")
        print("Unexpected error:", sys.exc_info()[0])
        notify("Error!", f'{subfolder}: {blink}')

yt_sites = ['streamable.com', 'clips.twitch.tv', 'v.redd.it', 'youtube.com']


if __name__ == "__main__":
    if any(x in blink for x in yt_sites):
        yt_dlp(subdir, blink)
    else:
        runGalleryDL(subdir, blink)
