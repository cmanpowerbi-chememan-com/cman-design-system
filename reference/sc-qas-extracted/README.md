# SC-QAS extracted evidence

Raw provenance for every token/component/pattern claim in `tokens/tokens.css`,
`tokens/tokens.json`, `typography/TYPOGRAPHY.md`, `components/COMPONENTS.md`, and
`patterns/PATTERNS.md`. If a value in those files looks wrong or you need to
re-verify it, check here first before re-scraping the live site.

## Source

- **App**: Chememan Supply Chain
- **URL**: https://sc-qas.chememan.com
- **Environment**: QAS / staging (not production)
- **Extraction date**: 2026-08-15
- **Stack observed**: ASP.NET MVC (Razor), Bootstrap 5.3.2 (jsdelivr CDN),
  Font Awesome 6.5.0 (cdnjs), jQuery 3.7.1, select2 4.1.0-rc.0, flatpickr 4.6.13.
  Served behind openresty.

## Files in this folder

| File | What it is |
|---|---|
| `site.css` | The app's ONLY external custom stylesheet (`/Content/site.css`), copied verbatim. |
| `layout-shell.css` | The shared app-shell `<style>` block (navbar height, `#wrapper`, sidebar, `#mainContent`) — identical across every authenticated page dump. |
| `select2-flatpickr.css` | select2 sizing + flatpickr compaction + uniform readonly/disabled field styling — identical across every authenticated page dump. |
| `table-overrides.css` | Table zebra striping (shared) + card-header min-height (dashboard pages only) + sort-col hover (list pages only) — see the file's own comments for which rule came from which page. |

## Full page dumps (not copied here — original location)

Two separate captures make up the full evidence base, at:
`C:\Users\JAKKAR~1\AppData\Local\Temp\claude\c--04-budget-management-web\5c30f1b3-4497-4dd1-b424-6b8079702e41\scratchpad\`

| Dump | Path | Auth state | md5 | Size |
|---|---|---|---|---|
| Login page | `root.html` (top level, NOT inside `theme_dump/`) | Unauthenticated GET to `https://sc-qas.chememan.com/` | `a9520a57…` | 3,671 bytes |
| Dashboard | `theme_dump\Home_Index.html` | Authenticated | `f3c7e6c6…` | 44,951 bytes |
| Dashboard (alias) | `theme_dump\root.html` | Authenticated GET to `/` (redirects to the dashboard once logged in) | `f3c7e6c6…` (identical to `Home_Index.html`) | 44,951 bytes |
| PO list | `theme_dump\Po.html` | Authenticated | `b054a400…` | 78,269 bytes |
| PO list (alias) | `theme_dump\Po_Index.html` | Authenticated | `b054a400…` (identical to `Po.html`) | 78,269 bytes |
| PO create | `theme_dump\Po_Create.html` | Authenticated | `6169014a…` | 312,811 bytes |

Plus `theme_dump\theme_report.txt` (aggregated colors / font-sizes / radii /
shadows, generated ONLY from the 5 files inside `theme_dump/` — it does not
scan the login page at all; see the caveat in step 3 below).

**Corrected count (2026-08-15): 6 files were captured across the two
extraction steps, but only 4 are unique pages** — login, dashboard
(`Home_Index.html` ≡ `theme_dump/root.html`), PO list (`Po.html` ≡
`Po_Index.html`), PO create. The `theme_dump/root.html` alias is the
**authenticated** root (what a logged-in session sees at `/`) — a completely
different file from the top-level `root.html` (the **anonymous** login page),
despite sharing a filename. See `typography/TYPOGRAPHY.md` for the full note.
Both scratch paths above are session-scoped, not part of this repo — if you
need to re-verify against the raw HTML, re-pull from the live app or ask for
a fresh dump; only the derived CSS evidence is preserved here.

## How to re-verify a token

1. Open the relevant file in this folder and search for the value.
2. If it's not here, it was either (a) marked `/* derived, not observed in app */`
   in `tokens/tokens.css` — meaning it was interpolated, not scraped — or
   (b) genuinely not observed and should be flagged.
3. `theme_report.txt` (see path above) has an aggregate frequency count per
   color/font-size/radius/shadow **across the 5 authenticated dump files —
   not 5 independent pages, and not the login page at all.** Of those 5,
   `Home_Index.html`/`theme_dump/root.html` are the same dashboard counted
   twice, and `Po.html`/`Po_Index.html` are the same PO list counted twice —
   so a higher frequency count there means "used on more of the 3 unique
   authenticated pages", not "used on more of the 5 filenames". A value that
   ONLY appears on the login page (e.g. the `.72rem` login sub-brand text,
   the `1rem` login brand, the 16px card radius) will show a count of **zero**
   in `theme_report.txt` even though it is real — check the top-level
   `root.html` directly for anything login-specific.
