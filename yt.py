from googleapiclient.discovery import build

import re


api_key = 'AIzaSyDMBC4iFnZEZPdrw3IhnvehtWQ2YEaMaLw'

youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.playlistItems().list(
    part='contentDetails',
    playlistId='PLBOPKXNP1R8n0Ew9ceUYAMiCsmGoGsVN8'
)

response = request.execute()

vid_ids = []
for item in response['items']:
    vid_ids.append(item['contentDetails']['videoId'])
print(','.join(vid_ids))
print('end')


vid_request = youtube.videos().list(
    part='contentDetails',
    id=','.join(vid_ids)
)

vid_response = vid_request.execute()

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

for item in vid_response['items']:
    duration = item['contentDetails']['duration']

    hours = hours_pattern.search(duration)
    minutes = minutes_pattern.search(duration)
    seconds = seconds_pattern.search(duration)

    if hours:
        hours = int(hours.group(1))
    else:
        hours = 0

    if minutes:
        minutes = int(minutes.group(1))
    else:
        minutes = 0

    if seconds:
        seconds = int(seconds.group(1))
    else:
        seconds = 0

    print(f'{hours} : {minutes} : {seconds}')
