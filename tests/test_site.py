from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://andymdoyle.github.io/CookWatt-support/"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def matching(self, tag, **attrs):
        return [
            item for name, item in self.elements
            if name == tag and all(item.get(key) == value for key, value in attrs.items())
        ]


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.pages = {name: Page(ROOT / name) for name in ("index.html", "privacy.html")}

    def test_page_metadata_and_navigation(self):
        for name, page in self.pages.items():
            with self.subTest(page=name):
                self.assertEqual(len(page.matching("h1")), 1)
                self.assertEqual(page.matching("html")[0]["lang"], "en-GB")
                self.assertTrue(page.matching("meta", name="viewport"))
                self.assertTrue(page.matching("meta", name="description"))
                self.assertTrue(page.matching("meta", name="color-scheme"))
                self.assertEqual(
                    page.matching("link", rel="canonical")[0]["href"],
                    ORIGIN + ("" if name == "index.html" else name),
                )
                current = [attrs for tag, attrs in page.elements
                           if tag == "a" and attrs.get("aria-current") == "page"]
                self.assertEqual(len(current), 1)
                self.assertEqual(current[0]["href"], "./" if name == "index.html" else name)

    def test_contact_is_real_and_consistent(self):
        for name, page in self.pages.items():
            with self.subTest(page=name):
                emails = [urlparse(attrs["href"]).path for tag, attrs in page.elements
                          if tag == "a" and attrs.get("href", "").startswith("mailto:")]
                self.assertTrue(emails)
                self.assertEqual(set(emails), {"apps@andydoyle.org"})

    def test_local_links_assets_and_fragments_exist(self):
        for name, page in self.pages.items():
            ids = [attrs["id"] for _, attrs in page.elements if "id" in attrs]
            self.assertEqual(len(ids), len(set(ids)), f"Duplicate IDs in {name}")
            for tag, attrs in page.elements:
                for key in ("href", "src", "srcset"):
                    if key not in attrs:
                        continue
                    value = urlparse(attrs[key])
                    if value.scheme or value.netloc:
                        continue
                    target = ROOT / unquote(value.path or name)
                    if target.is_dir():
                        target /= "index.html"
                    self.assertTrue(target.is_file(), f"{name}: missing {attrs[key]}")
                    if value.fragment:
                        target_ids = {item.get("id") for _, item in Page(target).elements}
                        self.assertIn(value.fragment, target_ids)

    def test_no_embedded_scripts_forms_or_remote_assets(self):
        for name, page in self.pages.items():
            with self.subTest(page=name):
                for tag in ("script", "form", "iframe"):
                    self.assertFalse(page.matching(tag))
                for tag, attrs in page.elements:
                    if tag in ("img", "source", "link") and attrs.get("rel") != "canonical":
                        for key in ("src", "srcset", "href"):
                            self.assertFalse(urlparse(attrs.get(key, "")).netloc)
                policies = [attrs.get("content", "") for tag, attrs in page.elements
                            if tag == "meta" and attrs.get("http-equiv") == "Content-Security-Policy"]
                self.assertEqual(len(policies), 1)
                self.assertIn("default-src 'self'", policies[0])


if __name__ == "__main__":
    unittest.main()
