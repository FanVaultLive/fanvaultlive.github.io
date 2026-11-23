"""Unit checks for the existing-feed bridge; no network or prod writes."""
import importlib.util
from pathlib import Path
import unittest
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
from urllib.parse import quote

SRC = Path(__file__).resolve().parents[1] / 'tools' / 'refresh_express_feed.py'
spec = importlib.util.spec_from_file_location('bridge', SRC)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)

TARGET = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Dotland Open Web Express 🚂🌈</title>
    <link>https://fanvaultlive.github.io/dotland/experiment-001/</link>
    <lastBuildDate>Mon, 23 Nov 2026 05:56:26 GMT</lastBuildDate>
    <item><title>Bowwow to BonBon</title><guid>bowwow</guid><description><![CDATA[<p>hello</p>]]></description></item>
    <item><title>First Automated Dot</title><guid>first-automated-dot</guid></item>
  </channel>
</rss>
'''
ID = '0Y8zSLl7PO0iNR69Q952l3'
MD = f'{bridge.SOURCE_ORIGIN}/m/{ID}.md'
BONBON = 'https://demo.bonbonweb.org/?url=' + quote(MD, safe='')
FEED = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>
<title>{bridge.FEED_TITLE}</title>
<atom:link href="{bridge.SOURCE_URL}" rel="self" type="application/rss+xml"/>
<item><title>One &amp; Little Dot</title><link>{BONBON.replace('&', '&amp;')}</link>
<guid isPermaLink="false">urn:mdlab:{ID}</guid>
<pubDate>Mon, 23 Nov 2026 21:14:37 GMT</pubDate>
<description>Approved sample\n\nOriginal Markdown: {MD}</description></item>
</channel></rss>'''

class RefreshTests(unittest.TestCase):
    def test_import_preserves_existing_posts_and_is_idempotent(self):
        items = bridge.parse_approved_items(FEED.encode())
        self.assertEqual(len(items), 1)
        out = bridge.merge_feed(TARGET, items, now=datetime(2026, 11, 23, 21, 30, tzinfo=timezone.utc))
        root = ET.fromstring(out)
        self.assertEqual(len(root.findall('channel/item')), 3)
        self.assertEqual(root.findall('channel/item')[0].findtext('title'), 'One & Little Dot')
        self.assertIn('<![CDATA[<p>hello</p>]]>', out)
        self.assertIn('urn:mdlab:' + ID, out)
        self.assertEqual(out, bridge.merge_feed(out, items, now=datetime(2026, 11, 24, tzinfo=timezone.utc)))

    def test_takedown_removes_only_managed_articles(self):
        approved = bridge.parse_approved_items(FEED.encode())
        before = bridge.merge_feed(TARGET, approved)
        after = bridge.merge_feed(before, [])
        self.assertNotIn('urn:mdlab:', after)
        self.assertIn('Bowwow to BonBon', after)
        self.assertEqual(len(ET.fromstring(after).findall('channel/item')), 2)

    def test_reject_unknown_source_and_wrong_reader(self):
        with self.assertRaises(ValueError):
            bridge.parse_approved_items(FEED.replace(bridge.FEED_TITLE, 'Other Feed').encode())
        with self.assertRaises(ValueError):
            bridge.parse_approved_items(FEED.replace(BONBON, 'https://bad.example/').encode())

    def test_reject_untrusted_guid_and_duplicates(self):
        with self.assertRaises(ValueError):
            bridge.parse_approved_items(FEED.replace('urn:mdlab:' + ID, 'urn:mdlab:../../../x').encode())
        with self.assertRaises(ValueError):
            bridge.parse_approved_items(FEED.replace('</channel>', FEED.split('<item>')[1].split('</item>')[0].join(['<item>','</item></channel>'])).encode())

    def test_reject_bad_destination(self):
        with self.assertRaises(ValueError):
            bridge.merge_feed(TARGET.replace('Dotland Open Web Express 🚂🌈', 'Not Our Feed'), [])
        with self.assertRaises(ValueError):
            bridge.merge_feed(TARGET.replace('</channel>', bridge.MARK_BEGIN + '</channel>'), [])

if __name__ == '__main__':
    unittest.main()
