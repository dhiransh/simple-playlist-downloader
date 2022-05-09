import yt_dlp
import os
from pytube import Playlist,YouTube
from pprint import pprint as pp
import pandas as pd
from common import write_to_csv

    
def download_videos():
    try:
        downloaded_df = pd.read_csv('downloaded_videos.csv')
        downloaded_videos = downloaded_df['link'].tolist()
    except FileNotFoundError:
        empty = pd.DataFrame([['link','title','audio_res','video_res']])
        empty.to_csv('downloaded_videos.csv',index=False,header=False)
        downloaded_videos = []
    download_df = pd.read_csv('download_list.csv')
    download_list =download_df.values.tolist()
    for link in download_list:
        if link[0] not in downloaded_videos:
            os.system(f'yt-dlp --extractor-args "youtube:player-client=web" --user-agent "" --merge-output-format mp4 -k -f {link[-1]}+{link[-2]} {link[0]}')
            write_to_csv('downloaded_videos.csv',link) 
        else:
            print('video has already been downloaded once')
                

download_videos()