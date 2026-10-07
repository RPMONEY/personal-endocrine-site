"""Generate the Logo directions artboard (Logos.dc.html)."""
import sys

SAGE = '#5C7A64'
INK = '#252A26'


def o_glyph(color, caps=False):
    # raised ring over a bar: the "person" O from her original logo, at full letter size and stem weight
    if caps:  # ring spans most of cap height, bar on the baseline
        return (f'<svg viewBox="0 0 66 75" style="width:0.66em;height:0.75em;display:inline-block;vertical-align:0" aria-hidden="true">'
                f'<circle cx="33" cy="32" r="23.5" fill="none" stroke="{color}" stroke-width="11"></circle>'
                f'<rect x="7" y="65" width="52" height="10" rx="1" fill="{color}"></rect></svg>')
    # lowercase: ring the width of an o, lifted so its top rises above x-height
    return (f'<svg viewBox="0 0 58 75" style="width:0.58em;height:0.75em;display:inline-block;vertical-align:0" aria-hidden="true">'
            f'<circle cx="29" cy="34" r="20" fill="none" stroke="{color}" stroke-width="10"></circle>'
            f'<rect x="8" y="65" width="42" height="10" rx="1" fill="{color}"></rect></svg>')


def mark(color, size):
    return (f'<svg viewBox="0 0 40 40" width="{size}" height="{size}" aria-hidden="true" style="display:block;flex:none">'
            f'<circle cx="20" cy="15" r="8.5" fill="none" stroke="{color}" stroke-width="4"></circle>'
            f'<rect x="9" y="29" width="22" height="4" rx="2" fill="{color}"></rect></svg>')


def app_icon(size, radius):
    return (f'<svg viewBox="0 0 40 40" width="{size}" height="{size}" aria-hidden="true" style="display:block;flex:none">'
            f'<rect width="40" height="40" rx="{radius}" fill="{SAGE}"></rect>'
            f'<circle cx="20" cy="16" r="7.5" fill="none" stroke="#FFFFFF" stroke-width="3.6"></circle>'
            f'<rect x="10.5" y="28" width="19" height="3.6" rx="1.8" fill="#FFFFFF"></rect></svg>')


GROT = "font-family:'Schibsted Grotesk',sans-serif"
SANS = "font-family:'Public Sans',sans-serif"


def lockup(kind, scale, ink, accent):
    """scale = font-size of the main word in px."""
    if kind == 'E':  # Endocrine-led, title case: mark is the o in Endocrine
        return (f'<span style="display:inline-flex;flex-direction:column;align-items:flex-start;gap:{scale*0.1:.1f}px;line-height:1;color:{ink}">'
                f'<span style="{GROT};font-weight:600;font-size:{scale*0.44:.1f}px;letter-spacing:0.01em;white-space:nowrap">Personal</span>'
                f'<span style="{GROT};font-weight:700;font-size:{scale}px;letter-spacing:-0.02em;white-space:nowrap">End{o_glyph(accent)}crine</span></span>')
    if kind == 'F':  # Endocrine-led, caps
        return (f'<span style="display:inline-flex;flex-direction:column;align-items:center;gap:{scale*0.22:.1f}px;line-height:1;color:{ink}">'
                f'<span style="{SANS};font-weight:600;font-size:{scale*0.36:.1f}px;letter-spacing:0.5em;margin-right:-0.5em;white-space:nowrap">PERSONAL</span>'
                f'<span style="{GROT};font-weight:700;font-size:{scale}px;letter-spacing:0.06em;margin-right:-0.06em;white-space:nowrap">END{o_glyph(accent, caps=True)}CRINE</span></span>')
    if kind == 'A':  # title case, one line, raised o
        return (f'<span style="{GROT};font-weight:700;font-size:{scale}px;letter-spacing:-0.015em;color:{ink};white-space:nowrap;line-height:1">'
                f'Pers{o_glyph(accent)}nal Endocrine</span>')
    if kind == 'B':  # stacked caps: her structure, site type
        return (f'<span style="display:inline-flex;flex-direction:column;align-items:center;gap:{scale*0.28:.0f}px;line-height:1;color:{ink}">'
                f'<span style="{GROT};font-weight:700;font-size:{scale}px;letter-spacing:0.09em;margin-right:-0.09em;white-space:nowrap">PERS{o_glyph(accent, caps=True)}NAL</span>'
                f'<span style="{SANS};font-weight:600;font-size:{scale*0.4:.1f}px;letter-spacing:0.38em;margin-right:-0.38em;white-space:nowrap">ENDOCRINE</span></span>')
    if kind == 'C':  # symbol + wordmark
        return (f'<span style="display:inline-flex;align-items:center;gap:{scale*0.45:.0f}px;line-height:1;color:{ink}">'
                f'{mark(accent, round(scale*1.55))}'
                f'<span style="{GROT};font-weight:700;font-size:{scale}px;letter-spacing:-0.015em;white-space:nowrap">Personal Endocrine</span></span>')
    if kind == 'D':  # lowercase, two weights
        return (f'<span style="{GROT};font-size:{scale}px;letter-spacing:-0.02em;color:{ink};white-space:nowrap;line-height:1">'
                f'<span style="font-weight:700">pers{o_glyph(accent)}nal</span>'
                f'<span style="font-weight:500;color:{accent}"> endocrine</span></span>')


OPTIONS = [
    ('E', 'Endocrine-led, title case',
     'The person mark is the o in Endocrine. Personal sits above as the qualifier.', 28),
    ('F', 'Endocrine-led, caps',
     'Same idea in caps, centered. More formal; closest to her original layout.', 26),
    ('A', 'Title case, raised O',
     'Her O idea set in the site’s typeface. Reads as one name, works on one line at any size.', 21),
    ('B', 'Stacked caps',
     'Closest to her original. Weakness: ENDOCRINE drops to about 9px in the nav.', 24),
    ('C', 'Symbol + wordmark',
     'The O becomes a standalone symbol. Most flexible: symbol alone for favicon, social and signage.', 21),
    ('D', 'Lowercase, two weights',
     'Softest and most approachable. Sage “endocrine” carries the brand color.', 22),
]


def nav(kind, size):
    links = ''.join(f'<span style="font-size:15px;font-weight:500">{t}</span>' for t in
                    ['Specialties', 'Pricing', 'Dr. Choi', 'FAQ'])
    return (f'<div style="background:#F2F1EC;border:1px solid #D8DAD0;border-radius:16px;padding:18px 28px;display:flex;align-items:center;justify-content:space-between;gap:24px;color:{INK}">'
            f'{lockup(kind, size, INK, SAGE)}'
            f'<div style="display:flex;align-items:center;gap:24px">{links}'
            f'<span style="background:{SAGE};color:#fff;font-weight:600;font-size:15px;padding:12px 20px;border-radius:999px">Request a consultation</span></div></div>')


def mobile(kind, size):
    return (f'<div style="width:390px;flex:none;background:#F2F1EC;border:1px solid #D8DAD0;border-radius:16px;padding:16px 20px;display:flex;align-items:center;justify-content:space-between;box-sizing:border-box">'
            f'{lockup(kind, size, INK, SAGE)}'
            f'<span style="width:44px;height:44px;border:1px solid #D8DAD0;border-radius:999px;display:flex;align-items:center;justify-content:center;flex:none">'
            f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"></path></svg></span></div>')


def footer(kind):
    return (f'<div style="flex:1 1 0;min-width:0;background:{INK};border-radius:16px;padding:28px;display:flex;align-items:center;justify-content:center">'
            f'{lockup(kind, 20, "#FFFFFF", "#9DB8A3")}</div>')


def favicons(kind):
    tab = (f'<div style="display:flex;align-items:center;gap:8px;background:#FFFFFF;border:1px solid #D8DAD0;border-radius:10px 10px 0 0;padding:9px 14px;font-size:13px;color:{INK};width:200px">'
           f'{app_icon(16, 4)}<span style="white-space:nowrap;overflow:hidden">Personal Endocrine</span></div>')
    return (f'<div style="display:flex;align-items:flex-end;gap:20px;flex:none">'
            f'{app_icon(64, 15)}{app_icon(32, 8)}{tab}</div>')


def card(kind, name, blurb, nav_size):
    big = {'B': 60, 'E': 80, 'F': 70}.get(kind, 64)
    return f'''<section style="background:#F8F8F4;border:1px solid #D8DAD0;border-radius:28px;padding:40px;display:flex;flex-direction:column;gap:28px">
<div style="display:flex;justify-content:space-between;align-items:baseline;gap:24px">
<div style="display:flex;gap:14px;align-items:baseline"><span style="{GROT};font-weight:700;font-size:28px;color:{SAGE}">{kind}</span><span style="{GROT};font-weight:600;font-size:24px">{name}</span></div>
<span style="font-size:15px;color:#5D635D;max-width:560px;text-align:right">{blurb}</span></div>
<div style="background:#F2F1EC;border-radius:20px;height:240px;display:flex;align-items:center;justify-content:center">{lockup(kind, big, INK, SAGE)}</div>
{nav(kind, nav_size)}
<div style="display:flex;gap:20px;align-items:stretch">{mobile(kind, nav_size - 2)}{footer(kind)}{favicons(kind)}</div>
</section>'''


def page():
    cards = '\n'.join(card(*o) for o in OPTIONS)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Logo directions</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600&amp;family=Schibsted+Grotesk:wght@500;600;700&amp;display=swap">
<style>body{{margin:0;background:#E4E6DE}}</style>
</helmet>
<div style="width:1600px;background:#E4E6DE;color:{INK};{SANS};font-size:17px;line-height:1.5;padding:56px;box-sizing:border-box;display:flex;flex-direction:column;gap:32px">
<div style="display:flex;flex-direction:column;gap:8px">
<span style="{GROT};font-weight:700;font-size:40px;letter-spacing:-0.02em">Logo directions</span>
<span style="font-size:17px;color:#4A504A;max-width:900px">Her raised O, rebuilt in the site’s typeface and sage. Each shown at hero size, in the real nav, on mobile, in the footer and as the favicon.</span>
</div>
{cards}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1600,"height":3000}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''


open(sys.argv[1], 'w', encoding='utf-8').write(page())
print('ok')
