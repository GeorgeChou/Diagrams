# Nvidia DSX POD

Two static diagrams of Nvidia's DSX POD reference design (containerized Vera Rubin AI factory, announced Oct 21, 2026 at GTC Berlin):

- `architecture.html` / `architecture.png`: what is inside the factory-built core container (7 × NVL72 racks, 800V DC distribution, liquid loop, network fabric, controls) and what the site must supply (800V DC power, water and heat rejection, network, links to other PODs)
- `build-process.html` / `build-process.png`: factory integration and test in parallel with site preparation, then on-site hookup and commissioning (≈14 days from arrival)

Used in the Knowledge DB note "Vertiv vs Competitors — Data Center Power & Cooling" in Notion. Re-render with Playwright at viewport 1360 px wide, screenshotting `.wrap`.
