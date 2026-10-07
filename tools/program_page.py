"""Create Program.dc.html (Diabetes and Weight Management Program) and link to it.
Only facts already published by the practice: price, schedule, inclusions, consultation first."""
import re, sys, glob

P = sys.argv[1]
rd = lambda p: open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)

shell = rd(f'{P}/Diabetes.dc.html')
GROT = "font-family: 'Schibsted Grotesk', sans-serif;"
CHECK = ('<li style="display: flex; gap: 12px; align-items: flex-start;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#5C7A64" '
         'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="flex: none; margin-top: 3px;"><path d="M5 12l5 5L20 7"></path></svg><span>{}</span></li>')
H2 = f'<h2 style="margin: 0; {GROT} font-weight: 700; font-size: clamp(26px, 2.4vw, 32px); line-height: 1.2; letter-spacing: -0.015em;">{{}}</h2>'

STAGES = [
    ('Start with an initial consultation', 'Up to an hour with Dr. Choi to review your health history, medications, lab results and goals. Together you decide whether the program is the right fit.'),
    ('Visits every two weeks for six months', 'Frequent follow-up means your plan can be adjusted as you go, rather than waiting months between appointments.'),
    ('Support between visits', 'Glucose log and CGM reviews, direct telephone visits and portal messaging with Dr. Choi when questions come up.'),
]
stages = ''.join(
    f'<div style="display: flex; flex-direction: column; gap: 6px; padding: 20px 0; border-top: 1px solid #D8DAD0;">'
    f'<div style="{GROT} font-weight: 600; font-size: 20px; color: #252A26;">{t}</div><p style="margin: 0;">{d}</p></div>' for t, d in STAGES)

INCLUDED = ['Follow-up visit with Dr. Choi every two weeks', 'Direct telephone visits', 'Glucose log and CGM reviews',
            'Direct portal messaging with Dr. Choi', 'Prior authorizations, appeals and forms included']

content = f'''<section style="max-width: 1200px; margin: 0 auto; padding: 64px 24px 88px; display: flex; flex-wrap: wrap; gap: 48px; align-items: start;">
<div style="flex: 999 1 560px; min-width: 0; display: flex; flex-direction: column; gap: 16px;">
<a href="Pricing.dc.html" style="font-size: 14px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: {{{{accent}}}}; text-decoration: none;">Pricing and programs</a>
<h1 style="margin: 0; {GROT} font-weight: 700; font-size: clamp(34px, 3.4vw, 48px); line-height: 1.1; letter-spacing: -0.02em; max-width: 820px;">Diabetes and Weight Management Program</h1>
<p style="margin: 0; font-size: 23px; line-height: 1.4; font-weight: 500; color: #252A26; max-width: 720px;">Six months of close, physician-led care for diabetes, weight or both.</p>
<article style="margin-top: 24px; max-width: 720px; display: flex; flex-direction: column; gap: 18px; font-size: 18px; line-height: 1.65; color: #3A403B;">
<p style="margin: 0;">Diabetes and weight both respond to steady attention. A plan that looks good on paper often needs adjusting once real life, new medications and new numbers come into it. This program is built for that: frequent visits with Dr. Choi and support between them, for six months.</p>
{H2.format('How it works')}
<div style="border-bottom: 1px solid #D8DAD0;">{stages}</div>
{H2.format('What’s included')}
<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 12px;">{''.join(CHECK.format(i) for i in INCLUDED)}</ul>
<p style="margin: 8px 0 0;">Learn more about how Dr. Choi approaches <a href="Diabetes.dc.html">diabetes</a> and <a href="Weight.dc.html">weight management</a>.</p>
</article>
</div>
<aside class="side" style="flex: 1 1 320px; min-width: 0; background: #F8F8F4; border: 1px solid #D8DAD0; border-radius: 24px; padding: 32px; display: flex; flex-direction: column; gap: 14px;">
<div style="font-size: 13px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #5D635D;">Program pricing</div>
<div style="display: flex; align-items: baseline; gap: 6px;"><span style="{GROT} font-size: 48px; font-weight: 700; line-height: 1;">$360</span><span style="color: #5D635D;">/ month for 6 months</span></div>
<div style="font-size: 16px; color: #3A403B;">or <strong style="color: #252A26;">$2,000</strong> paid up front, a $160 savings.</div>
<div style="font-size: 15px; color: #5D635D; border-top: 1px solid #E4E6DE; padding-top: 14px;">Starts with an initial consultation ($400).</div>
<a href="Book.dc.html" style="text-align: center; background: {{{{accent}}}}; color: #FFFFFF; text-decoration: none; padding: 14px 24px; border-radius: 999px; font-weight: 600; min-height: 44px; box-sizing: border-box; margin-top: 6px;">Request a consultation</a>
<a href="tel:9494412164" style="text-align: center; font-weight: 600; font-size: 15px;">Or call (949) 441-2164</a>
<a href="Pricing.dc.html" style="text-align: center; font-size: 15px;">Compare all plans</a>
</aside>
</section>'''

i = shell.index('<section style="max-width: 1200px; margin: 0 auto; padding: 64px 24px 88px;')
a = shell.index('Additional specialties</div>')
j = shell.index('</section>', a) + len('</section>')
page = shell[:i] + content + shell[j:]
page = page.replace('<title>Type 1 and Type 2 Diabetes</title>', '<title>Diabetes and Weight Management Program</title>')
wr(f'{P}/Program.dc.html', page)

# link to it from the program pricing card (home + pricing page) and the Diabetes / Weight pages
CARD_DESC = '<div style="color: #4A504A; font-size: 16px;">A 6-month intensive program. $360 a month, or $2,000 paid up front.</div>'
LINK = '\n<a href="Program.dc.html" style="align-self: flex-start; margin-top: -8px; font-weight: 600; font-size: 15px; color: {{accent}}; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; min-height: 36px;">Learn more<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"></path></svg></a>'
for f in (f'{P}/Main.dc.html', f'{P}/Pricing.dc.html'):
    s = rd(f)
    if 'Program.dc.html' not in s:
        assert s.count(CARD_DESC) == 1, f
        s = s.replace(CARD_DESC, CARD_DESC + LINK)
        wr(f, s); print('card link', f.rsplit('/', 1)[-1])
w = rd(f'{P}/Weight.dc.html')
old = '<a href="Pricing.dc.html" style="font-weight: 600; font-size: 16px;">See all pricing</a>'
assert w.count(old) == 1
w = w.replace(old, '<a href="Program.dc.html" style="font-weight: 600; font-size: 16px;">How the program works</a>')
wr(f'{P}/Weight.dc.html', w)
d = rd(f'{P}/Diabetes.dc.html')
old = '<a href="Pricing.dc.html" style="font-weight: 600; font-size: 16px;">See pricing and programs</a>'
assert d.count(old) == 1
d = d.replace(old, '<a href="Program.dc.html" style="font-weight: 600; font-size: 16px;">About the Diabetes and Weight Management Program</a>')
wr(f'{P}/Diabetes.dc.html', d)
print('program page built')
