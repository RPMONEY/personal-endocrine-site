import sys,re,html
s=open(sys.argv[1],encoding='utf-8').read()
s=s[s.find('</header>'):s.find('<footer')]
s=re.sub(r'<(script|style|svg)[^>]*>.*?</\1>','',s,flags=re.S)
s=re.sub(r'<(br|/p|/div|/h\d|/li|/a|/span)[^>]*>','\n',s)
s=re.sub(r'<[^>]+>','',s)
print('\n'.join(l.strip() for l in html.unescape(s).split('\n') if l.strip()))
