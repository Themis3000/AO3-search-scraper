# AO3 search scraper
This repo is for scraping fan fictions from archiveofourown.org

## How to use
- go to archiveofourown.org and make any search query you want
- paste the link for page one into page.txt
- run main.py. Downloaded pdfs will appear in `./downloads`

## Rate limits
archiveofourown.org *will* rate limit you. This will cause the script to pause for an amountof time every once in a while. Usually after being rate limited once, you will then be limited to about 100 requests per 5 minutes thereafter

## Pausing the process
You can halt this program using any method and as uncleanly as you'd like. This script stores what page it is on in page.txt, so progress will not be lost. Do note though that the page downloaded count only applies to the amount of pages downloaded in the current session and will not be saved between sessions, so if you stop at page 5 and start again the program will reset it's count

## Efficiency
This scraper only scrapes one page at a time, but does use multithreading in order to download multiple pdfs at a time. This scraper also makes the absolute minimal amount of requests to the server possible (1 request per fanfic, and an additional 1 request per each page)
