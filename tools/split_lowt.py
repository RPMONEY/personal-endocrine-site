import re, sys
P, BOOK = sys.argv[1], sys.argv[2]
rd = lambda p: open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)

# ---------- 1. Low T page from the Menopause page ----------
m = rd(f'{P}/Menopause.dc.html')
chip = lambda t: f'<span style="background: #E4E6DE; border-radius: 999px; padding: 8px 16px; font-size: 15px;">{t}</span>'
chips_old = ''.join(chip(t) + '\n' for t in ['Fatigue', 'Hot flashes', 'Weight changes', 'Decreased libido', 'Disrupted sleep'])
assert chips_old in m
H1 = "font-weight: 700; font-size: clamp(38px, 4.6vw, 60px); line-height: 1.05; letter-spacing: -0.025em; max-width: 820px;\">"
lead_old = 'When the ovaries or testes stop producing enough sex hormones, the effects reach into everyday life: your energy, your sleep and your weight.'
intro_old = 'When the gonads (ovaries and testes) no longer produce enough estrogen, progesterone or testosterone, many people start to experience:'
close_old = 'Based on your individual medical history, Dr. Choi can offer safe hormonal and non-hormonal treatment options for women in menopause and for men with low testosterone.'
for x in (lead_old, intro_old, close_old, H1 + 'Menopause and Male Hypogonadism</h1>', 'Talk with Dr. Choi about your hormones', '<title>Menopause and Male Hypogonadism</title>'):
    assert m.count(x) == 1, x[:50]

low = (m.replace(H1 + 'Menopause and Male Hypogonadism</h1>', H1 + 'Low Testosterone in Men</h1>')
        .replace('<title>Menopause and Male Hypogonadism</title>', '<title>Low Testosterone in Men</title>')
        .replace(lead_old, 'When the testes stop producing enough testosterone, the effects reach into everyday life: your energy, your sleep and your weight.')
        .replace(intro_old, 'When the testes no longer produce enough testosterone, many men start to experience:')
        .replace(chips_old, ''.join(chip(t) + '\n' for t in ['Fatigue', 'Weight changes', 'Decreased libido', 'Disrupted sleep']))
        .replace(close_old, 'Based on your individual medical history, Dr. Choi can offer safe hormonal and non-hormonal treatment options for men with low testosterone.')
        .replace('Talk with Dr. Choi about your hormones', 'Talk with Dr. Choi about low testosterone'))
meno = (m.replace(H1 + 'Menopause and Male Hypogonadism</h1>', H1 + 'Menopause</h1>')
         .replace('<title>Menopause and Male Hypogonadism</title>', '<title>Menopause</title>')
         .replace(lead_old, 'When the ovaries stop producing enough estrogen and progesterone, the effects reach into everyday life: your energy, your sleep and your weight.')
         .replace(intro_old, 'When the ovaries no longer produce enough estrogen and progesterone, many women start to experience:')
         .replace(close_old, 'Based on your individual medical history, Dr. Choi can offer safe hormonal and non-hormonal treatment options for women in menopause.')
         .replace('Talk with Dr. Choi about your hormones', 'Talk with Dr. Choi about menopause'))
wr(f'{P}/Menopause.dc.html', meno)
wr(f'{P}/LowT.dc.html', low)

# ---------- 2. "Additional specialties" rows on every specialty page ----------
SPECS = [('Diabetes.dc.html', 'Type 1 and Type 2 Diabetes'), ('Weight.dc.html', 'Weight Management'),
         ('Thyroid.dc.html', 'Thyroid'), ('Parathyroid.dc.html', 'Parathyroid'), ('Osteoporosis.dc.html', 'Osteoporosis'),
         ('Menopause.dc.html', 'Menopause'), ('LowT.dc.html', 'Low Testosterone in Men')]
SPEC_A = '<a href="{f}" class="spec" style="color: #252A26; text-decoration: none; font-weight: 500; font-size: 16px; min-height: 44px; display: inline-flex; align-items: center;">{t}</a>'
for f, _ in SPECS:
    s = rd(f'{P}/{f}')
    i = s.index('<a href="', s.index('Additional specialties</div>'))
    j = s.index('</div>', i)
    s = s[:i] + '\n'.join(SPEC_A.format(f=g, t=t) for g, t in SPECS if g != f) + '\n' + s[j:]
    wr(f'{P}/{f}', s)

# ---------- 3. Home: 8 cards in a 4-across grid ----------
h = rd(f'{P}/Main.dc.html')
CARD = '<div style="background: #F8F8F4; border: 1px solid #D8DAD0; border-radius: 20px; padding: 32px; display: flex; flex-direction: column; gap: 12px;">'
mi = h.index('Menopause and Male Hypogonadism</h3>')
cs = h.rindex(CARD, 0, mi); ce = h.index('</div>', h.index('href="Menopause.dc.html"', mi)) + 6
meno_card = h[cs:ce]
learn = meno_card[meno_card.index('<a href="Menopause.dc.html"'):]
icon_m = meno_card[meno_card.index('<svg'):meno_card.index('</svg>') + 6]
icon_t = icon_m.replace('<circle cx="12" cy="9" r="5"></circle><path d="M12 14v7M9 18h6"></path>',
                        '<circle cx="10" cy="14" r="5"></circle><path d="M13.5 10.5L20 4M15 4h5v5"></path>')
H3 = '<h3 style="margin: 0; font-family: \'Schibsted Grotesk\', sans-serif; font-size: 22px; font-weight: 600;">'
PP = '<p style="margin: 0; color: #4A504A; font-size: 16px;">'
new_meno = (CARD + '\n' + icon_m + '\n' + H3 + 'Menopause</h3>\n' + PP +
            'Care for hot flashes, fatigue, weight changes, low libido and poor sleep, with hormonal and non-hormonal options based on your medical history.</p>\n' + learn)
new_lowt = (CARD + '\n' + icon_t + '\n' + H3 + 'Low Testosterone in Men</h3>\n' + PP +
            'Care for fatigue, weight changes, low libido and poor sleep caused by low testosterone, with treatment based on your medical history.</p>\n' + learn.replace('Menopause.dc.html', 'LowT.dc.html'))
cta = ('<div style="background: #5C7A64; color: #FFFFFF; border-radius: 20px; padding: 32px; display: flex; flex-direction: column; gap: 12px;">\n'
       + H3.replace('font-weight: 600;', 'font-weight: 600; color: #FFFFFF;') + 'Not sure where to start?</h3>\n'
       '<p style="margin: 0; color: #E4E6DE; font-size: 16px;">Tell us what you’re experiencing. Dr. Choi will help you understand what’s going on and what to do next.</p>\n'
       '<a href="Book.dc.html" style="margin-top: auto; align-self: flex-start; background: #FFFFFF; color: #252A26; font-weight: 600; font-size: 15px; text-decoration: none; padding: 12px 20px; border-radius: 999px; min-height: 44px; box-sizing: border-box; display: inline-flex; align-items: center;">Request a consultation</a>\n</div>')
h = h[:cs] + new_meno + '\n' + new_lowt + '\n' + cta + h[ce:]
g_old = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">'
gi = h.index(g_old, h.index('id="care"'))
h = h[:gi] + '<div class="cards" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;">' + h[gi + len(g_old):]
css = '@media (max-width:1100px){.cards{grid-template-columns:repeat(2,1fr) !important}}\n@media (max-width:640px){.cards{grid-template-columns:1fr !important}}\n'
k = h.index('</style>'); h = h[:k] + css + h[k:]
wr(f'{P}/Main.dc.html', h)

# ---------- 4. Request form options ----------
b = rd(BOOK)
assert b.count('<option>Menopause or male hypogonadism</option>') == 1
wr(BOOK, b.replace('<option>Menopause or male hypogonadism</option>', '<option>Menopause</option><option>Low testosterone</option>'))
print('split done')
