import json
import os
import re
from html import unescape
import string
import unicodedata
import base64

def clean_html_title(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return unescape(cleantext)

def sanitize_title(title):
    return "".join(c for c in title if c.isalnum() or c.isspace())

def load_seen_links():
    seen_links = set()

    try:
        with open("seen_links.json", "r") as file:
            data = json.load(file)
            if isinstance(data, list):
                seen_links = set(data)
    except FileNotFoundError:
        print("seen_links.json not found. A new file will be created.")

    return seen_links

def save_seen_links(seen_links):
    try:
        with open("seen_links.json", "w") as file:
            json.dump(list(seen_links), file)
    except Exception as e:
        print("Failed to save seen links: ", e)

def clean_title(title):
    cleaned_title = title.strip()
    cleaned_title = ''.join(ch for ch in cleaned_title if ch in string.printable)
    cleaned_title = unicodedata.normalize('NFKD', cleaned_title).encode('ascii', 'ignore').decode('utf-8')
    cleaned_title = re.sub(r'[^\w\s-]', '', cleaned_title).strip()
    cleaned_title = re.sub(r'[-\s]+', '-', cleaned_title)

    return cleaned_title
