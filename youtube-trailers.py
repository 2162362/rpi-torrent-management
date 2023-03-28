# import required module
import os
import youtube_dl
import shutil
from googlesearch import search
from pytube import YouTube, Search

# assign directory
directory = '/mnt/mitsai/torrents/movies'

# functions
def search_trailer_google(text):
	# to search
	query = 'youtube official trailer ' + text
	for google_result in search(query, tld="com", num=1, stop=1, pause=2):
		return google_result

def search_trailer_pytube(text):
	# to search
	query = 'official trailer ' + text

	s = Search(query)
	for v in s.results:
  		return v.watch_url

def download_video_youtubedl(folder, url):
	filename = directory + '/' + folder + '/' + folder + '-trailer.mp4'
	cmd = 'youtube-dl -f bestvideo+bestaudio --output "' + filename + '" "' + url + '"'
	os.system(cmd)

def download_video_pytube(folder, url):
	filename = directory + '/' + folder + '/' + folder + '-trailer.mp4'
	yt = YouTube(url)
	yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(filename=filename)
	#shutil.copyfile(yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].default_filename, filename)
	#os.remove(yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].default_filename)

print('=>> G E T   T R A I L E R S <<=')
print('=>> Processing...')

# iterate over files in
# that directory
for entry in os.scandir(directory):
	if entry.is_dir():
		hasTrailer=0
		for folder_file in os.scandir(directory + '/' + entry.name):
			if folder_file.name.endswith('trailer.mp4'):
				hasTrailer=1
				break
		if hasTrailer == 0:
			#videoLink = search_trailer_google(entry.name) #use google
			videoLink = search_trailer_pytube(entry.name) #use youtube

			#download_video_youtubedl(entry.name, videoLink) #use plugin - support best quality
			download_video_pytube(entry.name, videoLink) #use youtube

			print('| +++')
			print('| ' + entry.name)
			print('| ' + videoLink)

print('=>> Done!')
