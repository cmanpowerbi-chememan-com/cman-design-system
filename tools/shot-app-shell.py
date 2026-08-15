"""Re-render examples/app-shell.png from examples/app-shell.html.

Run after any change to the demo page or the tokens it consumes:
    python -X utf8 tools/shot-app-shell.py

Headless Chromium via Playwright; writes the PNG next to the HTML. The image
is a review artifact for humans — the script never opens it.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'examples' / 'app-shell.html'
OUT = ROOT / 'examples' / 'app-shell.png'


def main() -> int:
    if not PAGE.exists():
        print(f'missing {PAGE}')
        return 1
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 1000})
        errors = []
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.goto(PAGE.as_uri())
        page.wait_for_timeout(400)
        shell = page.evaluate(
            "getComputedStyle(document.body).getPropertyValue('background-color')"
        )
        page.screenshot(path=str(OUT), full_page=True)
        browser.close()
    print(f'body background: {shell}')
    print(f'console errors : {len(errors)}')
    for e in errors[:5]:
        print(f'  {e}')
    print(f'wrote {OUT} ({OUT.stat().st_size} bytes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
