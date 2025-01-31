import csv
from youtube_comment_downloader import YoutubeCommentDownloader
import re


url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUJcmljayByb2xs"#youtube video URl
video_id = url.split("v=")[-1]#YT video ID

#to download YT video
downloader = YoutubeCommentDownloader()
comments = downloader.get_comments(video_id)

#detecting timestamps in comments
timestamp_pattern = re.compile(r'\b\d{1,2}:\d{2}\b')

timestamps = []

#Fetch comments
for comment in comments:
    text = comment['text']
    timestamp_match = timestamp_pattern.search(text)
    
    if timestamp_match:
        timestamps.append(timestamp_match.group(0))  #extract the timestamp
        if len(timestamps) == 20: #change to find the number of comments with timestamps
            break
            
#save to CSV
csv_filename = "timestamps.csv" #csv file name
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp"])  #write header
    for timestamp in timestamps:
        writer.writerow([timestamp])

print(f"Timestamps have been saved to {csv_filename}")
