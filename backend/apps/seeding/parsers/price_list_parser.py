"""Parses <country>_{sale,rent}_price_list.docx files into PriceRange rows.

Only the header paragraph is parsed (e.g. "Sale Price List (500,000 KSh to
1,000,000,000 KSh in increments of 100,000)") for listing type, currency and
bounds. The documented price_range schema stores a single min/max row per
country + listing_type, with no step/increment column, so the hundreds of
enumerated per-step paragraphs that follow the header in each file are
intentionally discarded.
"""

import re
from pathlib import Path

from docx import Document

CURRENCY_SYMBOL_TO_ISO = {
    "KSh": "KES",
    "UGX": "UGX",
    "TSh": "TZS",
}

HEADER_RE = re.compile(
    r"(Sale|Rent)\s+Price List\s*\(([\d,]+)\s*(\w+)\s+to\s+([\d,]+)\s*(\w+)",
    re.IGNORECASE,
)


def parse(docx_path: Path) -> dict:
    document = Document(docx_path)
    header = document.paragraphs[0].text

    match = HEADER_RE.search(header)
    if not match:
        raise ValueError(f"Could not parse price list header in {docx_path}: {header!r}")

    listing_type_word, min_str, min_symbol, max_str, max_symbol = match.groups()
    currency_code = CURRENCY_SYMBOL_TO_ISO.get(min_symbol, CURRENCY_SYMBOL_TO_ISO.get(max_symbol))
    if currency_code is None:
        raise ValueError(f"Unknown currency symbol in {docx_path}: {min_symbol!r}")

    country_name = docx_path.stem.split("_")[0].capitalize()

    return {
        "country": country_name,
        "listing_type": listing_type_word.lower(),
        "currency_code": currency_code,
        "min_price": int(min_str.replace(",", "")),
        "max_price": int(max_str.replace(",", "")),
    }
