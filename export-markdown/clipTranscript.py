import argparse
from utils import Clip, Video

def extract_clip_id(url):
    return url.split('/')[-1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Clip Transcript Downloader")
    parser.add_argument("directory", metavar="directory", type=str, help="YouTube clip URLs")
    parser.add_argument("urls", metavar="URL", type=str, nargs="+", help="YouTube clip URLs")
    args = parser.parse_args()

    video_id_clips = {}
    for url in args.urls:
        clip_id = extract_clip_id(url)
        try:
            clip = Clip(clip_id)
        except:
            print(f"Could not find clip with ID {clip_id}")
            continue

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
        video.render_markdown("./", transcript_exists=successful)
        # video.render_markdown(directory=args.directory, transcript_exists=successful)
        videos.append(video)

        if not successful:
            print(f"Could not find transcript for {video_name}, but added to markdown with title.")

    print("Transcripts downloaded and compiled successfully!")