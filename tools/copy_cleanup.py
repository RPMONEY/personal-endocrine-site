"""Surgical copy cleanup (insurance policy, Ongoing benefits, specialty text). Exact replacements only."""
import sys, glob
P, BOOK = sys.argv[1], sys.argv[2]
def path(n): return BOOK if n == 'Book' else f'{P}/{n}.dc.html'
def edit(n, pairs):
    f = path(n); s = open(f, encoding='utf-8').read()
    for old, new, cnt in pairs:
        c = s.count(old); assert c == cnt, (n, old[:70], c)
        s = s.replace(old, new)
    open(f, 'w', encoding='utf-8').write(s); print('ok', n, len(pairs))

POL = '<div class="pol" style="display: grid; grid-template-columns: 260px 1fr; gap: 8px 32px; padding: 22px 0; border-top: 1px solid #D8DAD0;"><div style="font-weight: 600; font-size: 17px; color: #252A26;">{}</div><div style="font-size: 17px; color: #3A403B;">{}</div></div>'
def pol(a, b): return POL.format(a, b)

# pricing card lines (home + pricing page)
CARDS = [('<span>Prior auth, appeals, forms</span>', '<span>Prior authorizations, appeals and forms</span>', 1),
         ('<span>Prior auths, appeals and forms included</span>', '<span>Prior authorizations, appeals and forms included</span>', 2),
         ('<span>Direct telephone visits</span>', '<span>Telephone visits</span>', 2),
         ('<span>Direct doctor portal messaging</span>', '<span>Direct portal messaging with Dr. Choi</span>', 2),
         ('<span>1 follow-up visit per month</span>\n<span>Telephone visits</span>\n<span>Glucose log and CGM reviews</span>',
          '<span>1 follow-up visit per month</span>\n<span>Telephone visits</span>\n<span>Review of relevant results and treatment data</span>', 1)]

FAQ_INS_OLD = ('<p style="margin: 0 0 10px;">Personal Endocrine does not participate with or bill insurance plans for your visits. You pay the practice directly for your care, at the time of your visit.</p><p style="margin: 0;">If you have commercial insurance, we can provide a superbill upon request that you may submit to your insurance company for possible out-of-network reimbursement. Coverage varies by plan, so we recommend checking with your insurer before your visit.</p>')
FAQ_INS_NEW = ('<p style="margin: 0 0 10px;">Personal Endocrine does not accept or bill insurance for visits. You pay the practice directly for your care.</p><p style="margin: 0;">If you have commercial insurance, we can provide a superbill on request that you may submit for possible out-of-network reimbursement. Reimbursement depends on your individual plan.</p>')
FAQ_CON_OLD = ('<p style="margin: 0 0 10px;">Personal Endocrine uses a direct specialty care model rather than a traditional concierge model.</p><p style="margin: 0;">You can pay for individual visits or choose a membership for ongoing care. Unlike a traditional concierge model, Personal Endocrine does not bill your insurance for visits in addition to charging a membership fee.</p>')
FAQ_CON_NEW = '<p style="margin: 0;">Personal Endocrine uses a direct specialty care model. You can pay for individual visits or choose a membership for ongoing care. Visits are paid directly to the practice rather than billed to insurance.</p>'
FAQ_LAB_OLD = 'In many cases, yes. You may still use your insurance for labs, imaging and other testing according to your plan’s coverage.'
FAQ_LAB_NEW = 'In many cases, yes. You may still use your insurance for labs, imaging and prescriptions, subject to your plan.'

edit('Main', CARDS + [
    ('See Dr. Choi in person in North Tustin or by telehealth, available in multiple languages.',
     'See Dr. Choi in North Tustin or by telehealth, with care available in English, Spanish and Korean.', 1),
    (FAQ_INS_OLD, FAQ_INS_NEW, 1), (FAQ_CON_OLD, FAQ_CON_NEW, 1), (FAQ_LAB_OLD, FAQ_LAB_NEW, 1)])

GTK_OLD = (pol('New patient deposit', 'A non-refundable $75 deposit is due when your appointment is confirmed. It’s credited toward your visit.')
  + pol('Payment', 'You pay Personal Endocrine directly, at the time of your visit.')
  + pol('Memberships', 'Memberships are optional. You can cancel with 30 days’ notice. If you re-enroll later, a $300 re-enrollment fee applies.')
  + pol('Superbills', 'If you have commercial insurance, we can provide a superbill on request that you may submit for possible out-of-network reimbursement. Coverage varies by plan.')
  + pol('Medicare and Medi-Cal', 'Dr. Choi has opted out of Medicare, so visits can’t be submitted to Medicare for reimbursement. Personal Endocrine also does not accept Medi-Cal.')
  + pol('Primary care', 'Dr. Choi specializes in endocrinology and does not provide primary care. Please keep a primary care physician for needs outside endocrinology.'))
GTK_NEW = (pol('New patient deposit', 'A $75 deposit reserves your first appointment and is applied toward the cost of your visit. The deposit is non-refundable.')
  + pol('Payment', 'Visits are self-pay and paid directly to Personal Endocrine at the time of your appointment.')
  + pol('Memberships', 'Membership is optional. You may cancel with 30 days’ notice. If you decide to rejoin later, a $300 re-enrollment fee applies.')
  + pol('Superbills', 'Have commercial insurance? We can provide a superbill for you to submit for possible out-of-network reimbursement. Reimbursement depends on your individual plan.')
  + pol('Medicare and Medi-Cal', 'Dr. Choi has opted out of Medicare, so visits cannot be submitted to Medicare for reimbursement. Personal Endocrine does not accept Medi-Cal.')
  + pol('Primary care', 'Personal Endocrine provides specialty endocrinology care, not primary care. Please continue seeing your primary care physician for healthcare needs outside endocrinology.'))
edit('Pricing', CARDS + [(GTK_OLD, GTK_NEW, 1),
    ('Personal Endocrine doesn’t bill insurance for your visits. You can still use your insurance',
     'Personal Endocrine does not accept or bill insurance for visits. You can still use your insurance', 1),
    ('Questions about cost? Call', 'Questions about pricing or insurance? Call', 1)])

edit('Ongoing', [
    ('<span>One follow-up visit with Dr. Choi</span>', '<span>One follow-up visit with Dr. Choi each month</span>', 1),
    ('<span>Direct telephone visits</span>', '<span>Telephone visits</span>', 1),
    ('<span>Glucose log and CGM reviews</span>', '<span>Review of relevant results and treatment data</span>', 1),
    ('schedule a direct telephone visit.', 'schedule a telephone visit.', 1),
    ('Membership is optional. You can cancel with 30 days’ notice. If you decide to re-enroll later, a $300 re-enrollment fee applies.',
     'Membership is optional. You may cancel with 30 days’ notice. If you decide to rejoin later, a $300 re-enrollment fee applies.', 1),
    ('Unlike a traditional concierge practice, Personal Endocrine doesn’t bill your insurance for visits on top of a membership fee. You can still use your insurance for labs, imaging and prescriptions.',
     'Personal Endocrine does not accept or bill insurance for visits. You can still use your insurance for labs, imaging and prescriptions, subject to your plan.', 1),
    ('Monthly follow-up, phone visits, CGM reviews and direct messaging.', 'Monthly follow-up, telephone access and messaging with Dr. Choi.', 1)])

edit('Program', [
    ('Diabetes and weight both respond to steady attention.', 'Managing diabetes or weight often takes more than a single appointment.', 1),
    ('Glucose log and CGM reviews, direct telephone visits and portal messaging', 'Glucose log and CGM reviews, telephone visits and portal messaging', 1),
    ('<span>Direct telephone visits</span>', '<span>Telephone visits</span>', 1)])

edit('PayPerVisit', [
    ('New patients pay a non-refundable $75 deposit when the appointment is confirmed. It’s credited toward the visit.',
     'A $75 deposit reserves your first appointment and is applied toward the cost of your visit. The deposit is non-refundable.', 1),
    ('Personal Endocrine doesn’t bill insurance for visits, but you can still use your insurance for labs, imaging and prescriptions. If you have commercial insurance, we can provide a superbill on request.',
     'Personal Endocrine does not accept or bill insurance for visits. If you have commercial insurance, we can provide a superbill on request that you may submit for possible out-of-network reimbursement. Reimbursement depends on your individual plan. You can still use your insurance for labs, imaging and prescriptions, subject to your plan.', 1)])

edit('Weight', [('follow-up visits every two weeks, direct telephone visits,', 'follow-up visits every two weeks, telephone visits,', 1)])

edit('Diabetes', [('Members and patients in the Diabetes and Weight Management Program can receive glucose log and CGM reviews between visits, along with direct portal messaging with Dr. Choi.',
                   'Patients in the Diabetes and Weight Management Program receive glucose log and CGM reviews between visits, along with direct portal messaging with Dr. Choi.', 1)])

edit('Thyroid', [
    (' For most patients being evaluated for primary thyroid dysfunction, TSH is the key initial laboratory test.', '', 1),
    ('Dr. Choi looks at why it is happening rather than treating a lab value in isolation.',
     'Dr. Choi works to understand what’s causing the thyroid abnormality and which treatment is appropriate.', 1),
    ('<p style="margin: 0;">For hypothyroidism, levothyroxine remains the standard treatment when thyroid hormone replacement is needed. Hyperthyroidism requires identifying the underlying cause before deciding among treatment options.</p>\n', '', 1)])

edit('Osteoporosis', [(' Some people at very high fracture risk may benefit from treatments that actively stimulate new bone formation.', '', 1)])

edit('Menopause', [('>And every woman experiences it differently.<', '>The experience is different for every woman.<', 1)])

edit('Book', [
    ('<span style="color: #5D635D; font-size: 13px;">Visits</span><span style="color: #252A26;">Self-pay, due at visit</span>',
     '<span style="color: #5D635D; font-size: 13px;">Visits</span><span style="color: #252A26;">Self-pay. We do not accept or bill insurance.</span>', 1),
    ('<span style="color: #5D635D; font-size: 13px;">Insurance</span><span style="color: #252A26;">Out-of-network with all plans</span>',
     '<span style="color: #5D635D; font-size: 13px;">Commercial insurance</span><span style="color: #252A26;">Superbills available on request for possible out-of-network reimbursement.</span>', 1),
    ('<span style="color: #5D635D; font-size: 13px;">Medicare, Medi-Cal</span><span style="color: #252A26;">Not accepted</span>',
     '<span style="color: #5D635D; font-size: 13px;">Medicare &amp; Medi-Cal</span><span style="color: #252A26;">Not accepted.</span>', 1),
    ('<span style="color: #5D635D; font-size: 13px;">Still covered</span><span style="color: #252A26;">Labs, imaging, prescriptions</span>',
     '<span style="color: #5D635D; font-size: 13px;">Your insurance can still be used for</span><span style="color: #252A26;">Labs, imaging and prescriptions, subject to your plan.</span>', 1),
    ('I understand that visits are self-pay, Personal Endocrine does not accept Medicare or Medi-Cal, and',
     'I understand that visits are self-pay, Personal Endocrine does not accept or bill any insurance, including Medicare and Medi-Cal, and', 1)])

# Parathyroid rename everywhere it is a label
PT = 'Parathyroid &amp; Calcium Disorders'
for f in glob.glob(f'{P}/*.dc.html') + [BOOK]:
    if any(x in f for x in ('Logos', 'Mobile', 'Palettes')): continue
    s = open(f, encoding='utf-8').read(); n = s.count('>Parathyroid<') + s.count('>Parathyroid Conditions<')
    if n:
        s = s.replace('>Parathyroid<', f'>{PT}<').replace('>Parathyroid Conditions<', f'>{PT}<').replace('<title>Parathyroid Conditions</title>', f'<title>{PT}</title>')
        open(f, 'w', encoding='utf-8').write(s); print('parathyroid', f.rsplit('/', 1)[-1], n)
