"""Convert the Design canvas .dc.html pages into a static site for Cloudflare Pages.
usage: python3 build.py <src_project_dir> <headshot.jpg> <out_dir>
"""
import sys, os, re, shutil, json

SRC, HEADSHOT, OUT = sys.argv[1:4]
ACCENT = '#5C7A64'
ORIGIN = 'https://personalendocrine.com'
FB = 'https://www.facebook.com/profile.php?id=61577977966627'
IG = 'https://www.instagram.com/personal_endocrine/'
PHONE = '(949) 441-2164'

PAGES = {  # source file -> (output path, url path, title, description)
    'Main.dc.html': ('index.html', '/', 'Personal Endocrine | Endocrinologist in North Tustin, CA',
                     'Direct-pay endocrinology with Dr. Jinsun Choi in North Tustin, CA. Longer visits for diabetes, weight, thyroid, bone health, menopause and low testosterone.'),
    'Book.dc.html': ('appointment.html', '/appointment', 'Request a Consultation | Personal Endocrine',
                     'Request a consultation with Dr. Jinsun Choi, board-certified endocrinologist in North Tustin, CA. In person or telehealth.'),
    'Pricing.dc.html': ('pricing.html', '/pricing', 'Pricing, Memberships and Insurance | Personal Endocrine',
                        'Self-pay pricing for visits, the Ongoing Care membership and the Diabetes and Weight Management Program. Personal Endocrine does not bill insurance for visits.'),
    'Program.dc.html': ('diabetes-weight-program.html', '/diabetes-weight-program', 'Diabetes and Weight Management Program | Personal Endocrine',
                        'A six-month, physician-led program with Dr. Jinsun Choi: visits every two weeks, glucose log and CGM reviews, telephone visits and portal messaging.'),
    'PayPerVisit.dc.html': ('pay-per-visit.html', '/pay-per-visit', 'Pay Per Visit Endocrinology Pricing | Personal Endocrine',
                            'See Dr. Jinsun Choi without a membership: initial consultation, follow-up, telephone visit and forms pricing at Personal Endocrine in North Tustin.'),
    'Ongoing.dc.html': ('ongoing-care.html', '/ongoing-care', 'Ongoing Care Membership | Personal Endocrine',
                        'A $250 monthly membership with Dr. Jinsun Choi: monthly follow-up, telephone visits and direct portal messaging for chronic endocrine conditions.'),
    'DrChoi.dc.html': ('dr-choi.html', '/dr-choi', 'Jinsun Choi, MD, Endocrinologist | Personal Endocrine',
                       'Dr. Jinsun Choi is board-certified in Endocrinology and Obesity Medicine, trained at UC Irvine, Cedars-Sinai and Harbor-UCLA, with 15+ years in Orange County.'),
    'Diabetes.dc.html': ('diabetes.html', '/diabetes', 'Diabetes Specialist in North Tustin, CA | Personal Endocrine',
                         'Type 1 and type 2 diabetes care with Dr. Jinsun Choi in North Tustin: insulin and medication management, CGM and a plan that is realistic to live with.'),
    'Weight.dc.html': ('weight-management.html', '/weight-management', 'Medical Weight Loss in North Tustin, CA | Personal Endocrine',
                       'Physician-led obesity treatment with Dr. Jinsun Choi, board-certified in Obesity Medicine: nutrition, activity and, when appropriate, GLP-1 medications.'),
    'Thyroid.dc.html': ('thyroid.html', '/thyroid', 'Thyroid Specialist in North Tustin, CA | Personal Endocrine',
                        'Evaluation and treatment of hypothyroidism, hyperthyroidism and other thyroid conditions with Dr. Jinsun Choi, endocrinologist in North Tustin, CA.'),
    'Parathyroid.dc.html': ('parathyroid.html', '/parathyroid', 'Parathyroid &amp; Calcium Disorders | Personal Endocrine',
                            'Evaluation of high or low calcium, hyperparathyroidism and hypoparathyroidism with Dr. Jinsun Choi, endocrinologist in North Tustin, CA.'),
    'Osteoporosis.dc.html': ('osteoporosis.html', '/osteoporosis', 'Osteoporosis Doctor in North Tustin, CA | Personal Endocrine',
                             'Osteoporosis evaluation and treatment with Dr. Jinsun Choi in North Tustin: bone density, fracture risk assessment and a long-term plan to protect your bones.'),
    'Menopause.dc.html': ('menopause.html', '/menopause', 'Menopause Specialist in North Tustin, CA | Personal Endocrine',
                          'Menopause care with Dr. Jinsun Choi in North Tustin, including menopausal hormone therapy and non-hormonal options chosen around your health history.'),
    'Privacy.dc.html': ('privacy-policy.html', '/privacy-policy', 'Privacy Policy | Personal Endocrine',
                        'How Personal Endocrine, P.C. collects, uses and protects information when you visit our website.'),
    'NPP.dc.html': ('notice-of-privacy-practices.html', '/notice-of-privacy-practices', 'Notice of Privacy Practices | Personal Endocrine',
                    'How medical information about you may be used and disclosed at Personal Endocrine, P.C., and how you can get access to this information.'),
    'GFE.dc.html': ('good-faith-estimate.html', '/good-faith-estimate', 'Your Right to a Good Faith Estimate | Personal Endocrine',
                    'Because visits at Personal Endocrine are self-pay, you have the right to a Good Faith Estimate of expected charges under federal law.'),
    'Terms.dc.html': ('terms-of-use.html', '/terms-of-use', 'Terms of Use | Personal Endocrine',
                      'Terms that apply to your use of the Personal Endocrine, P.C. website.'),
    'Accessibility.dc.html': ('accessibility.html', '/accessibility', 'Accessibility Statement | Personal Endocrine',
                              'How to get help if you have difficulty accessing any part of the Personal Endocrine website.'),
    'LowT.dc.html': ('low-testosterone.html', '/low-testosterone', 'Low Testosterone in Men (Hypogonadism) | Personal Endocrine',
                     'Evaluation and treatment of low testosterone and male hypogonadism with Dr. Jinsun Choi: careful diagnosis with repeat morning testing before any therapy.'),
}
FILE_URL = {k: v[1] for k, v in PAGES.items()}

# link text -> home anchor (interior pages had every home link collapsed to Main.dc.html)
TEXT_ANCHOR = {
    'Specialties': '/#care', 'Our specialties': '/#care', 'Our approach': '/#how',
    'Pricing': '/#pricing', 'Pricing and memberships': '/#pricing', 'See pricing': '/#pricing',
    'See all pricing': '/#pricing', 'See pricing and programs': '/#pricing',
    'Dr. Choi': '/#doctor', 'Meet Dr. Choi': '/#doctor', 'FAQ': '/#faq',
    'Frequently asked questions': '/#faq',
}
PLACEHOLDER = {'Patient portal'}

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">'
           '<rect width="40" height="40" rx="9" fill="#252A26"/>'
           '<circle cx="20" cy="17" r="8.2" fill="none" stroke="#FFFFFF" stroke-width="3.4"/>'
           '<rect x="11" y="29" width="18" height="3.2" fill="#FFFFFF"/></svg>')

MAP = ('<iframe title="Map to Personal Endocrine, 12231 Newport Avenue, North Tustin" '
       'src="https://maps.google.com/maps?q=12231+Newport+Ave,+North+Tustin,+CA+92705&amp;z=15&amp;output=embed" '
       'width="100%" height="250" style="display: block; border: 0;" loading="lazy" '
       'referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>')

SCHEMA = {
    '@context': 'https://schema.org', '@type': 'Physician', '@id': ORIGIN + '/#practice',
    'name': 'Personal Endocrine', 'url': ORIGIN + '/',
    'description': 'Direct-pay endocrinology practice of Dr. Jinsun Choi in North Tustin, CA, offering in-person and telehealth visits.',
    'hasMap': 'https://www.google.com/maps/search/?api=1&query=12231+Newport+Ave+North+Tustin+CA+92705',
    'isAcceptingNewPatients': True,
    'image': ORIGIN + '/img/dr-jinsun-choi.jpg',
    'telephone': '+1-949-441-2164', 'faxNumber': '+1-949-441-2184',
    'email': 'info@personalendocrine.com',
    'medicalSpecialty': 'Endocrine',
    'availableLanguage': ['English', 'Spanish', 'Korean'],
    'address': {'@type': 'PostalAddress', 'streetAddress': '12231 Newport Avenue',
                'addressLocality': 'North Tustin', 'addressRegion': 'CA',
                'postalCode': '92705', 'addressCountry': 'US'},
    'employee': {'@id': ORIGIN + '/dr-choi#jinsun-choi'},
    'sameAs': [FB, IG],
}

PERSON = {
    '@context': 'https://schema.org', '@type': 'Person', '@id': ORIGIN + '/dr-choi#jinsun-choi',
    'name': 'Jinsun Choi', 'honorificSuffix': 'MD', 'jobTitle': 'Endocrinologist',
    'url': ORIGIN + '/dr-choi', 'image': ORIGIN + '/img/dr-jinsun-choi.jpg',
    'worksFor': {'@id': ORIGIN + '/#practice'},
    'alumniOf': [{'@type': 'CollegeOrUniversity', 'name': 'University of California, Irvine, School of Medicine'}],
    'knowsLanguage': ['English', 'Spanish', 'Korean'],
    'knowsAbout': ['Diabetes', 'Obesity medicine', 'Thyroid disease', 'Parathyroid disorders', 'Osteoporosis', 'Menopause', 'Male hypogonadism'],
}


def faq_schema(body):
    qa = []
    for q, a in re.findall(r'<summary[^>]*>(.*?)<svg.*?</summary><div[^>]*>(.*?)</div></details>', body, re.S):
        if not re.sub(r'<[^>]+>', '', q).strip(): continue  # mobile menu, not an FAQ
        a = re.sub(r'<[^>]+>', ' ', a.replace('</p><p', '</p> <p'))
        a = re.sub(r'\s+', ' ', a).strip()
        qa.append({'@type': 'Question', 'name': q.strip(), 'acceptedAnswer': {'@type': 'Answer', 'text': a}})
    assert len(qa) >= 8, len(qa)
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': qa}


# Forms have no backend yet: the appointment form needs a HIPAA-compliant destination.
# Until one is chosen, submitting tells the patient to call instead of silently dropping data.
FORM_JS = '''<script>
document.querySelectorAll('form').forEach(function (f) {
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var n = f.querySelector('.pe-note');
    if (!n) {
      n = document.createElement('p');
      n.className = 'pe-note';
      n.setAttribute('role', 'status');
      n.style.cssText = 'margin:0;font-size:15px;flex-basis:100%;';
      f.appendChild(n);
    }
    n.textContent = f.dataset.kind === 'news'
      ? 'Email signup is coming soon.'
      : 'Online requests are coming soon. Please call ''' + PHONE + ''' to request your consultation.';
  });
});
</script>'''


# phones have no hover: highlight whichever pricing card is centered on screen as you scroll
PLAN_JS = """<script>
(function () {
  var cards = [].slice.call(document.querySelectorAll('.plans .plan'));
  if (!cards.length || !window.matchMedia('(hover: none)').matches) return;
  var ticking = false;
  function pick() {
    ticking = false;
    var stacked = cards[1] && cards[1].getBoundingClientRect().top >= cards[0].getBoundingClientRect().bottom - 1;
    if (!stacked) return;
    var mid = window.innerHeight / 2, best = null, dist = Infinity;
    cards.forEach(function (c) {
      var r = c.getBoundingClientRect(), d = Math.abs((r.top + r.bottom) / 2 - mid);
      if (d < dist) { dist = d; best = c; }
    });
    cards.forEach(function (c) { c.classList.toggle('on', c === best); });
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(pick); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  pick();
})();
</script>"""

def rewrite_links(body, is_home):
    ids = set(re.findall(r'\sid="([^"]+)"', body))
    def fix(m):
        attrs, text = m.group(1), m.group(2)
        hm = re.search(r'href="([^"]*)"', attrs)
        href = hm.group(1)
        label = re.search(r'aria-label="([^"]*)"', attrs)
        label = label.group(1) if label else text.strip()
        new = href
        if label == 'Facebook':
            new = FB
        elif label == 'Instagram':
            new = IG
        elif label in PLACEHOLDER:
            new = '#'
        elif href in FILE_URL and href != 'Main.dc.html':
            new = FILE_URL[href]
        elif href == 'Main.dc.html':
            new = TEXT_ANCHOR.get(text.strip(), '/')
        elif href.startswith('#') and href[1:] in ids:
            new = href  # in-page anchor (legal page contents)
        elif href.startswith('#') and href != '#top' and not is_home:
            new = '/' + href
        elif href == '#top' and not is_home:
            new = '/'
        attrs = attrs.replace(f'href="{href}"', f'href="{new}"', 1)
        if new.startswith('http') and 'google.com/maps' not in new:
            attrs += ' target="_blank" rel="noopener"'
        return f'<a{attrs}>{text}'
    return re.sub(r'<a(\s[^>]*?)>([^<]*)', fix, body)


def build(name):
    out_path, url, title, desc = PAGES[name]
    s = open(os.path.join(SRC, name), encoding='utf-8').read()
    helmet = s[s.index('<helmet>') + 8:s.index('</helmet>')]
    body = s[s.index('</helmet>') + 9:s.index('</x-dc>')]
    body = body.replace('{{accent}}', ACCENT)
    body = rewrite_links(body, name == 'Main.dc.html')
    body = body.replace('/_blob/8dffb91312f1eb610f55b25b5af9c044', '/img/dr-jinsun-choi-coat.jpg')
    body = re.sub(r'/_blob/[0-9a-f]+', '/img/dr-jinsun-choi.jpg', body)
    if name == 'Book.dc.html':
        i = body.index('<svg viewBox="0 0 400 250"')
        j = body.index('</svg>', i) + 6
        body = body[:i] + MAP + body[j:]
    # make forms submittable so the handler fires; tag the newsletter form
    body = body.replace('<form style="display: flex; gap: 8px; width: 100%; max-width: 420px; margin: 0;">',
                        '<form data-kind="news" style="display: flex; flex-wrap: wrap; gap: 8px; width: 100%; max-width: 420px; margin: 0;">')
    body = body.replace('<button type="button"', '<button type="submit"')
    assert '{{' not in body and '.dc.html' not in body and '_blob' not in body, name
    helmet = helmet.replace('<link rel="stylesheet" href="https://fonts.googleapis.com',
                            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
                            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                            '<link rel="stylesheet" href="https://fonts.googleapis.com')
    canon = ORIGIN + url
    head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#F2F1EC">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Personal Endocrine">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{ORIGIN}/img/dr-jinsun-choi.jpg">
<meta name="twitter:card" content="summary_large_image">
{helmet.strip()}
<style>html{{scroll-behavior:smooth}}[id]{{scroll-margin-top:24px}}img{{max-width:100%}}</style>
'''
    if name == 'Main.dc.html':
        head += '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>\n'
        head += '<script type="application/ld+json">' + json.dumps(faq_schema(body), ensure_ascii=False) + '</script>\n'
    if name == 'DrChoi.dc.html':
        head += '<script type="application/ld+json">' + json.dumps(PERSON) + '</script>\n'
    # intrinsic size reserves space while loading; height:auto keeps the CSS aspect-ratio in charge
    body = body.replace('<img src="/img/dr-jinsun-choi.jpg" ', '<img src="/img/dr-jinsun-choi.jpg" width="1000" height="1250" ')
    body = body.replace('style="display: block; width: 100%; aspect-ratio: 4 / 5;', 'style="display: block; width: 100%; height: auto; aspect-ratio: 4 / 5;')
    html = head + '</head>\n<body>' + body.rstrip() + '\n' + FORM_JS + ('\n' + PLAN_JS if 'class="plans"' in body else '') + '\n</body>\n</html>\n'
    open(os.path.join(OUT, out_path), 'w', encoding='utf-8').write(html)
    print('ok', out_path)


if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, 'img'))
shutil.copy(HEADSHOT, os.path.join(OUT, 'img', 'dr-jinsun-choi.jpg'))
shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'img', 'dr-jinsun-choi-coat.jpg'), os.path.join(OUT, 'img', 'dr-jinsun-choi-coat.jpg'))
open(os.path.join(OUT, 'favicon.svg'), 'w').write(FAVICON)
for n in PAGES:
    build(n)

# old site paths -> new homes (301 keeps search rankings and bookmarks)
open(os.path.join(OUT, '_redirects'), 'w').write('''/about /dr-choi 301
/ourpratice /#how 301
/specialty-services /#care 301
/faqs /#faq 301
/index.html / 301
''')
# keep the *.pages.dev copy out of search results; the real domain stays indexable
open(os.path.join(OUT, '_headers'), 'w').write('''https://personalendocrine.rp-100.workers.dev/*
  X-Robots-Tag: noindex

https://:project.pages.dev/*
  X-Robots-Tag: noindex

https://:version.:project.pages.dev/*
  X-Robots-Tag: noindex

/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY
  Permissions-Policy: camera=(), microphone=(), geolocation=()

/img/*
  Cache-Control: public, max-age=2592000
''')
import datetime
TODAY = datetime.date.today().isoformat()
urls = ''.join(f'  <url><loc>{ORIGIN}{v[1]}</loc><lastmod>{TODAY}</lastmod></url>\n' for v in PAGES.values())
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n')
print('done')

# real 404 page (without one, Pages serves index.html for every unknown URL)
d = open(os.path.join(OUT, 'diabetes.html'), encoding='utf-8').read()
top = d[:d.index('<section')]
top = re.sub(r'<title>.*?</title>', '<title>Page not found | Personal Endocrine</title>', top)
top = re.sub(r'<link rel="canonical"[^>]*>\n', '', top)
top = re.sub(r'<meta (name="description"|property="og:[a-z]+"|name="twitter:card")[^>]*>\n', '', top)
top = top.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex">')
mid = '''<section style="max-width: 1200px; margin: 0 auto; padding: 96px 24px 120px; display: flex; flex-direction: column; gap: 18px; align-items: flex-start;">
<h1 style="margin: 0; font-family: 'Schibsted Grotesk', sans-serif; font-weight: 700; font-size: clamp(34px, 3.4vw, 48px); line-height: 1.1; letter-spacing: -0.02em;">We couldn’t find that page.</h1>
<p style="margin: 0; font-size: 19px; color: #4A504A; max-width: 620px;">It may have moved when we updated our site. Head to the home page, or call us at <a href="tel:9494412164">(949) 441-2164</a>.</p>
<a href="/" style="background: #5C7A64; color: #FFFFFF; text-decoration: none; padding: 14px 24px; border-radius: 999px; font-weight: 600;">Go to the home page</a>
</section>

'''
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(top + mid + d[d.index('<footer'):])
print('ok 404.html')

# build stamp: version.txt + an HTML comment on every page, so the live site shows which build it is
BUILD = sys.argv[4] if len(sys.argv) > 4 else None
if BUILD:
    open(os.path.join(OUT, 'version.txt'), 'w').write(f'Personal Endocrine site build {BUILD}\n')
    for fn in os.listdir(OUT):
        if fn.endswith('.html'):
            p = os.path.join(OUT, fn)
            s = open(p, encoding='utf-8').read().replace('<meta charset="utf-8">', f'<meta charset="utf-8">\n<!-- Personal Endocrine build {BUILD} -->', 1)
            open(p, 'w', encoding='utf-8').write(s)
    print('stamped build', BUILD)
