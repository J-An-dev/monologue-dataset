import face_recognition
import cv2
import os
from os.path import isfile
import sys
from subprocess import call
from face_timestamp import face_timestamp

def list_files(data_path,file_type):
	l=[]
	for root, dirs, files in os.walk(data_path):
		for file in files:
			if isfile(os.path.join(root, file)) and file_type in file:
				l.append(os.path.join(root, file))
	return l

files_list = list_files(data_path='../videos/obama/',file_type='.mkv')
files_list = [l.replace('.mkv','') for l in files_list if isfile(l)]


for i,file in enumerate(files_list):
	sys.stdout.write('{}/{}\r'.format(i+1,len(files_list)))
	sys.stdout.flush()
	file_name = file.split("/")[-1]
	output_path = '../videos/obama_crop/' + file_name

	out_w, out_h, x, y, ss, t = face_timestamp(file+'.mkv')

	# split video into several clips to remove unrelated intervals
	for i in range(len(ss)):
		k = "%02d" % i
		call('ffmpeg -y -i "%s" -ss "%s" -to "%s" -qscale 0 -avoid_negative_ts 1 "%s"' % (file+'.mkv', ss[i], t[i], output_path+'-'+k+'.mp4'), shell=True)

	# crop frames around speaker's face
	for j in range(len(ss)):
		k = "%02d" % j
		call('ffmpeg -i "%s" -filter:v  "crop="%s":"%s":"%s":"%s",scale=112:112" -qscale 0 "%s" -y' % (output_path + '-' + k + '.mp4', out_w[j], out_h[j], x[j], y[j], output_path + '_' + k + '.mp4'),shell=True)

	# create the video clips file-path list
	call('for f in ../videos/obama_crop/"%s"_*.mp4; do echo "file "$f"" >> ../videos/obama_crop/"%s"list.txt; done' % (file_name, file_name), shell=True)

	# merge clips into one video
	call('ffmpeg -f concat -safe 0 -i ../videos/obama_crop/"%s"list.txt -c copy ../videos/obama_done/"%s".mp4' % (file_name, file_name), shell=True)






