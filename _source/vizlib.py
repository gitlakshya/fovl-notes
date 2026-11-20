"""Tiny SVG helpers for the FoVL notes figures.
Colours come from CSS classes (see .viz rules in style.css) so figures follow light/dark mode."""
import math, html

def esc(s): return html.escape(str(s), quote=True)

def svg(w, h, body, label=''):
    return (f'<svg class="vz" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="{esc(label)}" style="max-width:{w}px" font-family="Inter,system-ui,sans-serif" font-size="13">{body}</svg>')

def fig(fid, w, h, body, caption, label=None):
    return (f'<!--viz:{fid}-->\n<figure class="diagram viz" id="fig-{fid}">' + svg(w, h, body, label or caption) +
            f'<figcaption>{caption}</figcaption></figure>\n<!--/viz:{fid}-->')

def text(x, y, s, cls='', anchor='middle', size=None, weight=None, rot=None):
    a = f' font-size="{size}"' if size else ''
    a += f' font-weight="{weight}"' if weight else ''
    a += f' transform="rotate({rot} {x} {y})"' if rot is not None else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" class="{cls}"{a}>{esc(s)}</text>'

def rect(x, y, w, h, cls='bx', r=10):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" class="{cls}"/>'

def box(x, y, w, h, label, cls='bx', sub=None, tcls='', size=13):
    out = rect(x, y, w, h, cls)
    lines = label.split('\n')
    n = len(lines) + (1 if sub else 0)
    y0 = y + h / 2 - (n - 1) * 8 + 4
    for i, l in enumerate(lines):
        out += text(x + w / 2, y0 + i * 16, l, tcls, size=size, weight=600)
    if sub:
        out += text(x + w / 2, y0 + len(lines) * 16, sub, 'mut', size=11)
    return out

def line(x1, y1, x2, y2, cls='ax', w=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}" stroke-width="{w}"{d}/>'

def arrow(x1, y1, x2, y2, cls='ar', w=1.8, label=None, lcls='mut', dash=None):
    ang = math.atan2(y2 - y1, x2 - x1)
    L = 8
    p1 = (x2 - L * math.cos(ang - .4), y2 - L * math.sin(ang - .4))
    p2 = (x2 - L * math.cos(ang + .4), y2 - L * math.sin(ang + .4))
    d = f' stroke-dasharray="{dash}"' if dash else ''
    out = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}" stroke-width="{w}"{d}/>'
    out += f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" class="{cls}f"/>'
    if label:
        if abs(x2 - x1) < abs(y2 - y1):
            out += text((x1 + x2) / 2 + 8, (y1 + y2) / 2 + 4, label, lcls, 'start', 11)
        else:
            out += text((x1 + x2) / 2, (y1 + y2) / 2 - 7, label, lcls, size=11)
    return out

def circle(x, y, r, cls='bx', label=None, tcls='', size=13):
    out = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" class="{cls}"/>'
    if label is not None:
        out += text(x, y + 4.5, label, tcls, size=size, weight=600)
    return out

def path(d, cls='ln1', w=2.5, fill='none', dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" class="{cls}" stroke-width="{w}" fill="{fill}"{ds}/>'

class Axes:
    """Maps data coords to a plotting rectangle and draws axes/ticks."""
    def __init__(self, x, y, w, h, xlim, ylim, logx=False, logy=False):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.xlim, self.ylim, self.logx, self.logy = xlim, ylim, logx, logy
    def _t(self, v, lim, log):
        if log:
            v, lo, hi = math.log10(v), math.log10(lim[0]), math.log10(lim[1])
        else:
            lo, hi = lim
        return (v - lo) / (hi - lo)
    def px(self, v): return self.x + self._t(v, self.xlim, self.logx) * self.w
    def py(self, v): return self.y + self.h - self._t(v, self.ylim, self.logy) * self.h
    def frame(self, xticks=(), yticks=(), xlabel='', ylabel='', grid=True, xfmt=str, yfmt=str):
        o = ''
        for t in yticks:
            yy = self.py(t)
            if grid: o += line(self.x, yy, self.x + self.w, yy, 'grid', 1)
            o += text(self.x - 6, yy + 4, yfmt(t), 'mut', 'end', 11)
        for t in xticks:
            xx = self.px(t)
            o += line(xx, self.y + self.h, xx, self.y + self.h + 4, 'ax', 1)
            o += text(xx, self.y + self.h + 17, xfmt(t), 'mut', 'middle', 11)
        o += line(self.x, self.y + self.h, self.x + self.w, self.y + self.h, 'ax', 1.2)
        o += line(self.x, self.y, self.x, self.y + self.h, 'ax', 1.2)
        if xlabel: o += text(self.x + self.w / 2, self.y + self.h + 36, xlabel, 'mut', size=12)
        if ylabel: o += text(self.x - 42, self.y + self.h / 2, ylabel, 'mut', size=12, rot=-90)
        return o
    def polyline(self, pts, cls='ln1', w=2.5, dash=None):
        d = 'M' + ' L'.join(f'{self.px(a):.1f},{self.py(b):.1f}' for a, b in pts)
        return path(d, cls, w, dash=dash)
    def dots(self, pts, cls='c1', r=4):
        return ''.join(f'<circle cx="{self.px(a):.1f}" cy="{self.py(b):.1f}" r="{r}" class="{cls}"/>' for a, b in pts)

def bars(ax, labels, values, cls='c1', fmt=lambda v: f'{v:g}', gap=.25, show=True, rot=None, lsize=11):
    n = len(values); bw = ax.w / n
    o = ''
    for i, (lab, v) in enumerate(zip(labels, values)):
        x0 = ax.x + i * bw + bw * gap / 2
        y0 = ax.py(v); y1 = ax.py(ax.ylim[0])
        c = cls[i] if isinstance(cls, (list, tuple)) else cls
        o += f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{bw*(1-gap):.1f}" height="{max(y1-y0,0):.1f}" rx="4" class="{c}"/>'
        if show: o += text(x0 + bw * (1 - gap) / 2, y0 - 5, fmt(v), '', size=11, weight=600)
        if rot:
            o += text(x0 + bw * (1 - gap) / 2, ax.y + ax.h + 14, lab, 'mut', 'end', lsize, rot=rot)
        else:
            o += text(x0 + bw * (1 - gap) / 2, ax.y + ax.h + 16, lab, 'mut', size=lsize)
    return o

def heat(x, y, cw, ch, rows, cols, M, fmt=lambda v: f'{v:.2f}', vmax=None, rlabel_w=70, cls='hm'):
    vmax = vmax or max(max(r) for r in M) or 1
    o = ''
    for j, c in enumerate(cols):
        o += text(x + rlabel_w + j * cw + cw / 2, y - 8, c, 'mut', size=11)
    for i, r in enumerate(rows):
        o += text(x + rlabel_w - 8, y + i * ch + ch / 2 + 4, r, 'mut', 'end', 11)
        for j in range(len(cols)):
            v = M[i][j]
            op = 0.08 + 0.85 * (v / vmax if vmax else 0)
            o += f'<rect x="{x+rlabel_w+j*cw+1:.1f}" y="{y+i*ch+1:.1f}" width="{cw-2:.1f}" height="{ch-2:.1f}" rx="4" class="{cls}" fill-opacity="{op:.2f}"/>'
            o += text(x + rlabel_w + j * cw + cw / 2, y + i * ch + ch / 2 + 4, fmt(v), 'hmt' if v / vmax > .55 else '', size=11)
    return o

def legend(x, y, items):
    o = ''
    for i, (cls, lab) in enumerate(items):
        o += f'<rect x="{x}" y="{y+i*18-9}" width="14" height="10" rx="2" class="{cls}"/>' + text(x + 20, y + i * 18, lab, '', 'start', 11)
    return o
