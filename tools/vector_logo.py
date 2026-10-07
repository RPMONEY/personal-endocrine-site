"""Export the PERSONAL / ENDOCRINE lockup as true vector files (SVG + PDF + PNG).

Chrome lays out the exact lockup used on the site; we read back each letter's pen position,
font size and baseline from the DOM, then draw the real glyph outlines from the font files
with fontTools. Every letter is a path, so the files need no fonts installed.
"""
import os
import cairosvg
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from playwright.sync_api import sync_playwright

S = '/tmp/claude-0/-home-claude/0185ca3d-049d-5066-a804-995bec835255/scratchpad'
F = S + '/fonts/node_modules/@fontsource'
OUT = S + '/logo-files'
INK, WHITE = '#252A26', '#FFFFFF'
FONTS = {  # key: (label, family, pkg, weight PERSONAL, weight ENDOCRINE, bar thickness em)
    'montserrat': ('Montserrat', 'montserrat', 500, 500, 0.07),
    'outfit': ('Outfit', 'outfit', 500, 400, 0.075),
}
SIZE = 100  # px size of PERSONAL in layout units


def woff(pkg, w):
    return f'{F}/{pkg}/files/{pkg}-latin-{w}-normal.woff2'


BL = '<span class="bl" style="display:inline-block;width:0;height:0"></span>'


def page(kind, fam, pkg, wp, we, t):
    o = ('<span class="o" style="position:relative;top:-0.155em;font-size:0.86em">O' + BL + '</span>'
         f'<span class="bar" style="display:inline-block;height:{t}em;background:#000"></span>')
    if kind == 'mark':
        body = f'<span class="ln" data-w="{wp}" style="font-weight:{wp};font-size:{SIZE*2}px;letter-spacing:0;line-height:1">{o}</span>'
    else:
        body = (f'<span style="display:inline-flex;flex-direction:column;align-items:center;gap:{SIZE*0.12:.1f}px;line-height:1">'
                f'<span class="ln" data-w="{wp}" style="font-weight:{wp};font-size:{SIZE}px;letter-spacing:0.08em;margin-right:-0.08em;white-space:nowrap">PERS{o}NAL{BL}</span>'
                f'<span class="ln" data-w="{we}" style="font-weight:{we};font-size:{SIZE*0.46:.1f}px;letter-spacing:0.34em;margin-right:-0.34em;white-space:nowrap">ENDOCRINE{BL}</span></span>')
    faces = ''.join(f"@font-face{{font-family:'L';font-weight:{w};src:url(file://{woff(pkg, w)})}}" for w in sorted({wp, we}))
    return f'''<html><head><style>{faces} body{{margin:40px;font-family:'L'}}</style></head><body>{body}
<script>document.fonts.ready.then(()=>{{
const o=document.querySelector('.o'),b=document.querySelector('.bar');
const ls=parseFloat(getComputedStyle(o).letterSpacing)||0, ow=o.getBoundingClientRect().width;
const glyph=ow-ls, bw=glyph*0.86, inset=(glyph-bw)/2;
b.style.width=bw+'px';b.style.marginLeft=(-ow+inset)+'px';b.style.marginRight=(ow-inset-bw)+'px';
document.body.dataset.done=1}})</script></body></html>'''


# read back, for every text character: x pen position, baseline y, font size, weight
MEASURE = '''() => {
 const out=[];
 document.querySelectorAll('.ln').forEach(ln=>{
   const w=+ln.dataset.w;
   const walker=document.createTreeWalker(ln,NodeFilter.SHOW_TEXT);
   let n; while((n=walker.nextNode())){
     const el=n.parentElement, fs=parseFloat(getComputedStyle(el).fontSize);
     const bl=el.querySelector(':scope > .bl') || ln.querySelector(':scope > .bl');
     const base=bl.getBoundingClientRect().bottom;
     for(let i=0;i<n.length;i++){const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+1);
       out.push({ch:n.data[i],x:r.getBoundingClientRect().left,y:base,fs,w});}
   }
 });
 const b=document.querySelector('.bar').getBoundingClientRect();
 return {chars:out,bar:{x:b.left,y:b.top,w:b.width,h:b.height}};
}'''


def build_svg(data, fonts, color):
    paths, xs, ys = [], [], []
    for c in data['chars']:
        f = fonts[c['w']]
        gs, upm = f.getGlyphSet(), f['head'].unitsPerEm
        gname = f.getBestCmap()[ord(c['ch'])]
        s = c['fs'] / upm
        tr = (s, 0, 0, -s, c['x'], c['y'])
        pen = SVGPathPen(gs)
        gs[gname].draw(TransformPen(pen, tr))
        paths.append(pen.getCommands())
        bp = BoundsPen(gs)
        gs[gname].draw(TransformPen(bp, tr))
        if bp.bounds:
            x0, y0, x1, y1 = bp.bounds
            xs += [x0, x1]; ys += [y0, y1]
    b = data['bar']
    paths.append(f"M{b['x']:.3f} {b['y']:.3f}h{b['w']:.3f}v{b['h']:.3f}h{-b['w']:.3f}Z")
    xs += [b['x'], b['x'] + b['w']]; ys += [b['y'], b['y'] + b['h']]
    x0, y0, w, h = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
    d = ' '.join(paths)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {y0:.3f} {w:.3f} {h:.3f}" '
            f'width="{w:.2f}" height="{h:.2f}"><title>Personal Endocrine</title>'
            f'<path fill="{color}" d="{d}"/></svg>\n'), (w, h)


os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    os.remove(os.path.join(OUT, f))
tmp = S + '/render/vec'
os.makedirs(tmp, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1600, 'height': 900})
    for key, (fam, pkg, wp, we, t) in FONTS.items():
        fonts = {w: TTFont(woff(pkg, w)) for w in {wp, we}}
        for kind in ('logo', 'mark'):
            path = f'{tmp}/{key}-{kind}.html'
            open(path, 'w').write(page(kind, fam, pkg, wp, we, t))
            pg.goto('file://' + path)
            pg.wait_for_selector('body[data-done]')
            data = pg.evaluate(MEASURE)
            for cname, color in (('dark', INK), ('white', WHITE)):
                name = f'personal-endocrine-{key}-{kind}-{cname}'
                svg, (w, h) = build_svg(data, fonts, color)
                open(f'{OUT}/{name}.svg', 'w').write(svg)
                cairosvg.svg2pdf(bytestring=svg.encode(), write_to=f'{OUT}/{name}.pdf')
                cairosvg.svg2png(bytestring=svg.encode(), write_to=f'{OUT}/{name}.png', output_width=2000 if kind == 'logo' else 600)
                print(name, round(w, 1), round(h, 1))
    b.close()
