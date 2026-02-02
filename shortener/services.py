from django.db.models import F
from .models import ShortURL
from .consts import base62Digits

def base62_encode(num:int)->str:
    if num==0:
        return base62Digits[0]
    base=len(base62Digits)
    encoded=[]
    while num>0:
        num,rem=divmod(num,base)
        encoded.append(base62Digits[rem])
    
    return ''.join(reversed(encoded))

def generate_shortKey(short_url: ShortURL) -> str:
    
    if short_url.shortKey:
        return short_url.shortKey

    shortKey = base62_encode(short_url.id)
    short_url.shortKey = shortKey
    short_url.save(update_fields=["shortKey"])

    return shortKey

def increment_click_count(short_url: ShortURL) -> None:

    ShortURL.objects.filter(id=short_url.id).update(
        clickCount=F('clickCount') + 1
    )

def create_short_url(*, user, originalUrl: str) -> ShortURL:
    short_url = ShortURL.objects.create(
        user=user,
        originalUrl=originalUrl
    )
    generate_shortKey(short_url)
    return short_url


def delete_short_url(short_url: ShortURL) -> None:
    short_url.isActive = False
    short_url.save(update_fields=["isActive"])

def update_short_url(*, short_url: ShortURL, originalUrl: str) -> ShortURL:
    short_url.originalUrl = originalUrl
    short_url.save(update_fields=["originalUrl"])
    return short_url
