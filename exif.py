import exifread
import os
import pickle

ROOTDIR = '/bigdrive/Photos/wedding sort/uniq'

def tags(file):
    with open(file, 'rb')   as f:
        return exifread.process_file(f)

all_tags = {}
for subdir, dirs, files in os.walk(ROOTDIR):
    for file in files:
        path = os.path.join(subdir, file)
        if '1424' in path:
            print("!!!!", path)
        all_tags[path] = tags(path)

with open('tags.pkl', 'wb') as tfile:
# Pickle the list using the highest protocol available.
    pickle.dump(all_tags, tfile, -1)
