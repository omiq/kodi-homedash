#!/usr/bin/env python3
"""Regenerate the Kodi repository tree under repo/ from the add-on sources.

Release flow:
    1. bump <version> in the add-on's addon.xml
    2. python3 make_repo.py
    3. git add -A && git commit && git push

Kodi (via repository.homedash) then sees the new version and updates over the
air. raw.githubusercontent.com has a short CDN cache, so allow a few minutes.
"""
import hashlib
import os
import xml.etree.ElementTree as ET
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(ROOT, "repo")
ZIPS = os.path.join(REPO, "zips")

# Add-on source dirs to publish (each holds an addon.xml).
ADDONS = ["script.homedash", "repository.homedash"]

SKIP_DIRS = {"__pycache__"}
SKIP_FILES = {".DS_Store"}


def addon_meta(src: str):
    tree = ET.parse(os.path.join(ROOT, src, "addon.xml"))
    root = tree.getroot()
    return root.get("id"), root.get("version")


def addon_block(src: str) -> str:
    """Raw <addon>...</addon> element, declaration stripped, for addons.xml."""
    with open(os.path.join(ROOT, src, "addon.xml"), encoding="utf-8") as f:
        text = f.read()
    return text[text.index("<addon"):].rstrip()


def make_zip(src: str, addon_id: str, version: str):
    out_dir = os.path.join(ZIPS, addon_id)
    os.makedirs(out_dir, exist_ok=True)
    zip_path = os.path.join(out_dir, f"{addon_id}-{version}.zip")
    base = os.path.join(ROOT, src)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                if name in SKIP_FILES or name.endswith(".pyc"):
                    continue
                full = os.path.join(dirpath, name)
                # Store with the addon folder as the zip's top-level dir.
                arc = os.path.join(src, os.path.relpath(full, base))
                z.write(full, arc)
    return zip_path


def main():
    os.makedirs(ZIPS, exist_ok=True)
    blocks = []
    for src in ADDONS:
        addon_id, version = addon_meta(src)
        blocks.append(addon_block(src))
        zp = make_zip(src, addon_id, version)
        print(f"  zipped {addon_id} {version} -> {os.path.relpath(zp, ROOT)}")

    addons_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<addons>\n' \
        + "\n".join(blocks) + "\n</addons>\n"
    xml_path = os.path.join(REPO, "addons.xml")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(addons_xml)

    digest = hashlib.md5(addons_xml.encode("utf-8")).hexdigest()
    with open(xml_path + ".md5", "w", encoding="utf-8") as f:
        f.write(digest)
    print(f"  wrote {os.path.relpath(xml_path, ROOT)} (md5 {digest})")


if __name__ == "__main__":
    main()
