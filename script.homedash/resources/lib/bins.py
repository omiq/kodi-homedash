"""Generic bin-day fetcher. Reads a pre-scrubbed JSON from a per-device URL
(set in addon settings, never committed). The council-specific lookup that knows
your address/UPRN lives server-side and emits this clean payload, so nothing here
reveals where you live.

Expected payload (either shape):
    {"next": "YYYY-MM-DD", "type": "recycling"}
    [ {"next": "YYYY-MM-DD", "type": "recycling"}, {"next": "...", "type": "..."} ]
"""
import json
import urllib.request

USER_AGENT = "KodiHomeDash/0.1"


def _when(item: dict) -> str:
    return item.get("next") or item.get("date") or ""


def next_collection(url: str):
    """Soonest collection from the endpoint, or None. URL empty -> None (not set)."""
    if not url:
        return None
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    if isinstance(data, dict):
        return data
    if isinstance(data, list) and data:
        return sorted(data, key=_when)[0]
    return None


def format_line(item) -> str:
    if not item:
        return ""
    kind = item.get("type") or item.get("bin") or "bin"
    when = _when(item) or "?"
    return f"Next bin: {kind} on {when}"
