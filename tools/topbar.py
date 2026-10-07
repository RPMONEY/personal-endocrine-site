"""Shared dark top bar on every page (address left; phone + languages right); phone leaves the desktop nav."""
import sys
TOPBAR = ('<!-- Top bar -->\n<div style="background: #252A26; color: #DDD9D2; font-size: 14px;">\n'
          '<div style="max-width: 1200px; margin: 0 auto; padding: 10px 24px; display: flex; flex-wrap: wrap; gap: 8px 24px; justify-content: space-between; align-items: center;">\n'
          '<span style="display: flex; flex-wrap: wrap; gap: 4px 0; align-items: center;"><span class="tb-addr">12231 Newport Ave, North Tustin, CA 92705</span><span class="tb-addr" aria-hidden="true" style="width: 1px; height: 14px; background: #4A504B; margin: 0 18px;"></span><a href="tel:9494412164" style="color: #FFFFFF; font-weight: 600; text-decoration: none;">(949) 441-2164</a></span>\n'
          '<span style="display: flex; flex-wrap: wrap; gap: 4px 0; align-items: center;"><span class="tb-addr">In person or telehealth</span><span class="tb-addr" aria-hidden="true" style="width: 1px; height: 14px; background: #4A504B; margin: 0 18px;"></span><span>English · Español · 한국어</span></span>\n'
          '</div>\n</div>\n\n')
NAV_TEL = '<a href="tel:9494412164" style="color: #252A26; text-decoration: none;">(949) 441-2164</a>\n'
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    if '<!-- Top bar -->' in s:
        i = s.index('<!-- Top bar -->'); j = s.index('<!-- Nav -->', i)
        s = s[:i] + TOPBAR + s[j:]
    else:
        h = s.index('<header'); s = s[:h] + TOPBAR + s[h:]
    n = s.index('<div class="nl"'); e = s.index('</div>', n)
    block = s[n:e]
    assert block.count(NAV_TEL) == 1, p
    s = s[:n] + block.replace(NAV_TEL, '') + s[e:]
    assert s.count('<!-- Top bar -->') == 1
    open(p, 'w', encoding='utf-8').write(s); print('ok', p.rsplit('/', 1)[-1])
