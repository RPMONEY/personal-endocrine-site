"""Dr. Choi bio page (DrChoi.dc.html), built from her published /about content only."""
import re, sys, glob

P, BOOK = sys.argv[1], sys.argv[2]
rd = lambda p: open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)

shell = rd(f'{P}/Diabetes.dc.html')
main = rd(f'{P}/Main.dc.html')
photo = re.search(r'/_blob/[0-9a-f]+', main).group(0)
GROT = "font-family: 'Schibsted Grotesk', sans-serif;"
H2 = f'<h2 style="margin: 0; {GROT} font-weight: 700; font-size: clamp(26px, 2.4vw, 32px); line-height: 1.2; letter-spacing: -0.015em;">{{}}</h2>'
ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'

CREDS = [('Medical degree', 'University of California, Irvine, School of Medicine'),
         ('Residency', 'Internal Medicine, Cedars-Sinai Medical Center'),
         ('Fellowship', 'Endocrinology, Diabetes and Metabolism, Harbor-UCLA Medical Center and City of Hope'),
         ('Board certification', 'Endocrinology and Obesity Medicine'),
         ('Hospital experience', 'Hoag Hospital and Kaiser Permanente, Orange County'),
         ('Languages', 'English, Spanish and Korean')]
creds = ''.join(
    f'<div class="cred" style="display: grid; grid-template-columns: 200px 1fr; gap: 4px 24px; padding: 18px 0; border-top: 1px solid #D8DAD0;">'
    f'<div style="font-size: 13px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #5D635D; padding-top: 3px;">{t}</div>'
    f'<div style="font-size: 18px; color: #252A26;">{d}</div></div>' for t, d in CREDS)

SPECS = [('Diabetes.dc.html', 'Type 1 and Type 2 Diabetes'), ('Weight.dc.html', 'Weight Management'), ('Thyroid.dc.html', 'Thyroid'),
         ('Parathyroid.dc.html', 'Parathyroid'), ('Osteoporosis.dc.html', 'Osteoporosis'), ('Menopause.dc.html', 'Menopause'),
         ('LowT.dc.html', 'Low Testosterone in Men')]
specs = ''.join(
    f'<a href="{h}" style="display: flex; justify-content: space-between; align-items: center; gap: 12px; background: #F8F8F4; border: 1px solid #D8DAD0; '
    f'border-radius: 14px; padding: 14px 18px; color: #252A26; text-decoration: none; font-weight: 600; font-size: 16px;">{t}<span style="color: {{{{accent}}}}; display: inline-flex;">{ARROW}</span></a>'
    for h, t in SPECS)

content = f'''<section style="max-width: 1200px; margin: 0 auto; padding: 64px 24px 72px; display: flex; flex-wrap: wrap; gap: 56px; align-items: center;">
<div style="flex: 999 1 520px; min-width: 0; display: flex; flex-direction: column; gap: 18px;">
<span style="font-size: 14px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: {{{{accent}}}};">Meet your doctor</span>
<h1 style="margin: 0; {GROT} font-weight: 700; font-size: clamp(38px, 4vw, 56px); line-height: 1.05; letter-spacing: -0.025em;">Jinsun Choi, MD</h1>
<p style="margin: 0; font-size: 23px; line-height: 1.4; font-weight: 500; color: #252A26; max-width: 640px;">Board-certified in Endocrinology and Obesity Medicine, practicing in Orange County for more than 15 years.</p>
<p style="margin: 0; font-size: 18px; line-height: 1.65; color: #3A403B; max-width: 640px;">Dr. Choi specializes in diabetes, metabolism and obesity medicine, and cares for patients with thyroid and parathyroid conditions, osteoporosis and hormone concerns. She sees patients in person in North Tustin or by telehealth, in English, Spanish or Korean.</p>
<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 6px;">
<a href="Book.dc.html" style="background: {{{{accent}}}}; color: #FFFFFF; text-decoration: none; padding: 15px 28px; border-radius: 999px; font-weight: 600; font-size: 17px; min-height: 44px; box-sizing: border-box; display: inline-flex; align-items: center;">Request a consultation</a>
<a href="tel:9494412164" style="border: 1.5px solid #252A26; color: #252A26; text-decoration: none; padding: 15px 28px; border-radius: 999px; font-weight: 600; font-size: 17px; min-height: 44px; box-sizing: border-box; display: inline-flex; align-items: center;">Call (949) 441-2164</a>
</div>
</div>
<div style="flex: 1 1 340px; min-width: 0; max-width: 460px;">
<img src="{photo}" alt="Dr. Jinsun Choi, board-certified endocrinologist" style="display: block; width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: 28px; background: #E4E6DE;">
</div>
</section>

<section style="background: #E4E6DE; border-top: 1px solid #D8DAD0; border-bottom: 1px solid #D8DAD0;">
<div style="max-width: 1200px; margin: 0 auto; padding: 72px 24px; display: flex; flex-wrap: wrap; gap: 48px;">
<div style="flex: 1 1 340px; min-width: 0;">{H2.format('About Dr. Choi')}</div>
<div style="flex: 999 1 560px; min-width: 0; max-width: 720px; display: flex; flex-direction: column; gap: 18px; font-size: 18px; line-height: 1.65; color: #3A403B;">
<p style="margin: 0;">Dr. Jinsun Choi has practiced endocrinology in Orange County for more than 15 years. She has been affiliated with Hoag Hospital and Kaiser Permanente. She is board-certified in Endocrinology and Obesity Medicine, and her clinical focus is diabetes, metabolism and obesity medicine, along with thyroid and parathyroid conditions, osteoporosis and hormone concerns.</p>
<p style="margin: 0;">She earned her medical degree at the University of California, Irvine, School of Medicine, completed her residency in internal medicine at Cedars-Sinai Medical Center, and completed her fellowship in endocrinology, diabetes and metabolism at Harbor-UCLA Medical Center and City of Hope.</p>
<p style="margin: 0;">She founded Personal Endocrine in her pursuit of “practicing medicine with passion and discernment, and providing a personal solution to common endocrine conditions.” Working outside insurance removes “the barriers of insurance and paperwork,” so visits can be about the patient: time to listen, to walk through lab results, and to make decisions together.</p>
<p style="margin: 0;">Dr. Choi believes “great care starts with a real relationship.” Her goal is to build “meaningful patient-doctor relationships with her patients, based on mutual respect and trust,” with a doctor “who knows your story, understands your goals,” and stays with you from one visit to the next.</p>
</div>
</div>
</section>

<section style="max-width: 1200px; margin: 0 auto; padding: 72px 24px; display: flex; flex-wrap: wrap; gap: 48px;">
<div style="flex: 1 1 340px; min-width: 0;">{H2.format('Training and experience')}</div>
<div style="flex: 999 1 560px; min-width: 0; max-width: 720px; border-bottom: 1px solid #D8DAD0;">{creds}</div>
</section>

<section style="max-width: 1200px; margin: 0 auto; padding: 0 24px 96px;">
<div style="background: {{{{accent}}}}; color: #FFFFFF; border-radius: 28px; padding: clamp(32px, 4vw, 56px); display: flex; flex-wrap: wrap; gap: 24px 40px; align-items: center; justify-content: space-between;">
<div style="display: flex; flex-direction: column; gap: 8px; max-width: 620px;">
<div style="font-family: 'Schibsted Grotesk', sans-serif; font-weight: 700; font-size: clamp(26px, 2.6vw, 34px); line-height: 1.15; letter-spacing: -0.015em;">Meet with Dr. Choi.</div>
<div style="font-size: 17px; color: #E4E6DE;">Up to an hour at your first visit. Most appointments within 1 to 3 business days.</div>
</div>
<a href="Book.dc.html" style="background: #FFFFFF; color: #252A26; text-decoration: none; padding: 15px 28px; border-radius: 999px; font-weight: 600; font-size: 17px; min-height: 44px; box-sizing: border-box; display: inline-flex; align-items: center;">Request a consultation</a>
</div>
</section>'''

i = shell.index('<section style="max-width: 1200px; margin: 0 auto; padding: 64px 24px 88px;')
a = shell.index('Additional specialties</div>')
j = shell.index('</section>', a) + len('</section>')
page = shell[:i] + content + shell[j:]
page = page.replace('<title>Type 1 and Type 2 Diabetes</title>', '<title>Jinsun Choi, MD</title>')
css = ('@media (max-width:640px){.cred{grid-template-columns:1fr !important}section[style*="padding: 72px 24px 0"]{padding:44px 24px 0 !important}'
       'section[style*="padding: 64px 24px 72px"]{padding:40px 24px 48px !important}'
       'div[style*="padding: 72px 24px;"]{padding:44px 24px !important}'
       'section[style*="padding: 72px 24px;"]{padding:44px 24px !important}'
       'section[style*="padding: 0 24px 96px"]{padding:0 24px 56px !important}}\n')
k = page.index('</style>'); page = page[:k] + css + page[k:]
wr(f'{P}/DrChoi.dc.html', page)

# point "Dr. Choi" nav, footer "Meet Dr. Choi" and the home "full bio" link at the new page
pat = re.compile(r'<a href="(?:Main\.dc\.html|#doctor)"([^>]*)>(Dr\. Choi|Meet Dr\. Choi|Read Dr\. Choi’s full bio|Read Dr\. Choi\'s full bio)</a>')
for f in glob.glob(f'{P}/*.dc.html') + [BOOK]:
    s = rd(f); n = len(pat.findall(s))
    if n:
        wr(f, pat.sub(lambda m: f'<a href="DrChoi.dc.html"{m.group(1)}>{m.group(2)}</a>', s)); print(f.rsplit('/', 1)[-1], n)
print('bio page built')
