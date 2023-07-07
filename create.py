import yt_dlp
import os
from pytube import Playlist,YouTube
from pprint import pprint as pp
import pandas as pd
from common import write_to_csv
 


def create_download_list():
    try:
        print('reading existing download list')
        df_input = pd.read_csv('download_list.csv')
        existing_list = df_input['link'].tolist()
        
    except FileNotFoundError:
        print('no existing download list found.Creating empty download_list.csv')
        empty = pd.DataFrame([['link','title','audio_res','video_res']])
        empty.to_csv('download_list.csv',index=False,header=False)
        existing_list = []
        
    try:
        print('reading existing negative list')
        df_negative = pd.read_csv('negative_list.csv')
        non_download_items = df_negative['link'].tolist()
    except:
        print('no existing negative list found.Creating empty negative_list.csv')
        empty = pd.DataFrame([['link','title']])
        empty.to_csv('negative_list.csv',index=False,header=False)
        non_download_items = []
        
    playlist_link = input('Paste Youtube Playlist Link here : ')

    playlist = Playlist(playlist_link)
    print(playlist)
    count = len(playlist)
    for video in playlist:
        if video in existing_list:
            print('video already in list to be downloaded....')
            count -= 1
        elif video in non_download_items:
            print('Video has been marked as non download. kindly delete the entry from negative list and run programme again.')
            count -= 1
        else:
            title = YouTube(video).title
            print(title)
            duration = divmod(YouTube(video).length, 60)
            length = f'{duration[0]}:{duration[1]}'
            print(length)
            print(f'{count} videos remaining to be downloaded...')
            download = input(f'Do you want to download -----{title} (enter y/n) to view click ({video}) : ')
            if download.lower() == 'y':
                count -= 1
                os.system(f'yt-dlp --extractor-args "youtube:player-client=web" --user-agent "" -F {video}')
                audio_input = input('Enter Audio Format ID : ')
                video_input = input('Enter vidoe Format ID : ')
                write_to_csv('download_list.csv',[video,title,length,audio_input,video_input])
            elif download.lower() == 'n':
                count -= 1
                print(f'you have chosen not to download the given video - {title}')
                write_to_csv('negative_list.csv',[video,title])
            else:
                break

create_download_list()