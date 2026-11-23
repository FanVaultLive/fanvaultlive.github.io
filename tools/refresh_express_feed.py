#!/usr/bin/env python3
"""Merge approved Markdown Lab articles into the existing Dotland RSS feed.

No GitHub credentials are read here. The GitHub Action, after review/merge,
may commit using its repository-scoped GITHUB_TOKEN. The source is an
explicitly pinned public RSS endpoint and supplies approved content only.
The destination's existing RSS items are left untouched.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from email.utils import format_datetime, parsedate_to_datetime
from pathlib import Path
import re
from urllib.parse import quote
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

SOURCE_URL = "https://markdown-publish-lab-preview-bjfylktp3-brianpucketts-projects.vercel.app/feed.xml"
DESTINATION = Path("dotland/experiment-001/feed.xml")
MARK_BEGIN = "  <!-- MD-PUB-003:LAB-BEGIN -->"
MARK_END = "  <!-- MD-PUB-003:LAB-END -->"
ID_RE = re.compile(r"urn:mdlab:([0-9A-Za-z]{22})\Z")
DATE_RE = re.compile(r"(<lastBuildDate>)[^<]*(</lastBuildDate>)")
RSS_NS = "http://www.w3.org/2005/Atom"
FEED_TITLE = "Dotland Express — Markdown Lab (Experimental)"
SOURCE_ORIGIN = SOURCE_URL.rsplit("/", 1)[0]
MAX_RESPONSE = 256 * 1024
MAX_ITEMS = 100

def xml_escape(value: str) -> str:
    return (value.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;")
            .replace("'", "&apos;"))

def assert_clean_text(value: str, field: str, max_length: int) -> str:
    if len(value) > max_length or any(ord(ch) < 32 and ch not in "\n\r\t" for ch in value):
        raise ValueError(f"Invalid {field} content in source feed")
    return value

def parse_approved_items(blob: bytes) -> list[dict[str, str]]:
    if len(blob) > MAX_RESPONSE or b"<!DOCTYPE" in blob.upper() or b"<!ENTITY" in blob.upper():
        raise ValueError("Feed too large or unexpected DTD")
    root = ET.fromstring(blob)
    if root.tag != "rss" or root.attrib.get("version") != "2.0":
        raise ValueError("Expected RSS 2.0 source")
    channel = root.find("channel")
    if channel is None or channel.findtext("title") != FEED_TITLE:
        raise ValueError("Unrecognized Markdown Lab source feed")
    self_link = channel.find(f"{{{RSS_NS}}}link")
    if self_link is None or self_link.get("href") != SOURCE_URL:
        raise ValueError("Markdown Lab RSS self-link does not match pinned source")
    found = []
    seen = set()
    items = channel.findall("item")
    if len(items) > MAX_ITEMS:
        raise ValueError("Too many RSS items")
    for item in items:
        guid = (item.findtext("guid") or "").strip()
        m = ID_RE.fullmatch(guid)
        if not m or guid in seen:
            raise ValueError("Malformed or duplicated Markdown Lab RSS GUID")
        seen.add(guid)
        id_ = m.group(1)
        title = assert_clean_text((item.findtext("title") or "").strip(), "title", 120)
        if not title:
            raise ValueError("Missing article title")
        summary = (item.findtext("description") or "").split("\n\nOriginal Markdown:")[0].strip()
        summary = assert_clean_text(summary, "description", 400)
        date = parsedate_to_datetime((item.findtext("pubDate") or "").strip())
        if date.tzinfo is None:
            raise ValueError("RSS pubDate lacks timezone")
        date = date.astimezone(timezone.utc)
        expected_md = f"{SOURCE_ORIGIN}/m/{id_}.md"
        expected_read = f"https://demo.bonbonweb.org/?url={quote(expected_md, safe='')}"
        if item.findtext("link") != expected_read:
            raise ValueError("Unexpected Markdown Lab reader link")
        found.append({
            "id": id_, "title": title, "summary": summary,
            "reader": expected_read, "markdown": expected_md,
            "date": format_datetime(date, usegmt=True),
        })
    return found

def fetch_approved_items() -> list[dict[str, str]]:
    req = Request(SOURCE_URL, headers={"User-Agent": "Dotland-Express-RSS-Bridge/0.1"})
    with urlopen(req, timeout=15) as resp:
        if resp.url != SOURCE_URL or resp.status != 200:
            raise ValueError("Markdown Lab feed redirected or unavailable")
        blob = resp.read(MAX_RESPONSE + 1)
    return parse_approved_items(blob)

def render_section(items: list[dict[str, str]]) -> str:
    lines = [MARK_BEGIN]
    for item in items:
        description = (item["summary"] + "\n\n" if item["summary"] else "") + "Original Markdown: " + item["markdown"]
        lines += [
            "    <item>",
            "      <title>" + xml_escape(item["title"]) + "</title>",
            "      <link>" + xml_escape(item["reader"]) + "</link>",
            "      <guid isPermaLink=\"false\">urn:mdlab:" + item["id"] + "</guid>",
            "      <pubDate>" + item["date"] + "</pubDate>",
            "      <category>Markdown Lab</category>",
            "      <description>" + xml_escape(description) + "</description>",
            "    </item>",
        ]
    lines.append(MARK_END)
    return "\n".join(lines)

def merge_feed(original: str, items: list[dict[str, str]], *, now: datetime | None = None) -> str:
    """Replace only the marked section; keep original items unchanged."""
    if "<!DOCTYPE" in original.upper() or "<!ENTITY" in original.upper():
        raise ValueError("Unexpected DTD in destination")
    old = ET.fromstring(original)
    if old.tag != "rss" or old.find("channel") is None:
        raise ValueError("Expected destination RSS")
    if old.findtext("channel/title") != "Dotland Open Web Express 🚂🌈":
        raise ValueError("Incorrect target feed")
    if original.count(MARK_BEGIN) != original.count(MARK_END):
        raise ValueError("Broken managed-section markers")
    if original.count(MARK_BEGIN) > 1:
        raise ValueError("Duplicate managed-section markers")
    section = render_section(items)
    if MARK_BEGIN in original:
        a = original.index(MARK_BEGIN)
        b = original.index(MARK_END, a) + len(MARK_END)
        candidate = original[:a] + section + original[b:]
    else:
        start = original.find("    <item>")
        if start == -1:
            raise ValueError("Original feed unexpectedly has no articles")
        candidate = original[:start] + section + "\n" + original[start:]
    if candidate == original:
        return original
    timestamp = format_datetime((now or datetime.now(timezone.utc)).astimezone(timezone.utc), usegmt=True)
    candidate, n = DATE_RE.subn(lambda m: m.group(1) + timestamp + m.group(2), candidate, count=1)
    if n != 1:
        raise ValueError("Destination missing lastBuildDate")
    finished = ET.fromstring(candidate)
    if len(finished.findall("channel/item")) < len(items) + 2:
        raise ValueError("Original RSS items might have been dropped")
    return candidate

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-source-file", type=Path, help="Offline RSS test source")
    parser.add_argument("--dest", type=Path, default=DESTINATION)
    args = parser.parse_args()
    source = args.input_source_file.read_bytes() if args.input_source_file else None
    items = parse_approved_items(source) if source is not None else fetch_approved_items()
    original = args.dest.read_text(encoding="utf-8")
    updated = merge_feed(original, items)
    if updated != original:
        args.dest.write_text(updated, encoding="utf-8")
        print(f"Updated {args.dest}: {len(items)} approved Markdown Lab items")
    else:
        print(f"No change to {args.dest}: {len(items)} approved Markdown Lab items")

if __name__ == "__main__":
    main()
