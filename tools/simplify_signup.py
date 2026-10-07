import sys, os

PANEL_OPEN = '<div style="width: calc(100% - 48px); max-width: 1152px; margin: 56px auto 0; box-sizing: border-box; background: #2F3531;'
LANG = '<span style="font-size: 14px; color: #A6A199;">English · Español · 한국어</span>'

def new_panel(tag):
    return (
        '<div style="width: calc(100% - 48px); max-width: 1152px; margin: 56px auto 0; box-sizing: border-box; border: 1px solid #3F4540; border-radius: 20px; padding: 22px 28px; display: flex; flex-wrap: wrap; gap: 16px 32px; align-items: center; justify-content: space-between;">\n'
        '<span style="font-family: \'Schibsted Grotesk\', sans-serif; font-weight: 600; font-size: 20px; color: #FFFFFF;">Stay in touch</span>\n'
        '<TAG style="display: flex; gap: 10px; flex: 0 1 460px; min-width: 0;">\n'
        '<input type="email" aria-label="Email address" placeholder="Email address" autocomplete="email" style="font: inherit; font-size: 15px; color: #FFFFFF; background: transparent; border: 1px solid #4A524C; border-radius: 999px; padding: 0 20px; height: 48px; flex: 1 1 auto; min-width: 0; box-sizing: border-box;">\n'
        '<button type="button" style="font: inherit; font-weight: 600; font-size: 15px; background: #5C7A64; color: #FFFFFF; border: 0; border-radius: 999px; padding: 0 26px; height: 48px; cursor: pointer; flex: none;">Subscribe</button>\n'
        '</TAG>\n'
        '</div>\n'
    ).replace('TAG', tag)

for path in sys.argv[1:]:
    name = os.path.basename(path)
    s = open(path, encoding='utf-8').read()
    start = s.index(PANEL_OPEN)
    btn = s.index('>Subscribe</button>', start)
    end = s.index('\n', btn) + 1
    for _ in range(2):
        le = s.index('\n', end)
        assert s[end:le] in ('</div>', '</form>'), (name, s[end:le])
        end = le + 1
    tag = 'form' if '<form' in s[start:end] else 'div'
    s = s[:start] + new_panel(tag) + s[end:]
    href = '#top' if name == 'Main.dc.html' else 'Main.dc.html'
    social = '\n<span style="display: flex; gap: 16px; font-size: 14px;"><a href="%s" style="color: #D9D6D0;">Facebook</a><a href="%s" style="color: #D9D6D0;">Instagram</a></span>' % (href, href)
    assert s.count(LANG) == 1, name
    s = s.replace(LANG, LANG + social, 1)
    open(path, 'w', encoding='utf-8').write(s)
    print('ok', name)
