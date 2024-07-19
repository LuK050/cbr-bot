from datetime import date
import logging
from typing import Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import aiohttp

BASE_URL: str = "https://cbr.ru/"


async def _get(path: str) -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL + path) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return None
    except Exception as _ex:
        logging.warning(_ex)
        return None


async def get_current_date() -> Optional[date]:
    response_text: Optional[str] = await _get("scripts/XML_daily.asp")

    if response_text is None:
        return None

    root: Element = ElementTree.fromstring(response_text)
    day, month, year = map(int, root.get("Date").split("."))
    current_date = date(year, month, day)
    return current_date


async def get_rates() -> Optional[dict[str, float]]:
    response_text: Optional[str] = await _get("scripts/XML_daily.asp")

    if response_text is None:
        return None

    root: Element = ElementTree.fromstring(response_text)
    rates: dict[str, float] = {}

    for i in root.iter(tag="Valute"):
        code: str = i[1].text
        rate: float = float(i[5].text.replace(",", "."))
        rates[code] = rate

    return rates
