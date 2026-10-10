# AI Hardware Supply Chain Map

An interactive 10-layer diagram of the AI hardware supply chain, from wafers to cloud companies, with a focus on Taiwan. Data is as of October 2026.

**How to use it:** open `index.html` in a browser, or view it on GitHub Pages.

- **Hover a layer** to open a large panel with its company logos, local-language names, tickers and key figures.
- **Click a layer** to pin the panel, and press Esc to close it.
- **Scroll or pinch** to zoom, and **drag** to move around.
- **Double-click a layer** to zoom to it.
- Use the **Fit width** and **Fit all** buttons to reset the view.

## Files

| Path | What it is |
|---|---|
| `index.html` | The finished page: one self-contained file with the data and logos built in |
| `artifact.html` | The same page without the `<html>`/`<head>` wrapper, used for Claude artifacts |
| `src/data.json` | Layers, groups, companies, tickers, key figures |
| `src/logos.json` | Company icons, stored as data URIs |
| `src/template.html` | Page layout, styles and interaction code |
| `tools/fetch_logos.py` | Downloads icons for any new company domains in `data.json` |
| `tools/build.py` | Combines the three `src` files into `index.html` and `artifact.html` |

## Updating

1. Edit `src/data.json`, for example new figures after earnings or a new company.
2. If you added companies, run `python tools/fetch_logos.py`. It needs Pillow (`pip install pillow`).
3. Run `python tools/build.py`, then commit.

A company with no usable logo shows a monogram in its layer color instead.

Figures come from company results, earnings calls and press reports. They are not investment advice.
