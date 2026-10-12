# Nos cards de serviço de /servicos/ e /itaituba/: tira o bloco "Veja cada serviço em detalhe" que tinha caído
# dentro do card 01 e põe um link "Saiba mais" em cada card (o card inteiro fica clicável). Idempotente.
import re, os

SITE = r'D:\projetos\edelmann-site'
ARROW = '<svg class="i" aria-hidden="true" focusable="false"><use href="#i-arrow"/></svg>'
# mesma ordem dos 6 cards nas duas páginas
LINKS = [('/servicos/formatacao-e-manutencao/', 'formatação e manutenção'), ('/servicos/redes-e-wifi/', 'redes e Wi-Fi'),
         ('/servicos/servidores/', 'servidores'), ('/servicos/seguranca-e-backup/', 'segurança'),
         ('/produtos/', 'os sistemas'), ('/servicos/seguranca-e-backup/', 'backup')]
CSS = ('.service .more{display:inline-flex;align-items:center;gap:.4rem;margin-top:1.25rem;font:600 .9375rem/1.2 var(--sans);color:var(--gold-ink);text-decoration:none}\n'
       '.service .more .i{width:18px;height:18px;stroke-width:2;transition:transform .2s}\n'
       '.service .more::after{content:"";position:absolute;inset:0}\n'
       '.service:hover .more .i{transform:translateX(3px)}\n'
       '.service .more:focus-visible{outline:none}\n'
       '.service:has(.more:focus-visible){outline:3px solid var(--gold);outline-offset:-3px}\n')

for p in ('servicos/index.html', 'itaituba/index.html'):
    f = os.path.join(SITE, p)
    s = open(f, encoding='utf-8').read()
    if 'class="more"' in s:
        print(p, 'já feito'); continue
    s = re.sub(r'\n\s*<p class="sub reveal" style="margin-top:2.5rem">Veja cada serviço em detalhe:</p>\n\s*<ul class="svc-links reveal">.*?</ul>\n', '\n', s, count=1, flags=re.S)
    a = s.index('<ul class="services')
    b = s.index('</section>', a)
    it = iter(LINKS)
    def add(m):
        h, t = next(it)
        return f'{m.group(1)}\n          <a class="more" href="{h}">Saiba mais<span class="sr"> sobre {t}</span>{ARROW}</a>'
    sec = re.sub(r'(<ul class="tags">.*?</ul>)', add, s[a:b])
    assert sec.count('class="more"') == 6, p
    s = s[:a] + sec + s[b:]
    s = s.replace('/* ===== Componentes extras ===== */', '/* ===== Componentes extras ===== */\n' + CSS, 1)
    assert 'Veja cada serviço em detalhe' not in s, p
    open(f, 'w', encoding='utf-8', newline='\n').write(s)
    print(p, 'ok')
