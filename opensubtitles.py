import fnmatch
import pathlib
import argparse
import os
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File

def download_subtitles(movie_name, extension, download_dir):
    ost = OpenSubtitles()
    f = File(os.path.join(download_dir, movie_name + extension))
    with open(os.path.join("/home", "pi","credentials.json")) as f:
        config = json.load(f)
    token = ost.login(config["subtitles_name"], config["subtitles_password"])
    languages = ['eng', 'por']
    for lang in languages:
        data = ost.search_subtitles([{'sublanguageid': lang, 'moviehash': f.get_hash()}])
        if len(data) == 0:
            data = ost.search_subtitles([{'sublanguageid': lang, 'query': movie_name}])

        if len(data) > 0:
            id_subtitle_file = data[0].get('IDSubtitleFile')
            id_iso639 = data[0].get('ISO639')
            response = ost.download_subtitles([id_subtitle_file], override_filenames={id_subtitle_file: f"{movie_name}.{id_iso639}.srt"}, output_directory=download_dir, extension='srt')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download subtitles from OpenSubtitles API')
    parser.add_argument('movie_name', type=str, help='Name of the movie to download subtitles for')
    parser.add_argument('download_dir', type=str, help='Directory to save the downloaded subtitles')
    args = parser.parse_args()

    movie_name = ''
    extension = ''
    for file in os.listdir(args.download_dir):
        if fnmatch.fnmatch(file, args.movie_name + '.*'):
            movie_name = file
            extension = pathlib.Path(file).suffixes[-1]

    download_subtitles(args.movie_name, extension, args.download_dir)
