# Página /suporte/ (suporte técnico e manutenção): texto em suporte.json. Usa sobre/index.html como casca, como o setores.py.
# Rodar depois do consultoria.py e antes do acabamento.py. Idempotente.
import os, re, json, html
from urllib.parse import quote
AQUI = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.dirname(AQUI); os.chdir(SITE)
URL = 'https://edelmann.com.br'
ARROW = '<svg class="i" aria-hidden="true" focusable="false"><use href="#i-arrow"/></svg>'
D = json.load(open(os.path.join(AQUI, 'suporte.json'), encoding='utf-8'))
WA_SUP = 'https://wa.me/5593981212924?text=' + quote(D['msg_whatsapp'], safe='!')
# o título completo já traz "| Edelmann"; nos metas de compartilhamento vai sem o sufixo
assert not [k for k in ('title', 'description', 'h1') if re.search(r'["<>&]', D[k])]
titulo_curto = D['title'].replace(' | Edelmann', '')

def trilha(*itens):  # BreadcrumbList: itens = (nome, caminho), o primeiro é o Início
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": URL + c} for i, (n, c) in enumerate(itens, 1)]}

s = open('sobre/index.html', encoding='utf-8').read()
s = re.sub(r'<title>.*?</title>', f'<title>{D["title"]}</title>', s, count=1)
for k in ('description', 'og:description', 'twitter:description'):
    s = re.sub(r'(<meta (?:name|property)="' + k + r'" content=")[^"]*', lambda m: m.group(1) + D['description'], s)
for k in ('og:title', 'twitter:title'):
    s = re.sub(r'(<meta (?:name|property)="' + k + r'" content=")[^"]*', lambda m: m.group(1) + titulo_curto, s)
s = s.replace('<link rel="canonical" href="https://edelmann.com.br/sobre/">', f'<link rel="canonical" href="{URL}/suporte/">')
s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + URL + '/suporte/', s)
s = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', s, flags=re.S)
ld = {"@context": "https://schema.org", "@type": "Service", "name": D['h1'], "serviceType": "Suporte técnico e manutenção de TI",
      "description": D['description'], "url": URL + "/suporte/",
      "areaServed": [{"@type": "City", "name": "Itaituba"}, {"@type": "City", "name": "Santarém"}, {"@type": "State", "name": "Pará"}],
      "provider": {"@type": "ProfessionalService", "@id": URL + "/#empresa", "name": "Edelmann Tecnologia", "url": URL + "/"}}
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": f['p'], "acceptedAnswer": {"@type": "Answer", "text": f['r']}} for f in D['faq']]}
blocos = ''.join('<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False, indent=1) + '\n</script>\n'
                 for o in (ld, trilha(('Início', '/'), ('Suporte técnico', '/suporte/')), faq_ld))
s = s.replace('<style>', blocos + '<style>', 1)
s = s.replace('<a href="/sobre/" aria-current="page">Sobre</a>', '<a href="/sobre/">Sobre</a>')

faq_html = ''.join(f'<h3>{html.escape(f["p"], quote=False)}</h3><p>{html.escape(f["r"], quote=False)}</p>' for f in D['faq'])
BTN_SUP = f'<a class="btn btn-primary" href="{WA_SUP}" target="_blank" rel="noopener">Preciso de suporte<span class="sr"> (abre o WhatsApp em nova aba)</span>{ARROW}</a>'
BTN_AGENDA = '<a class="btn btn-ghost" href="/contato/#agendar">Agendar conversa</a>'
veja = [('/itaituba/', 'Consultoria em TI de Itaituba a Santarém'), ('/produtos/', 'Soluções que desenvolvemos'),
        ('/artigos/backup-quanto-custa-perder-dados/', 'Backup: quanto custa perder os dados da empresa'),
        ('/artigos/sistema-de-gestao-o-que-perguntar-antes-de-contratar/', 'Sistema de gestão para pequena empresa: o que perguntar antes de contratar')]
veja_html = ''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in veja)
main = f'''<main id="conteudo" tabindex="-1">
  <section class="section" aria-labelledby="titulo">
    <div class="wrap">
      <nav class="crumbs" aria-label="Trilha"><a href="/">Início</a> › <span aria-current="page">Suporte técnico</span></nav>
      <p class="eyebrow">{D['eyebrow']}</p>
      <h1 id="titulo" style="font-size:var(--h2);line-height:1.08;max-width:52rem">{D['h1']}</h1>
      <p class="sub" style="margin-top:1.25rem;max-width:44rem">{D['lead']}</p>
      <div class="ctas" style="margin-top:1.75rem">
        {BTN_SUP}
        {BTN_AGENDA}
      </div>
      <div class="prose" style="margin-top:2.5rem">
        {D['secoes_html']}
        <h2>Perguntas frequentes</h2>
        {faq_html}
        <h2>Veja também</h2>
        <ul>{veja_html}</ul>
      </div>
    </div>
  </section>
  <section class="section band cta-band" aria-labelledby="cta-titulo">
    <div class="wrap">
      <h2 id="cta-titulo">Precisa de ajuda com a tecnologia da sua empresa?</h2>
      <p>Conte o que está acontecendo pelo WhatsApp. Se preferir olhar a tecnologia da empresa como um todo, agende uma conversa sobre a consultoria.</p>
      <div class="ctas">
        {BTN_SUP}
        {BTN_AGENDA}
      </div>
    </div>
  </section>
</main>'''
s = re.sub(r'<main id="conteudo" tabindex="-1">.*?</main>', lambda m: main, s, count=1, flags=re.S)
os.makedirs('suporte', exist_ok=True)
open('suporte/index.html', 'w', encoding='utf-8', newline='\n').write(s)

sm = open('sitemap.xml', encoding='utf-8').read()
u = f'{URL}/suporte/'
if f'<loc>{u}</loc>' not in sm:
    sm = sm.replace('</urlset>', f'  <url><loc>{u}</loc><lastmod>2026-10-29</lastmod></url>\n</urlset>')
open('sitemap.xml', 'w', encoding='utf-8', newline='\n').write(sm)
print('ok /suporte/')
