# Artigos de consultoria (/artigos/): textos que o dono de empresa procura no Google, cada um levando a "Agendar conversa".
# Os 8 artigos (texto, FAQ e datas) vêm de artigos_novos.json. Usa sobre/index.html como casca (cabeçalho, estilos, rodapé). Rodar depois do consultoria.py. Idempotente.
import os, re, json, html
from comum import URL, ARROW, WA, trilha, faq_ld, casca, sitemap_add
AQUI = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.dirname(AQUI); os.chdir(SITE)

FRASE = ('A Edelmann Tecnologia é uma consultoria em TI de Itaituba (PA) para pequenas e médias empresas, com mais de 15 anos de experiência em TI, '
         'em empresas de diversos setores. Atendemos presencialmente de Itaituba a Santarém, indo até a empresa; em projetos grandes, '
         'vamos até onde for preciso; nos demais casos, por videochamada.')
# ordem da lista em /artigos/: os comparativos primeiro. Datas fixas no JSON (publicado, atualizado): não ler o git durante a geração
ORDEM = ['consultoria-de-ti-ou-tecnico-avulso', 'como-escolher-empresa-de-ti-itaituba-santarem', 'whatsapp-pessoas-robo-ou-agente-de-ia',
         'planilha-ou-sistema', 'sistema-de-gestao-o-que-perguntar-antes-de-contratar', 'gastos-com-tecnologia', 'backup-quanto-custa-perder-dados', 'whatsapp-atendimento-fora-do-horario']
# "Leia também": até 4 artigos relacionados de cada um
RELAC = {
  'consultoria-de-ti-ou-tecnico-avulso': ['como-escolher-empresa-de-ti-itaituba-santarem', 'gastos-com-tecnologia', 'planilha-ou-sistema', 'backup-quanto-custa-perder-dados'],
  'como-escolher-empresa-de-ti-itaituba-santarem': ['consultoria-de-ti-ou-tecnico-avulso', 'gastos-com-tecnologia', 'backup-quanto-custa-perder-dados', 'planilha-ou-sistema'],
  'whatsapp-pessoas-robo-ou-agente-de-ia': ['whatsapp-atendimento-fora-do-horario', 'consultoria-de-ti-ou-tecnico-avulso', 'planilha-ou-sistema'],
  'planilha-ou-sistema': ['sistema-de-gestao-o-que-perguntar-antes-de-contratar', 'gastos-com-tecnologia', 'consultoria-de-ti-ou-tecnico-avulso', 'backup-quanto-custa-perder-dados'],
  'sistema-de-gestao-o-que-perguntar-antes-de-contratar': ['planilha-ou-sistema', 'consultoria-de-ti-ou-tecnico-avulso', 'como-escolher-empresa-de-ti-itaituba-santarem', 'gastos-com-tecnologia'],
  'gastos-com-tecnologia': ['planilha-ou-sistema', 'consultoria-de-ti-ou-tecnico-avulso', 'backup-quanto-custa-perder-dados', 'como-escolher-empresa-de-ti-itaituba-santarem'],
  'backup-quanto-custa-perder-dados': ['gastos-com-tecnologia', 'como-escolher-empresa-de-ti-itaituba-santarem', 'consultoria-de-ti-ou-tecnico-avulso', 'planilha-ou-sistema'],
  'whatsapp-atendimento-fora-do-horario': ['whatsapp-pessoas-robo-ou-agente-de-ia', 'planilha-ou-sistema', 'consultoria-de-ti-ou-tecnico-avulso', 'gastos-com-tecnologia'],
}
# os 8 artigos (texto, FAQ e datas) vêm de artigos_novos.json: {slug, h1, titulo_seo, descricao, conclusao, corpo_html, faq, publicado, atualizado}
ARTS = sorted(json.load(open(os.path.join(AQUI, 'artigos_novos.json'), encoding='utf-8')), key=lambda a: ORDEM.index(a['slug']))
POR_SLUG = {a['slug']: a for a in ARTS}
# h1, titulo_seo e descricao entram no HTML sem escape (atributos meta, <title>, <h3>): recusa caracteres que quebrariam a página
assert not [(a['slug'], k) for a in ARTS for k in ('h1', 'titulo_seo', 'descricao') if re.search(r'["<>&]', a[k])]
assert len(ARTS) == len(POR_SLUG) == 8 and all(set(RELAC[s]) <= set(ORDEM) and len(RELAC[s]) <= 4 for s in ORDEM)

MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
def por_extenso(iso): a, m, d = iso.split('-'); return f'{int(d)} de {MESES[int(m) - 1]} de {a}'
EMPRESA = {"@type": "ProfessionalService", "@id": URL + "/#empresa", "name": "Edelmann Tecnologia", "url": URL + "/", "logo": URL + "/img/icon-512.png"}

CSS_ART = '''.art-resumo{max-width:46rem;margin:1.75rem 0 0;padding:1.25rem 1.4rem;border-left:3px solid var(--gold);border-radius:0 10px 10px 0;background:var(--sand);font-size:1.0625rem;line-height:1.6;color:var(--ink)}
.art-data{margin:1rem 0 0;font:500 .8125rem/1.4 var(--mono);color:var(--muted)}
.tabela{margin:1.5rem 0 1.75rem;overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--paper);-webkit-overflow-scrolling:touch}
.tabela:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.tabela table{width:100%;min-width:34rem;border-collapse:collapse;font-size:.9375rem;line-height:1.45}
.tabela th,.tabela td{padding:.75rem .9rem;text-align:left;vertical-align:top;border-bottom:1px solid var(--line);color:var(--text)}
.tabela thead th{background:var(--sand);color:var(--ink);font-weight:600;white-space:nowrap}
.tabela tbody tr:last-child td{border-bottom:0}
.tabela tbody td:first-child{font-weight:600;color:var(--ink)}
.art-faq h3{margin:1.5rem 0 .4rem;font-size:1.1875rem;line-height:1.3}
.art-faq p{margin:0}
.sobre-box{margin:2.5rem 0 0;padding:1.4rem 1.5rem;border:1px solid var(--line);border-radius:12px;background:var(--paper)}
.sobre-box h2{margin:0 0 .6rem;font-size:1.25rem}
.sobre-box p{margin:0;font-size:.9375rem;line-height:1.6;color:var(--muted)}
.prose .sobre-box h2{margin-top:0}
'''
def leia_tambem(slug):
    itens = ''.join(f'<li><a href="/artigos/{s}/">{POR_SLUG[s]["h1"]}</a></li>' for s in RELAC[slug])
    return (f'\n<h2>Leia também</h2>\n<ul>{itens}</ul>\n'
            '<p>Por ramo: <a href="/setores/comercio/">Comércio</a> · <a href="/setores/saude/">Saúde</a> · <a href="/setores/educacao/">Educação</a></p>')

def faq_html(faq):
    if not faq: return ''
    return ('\n<div class="art-faq">\n<h2>Perguntas frequentes</h2>\n' +
            '\n'.join(f'<h3>{html.escape(f["p"], quote=False)}</h3>\n<p>{html.escape(f["r"], quote=False)}</p>' for f in faq) + '\n</div>')

SOBRE_BOX = ('\n<aside class="sobre-box" aria-labelledby="sobre-edelmann">\n<h2 id="sobre-edelmann">Sobre a Edelmann</h2>\n'
             f'<p>{FRASE}</p>\n</aside>')

def tabelas(corpo):  # tabela dentro de um quadro que rola na horizontal (a página não rola)
    return re.sub(r'<table>(.*?)</table>', lambda m: '<div class="tabela" role="region" aria-label="Tabela comparativa" tabindex="0"><table>' + m.group(1) + '</table></div>', corpo, flags=re.S)

def pagina(slug, titulo_seo, desc, h1, corpo, lds, datas=None, conclusao=None):
    url = f'{URL}/artigos/{slug}/' if slug else f'{URL}/artigos/'
    s = casca(url, f'{titulo_seo} | Edelmann', titulo_seo, desc, lds)
    if datas:  # só nos artigos
        s = s.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">\n'
                      f'<meta property="article:published_time" content="{datas[0]}">\n<meta property="article:modified_time" content="{datas[1]}">', 1)
        s = s.replace('</style>', '\n/* ===== Artigos ===== */\n' + CSS_ART + '</style>', 1)  # a casca (Sobre) é regerada do zero: não duplica
    s = s.replace('<li><a href="/artigos/">Artigos</a></li>', '<li><a href="/artigos/" aria-current="page">Artigos</a></li>', 1)  # menu do topo
    trilha_html = (f'<nav class="crumbs" aria-label="Trilha"><a href="/">Início</a> › <a href="/artigos/">Artigos</a> › <span aria-current="page">{h1}</span></nav>' if slug
                   else '<nav class="crumbs" aria-label="Trilha"><a href="/">Início</a> › <span aria-current="page">Artigos</span></nav>')
    resumo = f'\n      <p class="art-resumo">{conclusao}</p>' if conclusao else ''
    data = (f'\n      <p class="art-data">Atualizado em <time datetime="{datas[1]}">{por_extenso(datas[1])}</time></p>' if datas else '')
    main = f'''<main id="conteudo" tabindex="-1">
  <section class="section" aria-labelledby="titulo">
    <div class="wrap">
      {trilha_html}
      <p class="eyebrow">Artigos</p>
      <h1 id="titulo" style="font-size:var(--h2);line-height:1.08;max-width:52rem">{h1}</h1>{resumo}{data}
      <div class="prose" style="margin-top:2.5rem">
{corpo}
      </div>
    </div>
  </section>
  <section class="section band cta-band" aria-labelledby="cta-titulo">
    <div class="wrap">
      <h2 id="cta-titulo">Quer olhar isso na sua empresa?</h2>
      <p>Um encontro, presencial ou por videochamada, para entender o seu negócio e mostrar onde a tecnologia pode gerar resultado.</p>
      <div class="ctas">
        <a class="btn btn-primary" href="/contato/#agendar">Agendar conversa{ARROW}</a>
        <a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">Falar no WhatsApp<span class="sr"> (abre em nova aba)</span></a>
      </div>
    </div>
  </section>
</main>'''
    s = re.sub(r'<main id="conteudo" tabindex="-1">.*?</main>', lambda m: main, s, count=1, flags=re.S)
    d = os.path.join('artigos', slug) if slug else 'artigos'
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n').write(s)

for a in ARTS:
    sl = a['slug']; d0, d1 = a['publicado'], a['atualizado']
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": a['h1'], "description": a['descricao'],
           "inLanguage": "pt-BR", "datePublished": d0, "dateModified": d1, "image": URL + "/img/og.jpg",
           "author": EMPRESA, "publisher": EMPRESA, "mainEntityOfPage": f"{URL}/artigos/{sl}/"},
          trilha(('Início', '/'), ('Artigos', '/artigos/'), (a['h1'], f'/artigos/{sl}/'))]
    if a['faq']:
        ld.append(faq_ld([(f['p'], f['r']) for f in a['faq']]))
    corpo = tabelas(a['corpo_html']) + faq_html(a['faq']) + leia_tambem(sl) + SOBRE_BOX
    pagina(sl, a['titulo_seo'], a['descricao'], a['h1'], corpo, ld, (d0, d1), a['conclusao'])
lista = '<h2 class="sr">Artigos</h2><ul class="post-list">' + ''.join(
    f'<li><a href="/artigos/{a["slug"]}/"><p class="eyebrow">Artigo</p><h3>{a["h1"]}</h3><p>{a["descricao"]}</p></a></li>' for a in ARTS) + '</ul>'
DESC_LISTA = ('Artigos para donos de empresa: consultoria de TI ou técnico avulso, como escolher uma empresa de TI, '
              'atendimento no WhatsApp, planilha ou sistema, o que perguntar antes de contratar um sistema de gestão, gastos e backup.')
pagina('', 'Artigos sobre gestão e tecnologia', DESC_LISTA, 'Gestão e tecnologia, <em>sem complicação.</em>', lista, [
     {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Artigos sobre gestão e tecnologia", "url": f"{URL}/artigos/",
      "inLanguage": "pt-BR", "description": DESC_LISTA},
     trilha(('Início', '/'), ('Artigos', '/artigos/'))])

# sitemap: lastmod dos artigos = data da última revisão
sitemap_add(f'{URL}/artigos/', '2026-10-29')
for a in ARTS: sitemap_add(f'{URL}/artigos/{a["slug"]}/', a['atualizado'])
print('ok', len(ARTS), 'artigos')
