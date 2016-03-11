import pprint, pickle
from collections import Counter

wanted_tags = [
'EXIF ExifVersion',
'Image Make',
'Image Model'
]

c = Counter()
s = Counter()

with open('tags.pkl', 'rb') as pkl_file:
    tags = pickle.load(pkl_file)
    for tag in tags.values():
        c.update(tag.keys())
        try:
            id = ', '.join(sorted([tag['EXIF ExifImageWidth'].printable, tag['EXIF ExifImageLength'].printable]))+', '
        except KeyError:
            id = ''
        for key in wanted_tags:
            try:
                id += tag[key].printable+', '
            except KeyError:
                id += '!, '
        s.update([id])

pprint.pprint(c.most_common(50))
pprint.pprint(s.most_common(50))


