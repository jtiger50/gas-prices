"""Write data/*.geojson into the page.

The data goes between /*GEO_DATA*/ and /*END_GEO_DATA*/ in both src/template.html and
index.html, so each file is self-contained (no separate data file to load).
"""
import json, pathlib, re
here = pathlib.Path(__file__).parent
load = lambda n: json.loads((here / 'data' / f'{n}.geojson').read_text())
geo = {'maryland': load('maryland'), 'counties': load('md_counties'),
       'baltimore': load('baltimore_city'), 'purpleLine': load('purple_line')}
blob = json.dumps(geo, separators=(',', ':'))
pattern = re.compile(r'/\*GEO_DATA\*/.*?/\*END_GEO_DATA\*/', re.S)
src = here / 'src' / 'template.html'
html = src.read_text()
assert pattern.search(html), 'GEO_DATA markers missing from src/template.html'
html = pattern.sub(lambda m: '/*GEO_DATA*/' + blob + '/*END_GEO_DATA*/', html)
src.write_text(html)
(here / 'index.html').write_text(html)
print('wrote index.html and src/template.html with data,', len(html) // 1024, 'KB')
