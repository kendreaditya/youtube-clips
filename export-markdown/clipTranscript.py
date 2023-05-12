import argparse
from utils import Clip, Video

def extract_clip_id(url):
    return url.split('/')[-1]

def main():
    parser = argparse.ArgumentParser(description="YouTube Clip Transcript Downloader")
    parser.add_argument("urls", metavar="URL", type=str, nargs="+", help="YouTube clip URLs")
    args = parser.parse_args()

    video_id_clips = {}
    for url in args.urls:
        clip_id = extract_clip_id(url)
        clip = Clip(clip_id)

        if clip.video_id not in video_id_clips:
            video_id_clips[clip.video_id] = [clip]
        else:
            video_id_clips[clip.video_id].append(clip)

    videos = []        
    for video_id in video_id_clips:
        video_name = video_id_clips[video_id][0].video_name
        video = Video(video_id=video_id,
                      video_name=video_name,
                      clips=video_id_clips[video_id])
        successful = video.compile_clips()
        if successful:
            video.render_markdown(directory='./../')
            videos.append(video)
        else:
            print(f"Could not find transcript for {video_name}")

    print("Transcripts downloaded and compiled successfully!")

if __name__ == "__main__":
    main()