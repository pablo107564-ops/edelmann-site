# © 2026 Edelmann Tecnologia — edelmann.com.br
# Todos os direitos reservados. Proibido copiar, modificar, distribuir ou fazer engenharia reversa
# deste código sem autorização por escrito da Edelmann Tecnologia.
# Trechos comuns de artigos.py, setores.py e suporte.py (sem efeitos colaterais: pode ser importado).
# As funções leem e gravam a partir da pasta do site (a pasta acima desta).
import os, re, json
from urllib.parse import quote
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'https://edelmann.com.br'
ARROW = '<svg class="i" aria-hidden="true" focusable="false"><use href="#i-arrow"/></svg>'
FONE = '5593992222945'  # único lugar com o número do WhatsApp nos scripts (nos HTML escritos à mão ele aparece como tel: e texto)
def wa_url(msg): return f'https://wa.me/{FONE}?text=' + quote(msg, safe='!')
WA = wa_url('Olá! Quero agendar uma conversa com a Edelmann Tecnologia.')
WA_CHECK = wa_url('Olá! Quero receber o checklist "10 perguntas para descobrir onde a empresa perde dinheiro". Meu nome é ')

# descrição do checklist e duas perguntas de amostra (iguais às do PDF em edelmann-divulgacao/checklist.html)
CHECK_INFO = '''<div class="check-info">
        <p class="check-t">Checklist grátis</p>
        <p>Um checklist em PDF com 10 perguntas sobre o dia a dia da empresa. Enviamos pelo WhatsApp, você responde no seu tempo e vê onde pode estar perdendo tempo e dinheiro.</p>
        <p class="check-t">Duas perguntas de amostra</p>
        <ul>
          <li>Você sabe quanto vendeu ontem, sem precisar perguntar a ninguém?</li>
          <li>Você sabe quanto paga por mês em sistemas, assinaturas e internet?</li>
        </ul>
      </div>'''
CSS_CHECK = '''.signs-cta>div:first-child{flex:1 1 24rem}
.check-info{max-width:34rem;margin-top:1.1rem;text-align:left}
.check-info p{max-width:none;margin:0;font:400 .9375rem/1.5 var(--sans);color:var(--on-night)}
.check-info .check-t{margin-top:1rem;font:500 .75rem/1 var(--mono);letter-spacing:.04em;text-transform:uppercase;color:var(--gold-soft)}
.check-info .check-t:first-child{margin-top:0}
.check-info ul{display:grid;gap:.5rem;margin:.6rem 0 0;padding:0;list-style:none}
.check-info li{padding:.55rem .9rem;border-left:2px solid var(--gold-soft);border-radius:0 8px 8px 0;background:rgba(255,255,255,.04);font-size:.9375rem;line-height:1.4;color:#fff}
.cta-band .check-info{margin:1.75rem auto 0}
'''

def trilha(*itens):  # BreadcrumbList: itens = (nome, caminho), o primeiro é o Início
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": URL + c} for i, (n, c) in enumerate(itens, 1)]}

def faq_ld(pares):  # FAQPage: pares = (pergunta, resposta)
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pares]}

def casca(url, titulo, curto, desc, lds):
    """Sobre como casca (cabeçalho, estilos, rodapé): título, metas, canonical, og:url e JSON-LD (lista de objetos) da página nova.
    `titulo` vai no <title>; `curto` (sem o sufixo '| Edelmann') nos og:title e twitter:title."""
    s = open(os.path.join(SITE, 'sobre', 'index.html'), encoding='utf-8').read()
    s = re.sub(r'<title>.*?</title>', lambda m: f'<title>{titulo}</title>', s, count=1)
    for k in ('description', 'og:description', 'twitter:description'):
        s = re.sub(r'(<meta (?:name|property)="' + k + r'" content=")[^"]*', lambda m: m.group(1) + desc, s)
    for k in ('og:title', 'twitter:title'):
        s = re.sub(r'(<meta (?:name|property)="' + k + r'" content=")[^"]*', lambda m: m.group(1) + curto, s)
    s = s.replace('<link rel="canonical" href="https://edelmann.com.br/sobre/">', f'<link rel="canonical" href="{url}">')
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, s)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', s, flags=re.S)
    blocos = ''.join('<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False, indent=1) + '\n</script>\n' for o in lds)
    s = s.replace('<style>', blocos + '<style>', 1)
    return s.replace('<a href="/sobre/" aria-current="page">Sobre</a>', '<a href="/sobre/">Sobre</a>')

def sitemap_add(url, data):  # põe a URL no sitemap.xml se faltar e deixa o lastmod igual a `data`
    p = os.path.join(SITE, 'sitemap.xml')
    sm = open(p, encoding='utf-8').read()
    if f'<loc>{url}</loc>' not in sm:
        sm = sm.replace('</urlset>', f'  <url><loc>{url}</loc><lastmod>{data}</lastmod></url>\n</urlset>')
    sm = re.sub(r'(<loc>' + re.escape(url) + r'</loc><lastmod>)[^<]*', r'\g<1>' + data, sm)
    open(p, 'w', encoding='utf-8', newline='\n').write(sm)

VISUAL = '/* ===== Visual ===== */'
def com_visual(s):
    """Põe o visual.css como último bloco do <style> (sobrescreve os outros); se já existe, tira e põe de novo no fim."""
    css = open(os.path.join(SITE, '_ferramentas', 'visual.css'), encoding='utf-8').read()
    s = re.sub(r'\n' + re.escape(VISUAL) + r'\n.*?(?=\n/\* =====|</style>)', '', s, count=1, flags=re.S)
    return s.replace('</style>', f'\n{VISUAL}\n{css}</style>', 1)
