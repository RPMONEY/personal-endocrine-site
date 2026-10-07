import sys

PANEL_OPEN = '<div style="width: calc(100% - 48px); max-width: 1152px; margin: 8px auto 40px; box-sizing: border-box; background: #2F3531;'
FOOTER_OPEN = '<footer style="background: #252A26; color: #D9D6D0; font-size: 15px;">'
GRID_PAD = 'padding: 72px 24px 48px; display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 40px 32px;'

for path in sys.argv[1:]:
    s = open(path, encoding='utf-8').read()
    start = s.index(PANEL_OPEN)
    # panel ends at the first '</div>\n</div>\n' after the submit button
    btn = s.index('>Subscribe</button>', start)
    end = s.index('\n', btn) + 1          # end of button line
    for _ in range(2):                    # container close, then panel close
        line_end = s.index('\n', end)
        assert s[end:line_end] in ('</div>', '</form>'), repr(s[end:line_end])
        end = line_end + 1
    panel = s[start:end]
    s = s[:start] + s[end:]
    panel = panel.replace('margin: 8px auto 40px;', 'margin: 56px auto 0;', 1)
    i = s.index(FOOTER_OPEN) + len(FOOTER_OPEN)
    s = s[:i] + '\n' + panel.rstrip('\n') + s[i:]
    s = s.replace(GRID_PAD, GRID_PAD.replace('72px 24px 48px', '48px 24px 48px'), 1)
    open(path, 'w', encoding='utf-8').write(s)
    print('moved', path)
