from typing import List
import urllib.request
import xml.etree.ElementTree as ET
import sys
from models.currency import Currency
from .logger import logger

DEFAULT_CBR_URL = "https://www.cbr-xml-daily.ru/daily.xml"

@logger(handle=sys.stdout)
def get_currencies(url: str = DEFAULT_CBR_URL, timeout: int = 10) -> List[Currency]:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        data = resp.read()
    root = ET.fromstring(data)

    currencies: List[Currency] = []

    def get_text(tag: str) -> str:
        elem = val.find(tag)
        if elem is not None and elem.text:
            return elem.text.strip()
        return ""

    for val in root.findall(".//Valute"):
        val_id = val.attrib.get("ID", "")

        num_code = int(get_text("NumCode") or "0")
        char_code = get_text("CharCode")
        name = get_text("Name")
        nominal = int((get_text("Nominal") or "1").replace(" ", ""))
        value_str = get_text("Value")
        value = float(value_str.replace(",", ".")) if value_str else 0.0

        currencies.append(Currency(
            id_=val_id,
            num_code=num_code,
            char_code=char_code,
            name=name,
            value=value,
            nominal=nominal
        ))

    return currencies
