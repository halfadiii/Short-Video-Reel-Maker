import os
import csv
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip

def download_video(url):
    """Downloads video with audio and returns the file path."""
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'noplaylist': True,
        'outtmpl': os.path.join('videos', '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'merge_output_format': 'mp4'
    }
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url)
        video_title = result.get('title', 'downloaded_video')
        return os.path.join('videos', f"{video_title}.mp4")

def timestamp_to_seconds(timestamp):
    """Converts a timestamp in HH:MM:SS or MM:SS format to seconds."""
    parts = list(map(int, timestamp.split(":")))
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return parts[0]  # In case it's only seconds
 
# Main script execution
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUJcmljayByb2xs"  #update with the URL ;-)
    videos_folder = "videos"
    os.makedirs(videos_folder, exist_ok=True)
    full_video_path = download_video(url)

    csv_filename = "timestamps.csv"#timestamp csv path
    clip_duration = 25

    #prcessing timestamps
    timestamps = []
    with open(csv_filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            timestamps.append(row[0])

    for idx, ts in enumerate(timestamps):
        start_seconds = timestamp_to_seconds(ts)
        with VideoFileClip(full_video_path) as video:
            target_height = 1920
            target_width = 1080
            x_center = video.size[0] / 2
            y_center = video.size[1] / 2
            crop_width = min(video.size[0], video.size[1] * target_width / target_height)
            crop_height = crop_width * target_height / target_width

            #fix dimentions
            crop_width = int(crop_width // 2 * 2)
            crop_height = int(crop_height // 2 * 2)

            #make start and end of the clip
            start_clip = max(0, start_seconds - clip_duration // 2)
            end_clip = min(start_clip + clip_duration, video.duration)

            #crop & resize video 
            cropped = video.subclip(start_clip, end_clip).crop(
                x_center - crop_width / 2, y_center - crop_height / 2,
                width=crop_width, height=crop_height
            ).resize((target_width, target_height))

            output_file = os.path.join(videos_folder, f"clip_{idx+1}_{ts.replace(':', '-')}.mp4")
            cropped.write_videofile(output_file, codec="libx264", audio_codec='aac', fps=video.fps)

    print("All clips have been processed and saved.")
