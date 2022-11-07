# Spider
With that program, you can able to crawl web pages

## Requirements
To run this program requirements must be met

To do that:
```
pip3 install -r requirements.txt
```

## Usage
```
python3 spider.py -u <target_url>
```

If you want to write results to the file
```
python3 spider.py -u <target_url> -o <filename>
```

## Blacklisted Extensions
In that program, some extensions will not be visited but you can see them in the result.
If you want to add or remove from the extension blacklist you can change this section from the code.
```
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
```

## Language
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)