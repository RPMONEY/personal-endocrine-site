"""Rewrite the main section of all seven specialty pages from the approved copy spec.

Header, footer and the "Additional specialties" row are untouched; only the hero + article +
side card section is regenerated, on one shared template so every page matches.
"""
import sys

P = sys.argv[1]

H1 = '<h1 style="margin: 0; font-family: \'Schibsted Grotesk\', sans-serif; font-weight: 700; font-size: clamp(34px, 3.4vw, 48px); line-height: 1.1; letter-spacing: -0.02em; max-width: 820px;">{}</h1>'
LEAD = '<p style="margin: 0; font-size: 23px; line-height: 1.4; font-weight: 500; color: #252A26; max-width: 720px;">{}</p>'
PARA = '<p style="margin: 0;">{}</p>'
SUBHEAD = '<div style="font-family: \'Schibsted Grotesk\', sans-serif; font-weight: 600; font-size: 22px; color: #252A26;">{}</div>'
CLOSE = '<p style="margin: 10px 0 0; padding-left: 20px; border-left: 3px solid {{{{accent}}}}; font-size: 20px; line-height: 1.5; font-weight: 500; color: #252A26;">{}</p>'
CHECK = ('<span style="display: flex; gap: 10px; align-items: center;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#5C7A64" '
         'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="flex: none;"><path d="M5 12l5 5L20 7"></path></svg>{}</span>')


def q(t):
    """Typographic apostrophes and quotes; guard against em dashes."""
    assert '—' not in t and '--' not in t, t
    t = t.replace("'", '’')
    return t


def ongoing_support():
    return ('<div style="display: flex; flex-direction: column; gap: 10px; margin-top: 8px;">\n'
            + SUBHEAD.format('Ongoing support') + '\n'
            + PARA.format(q("Diabetes doesn't only need attention on appointment days. Members and patients in the Diabetes and Weight Management Program can receive glucose log and CGM reviews between visits, along with direct portal messaging with Dr. Choi.")) + '\n'
            '<a href="Main.dc.html" style="font-weight: 600; font-size: 16px;">See pricing and programs</a>\n</div>')


def program_box():
    return ('<div style="background: #E4E6DE; border-radius: 20px; padding: 24px 28px; display: flex; flex-direction: column; gap: 8px; margin-top: 8px;">\n'
            '<div style="font-size: 13px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: {{accent}};">Diabetes and Weight Management Program</div>\n'
            '<div style="font-family: \'Schibsted Grotesk\', sans-serif; font-weight: 700; font-size: 28px; line-height: 1.15;">$360 a month, or $2,000 for 6 months</div>\n'
            '<div style="font-size: 16px; color: #3A403B;">A six-month intensive program with follow-up visits every two weeks, direct telephone visits, glucose log and CGM reviews, and direct portal messaging with Dr. Choi. Every plan starts with an initial consultation.</div>\n'
            '<a href="Main.dc.html" style="font-weight: 600; font-size: 16px;">See all pricing</a>\n</div>')


PAGES = {
    'Diabetes.dc.html': dict(
        title='Type 1 and Type 2 Diabetes', card='your diabetes',
        lead="Diabetes care should fit into your life, not take it over.",
        body=["Managing diabetes involves more than watching a number. Blood sugar is affected by what you eat, how active you are, medications, sleep, stress and the way your own body produces and responds to insulin. The right treatment plan needs to account for all of it.",
              "Dr. Choi takes the time to understand your glucose patterns, medications, health history and daily routine, then works with you to build a plan that is both medically sound and realistic to live with.",
              "For people with type 1 diabetes, that may include adjusting insulin therapy and using continuous glucose monitoring to better understand time in range, highs and lows. For people with type 2 diabetes, treatment may involve nutrition and activity changes along with medications selected for your individual health needs and goals.",
              "Modern diabetes care looks beyond A1C alone. Cardiovascular health, kidney health, weight and the risk of hypoglycemia can all influence treatment decisions.",
              "Whether you're newly diagnosed, adjusting treatment or simply frustrated that your numbers aren't where you want them to be, you'll have time to ask questions, understand your options and make decisions together."],
        extra=ongoing_support),
    'Weight.dc.html': dict(
        title='Weight Management', card='your weight',
        lead="Obesity is a medical condition. It deserves to be treated like one.",
        body=["Weight is influenced by far more than willpower. Genetics, appetite regulation, sleep, medications, stress, hormones, activity and the way the body adapts to weight loss can all play a role. Obesity is also associated with conditions including type 2 diabetes, high blood pressure, abnormal cholesterol and cardiovascular disease.",
              "That's why Dr. Choi starts by looking beyond the number on the scale. She reviews your health history, previous attempts at weight loss, medications, eating patterns and metabolic health to understand what may be making weight difficult to manage.",
              "Treatment is individualized. Depending on your needs, it may include changes in nutrition and physical activity, treatment of contributing medical conditions and, when appropriate, prescription weight-management medication.",
              "Newer medications, including GLP-1 and related incretin-based therapies, have significantly expanded the options available for treating obesity. These medications can produce meaningful weight loss and improvements in several cardiometabolic measures when used in appropriate patients. They aren't right for everyone, and medication is only one part of long-term weight management.",
              "The goal isn't a crash diet or a number chosen for you. It's a medically informed approach that you and Dr. Choi can realistically sustain."],
        extra=program_box),
    'Thyroid.dc.html': dict(
        title='Thyroid Conditions', card='your thyroid',
        lead="“I don't feel well. Is it my thyroid?”",
        body=["It's one of the most common questions an endocrinologist hears, and it deserves a careful answer.",
              "Thyroid hormones influence metabolism throughout the body, which is one reason thyroid problems can produce symptoms that seem unrelated. An underactive thyroid can be associated with fatigue, feeling cold, constipation, dry skin and changes in weight. An overactive thyroid may cause a rapid heartbeat, tremor, heat intolerance, difficulty sleeping and unintended weight loss.",
              "But those symptoms aren't unique to thyroid disease. Feeling tired or gaining weight doesn't automatically mean your thyroid is the cause. Diagnosis starts with your symptoms and medical history and is confirmed with appropriate laboratory testing. For most patients being evaluated for primary thyroid dysfunction, TSH is the key initial laboratory test.",
              "If an abnormality is found, Dr. Choi looks at why it is happening rather than treating a lab value in isolation. Thyroid conditions can have different causes and may require very different approaches.",
              "For hypothyroidism, levothyroxine remains the standard treatment when thyroid hormone replacement is needed. Hyperthyroidism requires identifying the underlying cause before deciding among treatment options.",
              "Dr. Choi takes the time to put your symptoms, examination, medical history and laboratory results together and explain what they mean before deciding what comes next."]),
    'Parathyroid.dc.html': dict(
        title='Parathyroid Conditions', card='your parathyroid health',
        lead="Parathyroid is not thyroid.",
        body=["The names sound similar, but they do very different jobs. The four small parathyroid glands are usually located behind the thyroid and produce parathyroid hormone, or PTH, which plays a central role in controlling calcium levels and bone metabolism.",
              "When too much PTH is produced, calcium in the blood may rise. This is known as hyperparathyroidism. Some people have few noticeable symptoms and discover it only after routine bloodwork shows high calcium. In others, it may be associated with kidney stones, loss of bone density or osteoporosis and impaired kidney function.",
              "The opposite problem, hypoparathyroidism, occurs when the body doesn't produce enough PTH. Calcium can fall too low, sometimes causing tingling, numbness, muscle cramps or spasms and, when severe, more serious complications.",
              "Because calcium abnormalities can have several causes, an abnormal calcium result by itself doesn't tell the whole story. Evaluation may involve repeating calcium measurements and considering PTH, vitamin D, kidney function, bone density and other testing in context.",
              "Dr. Choi works through those results with you to determine what's causing the abnormality, whether treatment is necessary and what kind of monitoring makes sense."]),
    'Osteoporosis.dc.html': dict(
        title='Osteoporosis', card='your bone health',
        lead="Strong bones matter at every age.",
        body=["Bone naturally changes throughout life, but osteoporosis occurs when bones become fragile enough that the risk of fracture rises substantially. It is often called a silent disease because bone loss itself usually causes no symptoms. For some people, the first sign is a fracture.",
              "That makes identifying fracture risk before a fracture happens especially important.",
              "Dr. Choi looks beyond a single bone-density number. Your evaluation may include bone-density testing along with your age, fracture history, family history, medications and medical conditions that can affect bone. Depending on the situation, laboratory testing may also help identify secondary causes of bone loss.",
              "Treatment depends on your individual level of risk. Nutrition, adequate calcium and vitamin D when appropriate, weight-bearing and resistance exercise, fall prevention and avoiding tobacco all contribute to bone health. For people at higher risk of fracture, medication can significantly reduce that risk, and several different types of osteoporosis medication are available.",
              "The best choice isn't the same for everyone. Treatment decisions can depend on fracture history, bone density, other medical conditions and the benefits and risks of each medication. Some people at very high fracture risk may benefit from treatments that actively stimulate new bone formation.",
              "Dr. Choi helps you understand your actual fracture risk and build a long-term plan to protect your bones, rather than simply reacting to a number on a scan."]),
    'Menopause.dc.html': dict(
        title='Menopause', card='menopause',
        lead="Menopause care should be based on you, not a one-size-fits-all answer about hormones.",
        body=["Menopause is a normal stage of life, but the symptoms that come with it can have a very real effect on how you feel day to day. Hot flashes and night sweats are common, but menopause can also affect sleep, sexual health, vaginal and urinary symptoms, bone health and overall quality of life.",
              "And every woman experiences it differently.",
              "Dr. Choi takes the time to understand your symptoms, medical history, risk factors and what matters most to you before discussing treatment. For some women, menopausal hormone therapy may be appropriate. For others, non-hormonal treatments may be a better choice.",
              "Hormone therapy remains the most effective treatment for bothersome hot flashes and night sweats and can also help prevent bone loss. Current evidence supports an individualized approach that considers factors including age, time since menopause, symptoms and personal health risks rather than treating hormone therapy as universally right or universally wrong.",
              "The goal is to help you understand your options clearly so you and Dr. Choi can decide what makes sense for you."],
        close="You shouldn't have to guess whether what you're experiencing is “just menopause” or whether anything can be done about it."),
    'LowT.dc.html': dict(
        title='Low Testosterone in Men', card='low testosterone',
        lead="Low testosterone is more than a number on a lab report.",
        body=["Fatigue, decreased sex drive, changes in body composition, reduced strength and other symptoms can sometimes be associated with low testosterone, but those symptoms can have many other causes as well.",
              "That's why testosterone deficiency shouldn't be diagnosed from symptoms alone or from a single low test result.",
              "Evidence-based guidelines recommend diagnosing male hypogonadism when a man has symptoms or signs consistent with testosterone deficiency and testosterone levels that are consistently low, typically confirmed with repeat morning testing. Evaluation may also include additional testing to understand why testosterone is low.",
              "Dr. Choi looks at your symptoms, medical history, medications and laboratory results together before recommending treatment. When true testosterone deficiency is present, she can help identify potential causes and discuss whether testosterone therapy is appropriate.",
              "Treatment isn't simply about getting a testosterone level into a particular range. It means weighing potential benefits against risks, considering fertility and other health factors, and monitoring treatment appropriately if you decide to proceed."],
        close="The first step isn't assuming you need testosterone. It's finding out what's actually going on."),
}

SECTION_OPEN = '<section style="max-width: 1200px; margin: 0 auto; padding: 64px 24px 88px; display: flex; flex-wrap: wrap; gap: 48px; align-items: start;">'


def section(d):
    parts = [SECTION_OPEN,
             '<div style="flex: 999 1 560px; min-width: 0; display: flex; flex-direction: column; gap: 16px;">',
             '<a href="Main.dc.html" style="font-size: 14px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: {{accent}}; text-decoration: none;">Our specialties</a>',
             H1.format(d['title']), LEAD.format(q(d['lead'])),
             '<article style="margin-top: 24px; max-width: 720px; display: flex; flex-direction: column; gap: 18px; font-size: 18px; line-height: 1.65; color: #3A403B;">']
    parts += [PARA.format(q(t)) for t in d['body']]
    if d.get('close'):
        parts.append(CLOSE.format(q(d['close'])))
    if d.get('extra'):
        parts.append(d['extra']())
    parts += ['</article>', '</div>',
              '<aside class="side" style="flex: 1 1 320px; min-width: 0; background: #F8F8F4; border: 1px solid #D8DAD0; border-radius: 24px; padding: 32px; display: flex; flex-direction: column; gap: 18px;">',
              f'<div style="font-family: \'Schibsted Grotesk\', sans-serif; font-weight: 600; font-size: 22px; line-height: 1.25;">Talk with Dr. Choi about {d["card"]}</div>',
              '<div style="display: flex; flex-direction: column; gap: 10px; font-size: 15px; color: #4A504A;">',
              CHECK.format('Up to an hour at your first visit'), CHECK.format('Every visit with Dr. Choi'),
              CHECK.format('Most appointments within 1 to 3 business days'), '</div>',
              '<a href="Book.dc.html" style="text-align: center; background: {{accent}}; color: #FFFFFF; text-decoration: none; padding: 14px 24px; border-radius: 999px; font-weight: 600; min-height: 44px; box-sizing: border-box;">Request a consultation</a>',
              '<a href="tel:9494412164" style="text-align: center; font-weight: 600; font-size: 15px;">Or call (949) 441-2164</a>',
              '</aside>', '</section>']
    return '\n'.join(parts)


for name, d in PAGES.items():
    path = f'{P}/{name}'
    s = open(path, encoding='utf-8').read()
    i = s.index(SECTION_OPEN)
    j = s.index('</section>', i) + len('</section>')
    s = s[:i] + section(d) + s[j:]
    t0 = s.index('<title>'); t1 = s.index('</title>')
    s = s[:t0 + 7] + d['title'] + s[t1:]
    open(path, 'w', encoding='utf-8').write(s)
    words = len((' '.join(d['body']) + ' ' + d.get('close', '')).split())
    print(f'{name:22s} {words} words')
