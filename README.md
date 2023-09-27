Fork that allows for the extraction of links from web pages to a .JSON file. 

## Includes the following additions:
- Extracted links are checked if they end correctly (.com, .net, etc.). This means no links leading to files.
- Links which match the site that's being scanned don't get included.
- Each validated link is assigned an ID and written to JSON.

## Sections

- [Dependencies :heavy_plus_sign:](#dependencies)
- [Install :package:](#install)
- [Run :runner:](#run)
- [Bonus :medal_sports:](#bonus)

## Dependencies
- Python 3.8+
- Requests
- BeautifulSoup

## Install

01 -) Clone:
```shell
$ git clone https://github.com/nitrogency/links-extractor-to-json
```

02 -) Go to `links-extractor` directory:
```shell
$ cd links-extractor
links-extractor $
```

## Run

01 -) In your `script.py` call `Extractor` main class like (can be found in example.py):
```python
import uuid
import json
import re
from src.services.extractor import Extractor
from src.utils.printer import Printer

output_file_path = 'data.json'

try:
    with open(output_file_path, 'r') as existing_json_file:
        existing_data = json.load(existing_json_file)
except FileNotFoundError:
    existing_data = []
    with open(output_file_path, 'w') as new_json_file:
        json.dump(existing_data, new_json_file, indent=4)

urls = ['http://google.com', 'http://github.com']
extractor = Extractor()
links = extractor.extract(urls, timeout=10)

output_data = []

domain_pattern = r'^https?://([^/]+)'

for url, extracted_links in links.items():
    Printer.message(f"Url: {url}")
    domain_match = re.search(domain_pattern, url).group(1)
    extracted_links_list = [
        re.search(domain_pattern, link).group(1) 
        for link in extracted_links 
        if isinstance(link, str) and re.search(domain_pattern, link) 
        and not (domain_match and re.search(domain_pattern, link).group(1) == domain_match) 
        and re.search(r'\.[a-zA-Z]{2,}', link)
        ]

    url_exists = any([entry['domain'] == url for entry in existing_data])

    if not url_exists:
        entry = {
            'id': str(uuid.uuid4()),
            'domain': url,
            'extracted_links': extracted_links_list
        }
        output_data.append(entry)
    else:
        Printer.warning(f"{url} already exists in the JSON file and will not be added.")

if output_data:

    existing_data.extend(output_data)

    with open(output_file_path, 'w') as json_file:
        json.dump(output_data, json_file, indent=4)
    
    Printer.success(f"Data written to {output_file_path}")
else:
    Printer.success(f"No new data to append.")

```

And you should find this output in the `data.json` file:
```json
[
    {
        "id": "d3a12f34-15db-4f10-b215-2b392956be92",
        "domain": "http://github.com",
        "extracted_links": [
            "docs.github.com",
            "skills.github.com",
            "github.blog",
            "education.github.com",
            "resources.github.com",
            "resources.github.com",
            "resources.github.com",
            "resources.github.com",
            "partner.github.com",
            "docs.github.com",
            "docs.github.com",
            "githubuniverse.com",
            "resources.github.com",
            "resources.github.com",
            "resources.github.com",
            "resources.github.com",
            "docs.github.com",
            "partner.github.com",
            "www.electronjs.org",
            "desktop.github.com",
            "docs.github.com",
            "github.community",
            "services.github.com",
            "skills.github.com",
            "www.githubstatus.com",
            "support.github.com?tags=dotcom-footer",
            "github.blog",
            "socialimpact.github.com",
            "shop.github.com",
            "x.com",
            "www.facebook.com",
            "www.linkedin.com",
            "www.youtube.com",
            "www.twitch.tv",
            "www.tiktok.com",
            "docs.github.com",
            "docs.github.com"
        ]
    },
    {
        "id": "58e0557e-f1c6-485a-9a99-b8cf94470a5e",
        "domain": "http://google.com",
        "extracted_links": [
            "www.google.com",
            "maps.google.lt",
            "play.google.com",
            "www.youtube.com",
            "news.google.com",
            "mail.google.com",
            "drive.google.com",
            "www.google.lt",
            "www.google.lt",
            "accounts.google.com",
            "www.google.lt",
            "www.google.com"
        ]
    }
]
```


## Bonus

01 -) Run tests with **pytest**:
```bash
links-extractor $ pytest
```

02 -) Run **autopep8** lint on files like:
```bash
links-extractor $  autopep8 --in-place --aggressive --aggressive src/services/extractor.py
```
