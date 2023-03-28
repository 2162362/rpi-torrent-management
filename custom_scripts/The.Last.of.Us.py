import os
import glob
import sys
import shutil

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python The.Last.of.Us.py <destination> <file_name>")
        sys.exit(1)

    torrent_destination = sys.argv[1]
    file_name = sys.argv[2]

    full_path = os.path.join(torrent_destination, file_name)
    if not os.path.isdir(full_path):
        print(f"{full_path} is not a valid directory")
        sys.exit(1)

    for file in glob.glob(f"{full_path}/{file_name}*"):
        source = os.path.join(full_path, file)
        print(f"{source}")
        serie_destination = os.path.join(torrent_destination, "The Last of Us", "Season 1")
        shutil.copy(source, serie_destination)
        print(f"{file_name} has been copied to {serie_destination}")
        sys.exit(0)

    #print(f"{file_name} not found in {full_path}")
    #sys.exit(1)
