"""Swap the Montserrat PERSONAL/ENDOCRINE lockup into nav + footer, and add Montserrat to the font link."""
import sys

def lockup(size, color):
    return (f'<span style="display: inline-flex; flex-direction: column; align-items: center; gap: {size*0.12:.1f}px; line-height: 1; color: {color}; font-family: \'Montserrat\', sans-serif; font-weight: 500;">'
            f'<span style="font-size: {size}px; letter-spacing: 0.08em; margin-right: -0.08em; white-space: nowrap;">PERS'
            f'<span style="position: relative; top: -0.155em; font-size: 0.86em;">O</span>'
            f'<span aria-hidden="true" style="display: inline-block; width: 0.621em; height: 0.07em; margin-left: -0.752em; margin-right: 0.131em; background: currentColor;"></span>NAL</span>'
            f'<span style="font-size: {size*0.46:.1f}px; letter-spacing: 0.34em; margin-right: -0.34em; white-space: nowrap;">ENDOCRINE</span></span>')

NAV_OLD = ('<svg width="34" height="34" viewBox="0 0 40 40" aria-hidden="true" style="display: block; flex: none;"><circle cx="20" cy="15" r="8.5" fill="none" stroke="#5C7A64" stroke-width="4"></circle><rect x="9" y="29" width="22" height="4" rx="2" fill="#5C7A64"></rect></svg>\n'
           '<span style="font-family: \'Schibsted Grotesk\', sans-serif; font-weight: 700; font-size: 21px; letter-spacing: -0.01em;">Personal Endocrine</span>')
FOOT_OLD = ('<span style="display: flex; align-items: center; gap: 10px; font-family: \'Schibsted Grotesk\', sans-serif; font-weight: 700; font-size: 18px; color: #FFFFFF; margin-bottom: 4px;"><svg width="26" height="26" viewBox="0 0 40 40" aria-hidden="true" style="display: block; flex: none;"><circle cx="20" cy="15" r="8.5" fill="none" stroke="#9DB8A3" stroke-width="4"></circle><rect x="9" y="29" width="22" height="4" rx="2" fill="#9DB8A3"></rect></svg>Personal Endocrine</span>')
FOOT_NEW = '<span style="display: flex; margin-bottom: 8px;">' + lockup(20, '#FFFFFF') + '</span>'
FONT_OLD = 'family=Public+Sans:wght@400;500;600&amp;family=Schibsted'
FONT_NEW = 'family=Montserrat:wght@500&amp;family=Public+Sans:wght@400;500;600&amp;family=Schibsted'

if __name__ == '__main__':
    for p in sys.argv[1:]:
        s = open(p, encoding='utf-8').read()
        for old in (NAV_OLD, FOOT_OLD, FONT_OLD):
            assert s.count(old) == 1, (p, old[:40])
        s = s.replace(NAV_OLD, lockup(22, '#252A26')).replace(FOOT_OLD, FOOT_NEW).replace(FONT_OLD, FONT_NEW)
        open(p, 'w', encoding='utf-8').write(s)
        print('ok', p.rsplit('/', 1)[-1])
