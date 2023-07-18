import logging
import time
from datetime import datetime, timedelta

from config import load_config
from feed import check_feed, load_seen_links, save_seen_links
from generate import generate_image
from publish import WordPressUploader

config = load_config()

uploader = WordPressUploader()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

seen_links = load_seen_links()
num_articles = 0
start_time = datetime.now()

# Specify the categories here as a list
categories = ["News", "World News"]

while True:
    logger.info("Checking feed for new articles...")

    latest = check_feed(
        config['rss_feed_url'],
        seen_links,
        num_articles
    )

    if latest:
        title, content = latest

        logger.info("Generating image...")
        image = generate_image(title, content)
        logger.debug("Generated image: %s", image)

        logger.info("Uploading post to WordPress...")
        uploader.upload(title, content, image, categories=categories)
        logger.debug("Uploaded post: %s", title)
        
        num_articles += 1

    elapsed_time = datetime.now() - start_time
    next_check_time = datetime.now() + timedelta(seconds=config['loop_delay'])
    logger.info("Next time to check for updates: %s", next_check_time.strftime("%H:%M"))
    logger.info("Generated articles so far: %d", num_articles)
    logger.info("Running for: %s", str(elapsed_time))

    # Save seen links to the JSON file
    save_seen_links(seen_links)

    logger.info("Waiting for %d seconds", config['loop_delay'])
    time.sleep(config['loop_delay'])
