import re
from datetime import timedelta

from googleapiclient.discovery import build


api_key = 'AIzaSyDMBC4iFnZEZPdrw3IhnvehtWQ2YEaMaLw'


youtube = build('youtube', 'v3', developerKey=api_key)

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

nextpageToken = None

while True:
    total_seconds = 0
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId='PLBOPKXNP1R8n0Ew9ceUYAMiCsmGoGsVN8',
        maxResults=50,
        pageToken=nextpageToken
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

    video_secs = timedelta(
        hours=hours,
        minutes=minutes,
        seconds=seconds
    ).total_seconds()

    total_seconds += video_secs

    nextpageToken = response.get('nextpageToken')
    if not nextpageToken:
        break

total_seconds = int(total_seconds)

minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)

print(f'{hours}: {minutes}: {seconds}')
