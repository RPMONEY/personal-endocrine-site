import re
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/0185ca3d-049d-5066-a804-995bec835255/scratchpad'
ff=''.join(re.findall(r'@font-face\{[^}]*\}',open(f'{S}/render/live2/index.html').read().split('</style></head>')[0]))
for n in ['index','pricing','appointment','parathyroid','ongoing-care']:
    s=open(f'{S}/site/personal-endocrine/{n}.html').read().replace('</head>','<style>'+ff+'</style></head>',1)
    s=s.replace('src="/',f'src="file://{S}/site/personal-endocrine/')
    open(f'{S}/render/live2/{n}.html','w').write(s)
jobs=[('index','#care',1440),('index','#care',390),('index','#pricing',1440),('index','#pricing',390),
      ('appointment','aside',1440),('appointment','aside',390),('parathyroid','main h1, h1',1440),
      ('pricing','text=Good to know',1440),('ongoing-care','text=What’s included each month',1440)]
with sync_playwright() as p:
    b=p.chromium.launch()
    for n,sel,w in jobs:
        pg=b.new_page(viewport={'width':w,'height':900})
        pg.goto(f'file://{S}/render/live2/{n}.html'); pg.wait_for_timeout(500)
        sw=pg.evaluate('document.documentElement.scrollWidth')
        el=pg.locator(sel).first
        if sel.startswith('text='): el=el.locator('xpath=ancestor::section[1]')
        if sel.startswith('main h1'): el=el.locator('xpath=ancestor::section[1]')
        out=f'{S}/render/live2/c66_{n}_{sel.strip("#").split()[0].replace("=","")[:8]}_{w}.png'
        el.screenshot(path=out); print(out.rsplit('/',1)[1], 'sw', sw)
    b.close()
