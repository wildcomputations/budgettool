"""Functions to load a save a dictionary as a json file.
The intent is to create an API that can support other file formats
if/when needed.
"""

import json

def to_string(data):
    return json.dumps(data, sort_keys=True, indent=4)

def load(filename):
    with open(filename) as jfile:
        data = json.load(jfile)
    assert(data['filetype']=='budgettool')
    data['filename'] = filename
    return data

def save(data, filename=None, backup=False):
    """TODO:
    - optionally create backup file
    - experiment with collections.OrderedDict()
    """
    filename2 = data.pop('filename', None)
    if filename is None:
        filename = filename2
    with open(filename, 'w') as jfile:
        jfile.write(to_string(data))
