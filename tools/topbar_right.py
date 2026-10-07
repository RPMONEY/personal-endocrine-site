import sys
OLD_ADDR = '12231 Newport Ave, North Tustin, CA 92705 · In person and telehealth</span>'
NEW_ADDR = '12231 Newport Ave, North Tustin, CA 92705</span>'
OLD_R = '<span>English · Español · 한국어</span>\n</div>'
NEW_R = ('<span style="display: flex; flex-wrap: wrap; gap: 4px 0; align-items: center;"><span class="tb-addr">In person or telehealth</span>'
         '<span class="tb-addr" aria-hidden="true" style="width: 1px; height: 14px; background: #4A504B; margin: 0 18px;"></span>'
         '<span>English · Español · 한국어</span></span>\n</div>')
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    assert s.count(OLD_ADDR) == 1 and s.count(OLD_R) == 1, p
    s = s.replace(OLD_ADDR, NEW_ADDR).replace(OLD_R, NEW_R)
    open(p, 'w', encoding='utf-8').write(s); print('ok', p.rsplit('/', 1)[-1])
