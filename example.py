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




