import json, math, sys
D = sys.argv[1]; OUT = sys.argv[2]
topo = json.load(open(D + '/counties-10m.json'))
sc, tr = topo['transform']['scale'], topo['transform']['translate']
arcs = []
for a in topo['arcs']:
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy
        pts.append([round(x*sc[0]+tr[0], 5), round(y*sc[1]+tr[1], 5)])
    arcs.append(pts)
def arc(i):
    return arcs[i] if i >= 0 else arcs[~i][::-1]
def ring(idx):
    out = []
    for i in idx:
        p = arc(i); out.extend(p if not out else p[1:])
    return out
def geom(g):
    if g['type'] == 'Polygon': return {'type':'Polygon','coordinates':[ring(r) for r in g['arcs']]}
    return {'type':'MultiPolygon','coordinates':[[ring(r) for r in p] for p in g['arcs']]}
def feat(g): return {'type':'Feature','properties':{'id':g['id'],'name':g['properties']['name']},'geometry':geom(g)}
state = [feat(g) for g in topo['objects']['states']['geometries'] if g['id']=='24'][0]
counties = [feat(g) for g in topo['objects']['counties']['geometries'] if g['id'].startswith('24')]
balt = [c for c in counties if c['properties']['id']=='24510'][0]
print('counties', len(counties), balt['properties'])

# Purple Line: chain the MTA alignment parts into one ordered west->east centerline
pl = json.load(open(D + '/pl.geojson'))
parts = []
for f in pl['features']:
    for p in f['geometry']['coordinates']: parts.append(p)
def dist(a, b):
    kx = 111320*math.cos(math.radians(39)); return math.hypot((a[0]-b[0])*kx, (a[1]-b[1])*111320)
def length(p): return sum(dist(p[i], p[i+1]) for i in range(len(p)-1))
print('parts', len(parts), 'total km', round(sum(length(p) for p in parts)/1000, 2))
# start at westernmost endpoint
ends = [(min(p[0][0], p[-1][0]), i) for i, p in enumerate(parts)]
_, si = min(ends)
p = parts[si]; chain = p if p[0][0] < p[-1][0] else p[::-1]
used = {si}
while True:
    tail = chain[-1]; best = None
    for i, q in enumerate(parts):
        if i in used: continue
        for rev in (False, True):
            r = q[::-1] if rev else q
            d = dist(tail, r[0])
            if best is None or d < best[0]: best = (d, i, r)
    if best is None or best[0] > 60: break
    # skip parallel-track parts that run backwards (their far end must lie east of tail)
    used.add(best[1]); chain = chain + best[2][1:]
chain = chain[:max(range(len(chain)), key=lambda i: chain[i][0])+1]
print('chain parts', len(used), 'km', round(length(chain)/1000, 2), 'start', chain[0], 'end', chain[-1])
# Douglas-Peucker ~8 m
def dp(pts, tol):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; kx = 111320*math.cos(math.radians(39))
    ax, ay, bx, by = a[0]*kx, a[1]*111320, b[0]*kx, b[1]*111320
    L = math.hypot(bx-ax, by-ay) or 1e-9; mi, md = 0, -1
    for i in range(1, len(pts)-1):
        px, py = pts[i][0]*kx, pts[i][1]*111320
        d = abs((bx-ax)*(ay-py) - (ax-px)*(by-ay)) / L
        if d > md: mi, md = i, d
    if md <= tol: return [a, b]
    return dp(pts[:mi+1], tol)[:-1] + dp(pts[mi:], tol)
simp = [[round(x, 5), round(y, 5)] for x, y in dp(chain, 8)]
print('simplified pts', len(simp), 'km', round(length(simp)/1000, 2))
line = {'type':'Feature','properties':{'name':'Purple Line (MTA alignment, one track)','length_km':round(length(chain)/1000,3)},'geometry':{'type':'LineString','coordinates':simp}}
def area(r): return sum(r[i][0]*r[i+1][1]-r[i+1][0]*r[i][1] for i in range(len(r)-1))/2
def rewind(g):  # d3-geo wants exterior rings clockwise (negative planar area), holes CCW
    polys = g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
    for poly in polys:
        for k, r in enumerate(poly):
            if (area(r) > 0) == (k == 0): r.reverse()
    return g
def load(fn):
    fc = json.load(open(D + '/' + fn))
    for f in fc['features']: rewind(f['geometry'])
    return fc
state = load('state500k.geojson')['features'][0]
counties = load('cnty500k.geojson')['features']
balt = load('balt500k.geojson')['features'][0]
for name, obj in [('maryland', state), ('md_counties', {'type':'FeatureCollection','features':counties}), ('baltimore_city', balt), ('purple_line', line)]:
    json.dump(obj, open(f'{OUT}/{name}.geojson', 'w'), separators=(',', ':'))
