# Artigos de consultoria (/artigos/): textos que o dono de empresa procura no Google, cada um levando a "Agendar conversa".
# Os artigos novos (comparativos) vêm de artigos_novos.json. Usa sobre/index.html como casca (cabeçalho, estilos, rodapé). Rodar depois do consultoria.py. Idempotente.
import os, re, json, html
AQUI = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.dirname(AQUI); os.chdir(SITE)
URL = 'https://edelmann.com.br'
WA = 'https://wa.me/5593981212924?text=Ol%C3%A1!%20Quero%20agendar%20uma%20conversa%20com%20a%20Edelmann%20Tecnologia.'
ARROW = '<svg class="i" aria-hidden="true" focusable="false"><use href="#i-arrow"/></svg>'

# os 3 artigos mais antigos (texto simples); os comparativos novos estão em artigos_novos.json
ANTIGOS = [
  ('gastos-com-tecnologia', 'Como saber se a sua empresa está gastando demais com tecnologia',
   'Assinaturas esquecidas, equipamento parado e sistemas que não conversam: saiba onde a tecnologia pode estar pesando no caixa da sua empresa.',
   '''<p>Tecnologia deveria economizar dinheiro. Quando ninguém olha para ela com calma, acontece o contrário: os gastos se acumulam em silêncio, um pouco a cada mês.</p>
<h2>O gasto que ninguém vê</h2>
<p>Raramente o problema é uma conta grande. São várias pequenas, espalhadas em cartões, boletos e faturas diferentes, que ninguém olha em conjunto. Somadas ao longo do ano, viram um valor que faria diferença no caixa.</p>
<h2>Onde o dinheiro costuma escapar</h2>
<ul>
<li><strong>Assinaturas esquecidas</strong> de testes que viraram cobrança mensal.</li>
<li><strong>Licenças a mais</strong> para funcionários que já saíram.</li>
<li><strong>Sistemas que não conversam</strong>, obrigando alguém a redigitar informação.</li>
<li><strong>Paradas não planejadas</strong>: um computador ou a internet fora do ar no horário de maior venda.</li>
<li><strong>Falta de cópia de segurança</strong>: o custo só aparece no dia em que se perde tudo.</li>
</ul>
<div class="note-box">O gasto mais caro com tecnologia nem sempre está na fatura. Muitas vezes está no tempo da equipe e na venda que não aconteceu.</div>
<h2>Como a Edelmann ajuda</h2>
<p>Fazemos o diagnóstico completo dos gastos com tecnologia da sua empresa e entregamos o que cortar, o que juntar e onde investir para ter retorno. Você decide com o número na mão.</p>'''),
  ('backup-quanto-custa-perder-dados', 'Backup: quanto custa perder os dados da empresa',
   'Um computador que queima, um vírus ou um celular perdido podem levar anos de informação. Veja quanto isso custa e por que ter backup não basta.',
   '''<p>Quase toda empresa só pensa em backup depois do primeiro susto. O problema é que, nesse dia, normalmente já é tarde: o cadastro de clientes, as notas, o financeiro e o histórico de vendas foram junto.</p>
<h2>O custo que ninguém coloca na conta</h2>
<ul>
<li><strong>Dias parado</strong> enquanto se tenta recuperar ou refazer o que se perdeu.</li>
<li><strong>Retrabalho</strong> para redigitar cadastros, pedidos e lançamentos.</li>
<li><strong>Venda perdida</strong> com o cliente que não pôde ser atendido.</li>
<li><strong>Problemas com o fisco e com clientes</strong> quando faltam notas e comprovantes.</li>
</ul>
<div class="note-box">A pergunta não é "se" um computador vai falhar, e sim "quando". Backup é o que decide se esse dia vai ser um susto ou um prejuízo.</div>
<h2>Ter backup não é o mesmo que estar protegido</h2>
<p>Muitas empresas descobrem no pior momento que a cópia estava incompleta, desatualizada ou não abria. Um pendrive na gaveta ou uma pasta na nuvem configurada há anos raramente resolve.</p>
<h2>Como a Edelmann ajuda</h2>
<p>Avaliamos como os dados da sua empresa estão guardados hoje, mostramos os riscos reais e deixamos a proteção funcionando e conferida.</p>'''),
  ('whatsapp-atendimento-fora-do-horario', 'WhatsApp no atendimento: o cliente que você perde fora do horário',
   'O cliente manda mensagem às 21h e compra de quem responder primeiro. Veja onde o atendimento pelo WhatsApp deixa venda passar.',
   '''<p>Muitos clientes chegam pelo WhatsApp. E vários chegam fora do horário: à noite, no fim de semana, no feriado. Quem responde primeiro, normalmente, leva a venda.</p>
<h2>Onde o atendimento pelo WhatsApp costuma falhar</h2>
<ul>
<li><strong>Mensagem sem resposta</strong> por horas, porque ninguém está de olho.</li>
<li><strong>Um único celular</strong> para todo mundo, sem saber quem respondeu o quê.</li>
<li><strong>Perguntas repetidas</strong> (preço, horário, endereço) tomando o tempo da equipe.</li>
<li><strong>Cliente esquecido</strong>: pediu orçamento, ninguém voltou a falar com ele.</li>
</ul>
<h2>Como a Edelmann ajuda</h2>
<p>Analisamos como a sua empresa atende hoje e montamos um atendimento que responde na hora, a qualquer hora, e passa para a equipe quando precisa, sem deixar nenhum cliente esquecido. Desenvolvemos a nossa própria <a href="/agente-whatsapp/">solução de atendimento automático no WhatsApp</a>.</p>
<div class="note-box">Cada mensagem sem resposta é um cliente indo para o concorrente. Responder rápido costuma ser o que decide a venda.</div>'''),
]

# Os 4 artigos do formato "comparativo" (conclusão no começo, tabela, perguntas no fim) ficam em artigos_novos.json.
NOVOS = json.load(open(os.path.join(AQUI, 'artigos_novos.json'), encoding='utf-8'))
FRASE = ('A Edelmann Tecnologia é uma consultoria em TI de Itaituba (PA) para pequenas e médias empresas, com mais de 15 anos de experiência em TI, '
         'em empresas de diversos setores. Atendemos presencialmente de Itaituba a Santarém, indo até a empresa; em projetos grandes, '
         'vamos até onde for preciso; nos demais casos, por videochamada.')
# título curto para o Google (só no <title> e no og:title; o h1 e o headline não mudam) dos artigos antigos
SEO = {'gastos-com-tecnologia': 'Gastos com tecnologia: onde a empresa gasta demais',
       'whatsapp-atendimento-fora-do-horario': 'WhatsApp fora do horário: o cliente que você perde'}
# ordem da lista em /artigos/: os comparativos primeiro. Datas fixas (não ler o git durante a geração): (publicado, atualizado)
ORDEM = ['consultoria-de-ti-ou-tecnico-avulso', 'como-escolher-empresa-de-ti-itaituba-santarem', 'whatsapp-pessoas-robo-ou-agente-de-ia',
         'planilha-ou-sistema', 'gastos-com-tecnologia', 'backup-quanto-custa-perder-dados', 'whatsapp-atendimento-fora-do-horario']
DATAS = {s: ('2026-10-18', '2026-10-29') for s in ORDEM}
DATAS.update({n['slug']: ('2026-10-29', '2026-10-29') for n in NOVOS if n['slug'] != 'planilha-ou-sistema'})
DATAS.update({s: ('2026-10-18', '2026-10-28') for s, *_ in ANTIGOS})  # texto dos 3 antigos não mudou em 29/10: mantém a data da última revisão do texto
# "Leia também": até 4 artigos relacionados de cada um
RELAC = {
  'consultoria-de-ti-ou-tecnico-avulso': ['como-escolher-empresa-de-ti-itaituba-santarem', 'gastos-com-tecnologia', 'planilha-ou-sistema', 'backup-quanto-custa-perder-dados'],
  'como-escolher-empresa-de-ti-itaituba-santarem': ['consultoria-de-ti-ou-tecnico-avulso', 'gastos-com-tecnologia', 'backup-quanto-custa-perder-dados', 'planilha-ou-sistema'],
  'whatsapp-pessoas-robo-ou-agente-de-ia': ['whatsapp-atendimento-fora-do-horario', 'consultoria-de-ti-ou-tecnico-avulso', 'planilha-ou-sistema'],
  'planilha-ou-sistema': ['gastos-com-tecnologia', 'consultoria-de-ti-ou-tecnico-avulso', 'backup-quanto-custa-perder-dados', 'whatsapp-pessoas-robo-ou-agente-de-ia'],
  'gastos-com-tecnologia': ['planilha-ou-sistema', 'consultoria-de-ti-ou-tecnico-avulso', 'backup-quanto-custa-perder-dados', 'como-escolher-empresa-de-ti-itaituba-santarem'],
  'backup-quanto-custa-perder-dados': ['gastos-com-tecnologia', 'como-escolher-empresa-de-ti-itaituba-santarem', 'consultoria-de-ti-ou-tecnico-avulso', 'planilha-ou-sistema'],
  'whatsapp-atendimento-fora-do-horario': ['whatsapp-pessoas-robo-ou-agente-de-ia', 'planilha-ou-sistema', 'consultoria-de-ti-ou-tecnico-avulso', 'gastos-com-tecnologia'],
}
# unifica: {slug, h1, titulo_seo, descricao, conclusao, corpo_html, faq}. Os 3 antigos não têm conclusão nem perguntas (ainda).
POR_SLUG = {n['slug']: n for n in NOVOS}
for sl, t, d, corpo in ANTIGOS:
    POR_SLUG[sl] = dict(slug=sl, h1=t, titulo_seo=SEO.get(sl, t), descricao=d, conclusao=None, corpo_html=corpo, faq=[])
ARTS = [POR_SLUG[s] for s in ORDEM]
# h1, titulo_seo e descricao entram no HTML sem escape (atributos meta, <title>, <h3>): recusa caracteres que quebrariam a página
assert not [(a['slug'], k) for a in ARTS for k in ('h1', 'titulo_seo', 'descricao') if re.search(r'["<>&]', a[k])]
assert len(ARTS) == len(POR_SLUG) == 7 and all(set(RELAC[s]) <= set(ORDEM) and len(RELAC[s]) <= 4 for s in ORDEM)

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

def trilha(*itens):  # BreadcrumbList: itens = (nome, caminho), o primeiro é o Início
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": URL + c} for i, (n, c) in enumerate(itens, 1)]}

casca = open('sobre/index.html', encoding='utf-8').read()

def pagina(slug, titulo_seo, desc, h1, corpo, extra_ld=None, datas=None, conclusao=None):
    url = f'{URL}/artigos/{slug}/' if slug else f'{URL}/artigos/'
    s = re.sub(r'<title>.*?</title>', f'<title>{titulo_seo} | Edelmann</title>', casca, count=1)
    for k in ('description', 'og:description', 'twitter:description'):
        s = re.sub(r'(<meta (?:name|property)="' + k + r'" content=")[^"]*', lambda m: m.group(1) + desc, s)
    for k in ('og:title', 'twitter:title'):
        s = re.sub(r'(<meta (?:name|property)="' + k + r'" content=")[^"]*', lambda m: m.group(1) + titulo_seo, s)
    s = s.replace('<link rel="canonical" href="https://edelmann.com.br/sobre/">', f'<link rel="canonical" href="{url}">')
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, s)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', s, flags=re.S)
    if extra_ld:
        blocos = ''.join('<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False, indent=1) + '\n</script>\n'
                         for o in (extra_ld if isinstance(extra_ld, list) else [extra_ld]))
        s = s.replace('<style>', blocos + '<style>', 1)
    if datas:  # só nos artigos
        s = s.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">\n'
                      f'<meta property="article:published_time" content="{datas[0]}">\n<meta property="article:modified_time" content="{datas[1]}">', 1)
        s = s.replace('</style>', '\n/* ===== Artigos ===== */\n' + CSS_ART + '</style>', 1)  # a casca (Sobre) é regerada do zero: não duplica
    s = s.replace('<a href="/sobre/" aria-current="page">Sobre</a>', '<a href="/sobre/">Sobre</a>')
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
    sl = a['slug']; d0, d1 = DATAS[sl]
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": a['h1'], "description": a['descricao'],
           "inLanguage": "pt-BR", "datePublished": d0, "dateModified": d1, "image": URL + "/img/og.jpg",
           "author": EMPRESA, "publisher": EMPRESA, "mainEntityOfPage": f"{URL}/artigos/{sl}/"},
          trilha(('Início', '/'), ('Artigos', '/artigos/'), (a['h1'], f'/artigos/{sl}/'))]
    if a['faq']:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f['p'], "acceptedAnswer": {"@type": "Answer", "text": f['r']}} for f in a['faq']]})
    corpo = tabelas(a['corpo_html']) + faq_html(a['faq']) + leia_tambem(sl) + SOBRE_BOX
    pagina(sl, a['titulo_seo'], a['descricao'], a['h1'], corpo, ld, (d0, d1), a['conclusao'])
lista = '<h2 class="sr">Artigos</h2><ul class="post-list">' + ''.join(
    f'<li><a href="/artigos/{a["slug"]}/"><p class="eyebrow">Artigo</p><h3>{a["h1"]}</h3><p>{a["descricao"]}</p></a></li>' for a in ARTS) + '</ul>'
DESC_LISTA = ('Artigos para donos de empresa: consultoria de TI ou técnico avulso, como escolher uma empresa de TI, '
              'atendimento no WhatsApp, planilha ou sistema, gastos e backup.')
pagina('', 'Artigos sobre gestão e tecnologia', DESC_LISTA, 'Gestão e tecnologia, <em>sem complicação.</em>', lista, [
     {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Artigos sobre gestão e tecnologia", "url": f"{URL}/artigos/",
      "inLanguage": "pt-BR", "description": DESC_LISTA},
     trilha(('Início', '/'), ('Artigos', '/artigos/'))])

# sitemap
sm = open('sitemap.xml', encoding='utf-8').read()
for u in ['/artigos/'] + [f'/artigos/{s}/' for s in ORDEM]:
    if f'<loc>{URL}{u}</loc>' not in sm:
        sm = sm.replace('</urlset>', f'  <url><loc>{URL}{u}</loc><lastmod>2026-10-29</lastmod></url>\n</urlset>')
sm = re.sub(r'(<loc>' + re.escape(f'{URL}/artigos/') + r'</loc><lastmod>)[^<]*', r'\g<1>2026-10-29', sm)
for sl, (_, mod) in DATAS.items():  # lastmod dos artigos = data da última revisão
    sm = re.sub(r'(<loc>' + re.escape(f'{URL}/artigos/{sl}/') + r'</loc><lastmod>)[^<]*', r'\g<1>' + mod, sm)
open('sitemap.xml', 'w', encoding='utf-8', newline='\n').write(sm)
print('ok', len(ARTS), 'artigos')
