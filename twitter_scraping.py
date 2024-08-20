username = "omarsar0"
domain = "Machine Learning_" + username

import os
import time
import subprocess
import requests
import uuid
import pandas as pd
from ntscraper import Nitter  # Import Nitter scraper module

# Initialize Nitter scraper
scraper = Nitter()

# Function to download images
def download_image(url, folder):
    # Create folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Generate a unique identifier for the file
    filename = str(uuid.uuid4()) + os.path.splitext(url)[1]

    # Download the media file
    response = requests.get(url)
    time.sleep(1)
    if response.status_code == 200:
        with open(os.path.join(folder, filename), 'wb') as file:
            file.write(response.content)
        return filename
    else:
        return None

# Function to download videos
def download_video(url, folder):
    # Create folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Generate a unique identifier for the file
    filename = str(uuid.uuid4()) + '.mp4'  # Save as mp4 format
    output_file = os.path.join(folder, filename)

    # Get video duration using ffprobe
    ffprobe_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', url]
    duration_output = subprocess.run(ffprobe_cmd, capture_output=True, text=True)
    duration = float(duration_output.stdout.strip()) if duration_output.stdout else 0  # Duration in seconds

    # Check if the video duration is less than 1 minute (60 seconds)
    if duration < 60:
        time.sleep(1)
        # Download video using ffmpeg
        cmd = ['ffmpeg', '-i', url, '-c', 'copy', output_file]
        subprocess.run(cmd, capture_output=True, text=True)

        # Check if the video was downloaded successfully
        if os.path.exists(output_file):
            return filename
        else:
            return None
    else:
        return None  # Video longer than 1 minute, skip downloading

# Function to create dataset of tweets
def create_tweets_dataset(domain, no_of_tweets):
    # Get tweets from the specified username
    tweets = scraper.get_tweets(username, mode="user", number=no_of_tweets)

    # Initialize data dictionary
    data = {
        'caption':[],
        'hashtags':[],
        'Photo/Video_ID_1':[],
        'Photo/Video_ID_2':[],
        'Photo/Video_ID_3':[],
        'Photo/Video_ID_4':[],
        'Photo/Video_ID_5':[],
        'Photo/Video_ID_6':[],
        'Photo/Video_ID_7':[]
    }

    # Iterate through tweets
    for tweet in tweets['tweets']:
        # Add tweet caption and hashtags to data dictionary
        data['caption'].append(tweet['text'])
        data['hashtags'].append([t for t in tweet['text'].split() if t.startswith('#')])

        # Download images from the tweet
        j = 1
        for pic_url in tweet['pictures']:
            filename = download_image(pic_url, domain)
            if filename:
                data[f'Photo/Video_ID_{j}'].append(filename)
                j += 1
                if j > 7:
                    break

        # Download videos from the tweet
        for vid_url in tweet['videos']:
            filename = download_video(vid_url, domain)
            if filename:
                data[f'Photo/Video_ID_{j}'].append(filename)
                j += 1
                if j > 7:
                    break

        # Fill remaining slots with empty strings
        while j <= 7:
            data[f'Photo/Video_ID_{j}'].append("")
            j += 1

    # Create DataFrame from data dictionary
    df = pd.DataFrame(data)

    # Save DataFrame to CSV file
    df.to_csv(domain +".csv")

# Example usage
create_tweets_dataset(domain, 100)