import os
import re
import fnmatch
import glob
import sys
import shutil

def findfiles(which, where='.'):
    '''Returns list of filenames from `where` path matched by 'which'
       shell pattern. Matching is case-insensitive.'''

    # TODO: recursive param with walk() filtering
    rule = re.compile(fnmatch.translate(which), re.IGNORECASE)
    return [name for name in os.listdir(where) if rule.match(name)]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python NieRAutomata.Ver1.1a.py <torrent_destination> <file_name>")
        sys.exit(1)

    torrent_destination = sys.argv[1]
    file_name = sys.argv[2]

    full_path = os.path.join(torrent_destination, file_name)
    if not os.path.isdir(full_path):
        print(f"{full_path} is not a valid directory")
        sys.exit(1)

    escaped_full_path = full_path.replace('[', '[[').replace(']', ']*')
    filtered_search = f"{os.path.basename(__file__).lower().rsplit('.', 1)[0]}"
    #print(filtered_search)
    for file in findfiles(f"{filtered_search}*", full_path):
        source = os.path.join(full_path, file)
        print(f"{source}")
        serie_destination = os.path.join(torrent_destination, "NieR Automata Ver1.1a")
        shutil.copy(source, serie_destination)
        print(f"{file_name} has been copied to {serie_destination}")
        #shutil.rmtree(full_path)

    #print(f"{file_name.lower()} not found in {full_path}")
    #sys.exit(1)
