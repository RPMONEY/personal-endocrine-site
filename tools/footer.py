import sys, os

def footer(main):
    a = (lambda anchor: anchor) if main else (lambda anchor: 'Main.dc.html')
    head = 'style="font-size: 13px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #FFFFFF; margin-bottom: 4px;"'
    link = 'style="color: #C9C6BF; text-decoration: none;"'
    col = 'style="display: flex; flex-direction: column; gap: 10px;"'
    icon = 'style="display: inline-flex; align-items: center; justify-content: center; width: 40px; height: 40px; border: 1px solid #4A504B; border-radius: 999px; color: #C9C6BF; text-decoration: none;"'
    return f'''<footer style="background: #252A26; color: #C9C6BF; font-size: 15px; line-height: 1.6;">
<div style="max-width: 1200px; margin: 0 auto; padding: 64px 24px 0;">
<div style="display: flex; flex-wrap: wrap; gap: 16px 48px; align-items: center; justify-content: flex-start; padding-bottom: 40px; border-bottom: 1px solid #3A3F3B;">
<div style="display: flex; flex-direction: column; gap: 2px;">
<span style="font-weight: 600; font-size: 17px; color: #FFFFFF;">Stay in touch</span>
<span style="font-size: 14px; color: #A6A199;">Occasional updates from Personal Endocrine.</span>
</div>
<form style="display: flex; gap: 8px; width: 100%; max-width: 420px; margin: 0;">
<input type="email" aria-label="Email address" placeholder="Email address" autocomplete="email" style="font: inherit; font-size: 15px; color: #FFFFFF; background: transparent; border: 1px solid #4A504B; border-radius: 999px; padding: 0 18px; height: 44px; flex: 1 1 auto; min-width: 0; box-sizing: border-box;">
<button type="button" style="font: inherit; font-weight: 600; font-size: 15px; background: #5C7A64; color: #FFFFFF; border: 0; border-radius: 999px; padding: 0 22px; height: 44px; cursor: pointer; flex: none;">Subscribe</button>
</form>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 40px 32px; padding: 48px 0;">
<div {col}>
<span style="display: flex; margin-bottom: 8px;"><span style="display: inline-flex; flex-direction: column; align-items: center; gap: 2.4px; line-height: 1; color: #FFFFFF; font-family: 'Montserrat', sans-serif; font-weight: 500;"><span style="font-size: 20px; letter-spacing: 0.08em; margin-right: -0.08em; white-space: nowrap;">PERS<span style="position: relative; top: -0.155em; font-size: 0.86em;">O</span><span aria-hidden="true" style="display: inline-block; width: 0.621em; height: 0.07em; margin-left: -0.752em; margin-right: 0.131em; background: currentColor;"></span>NAL</span><span style="font-size: 9.2px; letter-spacing: 0.34em; margin-right: -0.34em; white-space: nowrap;">ENDOCRINE</span></span></span>
<span style="font-size: 14px;">Jinsun Choi, MD</span>
<span style="font-size: 14px; color: #A6A199;">English · Español · 한국어</span>
<span style="display: flex; gap: 8px; margin-top: 6px;"><a href="{a('#top')}" aria-label="Facebook" title="Facebook" {icon}><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="3.2"></circle><path d="M3.5 19c.6-3 2.8-4.8 5.5-4.8s4.9 1.8 5.5 4.8"></path><circle cx="17" cy="9" r="2.4"></circle><path d="M16.2 14.3c2.3.2 3.8 1.8 4.3 4.2"></path></svg></a><a href="{a('#top')}" aria-label="Instagram" title="Instagram" {icon}><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 8.5h3l1.6-2.5h6.8L17 8.5h3v10H4z"></path><circle cx="12" cy="13.2" r="3.2"></circle></svg></a></span>
</div>
<nav aria-label="Specialties" {col}>
<span {head}>Specialties</span>
<a href="Diabetes.dc.html" {link}>Type 1 and Type 2 Diabetes</a>
<a href="Weight.dc.html" {link}>Weight Management</a>
<a href="Thyroid.dc.html" {link}>Thyroid</a>
<a href="Parathyroid.dc.html" {link}>Parathyroid &amp; Calcium Disorders</a>
<a href="Osteoporosis.dc.html" {link}>Osteoporosis</a>
<a href="Menopause.dc.html" {link}>Menopause</a>
<a href="LowT.dc.html" {link}>Low Testosterone in Men</a>
</nav>
<nav aria-label="Your care" {col}>
<span {head}>Your care</span>
<a href="{a('#how')}" {link}>Our approach</a>
<a href="Pricing.dc.html" {link}>Pricing and memberships</a>
<a href="DrChoi.dc.html" {link}>Meet Dr. Choi</a>
<a href="{a('#faq')}" {link}>Frequently asked questions</a>
<a href="Book.dc.html" {link}>Request a consultation</a>
<a href="{a('#top')}" {link}>Patient portal</a>
</nav>
<div {col}>
<span {head}>Visit</span>
<span>12231 Newport Avenue<br>North Tustin, CA 92705</span>
<a href="https://www.google.com/maps/search/?api=1&amp;query=12231+Newport+Ave+North+Tustin+CA+92705" {link}>Get directions</a>
<span>In person or telehealth</span>
</div>
<div {col}>
<span {head}>Contact</span>
<a href="tel:9494412164" {link}>(949) 441-2164</a>
<span>Fax (949) 441-2184</span>
<a href="mailto:info@personalendocrine.com" {link}>info@personalendocrine.com</a>
</div>
</div>
<div style="display: flex; flex-wrap: wrap; gap: 12px 32px; align-items: flex-start; justify-content: space-between; padding: 24px 0 32px; border-top: 1px solid #3A3F3B; font-size: 13px; color: #8F8A83;">
<div style="display: flex; flex-direction: column; gap: 2px;"><span>© 2026 Personal Endocrine, P.C.</span><span>This site does not provide medical advice. In an emergency, call 911.</span></div>
<nav aria-label="Legal" style="display: flex; flex-wrap: wrap; gap: 8px 20px;">
<a href="Privacy.dc.html" style="color: #8F8A83; text-decoration: none;">Privacy Policy</a>
<a href="NPP.dc.html" style="color: #8F8A83; text-decoration: none;">Notice of Privacy Practices</a>
<a href="GFE.dc.html" style="color: #8F8A83; text-decoration: none;">Good Faith Estimate</a>
<a href="Terms.dc.html" style="color: #8F8A83; text-decoration: none;">Terms of Use</a>
<a href="Accessibility.dc.html" style="color: #8F8A83; text-decoration: none;">Accessibility Statement</a>
</nav>
</div>
</div>
</footer>'''

if __name__ == '__main__':
    if sys.argv[1] == '--preview':
        out = sys.argv[2]
        html = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
                '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600&family=Schibsted+Grotesk:wght@500;600;700&display=swap">'
                '<style>body{margin:0;font-family:"Public Sans",sans-serif;background:#F2F1EC}input::placeholder{color:#A6A199}</style></head><body>'
                + footer(True) + '</body></html>')
        open(out, 'w', encoding='utf-8').write(html)
        sys.exit()
    for path in sys.argv[1:]:
        name = os.path.basename(path)
        s = open(path, encoding='utf-8').read()
        i = s.index('<footer')
        j = s.index('</footer>', i) + len('</footer>')
        s = s[:i] + footer(name == 'Main.dc.html') + s[j:]
        open(path, 'w', encoding='utf-8').write(s)
        print('ok', name)
