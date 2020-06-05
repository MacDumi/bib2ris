#!/usr/bin/env python3
import sys, os
from pybtex.database.input import bibtex

item_type ={'article' : 'JOUR',
            'inpress' : 'INPR',
            'book'    : 'BOOK',
            'misc'    : 'ELEC'}

keys = {'year'      : 'PY',
        'url'       : 'UR',
        'number'    : 'M1',
        'title'     : 'TI',
        'volume'    : 'VL',
        'doi'       : 'DO',
        'publisher' : 'PB',
        'journal'   : 'JO',
        'year'      : 'PY',
        'start_page': 'SP',
        'end_page'  : 'EP',
        'address'   : 'PP',
        'note'      : 'N1'}

# Path to the bibtex file
bib_file = sys.argv[1]
# Create a parser
parser = bibtex.Parser()
# Load the bibtex file
data = parser.parse_file('ads.bib')

# Create a dictionary holding all the entries
library = {}
for label, entry in data.entries.items():
    item = {}
    item['type'] = entry.type
    authors = []
    if len(entry.persons):
        for person in entry.persons.items()[0][1]:
            first_name = ' '.join(person.first_names)
            last_name  = ' '.join(person.last_names)
            authors.append(', '.join([last_name, first_name]))
        item['authors'] = authors
    item['data'] = {}
    for key, content in entry.fields.items():
        if key == 'pages':
            pages = content.split('--')
            if len(pages) > 1:
                item['data']['start_page'], item['data']['end_page'] = pages
            else:
                item['data']['start_page'] = pages[0]
        else:
            item['data'][key] = content
    library[label] = item

# Convert the library with bibtex data to ris
ris = ''
for key, item in library.items():
    entry  = ''
    type_ = item_type[item['type']]
    entry += f'TY - {type_}\n'
    if 'authors' in item:
        for author in item['authors']:
            entry += f'AU - {author}\n'
    for chunk, data  in item['data'].items():
        temp = keys[chunk]
        entry += f'{temp} - {data}\n'
    entry += 'ER -\n'
    ris += entry

# Save to file
new_name = f'{os.path.splitext(bib_file)[0]}.ris'
with open(new_name, 'w') as f:
    f.writelines(ris)
print("All done")





