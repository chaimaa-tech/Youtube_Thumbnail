from dotenv import load_dotenv
import os
from googleapiclient.discovery import build

load_dotenv()
youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY")) #youtube client object
print(youtube.channels().list(part="snippet", id="UC_x5XG1OV2P6uZZ5FSM9Ttw").execute())
'''
1) part="snippet"
This is one of the most important parameters.

part tells the API which fields you want returned.

For a channel, common parts are:

snippet: basic info like title, description, thumbnails, published date
statistics: views, subscriber count, video count
brandingSettings: banner image, channel branding
contentDetails: uploads playlist ID, related playlists
status: privacy status etc.

'''
# List of channel IDs to extract
channels = [
    "@buzzfeedtasty",
    "@JoshuaWeissman",
    "@bingingwithbabish",
    "@gordonramsay",
    "@NickDiGiovanni",
    "@Maangchi",
    "@foodwishes",
    "@ethanchlebowski"
]

for handle in channels:
    result = youtube.channels().list(
        part="id,snippet",
        forHandle=handle
    ).execute()

    channel = result["items"][0]

    print(channel["snippet"]["title"], "→", channel["id"])