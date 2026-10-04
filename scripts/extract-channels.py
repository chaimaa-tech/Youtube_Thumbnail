import json
from datetime import date, datetime, timezone
from pathlib import Path
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# List of channel handles to extract
CHANNELS = [
    "@buzzfeedtasty",
    "@JoshuaWeissman",
    "@bingingwithbabish",
    "@gordonramsay",
    "@NickDiGiovanni",
    "@Maangchi",
    "@foodwishes",
    "@ethanchlebowski"
]


def get_channel_info(youtube, handle, extracted_at):
    try:
        result = youtube.channels().list(
            part="snippet,statistics,brandingSettings,contentDetails,status",
            forHandle=handle
        ).execute()

        """
        API parameters:

        part tells the API which fields we want returned.

        Common channel parts:
        - snippet: title, description, thumbnails, published date
        - statistics: views, subscriber count, video count
        - brandingSettings: banner and channel branding
        - contentDetails: uploads playlist ID and related playlists
        - status: privacy and other status information
        """

        # Handle does not exist / channel was not found
        if not result.get("items"):
            print(f"⚠️ Channel not found: {handle}")
            return None

        # Add extraction timestamp to the raw API response
        result["extracted_at"] = extracted_at

        return result

    except HttpError as e:
        print(f"❌ YouTube API error for {handle}: {e}")
        return None

    except Exception as e:
        print(f"❌ Unexpected error for {handle}: {e}")
        return None


def save_channel_info(channel_info):

    # Date corresponding to this extraction run
    today = date.today().isoformat()

    folder = Path("bronze") / "channels" / f"dt={today}"
    folder.mkdir(parents=True, exist_ok=True)

    # Get channel title from the API response
    channel_title = channel_info["items"][0]["snippet"]["title"]

    filename = folder / f"{channel_title}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(channel_info, f, indent=4, ensure_ascii=False)

    print(f"✓ Saved: {filename}")


def main():

    # Load environment variables
    load_dotenv()

    # YouTube API client
    youtube = build(
        "youtube",
        "v3",
        developerKey=os.getenv("YOUTUBE_API_KEY")
    )

    # one timestamp for the entire extraction run
    extracted_at = datetime.now(timezone.utc).isoformat()

    # Extract and save each channel
    for handle in CHANNELS:

        info = get_channel_info(
            youtube,
            handle,
            extracted_at
        )

        if info is not None:
            save_channel_info(info)


if __name__ == "__main__":
    main()
