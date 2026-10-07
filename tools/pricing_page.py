"""Create Pricing.dc.html (shell from Diabetes page) and point every pricing link at it."""
import re, sys

P, BOOK = sys.argv[1], sys.argv[2]
rd = lambda p: open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)

main = rd(f'{P}/Main.dc.html')
shell = rd(f'{P}/Diabetes.dc.html')

# plan cards + their CSS come straight from the home page so both stay identical
ps = main.index('<div class="plans"')
depth, k = 0, ps
for m in re.finditer(r'<div\b|</div>', main[ps:]):
    depth += 1 if m.group(0) == '<div' else -1
    if depth == 0:
        k = ps + m.end(); break
plans = main[ps:k]
plan_css = '\n'.join(l for l in main.split('\n') if l.startswith(('.plan', '.plans')))

GROT = "font-family: 'Schibsted Grotesk', sans-serif;"
H2 = f'<h2 style="margin: 0; {GROT} font-weight: 700; font-size: clamp(28px, 2.6vw, 36px); line-height: 1.15; letter-spacing: -0.02em;">{{}}</h2>'
CHECK = ('<li style="display: flex; gap: 10px; align-items: flex-start;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#5C7A64" '
         'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="flex: none; margin-top: 4px;"><path d="M5 12l5 5L20 7"></path></svg><span>{}</span></li>')


def box(title, items, note=''):
    lis = ''.join(CHECK.format(i) for i in items)
    n = f'<p style="margin: 0; font-size: 15px; color: #5D635D;">{note}</p>' if note else ''
    return (f'<div style="flex: 1 1 320px; min-width: 0; background: #F8F8F4; border: 1px solid #D8DAD0; border-radius: 24px; padding: 32px; display: flex; flex-direction: column; gap: 16px;">'
            f'<div style="{GROT} font-weight: 600; font-size: 22px;">{title}</div>'
            f'<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 10px; font-size: 17px; color: #3A403B;">{lis}</ul>{n}</div>')


POLICIES = [
    ('New patient deposit', 'A non-refundable $75 deposit is due when your appointment is confirmed. It’s credited toward your visit.'),
    ('Payment', 'You pay Personal Endocrine directly, at the time of your visit.'),
    ('Memberships', 'Memberships are optional. You can cancel with 30 days’ notice. If you re-enroll later, a $300 re-enrollment fee applies.'),
    ('Superbills', 'If you have commercial insurance, we can provide a superbill on request that you may submit for possible out-of-network reimbursement. Coverage varies by plan.'),
    ('Medicare and Medi-Cal', 'Dr. Choi has opted out of Medicare, so visits can’t be submitted to Medicare for reimbursement. Personal Endocrine also does not accept Medi-Cal.'),
    ('Primary care', 'Dr. Choi specializes in endocrinology and does not provide primary care. Please keep a primary care physician for needs outside endocrinology.'),
]
rows = ''.join(
    f'<div class="pol" style="display: grid; grid-template-columns: 260px 1fr; gap: 8px 32px; padding: 22px 0; border-top: 1px solid #D8DAD0;">'
    f'<div style="font-weight: 600; font-size: 17px; color: #252A26;">{t}</div><div style="font-size: 17px; color: #3A403B;">{d}</div></div>'
    for t, d in POLICIES)

content = f'''<section style="max-width: 1200px; margin: 0 auto; padding: 64px 24px 72px; display: flex; flex-direction: column; gap: 16px;">
<span style="font-size: 14px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: {{{{accent}}}};">Pricing</span>
<h1 style="margin: 0; {GROT} font-weight: 700; font-size: clamp(34px, 3.4vw, 48px); line-height: 1.1; letter-spacing: -0.02em;">Simple, transparent pricing.</h1>
<p style="margin: 0; font-size: 23px; line-height: 1.4; font-weight: 500; color: #252A26; max-width: 760px;">You pay the practice directly, at the time of your visit. Every plan starts with an initial consultation, where you and Dr. Choi decide what level of care fits.</p>
<p style="margin: 0 0 24px; font-size: 15px; color: #5D635D;">Grand opening rates shown.</p>
{plans}
</section>

<section style="background: #E4E6DE; border-top: 1px solid #D8DAD0; border-bottom: 1px solid #D8DAD0;">
<div style="max-width: 1200px; margin: 0 auto; padding: 72px 24px; display: flex; flex-direction: column; gap: 28px;">
{H2.format('What you pay us, and what insurance still covers')}
<p style="margin: 0; font-size: 18px; color: #3A403B; max-width: 760px;">Personal Endocrine doesn’t bill insurance for your visits. You can still use your insurance for the care that happens outside the exam room.</p>
<div style="display: flex; flex-wrap: wrap; gap: 20px;">
{box('Paid directly to Personal Endocrine', ['Visits with Dr. Choi', 'Membership and program fees', 'Prior authorizations, appeals and forms, unless included in your plan'])}
{box('Still through your insurance', ['Labs', 'Imaging and other testing', 'Prescriptions'], 'Coverage varies by plan, so please confirm the details with your insurer.')}
</div>
</div>
</section>

<section style="max-width: 1200px; margin: 0 auto; padding: 72px 24px 96px; display: flex; flex-direction: column; gap: 20px;">
{H2.format('Good to know')}
<div style="border-bottom: 1px solid #D8DAD0;">{rows}</div>
<div style="margin-top: 28px; display: flex; flex-wrap: wrap; gap: 14px 24px; align-items: center;">
<a href="Book.dc.html" style="background: {{{{accent}}}}; color: #FFFFFF; text-decoration: none; padding: 15px 28px; border-radius: 999px; font-weight: 600; font-size: 17px; min-height: 44px; box-sizing: border-box; display: inline-flex; align-items: center;">Request a consultation</a>
<span style="font-size: 16px; color: #4A504A;">Questions about cost? Call <a href="tel:9494412164" style="font-weight: 600;">(949) 441-2164</a>.</span>
</div>
</section>'''

# swap main content: everything from the hero section to the end of "Additional specialties"
i = shell.index('<section style="max-width: 1200px; margin: 0 auto; padding: 64px 24px 88px;')
a = shell.index('Additional specialties</div>')
j = shell.index('</section>', a) + len('</section>')
page = shell[:i] + content + shell[j:]
page = page.replace('<title>Type 1 and Type 2 Diabetes</title>', '<title>Pricing</title>')
css = plan_css + '\n@media (max-width:640px){.pol{grid-template-columns:1fr !important}}\n'
k = page.index('</style>'); page = page[:k] + css + '\n' + page[k:]
wr(f'{P}/Pricing.dc.html', page)

# point pricing links at the new page (home hero "See pricing" keeps scrolling to the home section)
TEXTS = ('Pricing', 'Pricing and memberships', 'See all pricing', 'See pricing and programs')
pat = re.compile(r'<a href="(?:Main\.dc\.html|#pricing)"([^>]*)>(' + '|'.join(re.escape(t) for t in TEXTS) + r')</a>')
import glob
for f in glob.glob(f'{P}/*.dc.html') + [BOOK]:
    s = rd(f); n = len(pat.findall(s))
    if n:
        wr(f, pat.sub(lambda m: f'<a href="Pricing.dc.html"{m.group(1)}>{m.group(2)}</a>', s)); print(f.rsplit('/', 1)[-1], n)

# home: link from the pricing section to the full page
h = rd(f'{P}/Main.dc.html')
pe = h.index('<div class="plans"'); depth = 0
for m in re.finditer(r'<div\b|</div>', h[pe:]):
    depth += 1 if m.group(0) == '<div' else -1
    if depth == 0:
        end = pe + m.end(); break
link = '\n<a href="Pricing.dc.html" style="align-self: flex-start; font-weight: 600; font-size: 16px; color: {{accent}};">See full pricing, insurance and policies</a>'
if 'See full pricing, insurance and policies' not in h:
    h = h[:end] + link + h[end:]
h = h.replace('menopause, hypogonadism and other endocrine concerns', 'menopause, low testosterone and other endocrine concerns')
wr(f'{P}/Main.dc.html', h)
print('pricing page built')
