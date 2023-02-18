import os
import numpy as np
import urllib
import m3u8
import streamlink
import subprocess
from extractor import get_text_frame_cv2, get_rgb
from datetime import datetime, timedelta
from tqdm import tqdm_notebook as tqdm
import cv2


SAVING_FRAMES_PER_SECOND = 10

def get_stream(url):
    """
    Get upload chunk ur
    """
    streams = streamlink.streams(url)
    stream_url = streams["best"]

    m3u8_obj = m3u8.load(stream_url.args['url'])
    return m3u8_obj.segments[0]


def get_stream_best_url(url):
    streams = streamlink.streams(url)
    stream_url = streams["best"]
    return stream_url


def dl_stream(url, filename, chunks):
    """
    Download each chunks
    """
    pre_time_stamp = 0
    for i in range(chunks+1):
        stream_segment = get_stream(url)
        cur_time_stamp = \
            stream_segment.program_date_time.strftime("%Y%m%d-%H%M%S")

        if pre_time_stamp == cur_time_stamp:
            pass
        else:
            file = open(filename + '.ts', 'ab+')
            with urllib.request.urlopen(stream_segment.uri) as response:
                html = response.read()
                file.write(html)
            pre_time_stamp = cur_time_stamp


def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05) 
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return (result + ".00").replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s


def image_frame_mp4(video_file):
    filename, _ = os.path.splitext(video_file)
    filename += "-opencv"
    # make a folder by the name of the video file
    if not os.path.isdir(filename):
        os.mkdir(filename)
    # read the video file    
    cap = cv2.VideoCapture(video_file)
    # get the FPS of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    # get the list of duration spots to save
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
    # start the loop
    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            # break out of the loop if there are no frames to read
            break
        # get the duration by dividing the frame count by the FPS
        frame_duration = count / fps
        try:
            # get the earliest duration to save
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # the list is empty, all duration frames were saved
            break
        if frame_duration >= closest_duration:
            # if closest duration is less than or equals the frame duration, 
            # then save the frame
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}.jpg"), frame) 
            # drop the duration spot from the list, since this duration spot is already saved
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # increment the frame count
        count += 1


url = "https://www.youtube.com/watch?v=JeMc34IHvfw"
# dl_stream(url,"file", 10) # 30s
# subprocess.run(['ffmpeg', '-i', 'file.ts', 'video.mp4', '-y']) # convert from mp4
# image_frame_mp4("video.mp4")
best_url = get_stream_best_url(url)

#m3u8_obj = m3u8.load(best_url.args['url']) load m3u8
#capture = cv2.VideoCapture(best_url.args["url"])
capture = cv2.VideoCapture("./videos/cut.mp4")

c = 0
while True:
    c+=1
    is_read, frame = capture.read()
    if not is_read:
        break
    
    frame = frame[849:1030]
    rgb = get_rgb(frame)
    print(rgb)
    text = get_text_frame_cv2(frame)
    # só iremos analisar se a linha inferior que indica o tipo de sorteio for de acordo com a cor que queremos!
    print(text) 
    cv2.imwrite(os.path.join(f"./video-opencv/", f"frame.jpg"), frame) # save file in some path
