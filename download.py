import yt_dlp
import os
from pytube import Playlist,YouTube
from pprint import pprint as pp
import pandas as pd
from csv import writer

def write_to_csv(csv_file_name,data_list):
    with open(str(csv_file_name), 'a', newline='',encoding="utf-8") as f_object:  
        writer_object = writer(f_object)
        writer_object.writerow(data_list)  
        f_object.close()


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
            print(f'{count} videos remaining to be downloaded...')
            download = input(f'Do you want to download -----{title} (enter y/n) to view click ({video}) : ')
            if download.lower() == 'y':
                count -= 1
                os.system(f'yt-dlp --extractor-args "youtube:player-client=web" --user-agent "" -F {video}')
                audio_input = input('Enter Audio Format ID : ')
                video_input = input('Enter vidoe Format ID : ')
                write_to_csv('download_list.csv',[video,title,audio_input,video_input])
            elif download.lower() == 'n':
                count -= 1
                print(f'you have chosen not to download the given video - {title}')
                write_to_csv('negative_list.csv',[video,title])
            else:
                break
            
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
                
create_download_list()
# download_videos()