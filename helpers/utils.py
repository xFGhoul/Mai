import pyshorteners

from pyshorteners.exceptions import (
    BadAPIResponseException,
    BadURLException,
    ShorteningErrorException,
)

from config.ext.config_parser import config


from .logging import log


async def shorten_url(url: str):
    s = pyshorteners.Shortener(api_key=config["BITLY_API_TOKEN"])
    try:
        shortened_url = s.bitly.short(url)
    except (BadAPIResponseException, BadURLException, ShorteningErrorException):
        log.error("[red]ERROR WHEN TRYING TO SHORTERN URL.[/red]")

    return shortened_url
