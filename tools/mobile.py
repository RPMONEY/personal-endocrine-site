import sys, os

BASE_CSS = """input::placeholder{color:#A6A199}
.mnav{display:none;position:relative}
.mnav>summary{list-style:none;cursor:pointer;width:44px;height:44px;display:flex;align-items:center;justify-content:center;border:1px solid #D8DAD0;border-radius:999px}
.mnav>summary::-webkit-details-marker{display:none}
.mnav-panel{position:absolute;right:0;top:52px;z-index:20;background:#F8F8F4;border:1px solid #D8DAD0;border-radius:18px;padding:10px;min-width:250px;display:flex;flex-direction:column;box-shadow:0 12px 32px rgba(30,29,27,.12)}
.mnav-panel a{color:#252A26;text-decoration:none;padding:12px 14px;border-radius:12px;font-weight:500;font-size:16px}
@media (max-width:760px){.nl{display:none !important}.mnav{display:block}}
"""
BOOK_CSS = """select{appearance:none;-webkit-appearance:none;padding-right:48px !important;background-image:linear-gradient(45deg,transparent 50%,#5D635D 50%),linear-gradient(135deg,#5D635D 50%,transparent 50%) !important;background-position:calc(100% - 24px) 52%,calc(100% - 18px) 52% !important;background-size:6px 6px,6px 6px !important;background-repeat:no-repeat !important}
"""
MAIN_CSS = """@media (max-width:760px){.badge{left:16px !important}}
"""
ICON = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#252A26" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"></path></svg>'
CTA = '<a href="Book.dc.html" style="background: #5C7A64; color: #FFFFFF; text-align: center; font-weight: 600; margin-top: 6px; border-radius: 999px;">Request a consultation</a>'

def menu(links):
    items = ''.join('<a href="%s">%s</a>' % (h, t) for h, t in links)
    return '<details class="mnav"><summary aria-label="Menu">%s</summary><div class="mnav-panel">%s<a href="tel:9494412164">(949) 441-2164</a>%s</div></details>\n' % (ICON, items, CTA)

MAIN_LINKS = [('#care', 'Specialties'), ('#how', 'Our approach'), ('#pricing', 'Pricing'), ('#doctor', 'Dr. Choi'), ('#faq', 'FAQ')]
SUB_LINKS = [('Main.dc.html', 'Home'), ('Main.dc.html', 'Specialties'), ('Main.dc.html', 'Pricing'), ('Main.dc.html', 'FAQ')]
NAV_DIV = '<div style="display: flex; flex-wrap: wrap; gap: 8px 28px; align-items: center; font-size: 15px; font-weight: 500;">'

for path in sys.argv[1:]:
    name = os.path.basename(path)
    s = open(path, encoding='utf-8').read()
    css = BASE_CSS
    if 'input::placeholder' in s:
        css = css.replace('input::placeholder{color:#A6A199}\n', '')
    if name == 'Book.dc.html':
        css += BOOK_CSS
    if name == 'Main.dc.html':
        css += MAIN_CSS
        s = s.replace('<div style="position: absolute; left: -24px;', '<div class="badge" style="position: absolute; left: -24px;', 1)
    i = s.index('</style>')
    s = s[:i] + css + s[i:]
    assert s.count(NAV_DIV) == 1, name
    s = s.replace(NAV_DIV, NAV_DIV.replace('<div ', '<div class="nl" '), 1)
    marker = '</nav>\n</header>'
    assert s.count(marker) == 1, name
    s = s.replace(marker, menu(MAIN_LINKS if name == 'Main.dc.html' else SUB_LINKS) + marker, 1)
    open(path, 'w', encoding='utf-8').write(s)
    print('ok', name)
