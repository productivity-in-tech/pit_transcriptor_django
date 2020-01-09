import requests
import feedparser


def get_feed_text(feed_url):
    """retrieves the feed using requests as text to store in the DB and be
    checked against"""

    return requests.get(feed_url).text

def get_feed_item_title_and_href(feed_item):
    for link in feed_item['links']:
        if 'audio' in link['type']:
            return [feed_item['title'], link['href']]


def feed_core_data(feed):
    feed_data = feedparser.parse(feed)
    links = []
    for item in feed_data['items']:
        links.append(get_feed_item_title_and_href(item))
    return links
    

def compare_feed_content(stored_feed_data, feed_url):
    """
    retrieve the new feed data and check it against the stored data
    """
    new_feed_data = get_feed_text(feed_url)

    return stored_feed_data == new_feed_data
