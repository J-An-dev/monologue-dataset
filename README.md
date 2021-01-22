# Monologue Dataset w/ Face Centered

## Introduction
This repository is a monologue dataset inherited from the [speech2gesture dataset](https://github.com/amirbar/speech2gesture/blob/master/data/dataset.md) with further video 
processing. The main modifications include: (i) adding an extra speaker dataset retrieved from the 44th U.S. President Barack Obama's weekly address videos; 
(ii) cropping video frames around speakers’ face and removing unrelated intervals to achieve a clean version.

## Prerequisites for Video Download and Processing
- Video Download:
    1. OpenCV
    2. youtube-dl
    3. pandas
    4. tqdm
    5. argparse
    6. subprocess
    7. numpy
    8. shutil
    9. ffmpeg
- Video Processing:
    1. [face_recognition](https://github.com/ageitgey/face_recognition)
    2. OpenCV
    3. numpy
    4. subprocess
    5. ffmpeg

## Video Download
### CSV video links files
For each speaker, there is a separate CSV file that documents the video titles and Download links on YouTube. Those CSV file could be easily generated using 
the Python program [get_youtube_links.py](./video_download/get_youtube_links.py). In the program, I am using retrieving Obama's videos as the example by calling 
the YouTube API to search all the videos in the channel [The Obama White House](https://www.youtube.com/obamawhitehouse) that contain the keyword `weekly` in the titles. 
For more details about how to implement the YouTube API, please reference to the [developer document](https://developers.google.com/youtube/v3/getting-started).

### Download speaker original videos
To download the speaker videos from YouTube. Use the following script:
```
python -m video_download.download_youtube --base_path </path/to/dataset base folder> --speaker <speaker_name>
```
For example, to download Obama's videos:
```
python -m video_download.download_youtube --base_path ./videos --speaker obama
```
which would download all the videos documented in the file [videos_links_obama.csv](./video_download/videos_links_obama.csv) and store them under the folder `./videos/obama`. 
All the videos would be saved as `.mkv` format in 25fps.

## Video Processing
For each video, video processing include two parts:

1. [face_timestamp.py](./video_processing/face_timestamp.py) program analyses frames in one video for every 3 seconds and returns the start & end timestamp for each 
face-contained interval along with the face top-left corner coordinates and cropping window size. One thing need to stress is that each interval is trimmed base on the following strategy:
    - The program starts analyzing each video from the first frame
    - The face recognition would not start until find the first non-empty frame
    - The first interval's start timestamp records the frame that initially recognize the speaker's face in the video
    - The end timestamp for each interval is determined by following criteria:
        1. Cannot find the speaker's face in the current frame, or
        2. The difference between the face's coordinates in the current frame and in the start timestamp frame is larger than the threshold.
        
        *Note: For the first criterion, it would not save the start timestamp for the next interval until the program finds the next frame that contains the speaker's face. However, for the second criterion, it would save the start timestamp for the next interval, which is equal to the end timestamp for the current interval, at the same time.*

2. [crop_merge.py](video_processing/crop_merge.py) program reads though all the videos for one speaker. And for each video it calls the program [face_timestamp.py](./video_processing/face_timestamp.py) and uses those returned information for video cropping and merging:
    1. Split the video into several intervals according to the start & end timestamp of each interval, and name them in order and saved them separately under the folder `./videos/<speaker_name>_crop` like `./videos/obama_crop`.
    2. For each interval, crop frames around speaker's face according to the face's coordinates and window size, and overwrite the original interval.
    3. Merge all those intervals above into one video and save it under the folder `./videos/<speaker_name>_done` like `./videos/obama_done`.

        *Note: To merge intervals into one video, need to first create a list which documents the file path of each interval in order.*


## Sample Result
Here is the sample for a processed video which is centered around the speaker's face with unrelated intervals removed:

<p align="center">
  <img src="./sample.gif">
</p>

To watch the sample video and compare with the original one, please click the link: https://youtu.be/qINF7DoQCek.


