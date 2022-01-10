# Import the required module for text
# to speech conversion
from gtts import gTTS

# This module is imported so that we can 
# play the converted audio
from os import system, chdir
from os.path import expanduser, isdir


# TODO: create functions and test with the rest of the program
# TODO: make sure that the rPi version of os.system("xxxx") is used

homedir = expanduser("~")
vlc_path = "C:\\Program Files (x86)\\VideoLAN\\VLC"

# The text that you want to convert to audio
mytext = "Water Laterals"

# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine
# here. slow=False tells
# the module that the converted audio should 
# speak at a normal speed
myobj = gTTS(text=mytext, lang=language, slow=False)

# Saving the converted audio in a mp3 file
fname = "wLat.mp3"
# saves to PWD
myobj.save(fname)

# Playing the converted file

# first try vlc
try:
    if isdir(vlc_path):
        chdir(vlc_path)
        system("vlc .\\{}".format(fname))
    else:
        raise FileNotFoundError("VLC does not seem to be installed, falling back to default")
except FileNotFoundError as e:
    print(e)
    # if vlc doesnt work, try using the default player
    try:
        system(".\\{}".format(fname))
    except OSError as e:
        print(e)
        system("pause")
        exit(1)
