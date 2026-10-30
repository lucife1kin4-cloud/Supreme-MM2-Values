from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://supremevalues.com"
CATEGORY_URLS = {
    "Godlies": f"{BASE_URL}/mm2/godlies",
}
CACHE_FILE = Path(__file__).resolve().parent / "values.json"
TIMEOUT_SECONDS = 20
USER_AGENT = "SupremeMM2ValuesCommunityTool/0.1 (public value-list reader)"
REQUEST_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml",
}


class SupremeValuesError(Exception):
    """Raised when the public values page cannot be read safely."""


def _normalise_number(raw: str) -> int:
    return int(raw.replace(",", "").replace(" ", ""))


def parse_category_html(html: str) -> dict[str, dict[str, Any]]:
    """
    Parse visible item cards from a Supreme Values category page.

    The parser looks for text fragments such as:
        Item Name Value - 123
        Range - [100 - 125]
        Demand - 4 Rarity - 3

    It intentionally ignores entries without a numeric Value instead of
    treating missing/untradeable prices as zero.
    """
    soup = BeautifulSoup(html, "html.parser")
    text = "\n".join(soup.stripped_strings)

    # Keep extraction conservative: only accept explicit "Name Value - N".
    value_pattern = re.compile(
        r"(?P<name>[A-Za-z0-9][A-Za-z0-9 '&’().\-\[\]]{0,75}?)"
        r"\s+Value\s*-\s*(?P<value>[\d,]+)",
        re.IGNORECASE,
    )

    parsed: dict[str, dict[str, Any]] = {}
    for match in value_pattern.finditer(text):
        name = " ".join(match.group("name").split()).strip(" |:-")
        if not name or name.casefold() in {"value", "range", "demand"}:
            continue

        value = _normalise_number(match.group("value"))
        if value < 0:
            continue

        parsed[name] = {
            "name": name,
            "value": value,
            "source": "Supreme Values",
            "category": None,
        }

    # A page with no matches may mean that the website changed its layout.
    # Do not overwrite the local cache with an empty or misleading dataset.
    if not parsed:
        raise SupremeValuesError(
            "На странице не удалось найти карточки с числовым Value. "
            "Возможно, Supreme Values изменил разметку."
        )

    return parsed


def fetch_category(category: str = "Godlies") -> dict[str, dict[str, Any]]:
    if category not in CATEGORY_URLS:
        allowed = ", ".join(CATEGORY_URLS)
        raise SupremeValuesError(
            f"Категория пока не подключена. Доступно: {allowed}"
        )

    url = CATEGORY_URLS[category]
    try:
        response = requests.get(
            url,
            headers=REQUEST_HEADERS,
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise SupremeValuesError(f"Не удалось загрузить Supreme Values: {exc}") from exc

    items = parse_category_html(response.text)
    for item in items.values():
        item["category"] = category
    return items


def fetch_all() -> dict[str, dict[str, Any]]:
    """Fetch all categories currently configured in CATEGORY_URLS."""
    combined: dict[str, dict[str, Any]] = {}

    for category in CATEGORY_URLS:
        category_items = fetch_category(category)
        combined.update(category_items)
        time.sleep(1.0)  # Be polite; do not hammer the public site.

    return combined


def save_cache(items: dict[str, dict[str, Any]]) -> None:
    payload = {
        "source": "Supreme Values",
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "item_count": len(items),
        "items": items,
    }
    CACHE_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_cache() -> dict[str, dict[str, Any]]:
    if not CACHE_FILE.exists():
        return {}
    try:
        payload = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        return payload.get("items", {})
    except (OSError, json.JSONDecodeError):
        return {}


def refresh_values() -> dict[str, dict[str, Any]]:
    """
    Download current configured categories and save them locally.
    On error, preserve the old cache and report the error to the caller.
    """
    fresh_items = fetch_all()
    if not fresh_items:
        raise SupremeValuesError("Источник вернул пустой список; кэш не изменён.")
    save_cache(fresh_items)
    return fresh_items


def get_value(item_name: str) -> int | None:
    """Find an item in the local cache, case-insensitively."""
    query = item_name.casefold().strip()
    for name, item in load_cache().items():
        if name.casefold() == query:
            return int(item["value"])
    return None


if __name__ == "__main__":
    print("Supreme MM2 Values — source test")
    try:
        items = refresh_values()
        print(f"Загружено предметов: {len(items)}")
        print(f"Кэш сохранён: {CACHE_FILE}")
        for name, data in list(items.items())[:10]:
            print(f"{name}: {data['value']}")
    except SupremeValuesError as error:
        print(f"Ошибка: {error}")
        cached = load_cache()
        print(f"Сохранённых ранее предметов в кэше: {len(cached)}")
