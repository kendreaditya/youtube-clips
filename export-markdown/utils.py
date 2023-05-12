import requests
import json
import subprocess
import os
import re
import io
from dataclasses import dataclass
import webvtt

@dataclass
class Clip:
    url: str
    clip_name: str
    video_name: str
    video_id: str
    start: int
    end: int
    transcript: str
    clip_id: str

    def __init__(self, clip_id):
        self.url = f"https://www.youtube.com/clip/{clip_id}"
        self.clip_id = clip_id
        clip_json = self.getJSONFromHTML(self.url)
        self.clip_name = self.getClipName(clip_json)
        self.video_name = self.getVideoName(clip_json)
        self.video_id = self.videoID(clip_json)
        self.timestamps = self.getTimestamps(clip_json)

    def getJSONFromHTML(self, url, opts = {}):
    # Get the HTML from the specified URL.
        response = requests.get(url, opts)

        # Check if the request was successful.
        if response.status_code != 200:
            raise Exception(f"Request to {url} failed with status code {response.status_code}")

        # Convert the response body to a string.
        html = response.content.decode("utf-8")

        # Get the JSON string from the HTML.
        jsonStr = html.split("var ytInitialData = ")[1].split(";")[0]

        # Decode the JSON string.
        j = json.loads(jsonStr)


        # Return the JSON object.
        return j

    def getTimestamps(self, clip_json):
        try:
            stamps = clip_json['engagementPanels'][1]['engagementPanelSectionListRenderer']['content']['clipSectionRenderer']['contents'][0]['clipAttributionRenderer']['onScrubExit']['commandExecutorCommand']['commands'][3]['openPopupAction']['popup']['notificationActionRenderer']['actionButton']['buttonRenderer']['command']['commandExecutorCommand']['commands'][1]['loopCommand']
        except:
            stamps = clip_json['engagementPanels'][2]['engagementPanelSectionListRenderer']['content']['clipSectionRenderer']['contents'][0]['clipAttributionRenderer']['onScrubExit']['commandExecutorCommand']['commands'][3]['openPopupAction']['popup']['notificationActionRenderer']['actionButton']['buttonRenderer']['command']['commandExecutorCommand']['commands'][1]['loopCommand']

        self.start = int(stamps['startTimeMs'])
        self.end = int(stamps['endTimeMs'])

    def getClipName(self, clip_json):
        try:
            return clip_json['engagementPanels'][1]['engagementPanelSectionListRenderer']['content']['clipSectionRenderer']['contents'][0]['clipAttributionRenderer']['title']['runs'][0]['text']
        except:
            return clip_json['engagementPanels'][2]['engagementPanelSectionListRenderer']['content']['clipSectionRenderer']['contents'][0]['clipAttributionRenderer']['title']['runs'][0]['text']

    def videoID(self, clip_json):
        return clip_json['currentVideoEndpoint']['watchEndpoint']['videoId']

    def getVideoName(self, clip_json):
        try:
            return clip_json['engagementPanels'][2]['engagementPanelSectionListRenderer']['content']['structuredDescriptionContentRenderer']['items'][0]['videoDescriptionHeaderRenderer']['title']['runs'][0]['text']
        except:
            return clip_json['playerOverlays']['playerOverlayRenderer']['videoDetails']['playerOverlayVideoDetailsRenderer']['title']['simpleText']

@dataclass
class Video:
    url: str
    video_id: str
    video_name: str
    transcript_exists: bool
    clips: list
    transcript: str

    def __init__(self, video_id, video_name, clips=[]):
        self.video_id = video_id
        self.url = f"https://www.youtube.com/watch?v={self.video_id}"
        self.video_name = video_name
        self.clips = clips
        self.transcript_exists = False
    
    def compile_clips(self):
        try: 
            self.download_transcript(self.video_id)
            self.get_clip_transcripts()
            return True
        except:
            return False
    
    def download_transcript(self, video_id):
        args = ['yt-dlp', '--write-subs', '--write-auto-subs', '--sub-langs=en', '--embed-subs', '--skip-download', '--sub-format', 'vtt', '-o', f"{video_id}", self.url]
        output = str(subprocess.check_output(args))
        file_name = output.split('Destination: ')[-1].split('\\n\\r[download]')[0]
        self.transcript = webvtt.read(file_name)
        os.remove(file_name)
        self.transcript_exists = True
    
    def get_clip_transcripts(self):
        for clip in self.clips:
            clip.transcript = self.get_clip_transcript(clip)

    def time_to_seconds(self, time):
        parts = time.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    
    def get_clip_transcript(self, clip):
        transcript = set()

        start_seconds = clip.start/1000
        end_seconds = clip.end/1000

        for caption in self.transcript:
            caption_start = self.time_to_seconds(caption.start)
            caption_end = self.time_to_seconds(caption.end)

            if start_seconds <= caption_start <= end_seconds or start_seconds <= caption_end <= end_seconds:
                transcript.add(caption.text.strip())

        return ' '.join(transcript).replace('\n', ' ').strip()

    def render_markdown(self, directory=None):
        safe_file_name = re.sub(r'[^\w\d-]', '_', self.video_name)
        file_name = f"{safe_file_name}.md" if directory is None else os.path.join(directory, f"{safe_file_name}.md")

        with open(file_name, 'w') as f:
            f.write(f"# {self.video_name}\n\n")
            f.write(f"- [{self.video_name}]({self.url})\n\n")
            for clip in self.clips:
                f.write(f"\t- [{clip.clip_name}]({clip.url})\n")
                f.write(f"\t\t- {clip.transcript}\n\n")