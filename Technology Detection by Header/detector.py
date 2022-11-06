#!/usr/bin/env python3

# Libraries
##############################################################################
import requests
import re
import urllib3
from argparse import ArgumentParser
import sys
##############################################################################

# Disable HTTPS Warning
##############################################################################
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
##############################################################################

# Global Values
##############################################################################
DESCRIPTION = "The program that allows you detect technologies by Header"
URL_REGEX = r"^http(s)?:\/\/[0-9A-z.]+.[0-9A-z.]+.[a-z]+(/)?$"
##############################################################################

# Detection Techniques
##############################################################################
detect_techniques = {
    "Nginx":r"(?i)nginx(\/[\d.]+)?",
    "Apache":r"(?i)Apache(\/[\d.]+)?",
    "PHP":r"(?i)PHP(\/[\d.]+)?",
    "Python":r"(?i)Python(\/[\d.]+)?",
    "OpenSSL":r"(?i)OpenSSL(\/[\d.]+[a-z])?",
    "JBoss":r"(?i)JBoss-[\d.]+",
    "Microsoft IIS":r"(?i)(Microsoft-)?IIS(\/[\d.]+)?",
    "ASP.NET":r"ASP.NET",
    "Lighttpd":r"(?i)lighttpd(\/[\d.]+)?",
    "BaseHTTP":r"(?i)BaseHTTP(\/[\d.]+)?",
    "Django":r"(?i)Django(\/[\d.]+)?",
    "Drupal":r"(?i)'X-Generator':\s'Drupal\s([\d.]+)?"
}
##############################################################################

# Check Function
##############################################################################
def check_technologies(res):
    for k,v in detect_techniques.items():
        matches = re.search(v,res)
        if matches:
            print(k,"is found:", matches.group())
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
    args = parser.parse_args()

    target_url = str(args.url)  # Get Target URL from input
    if not re.match(URL_REGEX, target_url):
        print("Please provide valid URL")
        sys.exit(-1)

    # Send GET Request to Target URL
    try:
        res = requests.request("GET",target_url)
    except Exception as e:
        print(e)
        sys.exit(-1)

    # Get Response Headers
    headers = res.headers

    check_technologies(str(headers))
##############################################################################