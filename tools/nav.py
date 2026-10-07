import sys, re

main_path = sys.argv[1]
m = open(main_path, encoding='utf-8').read()
start = m.index('<div class="nl"')
end = m.index('</nav>\n</header>', start)
block = m[start:end]
# interior pages link to the home page instead of in-page anchors
block_sub = re.sub(r'href="#[a-z]+"', 'href="Main.dc.html"', block)

for path in sys.argv[2:]:
    s = open(path, encoding='utf-8').read()
    i = s.index('<div class="nl"')
    j = s.index('</nav>\n</header>', i)
    s = s[:i] + block_sub + s[j:]
    open(path, 'w', encoding='utf-8').write(s)
    print('ok', path.rsplit('/', 1)[-1])
