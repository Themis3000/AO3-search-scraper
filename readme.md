# AO3 search scraper
This repo is for scraping fan fictions from archiveofourown.org

## How to use
- Install python 3.6 or higher (versions older then 3.6 may still work, but it's untested. You can check your current version with python --version)
- Download the code for this repo and unzip the file.
- In the same file as `main.py`, create a folder named `downloads`
- Go to archiveofourown.org and make any search query you want
- Paste the link for page one into page.txt
- Navigate the file containing `main.py` it in terminal/command prompt/powershell. (On windows, an easy way to do this is to navigate to the file with `main.py` in it, `shift+right` click inside the file, and click "open powershell window here").
- Type `python -m pip install -r requirements.txt` and press enter
- Finally, type `python ./main.py` to start the script. Downloaded pdf's should appear in the `downloads` folder!

## Rate limits
archiveofourown.org *will* rate limit you. This will cause the script to pause for an amountof time every once in a while. Usually after being rate limited once, you will then be limited to about 100 requests per 5 minutes thereafter

## Pausing the process
You can halt this program using any method and as uncleanly as you'd like. This script stores what page it is on in page.txt, so progress will not be lost. Do note though that the page downloaded count only applies to the amount of pages downloaded in the current session and will not be saved between sessions, so if you stop at page 5 and start again the program will reset it's count

## Efficiency
This scraper only scrapes one page at a time, but does use multithreading in order to download multiple pdfs at a time. This scraper also makes the absolute minimal amount of requests to the server possible (1 request per fanfic, and an additional 1 request per each page)
