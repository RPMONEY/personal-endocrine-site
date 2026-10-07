"""Five legal pages (Privacy Policy, Notice of Privacy Practices, Good Faith Estimate, Terms of Use,
Accessibility Statement) on the existing page shell, plus working footer links on every page.
Content follows Ryan's spec; facts not supplied are shown as visible [NEEDS CONFIRMATION] markers."""
import sys, glob, re

P, BOOK = sys.argv[1], sys.argv[2]
rd = lambda p: open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)

shell = rd(f'{P}/Diabetes.dc.html')
GROT = "font-family: 'Schibsted Grotesk', sans-serif;"
TBD = lambda t: f'<mark class="tbd">[NEEDS CONFIRMATION: {t}]</mark>'
A = lambda href, text: f'<a href="{href}">{text}</a>'
EXT = lambda href, text: f'<a href="{href}" target="_blank" rel="noopener">{text}</a>'

CONTACT = ('<p style="margin: 0;">Personal Endocrine, P.C.<br>12231 Newport Avenue<br>North Tustin, CA 92705<br>'
           'Phone: <a href="tel:9494412164">(949) 441-2164</a><br>Email: <a href="mailto:info@personalendocrine.com">info@personalendocrine.com</a></p>')


def blocks_html(blocks):
    out = []
    for b in blocks:
        kind, val = b[0], b[1]
        if kind == 'p':
            out.append(f'<p style="margin: 0;">{val}</p>')
        elif kind == 'ul':
            out.append('<ul class="lg-list">' + ''.join(f'<li>{i}</li>' for i in val) + '</ul>')
        elif kind == 'h3':
            out.append(f'<h3 style="margin: 8px 0 0; {GROT} font-weight: 600; font-size: 19px; line-height: 1.3; color: #252A26;">{val}</h3>')
        elif kind == 'raw':
            out.append(val)
        elif kind == 'box':
            out.append(f'<div style="background: #E4E6DE; border-radius: 18px; padding: 22px 24px; color: #252A26; font-weight: 500;">{val}</div>')
    return '\n'.join(out)


def page(d):
    secs = []
    for sid, title, blocks in d['sections']:
        secs.append(f'<section id="{sid}" style="display: flex; flex-direction: column; gap: 14px; padding-top: 28px; border-top: 1px solid #D8DAD0;">'
                    f'<h2 style="margin: 0; {GROT} font-weight: 700; font-size: 24px; line-height: 1.25; letter-spacing: -0.01em; color: #252A26;">{title}</h2>'
                    f'{blocks_html(blocks)}</section>')
    toc = ''.join(f'<a href="#{sid}">{title}</a>' for sid, title, _ in d['sections'])
    updated = f'<p style="margin: 0; font-size: 15px; color: #5D635D;">{d["updated"]}</p>' if d.get('updated') else ''
    lead = f'<p style="margin: 0; font-size: 23px; line-height: 1.4; font-weight: 500; color: #252A26; max-width: 720px;">{d["lead"]}</p>' if d.get('lead') else ''
    intro = blocks_html(d.get('intro', []))
    content = f'''<section class="legal" style="max-width: 1200px; margin: 0 auto; padding: 64px 24px 88px; display: flex; flex-wrap: wrap; gap: 48px; align-items: start;">
<div style="flex: 999 1 560px; min-width: 0; display: flex; flex-direction: column; gap: 16px;">
<span style="font-size: 14px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: {{{{accent}}}};">{d['eyebrow']}</span>
<h1 style="margin: 0; {GROT} font-weight: 700; font-size: clamp(34px, 3.4vw, 48px); line-height: 1.1; letter-spacing: -0.02em; max-width: 820px;">{d['title']}</h1>
{lead}
{updated}
<article class="lg" style="margin-top: 20px; max-width: 720px; display: flex; flex-direction: column; gap: 18px; font-size: 18px; line-height: 1.65; color: #3A403B;">
{intro}
{chr(10).join(secs)}
</article>
</div>
<aside class="side lg-side" style="flex: 1 1 300px; min-width: 0; background: #F8F8F4; border: 1px solid #D8DAD0; border-radius: 24px; padding: 28px; display: flex; flex-direction: column; gap: 16px;">
<nav class="lg-toc" aria-label="On this page" style="display: flex; flex-direction: column; gap: 2px;">
<div style="font-size: 13px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #5D635D; margin-bottom: 6px;">On this page</div>
{toc}
</nav>
<div class="lg-q" style="display: flex; flex-direction: column; gap: 6px; font-size: 15px; color: #3A403B;">
<div style="font-weight: 600; font-size: 17px; color: #252A26;">Questions?</div>
<a href="tel:9494412164" style="font-weight: 600;">(949) 441-2164</a>
<a href="mailto:info@personalendocrine.com">info@personalendocrine.com</a>
</div>
</aside>
</section>'''
    i = shell.index('<section style="max-width: 1200px; margin: 0 auto; padding: 64px 24px 88px;')
    a = shell.index('Additional specialties</div>')
    j = shell.index('</section>', a) + len('</section>')
    out = shell[:i] + content + shell[j:]
    out = out.replace('<title>Type 1 and Type 2 Diabetes</title>', f'<title>{d["title"]}</title>')
    css = ('.lg-list{margin:0;padding-left:22px;display:flex;flex-direction:column;gap:8px}.lg-list li::marker{color:#5C7A64}'
           '.lg-toc a{color:#3A403B;text-decoration:none;font-size:15px;line-height:1.35;padding:6px 0}.lg-toc a:hover{color:#5C7A64}'
           '.lg-side{position:sticky;top:24px}.lg-q{border-top:1px solid #E4E6DE;padding-top:16px}'
           'mark.tbd{background:#E4E6DE;color:#252A26;font-weight:600;padding:1px 6px;border-radius:6px}'
           '@media (max-width:900px){.lg-side{position:static}.lg-toc{display:none !important}.lg-q{border-top:0;padding-top:0}}'
           '@media (max-width:640px){section.legal{padding:40px 24px 56px !important;gap:32px !important}.lg{gap:16px !important}}\n')
    k = out.index('</style>')
    out = out[:k] + css + out[k:]
    assert '—' not in out
    return out


# ---------------------------------------------------------------- Privacy Policy
PRIVACY = dict(
    eyebrow='Legal', title='Privacy Policy', updated='Last updated: October 2026',
    intro=[('p', 'Personal Endocrine, P.C. respects your privacy. This Privacy Policy explains how information may be collected, used and protected when you visit our website.'),
           ('p', f'This website Privacy Policy is separate from our {A("NPP.dc.html", "Notice of Privacy Practices")}, which describes how Personal Endocrine may use and disclose protected health information in connection with your medical care.')],
    sections=[
        ('provide', 'Information you provide to us', [
            ('p', 'We may collect information you voluntarily provide through this website, such as your:'),
            ('ul', ['Name', 'Email address', 'Telephone number', 'Appointment request information', 'Other information you choose to submit']),
            ('p', 'At this time, the appointment request and email signup forms on this website do not send information to us. To request an appointment, please call <a href="tel:9494412164">(949) 441-2164</a>.'),
            ('p', 'Please do not use general website forms or ordinary email to send sensitive medical information unless specifically instructed to do so. Patients should use the appropriate secure communication method provided by Personal Endocrine for medical information.')]),
        ('automatic', 'Information collected automatically', [
            ('p', 'When you visit this website, our website hosting provider automatically receives technical information needed to deliver and protect the site, such as your IP address, browser type, device type, the pages you request and the referring website.'),
            ('p', 'We do not currently use analytics services, advertising pixels or similar tracking technologies on this website. If that changes, we will update this Privacy Policy.')]),
        ('use', 'How we use information', [
            ('p', 'We may use information collected through this website to:'),
            ('ul', ['Respond to appointment requests and inquiries', 'Communicate with you', 'Operate and improve the website',
                    'Understand how visitors use the website', 'Maintain website security', 'Comply with legal obligations']),
            ('p', 'We do not sell personal information collected through this website.')]),
        ('health', 'Health information', [
            ('p', 'Information that Personal Endocrine receives or maintains in connection with providing healthcare may be protected by federal and state health privacy laws.'),
            ('p', f'Our use and disclosure of protected health information is governed by our {A("NPP.dc.html", "Notice of Privacy Practices")}, not solely by this website Privacy Policy.')]),
        ('ai', 'AI-assisted clinical documentation', [
            ('p', 'With a patient’s permission, Dr. Choi may use an AI-assisted documentation tool during a visit to help prepare clinical notes. The tool may process the conversation between you and Dr. Choi and may process information that is considered protected health information.'),
            ('p', 'Dr. Choi will ask for your permission before using the tool. You may decline its use, and your decision will not affect your care.'),
            ('p', 'Personal Endocrine applies applicable privacy and security requirements to protected health information processed in connection with patient care.')]),
        ('third-party', 'Third-party services', [
            ('p', 'We use third-party companies to help operate our website. These services may process information according to their own privacy practices and, where required, contractual privacy and security obligations. Currently, they include:'),
            ('ul', ['<strong>Website hosting.</strong> Cloudflare hosts and delivers this website and receives the technical information described above.',
                    '<strong>Fonts.</strong> Text on this website uses fonts from Google Fonts. When a page loads, your browser requests the fonts from Google, which receives your IP address and browser information.',
                    '<strong>Maps.</strong> Our appointment page displays an embedded Google Map. When the map loads, Google receives your IP address and browser information and may set its own cookies.',
                    '<strong>Links.</strong> Links to Google Maps directions, Facebook and Instagram share information with those services only if you click them.'])]),
        ('cookies', 'Cookies and similar technologies', [
            ('p', 'This website does not set its own cookies or use browser storage to identify or track visitors.'),
            ('p', 'Third-party services embedded in the website, such as the Google Map on our appointment page, may set their own cookies under their own policies. You can control cookies through your browser settings.')]),
        ('security', 'Security', [
            ('p', 'We use reasonable administrative, technical and physical safeguards designed to protect information.'),
            ('p', 'However, no website, email system or electronic transmission can be guaranteed to be completely secure.')]),
        ('links', 'Links to other websites', [
            ('p', 'Our website may contain links to third-party websites. Personal Endocrine is not responsible for the privacy practices or content of those websites.')]),
        ('children', 'Children', [
            ('p', 'This website is not directed to children for independent use. Parents or legal guardians should contact the practice regarding care for a minor.')]),
        ('changes', 'Changes to this policy', [
            ('p', 'We may update this Privacy Policy as our website, services or legal obligations change. The current version will be posted here with its most recent revision date.')]),
        ('contact', 'Contact us', [
            ('p', 'Questions about this Privacy Policy may be directed to:'), ('raw', CONTACT)]),
    ])

# ---------------------------------------------------------------- Notice of Privacy Practices
NPP = dict(
    eyebrow='Legal', title='Notice of Privacy Practices', lead='Your information. Your rights. Our responsibilities.',
    updated=f'Effective date: October 7, 2026',
    intro=[('box', 'This notice describes how medical information about you may be used and disclosed and how you can get access to this information. Please review it carefully.'),
           ('p', 'Personal Endocrine, P.C. is committed to protecting the privacy and security of your health information.')],
    sections=[
        ('rights', 'Your rights', [
            ('p', 'When it comes to your health information, you have certain rights. This section explains your rights and some of our responsibilities to help you.'),
            ('h3', 'Get an electronic or paper copy of your medical record'),
            ('p', 'You can ask to see or get an electronic or paper copy of your medical record and other health information we have about you. Ask us how to do this. We will provide a copy or a summary of your health information within the time required by law. We may charge a reasonable, cost-based fee.'),
            ('h3', 'Ask us to correct your medical record'),
            ('p', 'You can ask us to correct health information about you that you think is incorrect or incomplete. Ask us how to do this. We may say “no” to your request, but we will tell you why in writing within 60 days.'),
            ('h3', 'Request confidential communications'),
            ('p', 'You can ask us to contact you in a specific way (for example, home or office phone) or to send mail to a different address. We will say “yes” to all reasonable requests.'),
            ('h3', 'Ask us to limit what we use or share'),
            ('p', 'You can ask us not to use or share certain health information for treatment, payment or our operations. We are not required to agree to your request, and we may say “no” if it would affect your care.'),
            ('p', 'If you pay for a service or health care item out of pocket in full, you can ask us not to share that information for the purpose of payment or our operations with your health insurer. We will say “yes” unless a law requires us to share that information.'),
            ('h3', 'Get a list of those with whom we’ve shared information'),
            ('p', 'You can ask for a list (accounting) of the times we’ve shared your health information for six years prior to the date you ask, who we shared it with and why. We will include all the disclosures except for those about treatment, payment and health care operations, and certain other disclosures (such as any you asked us to make). We’ll provide one accounting a year for free but will charge a reasonable, cost-based fee if you ask for another one within 12 months.'),
            ('h3', 'Get a copy of this privacy notice'),
            ('p', 'You can ask for a paper copy of this notice at any time, even if you have agreed to receive the notice electronically. We will provide you with a paper copy promptly.'),
            ('h3', 'Choose someone to act for you'),
            ('p', 'If you have given someone medical power of attorney or if someone is your legal guardian, that person can exercise your rights and make choices about your health information. We will make sure the person has this authority and can act for you before we take any action.'),
            ('h3', 'File a complaint if you feel your rights are violated'),
            ('p', 'You can complain if you feel we have violated your rights by contacting us using the information at the end of this notice.'),
            ('p', f'You can also file a complaint with the U.S. Department of Health and Human Services Office for Civil Rights by sending a letter to 200 Independence Avenue, S.W., Washington, D.C. 20201, calling 1-877-696-6775, or visiting {EXT("https://www.hhs.gov/hipaa/filing-a-complaint/index.html", "hhs.gov/hipaa/filing-a-complaint")}.'),
            ('p', '<strong>Personal Endocrine will not retaliate against you for filing a complaint.</strong>')]),
        ('choices', 'Your choices', [
            ('p', 'For certain health information, you can tell us your choices about what we share. If you have a clear preference for how we share your information in the situations described below, talk to us. Tell us what you want us to do, and we will follow your instructions.'),
            ('p', 'In these cases, you have both the right and choice to tell us to:'),
            ('ul', ['Share information with your family, close friends or others involved in your care',
                    'Share information in a disaster relief situation']),
            ('p', 'If you are not able to tell us your preference, for example if you are unconscious, we may go ahead and share your information if we believe it is in your best interest. We may also share your information when needed to lessen a serious and imminent threat to health or safety.'),
            ('p', 'In these cases, we never share your information unless you give us written permission:'),
            ('ul', ['Marketing purposes', 'Sale of your information', 'Most sharing of psychotherapy notes'])]),
        ('uses', 'Our uses and disclosures', [
            ('p', 'We typically use or share your health information in the following ways.'),
            ('h3', 'Treat you'),
            ('p', 'We can use your health information and share it with other professionals who are treating you. For example, Dr. Choi may share information with your primary care doctor, a laboratory or a pharmacy involved in your care.'),
            ('h3', 'Run our practice'),
            ('p', 'We can use and share your health information to run our practice, improve your care and contact you when necessary. For example, we may use your health information to manage your appointments and review the quality of our care.'),
            ('h3', 'Payment for your care'),
            ('p', 'Personal Endocrine does not accept or bill insurance for visits. You pay the practice directly for your care. We can use your health information as needed to process payment for our services.'),
            ('p', 'If you have commercial insurance and request a superbill, we will prepare it with the information you need to submit to your insurer for possible out-of-network reimbursement. Reimbursement depends on your individual plan.'),
            ('p', 'When we help with prior authorizations, appeals or forms for medications or services you receive elsewhere, we share the health information your health plan needs for that purpose.'),
            ('h3', 'AI-assisted clinical documentation'),
            ('p', 'Personal Endocrine may use technology, including an AI-assisted documentation tool, to help Dr. Choi prepare clinical notes from a patient visit.'),
            ('p', 'Dr. Choi will ask for your permission before using this technology during your visit. You may decline, and your decision will not affect your care.'),
            ('p', 'Information processed through these tools may include protected health information and is subject to applicable privacy and security requirements.')]),
        ('other-uses', 'Other ways we may use or share your information', [
            ('p', 'We are allowed or required to share your information in other ways, usually in ways that contribute to the public good, such as public health and research. We have to meet many conditions in the law before we can share your information for these purposes.'),
            ('h3', 'Help with public health and safety issues'),
            ('p', 'We can share health information about you for certain situations such as:'),
            ('ul', ['Preventing disease', 'Helping with product recalls', 'Reporting adverse reactions to medications',
                    'Reporting suspected abuse, neglect or domestic violence', 'Preventing or reducing a serious threat to anyone’s health or safety']),
            ('h3', 'Do research'),
            ('p', 'We can use or share your information for health research.'),
            ('h3', 'Comply with the law'),
            ('p', 'We will share information about you if state or federal laws require it, including with the Department of Health and Human Services if it wants to see that we are complying with federal privacy law.'),
            ('h3', 'Respond to organ and tissue donation requests'),
            ('p', 'We can share health information about you with organ procurement organizations.'),
            ('h3', 'Work with a medical examiner or funeral director'),
            ('p', 'We can share health information with a coroner, medical examiner or funeral director when an individual dies.'),
            ('h3', 'Address workers’ compensation, law enforcement and other government requests'),
            ('p', 'We can use or share health information about you:'),
            ('ul', ['For workers’ compensation claims', 'For law enforcement purposes or with a law enforcement official, as permitted by law',
                    'With health oversight agencies for activities authorized by law',
                    'For special government functions such as military, national security and presidential protective services']),
            ('h3', 'Respond to lawsuits and legal actions'),
            ('p', 'We can share health information about you in response to a court or administrative order, or in response to a subpoena.'),
            ('h3', 'More protective laws'),
            ('p', 'California law and other laws may give certain health information more protection than federal law. When a more protective law applies, we follow it.')]),
        ('sud', 'Substance use disorder treatment records', [
            ('p', 'Some substance use disorder treatment records are protected by federal confidentiality rules (42 CFR Part 2). If we receive or maintain records that are subject to these rules, we will use and disclose them only as those rules permit.'),
            ('p', 'These records, and testimony relaying their content, will not be used or disclosed in any civil, criminal, administrative or legislative proceeding against you unless you give written consent, or a court issues an order after you, or the holder of the records, receive notice and an opportunity to be heard. A court order authorizing use or disclosure must be accompanied by a subpoena or other legal requirement compelling disclosure.')]),
        ('redisclosure', 'Information shared with others', [
            ('p', 'When we share your health information as this notice permits, the person or organization that receives it may share it again, and it may no longer be protected by the federal privacy rules.')]),
        ('responsibilities', 'Our responsibilities', [
            ('ul', ['We are required by law to maintain the privacy and security of your protected health information.',
                    'We will let you know promptly if a breach occurs that may have compromised the privacy or security of your information.',
                    'We must follow the duties and privacy practices described in this notice and give you a copy of it.',
                    'We will not use or share your information other than as described here unless you tell us we can in writing. If you tell us we can, you may change your mind at any time. Let us know in writing if you change your mind.'])]),
        ('changes', 'Changes to this notice', [
            ('p', 'We can change the terms of this notice, and the changes will apply to all information we have about you. The new notice will be available upon request, in our office and on our website.')]),
        ('questions', 'Questions or complaints', [
            ('raw', '<p style="margin: 0;">Personal Endocrine, P.C.<br>12231 Newport Avenue<br>North Tustin, CA 92705<br>Phone: <a href="tel:9494412164">(949) 441-2164</a></p>'),
            ('p', f'Privacy Officer: {TBD("Privacy Officer")}<br>Privacy contact email: {TBD("privacy contact email")}'),
            ('p', f'You may also file a complaint with the U.S. Department of Health and Human Services Office for Civil Rights at {EXT("https://www.hhs.gov/hipaa/filing-a-complaint/index.html", "hhs.gov/hipaa/filing-a-complaint")}.'),
            ('p', '<strong>Personal Endocrine will not retaliate against you for filing a complaint.</strong>'),
            ('p', f'Effective date: October 7, 2026')]),
    ])

# ---------------------------------------------------------------- Good Faith Estimate
CMS_DISPUTE = 'https://www.cms.gov/medical-bill-rights/help/dispute-a-bill'
GFE = dict(
    eyebrow='Legal', title='Your Right to a Good Faith Estimate', lead='Know what your care is expected to cost.',
    intro=[('p', 'Under federal law, healthcare providers must generally provide patients who do not have insurance or who are not using insurance to pay for their care with an estimate of the expected cost of scheduled healthcare services.'),
           ('p', 'This is called a Good Faith Estimate.'),
           ('p', 'Because visits at Personal Endocrine are self-pay, these protections may apply to your care.')],
    sections=[
        ('right', 'You have the right to receive a Good Faith Estimate', [
            ('p', 'If you do not have health insurance or do not plan to use insurance to pay for your care, you may request a written Good Faith Estimate of expected charges.'),
            ('p', 'When care is scheduled sufficiently in advance, federal law may also require us to provide an estimate without you requesting one.'),
            ('p', 'Your Good Faith Estimate will include expected charges for the items or services reasonably expected to be provided by Personal Endocrine as part of your scheduled care.'),
            ('p', 'The estimate is based on information known when it is prepared. Your actual care needs may change.')]),
        ('when', 'When will I receive it?', [
            ('ul', ['If you schedule care at least 3 business days in advance, you should receive a Good Faith Estimate in writing within 1 business day after scheduling.',
                    'If you schedule care at least 10 business days in advance, you should receive it within 3 business days after scheduling.',
                    'If you ask for a Good Faith Estimate before scheduling care, you should receive it within 3 business days after your request.']),
            ('p', 'You can ask us for a Good Faith Estimate before you schedule an appointment. Please keep a copy or picture of your Good Faith Estimate.')]),
        ('dispute', 'What if my bill is higher than the estimate?', [
            ('p', 'If you receive a bill that is at least $400 more than your Good Faith Estimate from any provider or facility, you can dispute the bill through the federal patient-provider dispute resolution process.'),
            ('p', 'You must start the dispute within 120 calendar days (about 4 months) of the date on the original bill. There is a $25 administrative fee to use the dispute process.'),
            ('p', f'To learn more or start a dispute, visit the {EXT(CMS_DISPUTE, "CMS medical bill dispute page")}, email <a href="mailto:FederalPPDRQuestions@cms.hhs.gov">FederalPPDRQuestions@cms.hhs.gov</a> or call 1-800-985-3059.')]),
        ('questions', 'Questions about your estimate?', [('raw', CONTACT)]),
    ])
GFE['sections'][-1][2].append(('p', '<em>This notice does not itself constitute a Good Faith Estimate.</em>'))

# ---------------------------------------------------------------- Terms of Use
TERMS = dict(
    eyebrow='Legal', title='Terms of Use', updated='Last updated: October 2026',
    intro=[('p', 'These Terms of Use apply to your use of the Personal Endocrine, P.C. website.'),
           ('p', 'By using this website, you agree to these Terms.')],
    sections=[
        ('advice', 'Not medical advice', [
            ('p', 'The information on this website is provided for general educational and informational purposes only.'),
            ('p', 'It is not intended to diagnose or treat any medical condition and is not a substitute for advice from a qualified healthcare professional who knows your individual medical history.'),
            ('p', 'Do not disregard professional medical advice or delay seeking care because of information you have read on this website.')]),
        ('relationship', 'No physician-patient relationship', [
            ('p', 'Using this website, reading its content or submitting a general inquiry does not by itself establish a physician-patient relationship with Dr. Jinsun Choi or Personal Endocrine.'),
            ('p', 'A physician-patient relationship is established only through the practice’s applicable patient intake and care process.')]),
        ('emergencies', 'Emergencies', [
            ('p', 'Do not use this website to seek emergency medical care.'),
            ('p', 'If you believe you are experiencing a medical emergency, call 911 or seek immediate emergency medical attention.')]),
        ('appointments', 'Appointment requests', [
            ('p', 'Submitting an appointment request through this website does not guarantee an appointment.'),
            ('p', 'An appointment is confirmed only after Personal Endocrine contacts you and completes its confirmation process.')]),
        ('accuracy', 'Accuracy of information', [
            ('p', 'We make reasonable efforts to provide useful and accurate information, but medical knowledge, practice policies, pricing and other information may change.'),
            ('p', 'We may update website content without notice.')]),
        ('third-party', 'Third-party websites', [
            ('p', 'This website may link to websites or services operated by third parties.'),
            ('p', 'Personal Endocrine does not control those services and is not responsible for their content, availability, security or privacy practices.')]),
        ('ip', 'Intellectual property', [
            ('p', 'Unless otherwise indicated, the text, graphics, branding, photographs and other original content on this website are owned by or licensed to Personal Endocrine and are protected by applicable intellectual property laws.'),
            ('p', 'You may view and use the website for personal, noncommercial purposes.')]),
        ('availability', 'Website availability', [
            ('p', 'We do not guarantee that the website will always be available, uninterrupted or free from errors.'),
            ('p', 'We may modify, suspend or discontinue portions of the website when necessary.')]),
        ('privacy', 'Privacy', [
            ('p', f'Your use of this website is also subject to our {A("Privacy.dc.html", "Privacy Policy")}.'),
            ('p', f'Health information maintained by Personal Endocrine in connection with healthcare services is addressed in our {A("NPP.dc.html", "Notice of Privacy Practices")}.')]),
        ('changes', 'Changes to these Terms', [
            ('p', 'We may update these Terms of Use from time to time. The current version and revision date will be posted on this page.')]),
        ('contact', 'Contact', [('raw', CONTACT)]),
    ])

# ---------------------------------------------------------------- Accessibility Statement
ACCESS = dict(
    eyebrow='Accessibility', title='Accessibility Statement', lead='We want this website to work for everyone.', updated='Last updated: October 2026',
    intro=[('p', 'Personal Endocrine is committed to providing a website that is accessible and usable for all visitors, including people with disabilities.'),
           ('p', 'We continue to work to improve the accessibility, usability and clarity of our website.')],
    sections=[
        ('help', 'Need help accessing something?', [
            ('p', 'If you have difficulty accessing any part of this website, encounter an accessibility barrier or need information provided in another format, please contact us.'),
            ('p', 'We will make reasonable efforts to provide the information or assistance you need through an accessible method.'),
            ('raw', '<p style="margin: 0;">Personal Endocrine, P.C.<br>Phone: <a href="tel:9494412164">(949) 441-2164</a><br>Email: <a href="mailto:info@personalendocrine.com">info@personalendocrine.com</a></p>'),
            ('p', 'When contacting us, it may be helpful to tell us which page or feature caused difficulty and the type of assistance you need.')]),
        ('ongoing', 'Ongoing accessibility', [
            ('p', 'Accessibility is an ongoing effort. As the website changes, we will continue to review its accessibility and make improvements where appropriate.')]),
    ])

PAGES = {'Privacy.dc.html': PRIVACY, 'NPP.dc.html': NPP, 'GFE.dc.html': GFE, 'Terms.dc.html': TERMS, 'Accessibility.dc.html': ACCESS}
for fn, d in PAGES.items():
    wr(f'{P}/{fn}', page(d)); print('page', fn)

# footer legal links: point at the new pages; "Accessibility" becomes "Accessibility Statement"
LINKS = {'Privacy Policy': ('Privacy.dc.html', 'Privacy Policy'), 'Notice of Privacy Practices': ('NPP.dc.html', 'Notice of Privacy Practices'),
         'Good Faith Estimate': ('GFE.dc.html', 'Good Faith Estimate'), 'Terms of Use': ('Terms.dc.html', 'Terms of Use'),
         'Accessibility': ('Accessibility.dc.html', 'Accessibility Statement'), 'Accessibility Statement': ('Accessibility.dc.html', 'Accessibility Statement')}
pat = re.compile(r'<a href="[^"]*" style="color: #8F8A83; text-decoration: none;">(Privacy Policy|Notice of Privacy Practices|Good Faith Estimate|Terms of Use|Accessibility Statement|Accessibility)</a>')
files = [f for f in glob.glob(f'{P}/*.dc.html') if not re.search(r'(Logos|Mobile|Palettes)', f)] + [BOOK]
for f in files:
    s = rd(f); n = len(pat.findall(s))
    assert n == 5, (f, n)
    s = pat.sub(lambda m: f'<a href="{LINKS[m.group(1)][0]}" style="color: #8F8A83; text-decoration: none;">{LINKS[m.group(1)][1]}</a>', s)
    wr(f, s)
print('footer links updated in', len(files), 'pages')
