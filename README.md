# Twitter Scraper

## Description
This Python script uses the `ntscraper` library to scrape tweets from a specified Twitter user, download the associated images and videos, and create a CSV dataset.

## Features
- Scrapes tweets from a specified Twitter user
- Downloads images and videos embedded in the tweets
- Creates a CSV dataset with the tweet captions, hashtags, and media file names

## Requirements
- Python 3.x
- The following Python packages:
  - `os`
  - `time`
  - `subprocess`
  - `requests`
  - `uuid`
  - `pandas`
  - `ntscraper`

## Usage
1. Install the required packages by running `pip install -r requirements.txt`.
2. Update the `username` and `domain` variables in the script to your desired values.
3. Run the script using `python twitter_scraping.py`.
4. The script will create a CSV file in the current directory with the downloaded media files.
