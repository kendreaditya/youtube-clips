import argparse
import requests
import json
import subprocess
import os
import re
from dataclasses import dataclass
from utils import Clip, Video

def download_audio_clip(clip, output_path):
    start_time = round(clip.start / 1000, 3)
    start_stamp = f"{int(start_time // 60)}:{round(start_time % 60, 2)}"
    end_time = round(clip.end / 1000, 3)
    end_stamp = f"{int(end_time // 60)}:{round(end_time % 60, 2)}"
    url = f"https://www.youtube.com/watch?v={clip.video_id}"
   
    # yt-dlp "https://www.youtube.com/watch?v=eOG-3VGq_5o&list=PLh_WzkOWyxbdbIwzussObo8Cum1A_iF9s&index=21" --output "sb-1.1.1.%(ext)s" --audio-quality 0 --extract-audio 
    # --audio-format mp3 --postprocessor-args "-ss 3:41 -to 4:31"
    args = [
        'yt-dlp',
        url,
        '-o', output_path,
        '--audio-quality', '0',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--postprocessor-args', f'-ss {start_stamp} -to {end_stamp}',
    ]

    subprocess.run(args, check=True)
   

def extract_clip_id(url):
    return url.split('/')[-1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Clip Audio Downloader")
    parser.add_argument("directory", metavar="directory", type=str, help="Directory to save audio clips", default=".")
    parser.add_argument("urls", metavar="URL", type=str, nargs="+", help="YouTube clip URLs")
    args = parser.parse_args()

    video_id_clips = {}
    for url in args.urls:
        clip_id = extract_clip_id(url)
        try:
            clip = Clip(clip_id)
        except Exception as e:
            print(f"Could not find clip with ID {clip_id}: {str(e)}")
            continue

        if clip.video_id not in video_id_clips:
            video_id_clips[clip.video_id] = [clip]
        else:
            video_id_clips[clip.video_id].append(clip)

    for video_id in video_id_clips:
        for clip in video_id_clips[video_id]:
            clip_audio_filename = re.sub(r'[^\w\d-]', '_', clip.clip_name) + '.mp3'
            # clip_audio_path = os.path.join(args.directory, clip_audio_filename)
            download_audio_clip(clip, clip_audio_filename)
            print(f"Downloaded audio clip: {clip.clip_name} to {clip_audio_filename}")
