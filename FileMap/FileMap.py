import os
import json
from easydict import EasyDict as edict

# Recursively creates a file map of EasyDict(s) in a tree hierarchy which ...
#       maps the file/folder structure with root as 'path' (input arg).
# Files in the dir become dict keys whose value is None; ...
#       Directories become dict keys whose value is another dict which maps that directory (... and so on, recursively).
print(os.getcwd())
def fmap(path):
    l = sorted(os.listdir(path))
    e = edict()
    for item in l:
        full_path = os.path.join(path, item)
        if(os.path.isdir(full_path)):
            try:
                childMap = fmap(full_path)      # Recursively run fmap for the directory.
                item = modifyForDotSyntax(item)
                e[item] = childMap
            except PermissionError:             # Encountered with 'System Volume Information' folder.
                pass                            # Do not add this directory at all to it's parent's dict.

        else:
            item = modifyForDotSyntax(item, directory=False)
            e[item] = None;
    return e

# To make dot notation of the EasyDict feasible, we need to ensure some special characters don't appear.
#       For eg, if the filename itself contained a '.', then EasyDict style dot notation won't work.
# '.' is allowed for filenames but not directory names.
def modifyForDotSyntax(s, directory=True):
    s = s.replace(' ', '_')
    # remove_chars = ['(', ')', '.', '-', '/', '\\', '+', '*', '&', '!', '@', '#', '$', '%', '=']
    # trans_table = str.maketrans('', '', ''.join(remove_chars))       # This is the syntax for translation
    # s = s.translate(trans_table)                                     # str.translate replaces unicode points using the map given.
    if(directory is True):
        letBe = ['_']
    else:
        letBe = ['_', '.']
    tempList = [ch if(ch.isalnum() is True or ch in letBe) else '' for ch in s]
    s = ''.join(tempList)   # Concatenates all strings in the list.
    return s

# Saves using json.dump(). File extension is added, if not already part of the name.
def save(myFMap, filename, verbose=True):
    if(filename[-5:].lower() != '.json'):
        filename = filename + '.json'
    with open(filename, 'w') as f:
        json.dump(myFMap, f)
    if(verbose is True):
        print('Saved the map to', filename)    

# File containing a JSON is loaded using json.load().
# The loaded object is a dict, which is then converted to EasyDict.    
def load(filename, verbose=False):
    if(filename[-5:].lower() != '.json'):
        filename = filename + '.json'
    with open(filename, "r") as f:
        data = json.load(f) 
    myFmap = edict(data)
    if(verbose is True):
        print("Loaded the map from", filename)
    return myFmap