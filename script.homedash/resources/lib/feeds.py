"""RSS/Atom fetching with the stdlib only (no external addon deps to install on
the Kodi box). Handles both RSS <item> and Atom <entry> by matching local tag
names, which sidesteps namespace handling."""
import html
import re
import urllib.request
import xml.etree.ElementTree as ET

_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"[ \t]*\n[ \t]*")

DEFAULT_FEEDS = ["https://retrogamecoders.com/feed/"]
USER_AGENT = "KodiHomeDash/0.1"


def configured_feeds(addon) -> list[str]:
    raw = addon.getSetting("feeds") if addon else ""
    urls = [u.strip() for u in raw.replace(",", "\n").splitlines() if u.strip()]
    return urls or DEFAULT_FEEDS


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _child(el, name: str):
    for c in el:
        if _local(c.tag) == name:
            return c
    return None


def _text(el) -> str:
    return (el.text or "").strip() if el is not None else ""


def _strip_html(raw: str) -> str:
    """Feed bodies are HTML; flatten to readable plain text for the viewer."""
    text = html.unescape(_TAG.sub("", raw))
    text = _WS.sub("\n", text)
    return "\n".join(line.strip() for line in text.splitlines()).strip()


def _link(el) -> str:
    """RSS <link> holds the URL as text; Atom <link> holds it in href."""
    link = _child(el, "link")
    if link is None:
        return ""
    return _text(link) or link.get("href", "")


def _parse(url: str, limit: int, source: str) -> list[dict]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as r:
        root = ET.fromstring(r.read())

    out: list[dict] = []
    for el in root.iter():
        if _local(el.tag) not in ("item", "entry"):
            continue
        title = _text(_child(el, "title"))
        date = ""
        for key in ("pubdate", "published", "updated", "date"):
            d = _child(el, key)
            if d is not None:
                date = _text(d)
                break
        body = ""
        for key in ("description", "summary", "content", "encoded"):
            b = _child(el, key)
            if b is not None and _text(b):
                body = _strip_html(_text(b))
                break
        if title:
            out.append({
                "title": title,
                "source": source,
                "date": date[:25],
                "body": body,
                "link": _link(el),
            })
        if len(out) >= limit:
            break
    return out


def fetch_all(urls: list[str], per_feed: int = 8) -> list[dict]:
    out: list[dict] = []
    for url in urls:
        label = url.split("//")[-1].split("/")[0]
        try:
            out.extend(_parse(url, per_feed, label))
        except Exception as e:  # surface the error in-list rather than crash the window
            out.append({"title": f"[feed error] {url}", "source": label, "date": str(e)[:30]})
    return out
