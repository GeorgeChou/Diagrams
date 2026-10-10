"""Build index.html (full page for GitHub Pages) and artifact.html (body-only
fragment) from src/template.html, src/data.json and src/logos.json.
Usage: python tools/build.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
tpl = (ROOT / "src/template.html").read_text(encoding="utf-8")
data = json.loads((ROOT / "src/data.json").read_text(encoding="utf-8"))
logos = json.loads((ROOT / "src/logos.json").read_text(encoding="utf-8"))
used = {c["d"] for L in data["layers"] for g in L["groups"] for c in g["cos"]}
logos = {k: v for k, v in logos.items() if k in used}

frag = (tpl.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))
           .replace("/*__LOGOS__*/{}", json.dumps(logos, separators=(",", ":"))))
(ROOT / "artifact.html").write_text(frag, encoding="utf-8")

head_end = frag.index("<style>")
page = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        "<meta name=\"description\" content=\"Interactive 10-layer map of the AI hardware supply chain, wafer to cloud.\">\n"
        + frag[:head_end] + frag[head_end:frag.index("</style>") + 8] + "\n</head>\n<body>\n"
        + frag[frag.index("</style>") + 8:] + "\n</body>\n</html>\n")
(ROOT / "index.html").write_text(page, encoding="utf-8")
print("built", len(page) // 1024, "KB;", len(logos), "logos")
