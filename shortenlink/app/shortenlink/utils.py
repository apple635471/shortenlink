"""utils for shortenlink app"""

import datetime

from django.db import models

from .core import shorten_url
from .exception import (
    ShortenURLCreationError,
    ShortenURLRetrievalError,
    TrackingCreationError,
    URLRetrievalError,
)


def _is_url_repeat(url: str, username: str, model: models.Model) -> bool:
    """Check if the URL is repeated"""
    return model.objects.filter(url=url, owner=username).exists()


def _url_counts(model) -> int:
    """Return the number of URLs"""
    return model.objects.count()


def is_url_owner(url: str, username: str, model: models.Model) -> bool:
    """Check if the URL is owned by the user"""
    return model.objects.filter(url=url, owner=username).exists()


def load_shorten_url(url: str, username: str, model: models.Model) -> str:
    """Load the shorten URL"""
    # try-catch handle if failed to retrieve
    try:
        return model.objects.get(url=url, owner=username).short_url
    except Exception as e:
        print(e)
        raise ShortenURLRetrievalError


def load_url(short_url: str, model: models.Model) -> tuple[int, str]:
    """Load the URL"""
    # try-catch handle if failed to retrieve
    try:
        urlmapping = model.objects.get(short_url=short_url)
        return urlmapping.id, urlmapping.url
    except Exception as e:
        print(e)
        raise URLRetrievalError


def track_shorten_url(
    url_id: int, user_info: object, track_model: models.Model
) -> None:
    """Track the usage of the shorten URL"""
    # try-catch handle if failed to create
    try:
        track_model.objects.create(
            url_mapping_id=url_id,
            ip_address=user_info.ip_address,
            accessed_at=user_info.accessed_at,
        )
    except Exception as e:
        print(e)
        raise TrackingCreationError


def save_shorten_url(
    url: str, short_url: str, username: str, model: models.Model
) -> str:
    """Save the URL"""
    # try-catch handle if failed to create
    try:
        model.objects.create(
            url=url,
            short_url=short_url,
            owner=username,
            created_at=datetime.datetime.now(datetime.timezone.utc),
        )
    except Exception as e:
        print(e)
        raise ShortenURLCreationError

    return short_url


def create_shorten_url(url: str, username: str, model: models.Model) -> str:
    """Create a shorten URL"""
    # check if the URL is repeated
    if _is_url_repeat(url, username, model):
        return load_shorten_url(url, username, model)

    # save the URL
    urlnum = _url_counts(model)
    short_url = shorten_url(urlnum)

    return save_shorten_url(url, short_url, username, model)


def show_urls(username: str, model: models.Model) -> dict[int, dict[str, str]]:
    """Show all the URLs"""
    urlmappings = {}
    objects = model.objects.filter(owner=username)
    for urlmapping in objects:
        urlmappings[urlmapping.id] = {
            "url": urlmapping.url,
            "short_url": urlmapping.short_url,
        }
    return urlmappings


def show_trackings(
    url_id: int, track_model: models.Model, page: int = 1
) -> tuple[int, int, dict[int, dict[str, any]]]:
    """Show all the trackings"""
    trackings = {}
    objects = track_model.objects.filter(url_mapping_id=url_id).order_by("-accessed_at")
    tracking_num = len(objects)
    start = (page - 1) * 10
    end = start + 10
    if start < tracking_num:
        objects = objects[start:end]
    else:
        page = (tracking_num // 10) + 1
        start = (page - 1) * 10
        end = start + 10
        objects = objects[start:end]
    for tracking in objects:
        trackings[tracking.id] = {
            "ip_address": tracking.ip_address,
            "accessed_at": tracking.accessed_at,
        }
    return page, tracking_num, trackings
