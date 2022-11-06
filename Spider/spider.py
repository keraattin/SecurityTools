#!/usr/bin/env python3

# Libraries
##############################################################################
import requests
import re
from urllib.parse import urljoin,urlparse
import urllib3
import random
from argparse import ArgumentParser
import sys
##############################################################################

# Disable HTTPS Warning
##############################################################################
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
##############################################################################

# Global Values
##############################################################################
USER_AGENTS     = []
URLS_TO_VISIT   = []
VISITED_URLS    = []
DESCRIPTION     = "The program that allows you to crawl web pages"
URL_REGEX       = r"^http(s)?:\/\/[0-9A-z.]+.[0-9A-z.]+.[a-z]+(/)?$"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36 OPR/84.0.4316.14",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.52",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) Version/5.1.9 Safari/534.59.10",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko)"
]
# Extensions to be not visited
BLACKLIST_EXT = [
    "png",
    "jpg",
    "jpeg",
    "pdf",
    "mp3",
    "mp4",
    "zip",
    "tar"
]
##############################################################################

# Extract links from page
##############################################################################
def extract_links(url):
    global URLS_TO_VISIT
    global VISITED_URLS

    # Set Headers
    # Set random user agent
    headers = {
        'User-Agent':random.choice(USER_AGENTS)
    }

    # Send GET Request to Target URL
    try:
        response = requests.request("GET", url, headers=headers).text
    except Exception as e:
        print(e)
    
    if url not in VISITED_URLS and url not in URLS_TO_VISIT:
        VISITED_URLS.append(url)
    
    # Find all the values in href tags
    url_list = re.findall('(?:href=")(.*?)"',str(response))

    for possible_url in url_list:
        # Keep going if "#" is not in possible URL
        if not "#" in possible_url:
            # Combine the path and domain
            joined_url = urljoin(target_url,possible_url)
            # If possible URL in Scope
            if domain == urlparse(joined_url).netloc.split('www.')[-1]:
                # Get Extension
                extension = joined_url.split('/')[-1].split('.')[-1]
                # If extension is not blacklisted then proceed
                if not extension in BLACKLIST_EXT:
                    if joined_url not in VISITED_URLS and joined_url not in URLS_TO_VISIT:
                        URLS_TO_VISIT.append(joined_url)
                        print(joined_url)
                # If extension is blacklisted add to Visited URLS list and
                # do not visit
                else:
                    if joined_url not in VISITED_URLS and joined_url not in URLS_TO_VISIT:
                        VISITED_URLS.append(joined_url)
                        print("[Not Visited]",joined_url)
##############################################################################

# Main
##############################################################################
if __name__ == '__main__':
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "-u",
        "--url", 
        type=str, 
        help="Target url", 
        required=True
    )
    parser.add_argument(
        "-o",
        "--out", 
        type=str, 
        help="Output file", 
        required=False
    )
    args = parser.parse_args()

    target_url = str(args.url)  # Get Target URL from input

    # Validate the URL
    if not re.match(URL_REGEX, target_url):
        print("Please provide valid URL")
        sys.exit(-1)
    
    # Get Domain
    domain = urlparse(target_url).netloc.split('www.')[-1]

    # Append Targets
    URLS_TO_VISIT.append(target_url+"/robots.txt")
    URLS_TO_VISIT.append(target_url)

    # Run
    while URLS_TO_VISIT:
        url = URLS_TO_VISIT.pop(0)
        extract_links(url)

    print("\n\n#####################################\n")
    print("Links:\n")
    print("_____________________________________\n")
    
    # If out argument provided
    # Write results to the file
    if args.out:
        with open(args.out,"w",encoding="utf-8") as f:
            for url in VISITED_URLS:
                f.write(url+"\n")
                print(url)
    else:
        for url in VISITED_URLS:
            print(url)
    
    print("_____________________________________\n")
    print("\n#####################################\n")
##############################################################################