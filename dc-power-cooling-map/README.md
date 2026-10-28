# Data center power and cooling map

Static matrix of who leads each data-center power and cooling segment, from the grid connection to the chip: Vertiv vs Schneider, Eaton, ABB/Siemens, Huawei, Delta 台達電, the HVAC majors, liquid-cooling specialists and Lite-On 光寶科 (October 2026).

- `segment-map.html`: source; dot size is an analyst judgment, labels carry published share or revenue figures with sources in the footer
- `segment-map.png`: rendered image, used in the Knowledge DB note "Vertiv vs competitors" and linked from the Vertiv Company DB page in Notion

To re-render after editing the HTML:

```
pip install playwright && playwright install chromium
python3 - <<'PY'
from playwright.sync_api import sync_playwright
import pathlib
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1700, "height": 900})
    pg.goto("file://" + str(pathlib.Path("segment-map.html").resolve()))
    pg.locator(".wrap").screenshot(path="segment-map.png"); b.close()
PY
```
