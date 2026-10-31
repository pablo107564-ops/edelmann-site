# Página /suporte/ (suporte técnico e manutenção): texto em suporte.json. Usa sobre/index.html como casca, como o setores.py.
# Rodar depois do consultoria.py. Idempotente.
import os, re, json, html
from urllib.parse import quote
from comum import URL, ARROW, trilha, faq_ld, casca, sitemap_add
AQUI = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.dirname(AQUI); os.chdir(SITE)
D = json.load(open(os.path.join(AQUI, 'suporte.json'), encoding='utf-8'))
WA_SUP = 'https://wa.me/5593981212924?text=' + quote(D['msg_whatsapp'], safe='!')
# o título completo já traz "| Edelmann"; nos metas de compartilhamento vai sem o sufixo
assert not [k for k in ('title', 'description', 'h1') if re.search(r'["<>&]', D[k])]
titulo_curto = D['title'].replace(' | Edelmann', '')

s = casca(f'{URL}/suporte/', D['title'], titulo_curto, D['description'], [
    {"@context": "https://schema.org", "@type": "Service", "name": D['h1'], "serviceType": "Suporte técnico e manutenção de TI",
     "description": D['description'], "url": URL + "/suporte/",
     "areaServed": [{"@type": "City", "name": "Itaituba"}, {"@type": "City", "name": "Santarém"}, {"@type": "State", "name": "Pará"}],
     "provider": {"@type": "ProfessionalService", "@id": URL + "/#empresa", "name": "Edelmann Tecnologia", "url": URL + "/"}},
    trilha(('Início', '/'), ('Suporte técnico', '/suporte/')),
    faq_ld([(f['p'], f['r']) for f in D['faq']])])

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

sitemap_add(f'{URL}/suporte/', '2026-10-29')
print('ok /suporte/')
