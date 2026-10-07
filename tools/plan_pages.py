"""Pay-per-visit and Ongoing care pages, on the same layout as the Program page.
Only facts the practice already publishes (prices, inclusions, FAQ policies)."""
import sys

P = sys.argv[1]
rd = lambda p: open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)

shell = rd(f'{P}/Diabetes.dc.html')
GROT = "font-family: 'Schibsted Grotesk', sans-serif;"
CHECK = ('<li style="display: flex; gap: 12px; align-items: flex-start;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#5C7A64" '
         'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="flex: none; margin-top: 3px;"><path d="M5 12l5 5L20 7"></path></svg><span>{}</span></li>')
H2 = f'<h2 style="margin: 0; {GROT} font-weight: 700; font-size: clamp(26px, 2.4vw, 32px); line-height: 1.2; letter-spacing: -0.015em;">{{}}</h2>'
ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'


def stages_html(stages):
    return '<div style="border-bottom: 1px solid #D8DAD0;">' + ''.join(
        f'<div style="display: flex; flex-direction: column; gap: 6px; padding: 20px 0; border-top: 1px solid #D8DAD0;">'
        f'<div style="{GROT} font-weight: 600; font-size: 20px; color: #252A26;">{t}</div><p style="margin: 0;">{d}</p></div>' for t, d in stages) + '</div>'


def price_table(rows):
    return '<div style="border-bottom: 1px solid #D8DAD0;">' + ''.join(
        f'<div style="display: flex; justify-content: space-between; gap: 24px; padding: 16px 0; border-top: 1px solid #D8DAD0;">'
        f'<span>{a}</span><span style="font-weight: 600; color: #252A26; white-space: nowrap;">{b}</span></div>' for a, b in rows) + '</div>'


def page(d):
    body = [f'<p style="margin: 0;">{t}</p>' for t in d['intro']]
    for kind, title, val in d['blocks']:
        body.append(H2.format(title))
        if kind == 'stages': body.append(stages_html(val))
        elif kind == 'table': body.append(price_table(val))
        elif kind == 'checks': body.append('<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 12px;">' + ''.join(CHECK.format(i) for i in val) + '</ul>')
        elif kind == 'paras': body += [f'<p style="margin: 0;">{t}</p>' for t in val]
    content = f'''<section style="max-width: 1200px; margin: 0 auto; padding: 64px 24px 88px; display: flex; flex-wrap: wrap; gap: 48px; align-items: start;">
<div style="flex: 999 1 560px; min-width: 0; display: flex; flex-direction: column; gap: 16px;">
<a href="Pricing.dc.html" style="font-size: 14px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: {{{{accent}}}}; text-decoration: none;">Pricing and programs</a>
<h1 style="margin: 0; {GROT} font-weight: 700; font-size: clamp(34px, 3.4vw, 48px); line-height: 1.1; letter-spacing: -0.02em; max-width: 820px;">{d['title']}</h1>
<p style="margin: 0; font-size: 23px; line-height: 1.4; font-weight: 500; color: #252A26; max-width: 720px;">{d['lead']}</p>
<article style="margin-top: 24px; max-width: 720px; display: flex; flex-direction: column; gap: 18px; font-size: 18px; line-height: 1.65; color: #3A403B;">
{chr(10).join(body)}
</article>
</div>
<aside class="side" style="flex: 1 1 320px; min-width: 0; background: #F8F8F4; border: 1px solid #D8DAD0; border-radius: 24px; padding: 32px; display: flex; flex-direction: column; gap: 14px;">
<div style="font-size: 13px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #5D635D;">{d['side_label']}</div>
<div style="display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap;"><span style="{GROT} font-size: 48px; font-weight: 700; line-height: 1;">{d['price']}</span><span style="color: #5D635D;">{d['price_note']}</span></div>
<div style="font-size: 16px; color: #3A403B;">{d['side_line']}</div>
<div style="font-size: 15px; color: #5D635D; border-top: 1px solid #E4E6DE; padding-top: 14px;">{d['side_small']}</div>
<a href="Book.dc.html" style="text-align: center; background: {{{{accent}}}}; color: #FFFFFF; text-decoration: none; padding: 14px 24px; border-radius: 999px; font-weight: 600; min-height: 44px; box-sizing: border-box; margin-top: 6px;">Request a consultation</a>
<a href="tel:9494412164" style="text-align: center; font-weight: 600; font-size: 15px;">Or call (949) 441-2164</a>
<a href="Pricing.dc.html" style="text-align: center; font-size: 15px;">Compare all plans</a>
</aside>
</section>'''
    i = shell.index('<section style="max-width: 1200px; margin: 0 auto; padding: 64px 24px 88px;')
    a = shell.index('Additional specialties</div>')
    j = shell.index('</section>', a) + len('</section>')
    out = shell[:i] + content + shell[j:]
    return out.replace('<title>Type 1 and Type 2 Diabetes</title>', f'<title>{d["title"]}</title>')


PAY = dict(
    title='Pay per visit', lead='See Dr. Choi when you need to, without a membership.',
    intro=['You don’t have to join anything to see Dr. Choi. With pay per visit, you pay for each visit at the time of care, and you and Dr. Choi decide together how often follow-up makes sense.',
           'It’s a good fit if you need a specialist evaluation or occasional follow-up for a condition that’s already well managed.'],
    blocks=[('table', 'Visit prices', [('Initial consultation, up to 1 hour, including a 10-minute call to review your results', '$400'),
                                       ('Follow-up, in person or telehealth, up to 30 minutes', '$180'),
                                       ('Telephone visit, up to 15 minutes', '$60'),
                                       ('Prior authorizations, appeals and forms', '$50')]),
            ('stages', 'How it works', [('Initial consultation', 'Up to an hour with Dr. Choi to go through your history, symptoms, medications and goals.'),
                                        ('Results call', 'A 10-minute call to walk through your lab results and what they mean for your care.'),
                                        ('Follow-up as needed', 'Book follow-up visits in person or by telehealth when you and Dr. Choi agree they’re needed.')]),
            ('paras', 'Good to know', ['New patients pay a non-refundable $75 deposit when the appointment is confirmed. It’s credited toward the visit.',
                                       'Personal Endocrine doesn’t bill insurance for visits, but you can still use your insurance for labs, imaging and prescriptions. If you have commercial insurance, we can provide a superbill on request.'])],
    side_label='Initial consultation', price='$400', price_note='',
    side_line='Up to an hour with Dr. Choi, plus a 10-minute results call.', side_small='Follow-ups $180. Telephone visits $60.')

ONGOING = dict(
    title='Ongoing care', lead='Consistent access to Dr. Choi for a chronic endocrine condition.',
    intro=['Ongoing care is a monthly membership for patients who want regular follow-up and a direct line to their endocrinologist, rather than starting from scratch at every appointment.',
           'It’s designed for chronic endocrine conditions that benefit from steady management, such as diabetes or thyroid disease.'],
    blocks=[('checks', 'What’s included each month', ['One follow-up visit with Dr. Choi', 'Direct telephone visits', 'Glucose log and CGM reviews',
                                                       'Direct portal messaging with Dr. Choi', 'Prior authorizations, appeals and forms included']),
            ('stages', 'How it works', [('Start with an initial consultation', 'Up to an hour with Dr. Choi. Together you decide whether ongoing care is the right level of support.'),
                                        ('Monthly follow-up', 'A follow-up visit each month keeps your treatment on track and adjusted as things change.'),
                                        ('Support between visits', 'Questions don’t have to wait. Message Dr. Choi through the portal or schedule a direct telephone visit.')]),
            ('paras', 'Membership terms', ['Membership is optional. You can cancel with 30 days’ notice. If you decide to re-enroll later, a $300 re-enrollment fee applies.',
                                           'Unlike a traditional concierge practice, Personal Endocrine doesn’t bill your insurance for visits on top of a membership fee. You can still use your insurance for labs, imaging and prescriptions.'])],
    side_label='Membership', price='$250', price_note='/ month',
    side_line='Monthly follow-up, phone visits, CGM reviews and direct messaging.', side_small='Starts with an initial consultation ($400). Cancel with 30 days’ notice.')

assert '—' not in str(PAY) + str(ONGOING)
wr(f'{P}/PayPerVisit.dc.html', page(PAY))
wr(f'{P}/Ongoing.dc.html', page(ONGOING))

# "Learn more" under the description on the two other pricing cards (home + pricing page)
LINK = ('\n<a href="{href}" style="align-self: flex-start; margin-top: -8px; font-weight: 600; font-size: 15px; color: {{{{accent}}}}; text-decoration: none; '
        'display: inline-flex; align-items: center; gap: 6px; min-height: 36px;">Learn more' + ARROW + '</a>')
DESCS = {'PayPerVisit.dc.html': '<div style="color: #4A504A; font-size: 16px;">Initial consultation, up to 1 hour. Includes a 10-minute call to review your results.</div>',
         'Ongoing.dc.html': '<div style="color: #4A504A; font-size: 16px;">For patients who want consistent access and ongoing management of a chronic endocrine condition.</div>'}
for f in ('Main.dc.html', 'Pricing.dc.html'):
    s = rd(f'{P}/{f}')
    for href, desc in DESCS.items():
        if f'href="{href}"' in s: continue
        assert s.count(desc) == 1, (f, href)
        s = s.replace(desc, desc + LINK.format(href=href))
    wr(f'{P}/{f}', s)
print('plan pages built')
