#!/bin/bash

file_type=$1
file_source=$2
file_name=$3

if [ "$file_type" == "Movies" ]; then
    python /home/pi/opensubtitles.py "$file_name" "$file_source"
    #python /home/pi/youtube-trailers.py
fi

python /home/pi/manage_torrent.py "$file_type" "$file_source" "$file_name"
