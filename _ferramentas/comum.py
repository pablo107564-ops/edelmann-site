# Trechos comuns de artigos.py, setores.py e suporte.py (sem efeitos colaterais: pode ser importado).
# As funções leem e gravam a partir da pasta do site (a pasta acima desta).
import os, re, json
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'https://edelmann.com.br'
ARROW = '<svg class="i" aria-hidden="true" focusable="false"><use href="#i-arrow"/></svg>'
WA = 'https://wa.me/5593981212924?text=Ol%C3%A1!%20Quero%20agendar%20uma%20conversa%20com%20a%20Edelmann%20Tecnologia.'
WA_CHECK = 'https://wa.me/5593981212924?text=Ol%C3%A1!%20Quero%20receber%20o%20checklist%20%2210%20perguntas%20para%20descobrir%20onde%20a%20empresa%20perde%20dinheiro%22.%20Meu%20nome%20%C3%A9%20'

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
    s = re.sub(r'<title>.*?</title>', f'<title>{titulo}</title>', s, count=1)
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
