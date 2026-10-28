# Artigos de consultoria (/artigos/): textos que o dono de empresa procura no Google, cada um levando a "Agendar conversa".
# Usa sobre/index.html como casca (cabeçalho, estilos, rodapé). Rodar depois do consultoria.py. Idempotente.
import os, re, json
AQUI = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.dirname(AQUI); os.chdir(SITE)
URL = 'https://edelmann.com.br'
WA = 'https://wa.me/5593981212924?text=Ol%C3%A1!%20Quero%20agendar%20uma%20conversa%20com%20a%20Edelmann%20Tecnologia.'
ARROW = '<svg class="i" aria-hidden="true" focusable="false"><use href="#i-arrow"/></svg>'

ARTIGOS = [
  ('planilha-ou-sistema', 'Planilha ou sistema: quando vale a pena mudar',
   'Planilha resolve no começo, mas cobra caro quando a empresa cresce. Veja os sinais de que chegou a hora de um sistema.',
   '''<p>Toda empresa começa na planilha, e está tudo bem. Ela é barata, flexível e todo mundo sabe usar. O problema aparece quando o negócio cresce e a planilha continua sendo o centro de tudo.</p>
<h2>Sinais de que a planilha já está custando caro</h2>
<ul>
<li><strong>Mais de uma versão do mesmo arquivo.</strong> "Planilha final", "final 2", "a do João". Ninguém sabe qual está certa.</li>
<li><strong>Informação digitada duas vezes.</strong> A venda vai para a planilha e depois para o financeiro, para o estoque, para a nota.</li>
<li><strong>Só uma pessoa entende o arquivo.</strong> Se ela falta, ninguém fecha o mês.</li>
<li><strong>Erros que só aparecem tarde.</strong> Uma fórmula quebrada pode distorcer meses de números sem ninguém perceber.</li>
<li><strong>Demora para responder perguntas simples.</strong> "Quanto vendemos este mês?" vira um trabalho manual.</li>
</ul>
<h2>Sistema não é sinônimo de gastar muito</h2>
<p>O erro mais comum é comprar o sistema mais completo do mercado e usar só uma pequena parte dele. O caminho certo é o contrário: entender o processo da empresa primeiro e escolher a ferramenta que resolve aquele processo, nem mais nem menos.</p>
<div class="note-box">A pergunta certa não é "qual o melhor sistema?", e sim "qual problema da minha empresa o sistema precisa resolver?".</div>
<h2>Quanto essa demora custa por mês?</h2>
<p>Redigitar, conferir e procurar a versão certa consome horas da equipe todo mês, e esse custo costuma passar despercebido. Na conversa, calculamos juntos quanto isso pesa na sua empresa.</p>
<h2>Como a Edelmann ajuda</h2>
<p>Olhamos a rotina da sua empresa, mostramos onde a planilha está custando caro e indicamos o caminho que se paga mais rápido. A mudança é conduzida por nós, junto com a sua equipe, sem parar a operação.</p>'''),
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

# datas reais de publicação e revisão (fixas: não ler o git durante a geração)
DATAS = {s: ('2026-10-18', '2026-10-28') for s in ('planilha-ou-sistema', 'gastos-com-tecnologia',
         'backup-quanto-custa-perder-dados', 'whatsapp-atendimento-fora-do-horario')}
# título curto para o Google (só no <title> e no og:title; o h1 e o headline não mudam)
SEO = {'gastos-com-tecnologia': 'Gastos com tecnologia: onde a empresa gasta demais',
       'whatsapp-atendimento-fora-do-horario': 'WhatsApp fora do horário: o cliente que você perde'}
EMPRESA = {"@type": "Organization", "@id": URL + "/#empresa", "name": "Edelmann Tecnologia", "url": URL + "/", "logo": URL + "/img/icon-512.png"}

def trilha(*itens):  # BreadcrumbList: itens = (nome, caminho), o primeiro é o Início
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": URL + c} for i, (n, c) in enumerate(itens, 1)]}

def leia_tambem(slug):
    outros = ''.join(f'<li><a href="/artigos/{s}/">{t}</a></li>' for s, t, *_ in ARTIGOS if s != slug)
    return (f'\n<h2>Leia também</h2>\n<ul>{outros}</ul>\n'
            '<p>Por ramo: <a href="/setores/comercio/">Comércio</a> · <a href="/setores/saude/">Saúde</a> · <a href="/setores/educacao/">Educação</a></p>')

casca = open('sobre/index.html', encoding='utf-8').read()

def pagina(slug, titulo, desc, h1, corpo, extra_ld=None, datas=None):
    url = f'{URL}/artigos/{slug}/' if slug else f'{URL}/artigos/'
    curto = SEO.get(slug, titulo)
    s = re.sub(r'<title>.*?</title>', f'<title>{curto} | Edelmann</title>', casca, count=1)
    for k in ('description', 'og:description', 'twitter:description'):
        s = re.sub(r'(<meta (?:name|property)="' + k + r'" content=")[^"]*', lambda m: m.group(1) + desc, s)
    for k in ('og:title', 'twitter:title'):
        s = re.sub(r'(<meta (?:name|property)="' + k + r'" content=")[^"]*', lambda m: m.group(1) + curto, s)
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
    s = s.replace('<a href="/sobre/" aria-current="page">Sobre</a>', '<a href="/sobre/">Sobre</a>')
    s = s.replace('<li><a href="/artigos/">Artigos</a></li>', '<li><a href="/artigos/" aria-current="page">Artigos</a></li>', 1)  # menu do topo
    trilha = f'<nav class="crumbs" aria-label="Trilha"><a href="/">Início</a> › <a href="/artigos/">Artigos</a> › <span aria-current="page">{titulo}</span></nav>' if slug else '<nav class="crumbs" aria-label="Trilha"><a href="/">Início</a> › <span aria-current="page">Artigos</span></nav>'
    main = f'''<main id="conteudo" tabindex="-1">
  <section class="section" aria-labelledby="titulo">
    <div class="wrap">
      {trilha}
      <p class="eyebrow">Artigos</p>
      <h1 id="titulo" style="font-size:var(--h2);line-height:1.08;max-width:52rem">{h1}</h1>
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

for slug, t, desc, corpo in ARTIGOS:
    d0, d1 = DATAS[slug]
    pagina(slug, t, desc, t, corpo + leia_tambem(slug), [
           {"@context": "https://schema.org", "@type": "Article", "headline": t, "description": desc,
            "inLanguage": "pt-BR", "datePublished": d0, "dateModified": d1, "image": URL + "/img/og.jpg",
            "author": EMPRESA, "publisher": EMPRESA, "mainEntityOfPage": f"{URL}/artigos/{slug}/"},
           trilha(('Início', '/'), ('Artigos', '/artigos/'), (t, f'/artigos/{slug}/'))], (d0, d1))
lista = '<h2 class="sr">Artigos</h2><ul class="post-list">' + ''.join(f'<li><a href="/artigos/{s}/"><p class="eyebrow">Artigo</p><h3>{t}</h3><p>{d}</p></a></li>' for s, t, d, _ in ARTIGOS) + '</ul>'
pagina('', 'Artigos sobre gestão e tecnologia', 'Artigos da Edelmann Tecnologia para donos de empresa: gestão, processos e tecnologia que gera resultado.', 'Gestão e tecnologia, <em>sem complicação.</em>', lista, [
     {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Artigos sobre gestão e tecnologia", "url": f"{URL}/artigos/",
      "inLanguage": "pt-BR", "description": 'Artigos da Edelmann Tecnologia para donos de empresa: gestão, processos e tecnologia que gera resultado.'},
     trilha(('Início', '/'), ('Artigos', '/artigos/'))])

# sitemap
sm = open('sitemap.xml', encoding='utf-8').read()
for u in ['/artigos/'] + [f'/artigos/{s}/' for s, *_ in ARTIGOS]:
    if f'<loc>{URL}{u}</loc>' not in sm:
        sm = sm.replace('</urlset>', f'  <url><loc>{URL}{u}</loc><lastmod>2026-10-18</lastmod></url>\n</urlset>')
sm = re.sub(r'(<loc>' + re.escape(f'{URL}/artigos/') + r'</loc><lastmod>)[^<]*', r'\g<1>2026-10-28', sm)
for sl, (_, mod) in DATAS.items():  # lastmod dos artigos = data da última revisão
    sm = re.sub(r'(<loc>' + re.escape(f'{URL}/artigos/{sl}/') + r'</loc><lastmod>)[^<]*', r'\g<1>' + mod, sm)
open('sitemap.xml', 'w', encoding='utf-8', newline='\n').write(sm)
print('ok', len(ARTIGOS), 'artigos')
