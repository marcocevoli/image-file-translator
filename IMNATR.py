#! python3
# IMNATR.py - Copies and renames image files after translating them

import shutil
import os
import pyinputplus as pyip
from pathlib import Path
from googletrans import Translator

translator = Translator()

# Define languages to choose from. 

langs = ['ca', 'en', 'es', 'it']

# Ask for source language using langs list

print('\n1) What is the source language?')
source_language = pyip.inputMenu(langs, numbered=True)

langs.remove(source_language) #removes source language from target languages list

# Ask for target language using langs list minus source language

print('\n2) What is the target language?')

target_language = pyip.inputMenu(langs, numbered=True)

# TODO - Create an interface or filtered choice for the user to input a path

user_path = pyip.inputFilepath('\n3) What is the main folder?\n', mustExist=True) #checks that path exists

# Check if directory is empty

if len(os.listdir(user_path)) == 0:
        print('There are no files in this directory.')

# Change current working directory to user path

os.chdir(user_path)

count = 0
for foldername, subfolders, filenames in os.walk(user_path):
    print(f'Checking files in {foldername}...')
# Loops all files in a folder
    for filename in filenames:

# Translate the file name only if it's an image file and it has a suffix = source language (i.e. "gatto.it.jpg")

            if Path(filename).suffixes[0] == '.' + source_language and Path(filename).suffix in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    to_trans = Path(filename).stem.split('.')[0]

# If there are dashes in the file name, replace them with spaces

                    if "-" in to_trans:
                            to_trans = to_trans.replace("-", " ")

# Translate with googletrans

                    translation = translator.translate(to_trans, src=source_language, dest=target_language)

# Assemble target file name, replacing back spaces to dashes and adding the correct suffix (ie. "cat.en.jpg")

                    translated_file = translation.text.replace(" ", "-") + "." + target_language + Path(filename).suffix

# TODO: sostituire i caratteri non ascii con i corrispondenti caratteri ascii
                    if "’" in translated_file:
                            translated_file = translated_file.replace("’", "-")

# Create the full path of translated file

                    full_path = os.path.join(Path(foldername), translated_file)
                    
# Debugging with "print"
                   # print(str(full_path))
                   # print(str(translated_file))

# Doesn't copy the file if it already exists

                    if os.path.exists(full_path) is False:
                            count += 1
                            shutil.copy(os.path.join(Path(foldername), filename), full_path) # Copy the image file(s) with shutil
                            print(count,')', filename,' => ',translated_file)
                            # TODO: crea glossario - glossary_file = os.path.join(Path(user_path),source_language + '_' + target_language + '.txt')
                            
                    else:
                            print('>>> The file %s already exists.\n' % translated_file)

print('\nTotal number of image files translated: %d' % count)
