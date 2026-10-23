# CPO company map

Static diagram placing a company's products on the co-packaged optics (CPO) light path:
InP substrate and epi → laser chips → external laser (ELSFP) → optical engine on the package → optical circuit switch, with pluggable transceivers shown as today's alternative.

Each product label shows the revenue line it is reported in, with dollars and its share of that company's total revenue.

- `cohr-lite.html`: Coherent (COHR) vs Lumentum (LITE), quarter ended June 2026
- `cohr-lite.png`: rendered image, used in the Notion note "InP 磷化銦 & CPO 共封裝光學", section 4B

To re-render after editing the HTML:

```
pip install playwright && playwright install chromium
python3 - <<'EOF'
from playwright.sync_api import sync_playwright
import pathlib
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 2000, "height": 800})
    pg.goto("file://" + str(pathlib.Path("cohr-lite.html").resolve()))
    pg.locator(".wrap").screenshot(path="cohr-lite.png"); b.close()
EOF
```
