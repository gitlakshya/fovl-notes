"""Insert generated figures into src fragments (idempotent: replaces previous <!--viz:id--> blocks)."""
import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figures
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
bad = []
files = {}
for f, h, x in figures.F:
    files.setdefault(f, []).append((h, x))
for f, items in files.items():
    p = os.path.join(SRC, f); s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!--viz:([\w-]+)-->.*?<!--/viz:\1-->\n?', '', s, flags=re.S)
    for h, x in items:
        heads = [(m.start(), m.end(), re.sub('<[^>]+>', '', m.group(1))) for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', s, re.S)]
        hit = [hd for hd in heads if h.lower() in hd[2].lower().replace('&amp;', '&').replace('’', "'")]
        if not hit: bad.append((f, h)); continue
        st, en, _ = hit[0]
        nxt = s.find('<h2', en)
        pos = nxt if nxt != -1 else len(s)
        s = s[:pos] + x + '\n' + s[pos:]
    open(p, 'w', encoding='utf-8').write(s)
print('inserted', len(figures.F) - len(bad), 'missing', bad)
