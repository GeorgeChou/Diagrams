"""Fetch one icon per company domain in src/data.json and save them as
data URIs in src/logos.json, so the page works offline and inside
sandboxes that block external images.

Order tried for each domain: icons declared in the homepage <head>,
/apple-touch-icon.png, Google's favicon service, DuckDuckGo's icon
service. The largest raster wins; an SVG icon is used when no raster
of at least 64px is found. Usage: python tools/fetch_logos.py
"""
import base64
import concurrent.futures as cf
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
TARGET = 96


def get(url, timeout=10):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.geturl(), r.headers.get("Content-Type", "")


def head_icons(domain):
    out = []
    for base in (f"https://www.{domain}", f"https://{domain}"):
        try:
            html, final, _ = get(base)
        except Exception:
            continue
        text = html[:200000].decode("utf-8", "ignore")
        for tag in re.findall(r"<link[^>]+>", text, re.I):
            rel = re.search(r'rel=["\']([^"\']+)', tag, re.I)
            href = re.search(r'href=["\']([^"\']+)', tag, re.I)
            if not rel or not href or "icon" not in rel.group(1).lower():
                continue
            out.append(urllib.parse.urljoin(final, href.group(1)))
        out.append(urllib.parse.urljoin(final, "/apple-touch-icon.png"))
        break
    return out


def load(url):
    try:
        data, _, ctype = get(url)
    except Exception:
        return None
    if len(data) < 100:
        return None
    if url.lower().split("?")[0].endswith(".svg") or "svg" in ctype:
        if b"<svg" in data[:2000].lower() and b"<script" not in data.lower():
            return ("svg", data, 10_000)
        return None
    try:
        img = Image.open(io.BytesIO(data))
        if getattr(img, "n_frames", 1) > 1 or img.format == "ICO":
            sizes = getattr(img, "ico", None)
            if sizes:
                img = img.ico.getimage(max(sizes.sizes()))
        img = img.convert("RGBA")
    except Exception:
        return None
    return ("png", img, min(img.size))


def best(domain):
    cands = head_icons(domain) + [
        f"https://www.google.com/s2/favicons?domain={domain}&sz=128",
        f"https://icons.duckduckgo.com/ip3/{domain}.ico",
    ]
    found = []
    for u in dict.fromkeys(cands):
        r = load(u)
        if r:
            found.append(r)
    rasters = [f for f in found if f[0] == "png"]
    svgs = [f for f in found if f[0] == "svg"]
    top = max(rasters, key=lambda f: f[2]) if rasters else None
    if svgs and (top is None or top[2] < 64):
        return domain, "data:image/svg+xml;base64," + base64.b64encode(svgs[0][1]).decode(), "svg"
    if top is None:
        return domain, None, 0
    img = top[1]
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    img.thumbnail((TARGET, TARGET), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return domain, "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), top[2]


def main():
    data = json.loads((ROOT / "src/data.json").read_text(encoding="utf-8"))
    domains = sorted({c["d"] for L in data["layers"] for g in L["groups"] for c in g["cos"]})
    out_path = ROOT / "src/logos.json"
    logos = json.loads(out_path.read_text()) if out_path.exists() and "--fresh" not in sys.argv else {}
    todo = [d for d in domains if d not in logos]
    with cf.ThreadPoolExecutor(12) as ex:
        for domain, uri, size in ex.map(best, todo):
            print(f"{domain:28s} {size}")
            if uri:
                logos[domain] = uri
    out_path.write_text(json.dumps(logos, indent=0, sort_keys=True))
    missing = [d for d in domains if d not in logos]
    print(f"\n{len(logos)} logos saved; missing: {missing}")


if __name__ == "__main__":
    main()
