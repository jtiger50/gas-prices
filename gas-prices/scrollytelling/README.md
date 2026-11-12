# What $2 billion looks like — scrollytelling graphic

Self-contained page: open `index.html` in a browser (all geodata is inlined; D3 and Scrollama load from a CDN, so you need to be online).

Scroll-driven steps, seven text cards (one per sentence of the two paragraphs):

1. **Budget** — bar chart, $2.0B vs. Maryland's $1.5B projected FY2027 deficit (hover a bar for exact values).
2. **Baltimore City** — the city outline fills with $1-bill-shaped tiles spreading out from the Inner Harbor until it's fully covered.
3. **Purple Line** — the camera pans straight southwest from Baltimore City to the Montgomery/Prince George's corridor (no zoom-out). The line is traced Bethesda → New Carrollton with a row of bills alongside it ("$100 bills"), then a return row New Carrollton → Bethesda ("Both ways"), then a grid of 60 small copies of the route fills in, one per round trip, ending at 59.5 ("Almost 60 times").
4. **Gas prices statewide** — the camera zooms out to all of Maryland; the Purple Line and Baltimore fade away and the state takes on a red wash. A gas-station price sign (seven-segment LED digits) counts up from the 2025 statewide average, $3.11, to the 2026 average, $3.91, as you scroll, with the percent change counting up beside it to +25.5%.
5. **Gas prices by metro area** — a dot marks each AAA metro area on the map, with a small LED price tag right above it (or, where the map is crowded, nearby with a short leader line). Each tag counts from the area's 2025 to its 2026 price with the change beside it. Cumberland (+32.6%) is then highlighted: a yellow-edged tag and a red, ringed dot.

## Files

| Path | What |
|---|---|
| `index.html` | The page to publish (written by `build.py`) |
| `src/template.html` | Page source: HTML/CSS/JS. `build.py` keeps the map data between `/*GEO_DATA*/` and `/*END_GEO_DATA*/`, so it also opens on its own |
| `build.py` | Writes `data/*.geojson` into the template and copies it to `index.html` |
| `data/*.geojson` | Processed boundaries and route (WGS84) |
| `data/aaa_gas_yoy.csv` | AAA regular gas prices by metro area, 2025 vs. 2026 (as supplied by the reporter; the values are also typed into `src/template.html`) |
| `src/fetch_geo.py` | How `data/` was made from the raw downloads (see below) |

Edit `src/template.html`, then run `python3 build.py`. Both files open straight from disk with the map data included.

Preview tip: `index.html?t=2.75` freezes the graphic at a scroll position (step index + progress), useful for screenshots.

## Sources

- **Maryland, county and Baltimore City boundaries:** U.S. Census Bureau 2023 cartographic boundary files (1:500,000, shoreline-clipped), from the TIGERweb `Generalized_ACS2023/State_County` MapServer (layer 7 = States 500K, layer 11 = Counties 500K). Baltimore City is GEOID 24510.
  `https://tigerweb.geo.census.gov/arcgis/rest/services/Generalized_ACS2023/State_County/MapServer`
- **Purple Line route:** Maryland Transit Administration, "Purple Line Alignment" feature service (owner MTA_GIS), downloaded as GeoJSON on 2026-11-10.
  `https://services.arcgis.com/njFNhDsUCentVYJW/arcgis/rest/services/Purple_Line_Alignment/FeatureServer/0`
  The service holds both tracks in 18 pieces (at-grade, tunnel, aerial). `fetch_geo.py` chains them into one west→east centerline (26.2 km / 16.3 mi) and simplifies it to ~8 m tolerance.
- **Gas prices:** AAA average price of a gallon of regular, by metro area, a year apart (2025 vs. 2026), supplied by the reporter. On the map, each area is marked at its main city; Bowie-St. Charles is marked between Bowie and St. Charles. Note: `../md_gas_prices_new.csv` only starts March 12, 2026, so it can't give year-over-year changes.
- **Bill size:** 2.61 × 6.14 in (U.S. Bureau of Engraving and Printing).

## The math

- $2B ÷ $100 = 20,000,000 bills × 6.14 in = 3,119 km (1,938 mi).
- Purple Line round trip = 2 × 26.2 km = 52.4 km → **59.5 round trips** ("almost 60" checks out; with MTA's published 16.2 mi it's 59.8).
- Baltimore City: 2,000,000,000 $1 bills × 16.03 sq in each ≈ 20.7 km² ≈ **8.0 sq mi**. Baltimore City's land area is about 80.9 sq mi (Census), so $2B in $1 bills covers about a tenth of the city. **The "blanket all of Baltimore City" sentence does not check out with $2 billion**; the graphic shows full coverage because that's what the sentence says. Worth confirming before publication.

Libraries: D3 7.9.0 (cdnjs), Scrollama 3.2.0 (jsDelivr). Fonts: Source Serif 4 (headlines, text) and Poppins (labels, UI) from Google Fonts, following the CNS interactive style. Always light mode; respects `prefers-reduced-motion`.
