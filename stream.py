import os
import numpy as np
import urllib
import m3u8
import streamlink
import subprocess
import yt_dlp
import re
from extractor import get_text_frame_cv2, get_rgb, get_game_type
from datetime import datetime, timedelta
from tqdm import tqdm_notebook as tqdm
import cv2


class Stream():
    def get_stream(self, url):
        """
        Get upload chunk ur
        """
        streams = streamlink.streams(url)
        stream_url = streams["best"]

        m3u8_obj = m3u8.load(stream_url.args['url'])
        return m3u8_obj.segments[0]


    def get_stream_best_url(self, url):
        streams = streamlink.streams(url)
        stream_url = streams["best"]
        return stream_url



class FrameExtractor():
    def __init__(self, url) -> None:
        self.url = url
        self.ydl_opts = { 
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s', # You can change the PATH as you want
        'download_archive': 'downloaded.txt',
        'noplaylist': True,   
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # 'progress_hooks': [hook]
        }


    def __stream_extractor(self, url):
        stream = Stream()
        best_url = stream.get_stream_best_url(url)

        # m3u8_obj = m3u8.load(best_url.args['url']) load m3u8
        # capture = cv2.VideoCapture(best_url.args["url"])
        capture = cv2.VideoCapture("./videos/output.mp4")
        while True:
            is_read, frame = capture.read()
            if not is_read:
                break
            
            # cut
            frame = frame[849:1030]
            # resize
            height, width, layers = frame.shape
            width = int((width / 100 ) * 30)
            height = int((height / 100 ) * 30)
            frame = cv2.resize(frame, (width, height))
            
            rgb = get_rgb(frame)
            game_type = get_game_type(rgb)
            if(game_type):
                text = get_text_frame_cv2(frame)
                string = re.sub("[^0-9]", "", text)
                print("filtado: " + string + "\noriginal: " + text)
            cv2.imwrite(os.path.join(f"./video-opencv/", f"frame.jpg"), frame) # save file in some path


    def extractor(self):
        url = self.url
        info = self.info(url)
        is_live = info["is_live"]
        #if(is_live):
        self.__stream_extractor(url)
    

    def info(self, video_url, download=False):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
             return ydl.extract_info(video_url, download=download)


url = "https://www.youtube.com/watch?v=21X5lGlDOfg"
frame = FrameExtractor(url)
frame.extractor()