from django.shortcuts import get_object_or_404
from .models import ShortURL


def get_active_short_url(shortKey: str) -> ShortURL:
    """
    Fetch an active ShortURL by short_key or raise 404.
    """
    return get_object_or_404(
        ShortURL,
        shortKey=shortKey,
        isActive=True
    )
def get_user_urls(user):
    return ShortURL.objects.filter(user=user, isActive=True).order_by("-createdAt")


def get_user_url_by_id(user, url_id):
    return get_object_or_404(
        ShortURL,
        id=url_id,
        user=user,
        isActive=True
    )
def short_url_exists_for_user(user, original_url: str) -> bool:
    return ShortURL.objects.filter(
        user=user,
        originalUrl=original_url,
        isActive=True
    ).exists()