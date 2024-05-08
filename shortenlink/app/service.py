"""callback for the shortenlink service"""

import datetime

from .models import URLMapping, URLTracking

from .shortenlink.utils import (
    create_shorten_url,
    load_url,
    track_shorten_url,
    show_urls,
    show_trackings,
)


class UserInfo(object):

    def __init__(self, ip_address: str):
        self.ip_address = ip_address
        self.accessed_at = datetime.datetime.now(datetime.timezone.utc)


def shorten_url(url: str) -> str:
    """Shorten a URL"""
    return create_shorten_url(url, URLMapping)


def retrieve_url(short_url: str) -> str:
    """Retrieve a URL"""
    _, url = load_url(short_url, URLMapping)
    return url


def record_activity(short_url: str, user_info: UserInfo):
    """Record the activity"""
    id, _ = load_url(short_url, URLMapping)
    return track_shorten_url(id, user_info, URLTracking)


def display_urls() -> tuple[int, dict]:
    """Display all the URLs"""
    urlmappings = show_urls(URLMapping)
    mapping_num = len(urlmappings)
    mappings = list(urlmappings.values())
    return mapping_num, mappings


def display_records(short_url: str, page=1):
    """Display all the records"""
    id, url = load_url(short_url, URLMapping)
    page, tracking_num, trackings = show_trackings(id, URLTracking, page=page)
    trackings = list(trackings.values())
    return url, page, tracking_num, trackings
