# Páginas por setor (/setores/<setor>/): dores típicas do ramo + o que muda + chamada para conversa e checklist.
# Usa sobre/index.html como casca. Rodar depois do consultoria.py. Idempotente.
import os, re, json
AQUI = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.dirname(AQUI); os.chdir(SITE)
URL = 'https://edelmann.com.br'
ARROW = '<svg class="i" aria-hidden="true" focusable="false"><use href="#i-arrow"/></svg>'
WA_CHECK = 'https://wa.me/5593981212924?text=Ol%C3%A1!%20Quero%20receber%20o%20checklist%20%2210%20perguntas%20para%20descobrir%20onde%20a%20empresa%20perde%20dinheiro%22.%20Meu%20nome%20%C3%A9%20'

SETORES = [
  ('comercio', 'Comércio', 'Consultoria em TI para o comércio',
   'Supermercados, lojas e materiais de construção: estoque que bate, caixa que fecha e números na mão para decidir. Consultoria em TI em Itaituba e região.',
   'Supermercados, materiais de construção, lojas e atacados.',
   [('Estoque que não bate', 'O sistema diz uma coisa, a prateleira diz outra, e a diferença vira prejuízo.'),
    ('Caixa que demora a fechar', 'Conferência manual no fim do dia, diferença que ninguém sabe explicar.'),
    ('Fila e venda perdida', 'Sistema lento ou internet fora do ar no horário de maior movimento.'),
    ('Compra no escuro', 'Sem saber o que mais vende e o que está parado, a compra vira chute.'),
    ('Nota fiscal com erro', 'Retrabalho com o contador e risco com o fisco.')],
   ['Estoque, vendas e financeiro conversando entre si', 'Fechamento de caixa mais rápido e com menos conferência manual',
    'Relatórios simples do que vende e do que está parado', 'Operação que continua mesmo com falha de internet']),
  ('saude', 'Saúde', 'Consultoria em TI para clínicas e farmácias',
   'Clínicas, consultórios, farmácias e laboratórios: agenda organizada, dados de pacientes protegidos e atendimento sem espera. Consultoria em TI em Itaituba e região.',
   'Clínicas, consultórios, farmácias e laboratórios.',
   [('Agenda bagunçada', 'Horário duplicado, paciente esquecido e falta sem aviso.'),
    ('Dados de pacientes expostos', 'Fichas e exames sem cópia de segurança nem controle de acesso, um risco diante da LGPD.'),
    ('Atendimento que demora', 'Recepção sobrecarregada respondendo as mesmas perguntas no telefone e no WhatsApp.'),
    ('Estoque de medicamentos e insumos', 'Vencimento que passa despercebido e falta do que mais sai.'),
    ('Financeiro e convênios', 'Repasses e glosas difíceis de acompanhar.')],
   ['Agenda e confirmações organizadas', 'Dados protegidos, com cópia de segurança e acesso controlado',
    'Atendimento mais rápido na recepção e no WhatsApp', 'Controle de estoque e de vencimentos']),
  ('educacao', 'Educação', 'Consultoria em TI para escolas',
   'Escolas particulares, cursos e faculdades: matrícula e financeiro organizados, comunicação com os pais e rede que funciona. Consultoria em TI em Itaituba e região.',
   'Escolas particulares, cursos livres e faculdades.',
   [('Matrícula e mensalidade no papel', 'Inadimplência difícil de acompanhar e cobrança feita na mão.'),
    ('Comunicação com os pais', 'Recados espalhados em grupos, e a informação importante se perde.'),
    ('Rede e equipamentos que falham', 'Laboratório e sala de aula parados quando a internet ou o computador cai.'),
    ('Dados de alunos sem proteção', 'Documentos e notas sem cópia de segurança, um risco diante da LGPD.'),
    ('Secretaria sobrecarregada', 'Declarações, boletins e atendimento consumindo o dia inteiro.')],
   ['Matrícula e financeiro organizados, com a inadimplência à vista', 'Comunicação clara com pais e alunos',
    'Rede e equipamentos estáveis', 'Dados de alunos protegidos e secretaria mais ágil']),
]

# frase de abertura, pergunta depois das dores e links "Veja também" de cada setor
EXTRA = {
  'comercio': dict(frase='Quem vende todos os dias não pode perder tempo conferindo caixa e estoque na mão.',
                   pergunta='Reconhece isso no seu comércio?', artigo='planilha-ou-sistema', solucao=('/balcao/', 'Conheça o Balcão PDV')),
  'saude': dict(frase='Agenda que falha e ficha de paciente sem proteção custam consulta e confiança.',
                pergunta='Reconhece isso na sua clínica ou farmácia?', artigo='backup-quanto-custa-perder-dados',
                solucao=('/agente-whatsapp/', 'Conheça o Agente de IA no WhatsApp')),
  'educacao': dict(frase='Secretaria sobrecarregada e dados de alunos sem proteção pesam no ano letivo.',
                   pergunta='Reconhece isso na sua escola?', artigo='backup-quanto-custa-perder-dados', solucao=None),
}
# títulos dos artigos (cópia local: importar artigos.py geraria as páginas)
TIT_ARTIGO = {'planilha-ou-sistema': 'Planilha ou sistema: quando vale a pena mudar',
              'backup-quanto-custa-perder-dados': 'Backup: quanto custa perder os dados da empresa'}
CHECK_BTN = f'<a class="btn btn-ghost" href="{WA_CHECK}" target="_blank" rel="noopener">Receber o checklist grátis<span class="sr"> (abre o WhatsApp em nova aba)</span></a>'

def trilha(*itens):  # BreadcrumbList: itens = (nome, caminho), o primeiro é o Início
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": URL + c} for i, (n, c) in enumerate(itens, 1)]}

casca = open('sobre/index.html', encoding='utf-8').read()

def gerar(slug, nome, h1, desc, quem, dores, ganhos):
    url = f'{URL}/setores/{slug}/'
    titulo = f'{h1} em Itaituba'
    x = EXTRA[slug]
    s = re.sub(r'<title>.*?</title>', f'<title>{titulo} | Edelmann</title>', casca, count=1)
    for k in ('description', 'og:description', 'twitter:description'):
        s = re.sub(r'(<meta (?:name|property)="' + k + r'" content=")[^"]*', lambda m: m.group(1) + desc, s)
    for k in ('og:title', 'twitter:title'):
        s = re.sub(r'(<meta (?:name|property)="' + k + r'" content=")[^"]*', lambda m: m.group(1) + titulo, s)
    s = s.replace('<link rel="canonical" href="https://edelmann.com.br/sobre/">', f'<link rel="canonical" href="{url}">')
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, s)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', s, flags=re.S)
    ld = {"@context": "https://schema.org", "@type": "Service", "name": h1, "serviceType": "Consultoria em TI",
          "areaServed": {"@type": "City", "name": "Itaituba"}, "provider": {"@type": "ProfessionalService", "@id": URL + "/#empresa", "name": "Edelmann Tecnologia", "url": URL + '/'}}
    blocos = ''.join('<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False, indent=1) + '\n</script>\n'
                     for o in (ld, trilha(('Início', '/'), (nome, f'/setores/{slug}/'))))
    s = s.replace('<style>', blocos + '<style>', 1)
    s = s.replace('<a href="/sobre/" aria-current="page">Sobre</a>', '<a href="/sobre/">Sobre</a>')
    dores_html = ''.join(f'<li><strong>{t}.</strong> {d}</li>' for t, d in dores)
    ganhos_html = ''.join(f'<li>{g}</li>' for g in ganhos)
    veja = [(f'/setores/{sl}/', h) for sl, _, h, *_ in SETORES if sl != slug]
    veja.append((f'/artigos/{x["artigo"]}/', TIT_ARTIGO[x['artigo']]))
    veja.append(('/itaituba/', 'Consultoria em TI em Itaituba e região'))
    if x['solucao']: veja.append(x['solucao'])
    veja_html = ''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in veja)
    main = f'''<main id="conteudo" tabindex="-1">
  <section class="section" aria-labelledby="titulo">
    <div class="wrap">
      <nav class="crumbs" aria-label="Trilha"><a href="/">Início</a> › <span aria-current="page">{nome}</span></nav>
      <p class="eyebrow">Setor · {nome}</p>
      <h1 id="titulo" style="font-size:var(--h2);line-height:1.08;max-width:52rem">{h1} em Itaituba.</h1>
      <p class="sub" style="margin-top:1.25rem;max-width:44rem">{x["frase"]} {quem} Atendimento presencial em <a class="link" href="/itaituba/">Itaituba e região</a>, ou por videochamada.</p>
      <div class="prose" style="margin-top:2.5rem">
        <h2>O que mais pesa no dia a dia</h2>
        <ul>{dores_html}</ul>
        <p><strong>{x["pergunta"]}</strong></p>
      </div>
      <div class="ctas" style="margin-top:0">{CHECK_BTN}</div>
      <div class="prose" style="margin-top:2.5rem">
        <h2>O que buscamos alcançar</h2>
        <ul>{ganhos_html}</ul>
        <div class="note-box">Começamos entendendo como a sua empresa funciona hoje. Só depois apresentamos as prioridades e o resultado esperado. Nada começa sem a sua aprovação.</div>
        <h2>Veja também</h2>
        <ul>{veja_html}</ul>
      </div>
    </div>
  </section>
  <section class="section band cta-band" aria-labelledby="cta-titulo">
    <div class="wrap">
      <h2 id="cta-titulo">Vamos conversar sobre a sua empresa?</h2>
      <p>Presencial em Itaituba e região, ou por videochamada. Se preferir começar devagar, peça o nosso checklist: 10 perguntas para descobrir onde a sua empresa perde dinheiro.</p>
      <p>Seu ramo é outro? Atendemos empresas de diversos setores. Conte o seu caso.</p>
      <div class="ctas">
        <a class="btn btn-primary" href="/contato/#agendar">Agendar conversa{ARROW}</a>
        <a class="btn btn-ghost" href="{WA_CHECK}" target="_blank" rel="noopener">Receber o checklist grátis<span class="sr"> (abre o WhatsApp em nova aba)</span></a>
      </div>
    </div>
  </section>
</main>'''
    s = re.sub(r'<main id="conteudo" tabindex="-1">.*?</main>', lambda m: main, s, count=1, flags=re.S)
    os.makedirs(f'setores/{slug}', exist_ok=True)
    open(f'setores/{slug}/index.html', 'w', encoding='utf-8', newline='\n').write(s)

for st in SETORES: gerar(*st)

sm = open('sitemap.xml', encoding='utf-8').read()
for slug, *_ in SETORES:
    u = f'{URL}/setores/{slug}/'
    if f'<loc>{u}</loc>' not in sm:
        sm = sm.replace('</urlset>', f'  <url><loc>{u}</loc><lastmod>2026-10-18</lastmod></url>\n</urlset>')
sm = re.sub(r'(<loc>https://edelmann\.com\.br/setores/[a-z]+/</loc><lastmod>)[^<]*', r'\g<1>2026-10-28', sm)
open('sitemap.xml', 'w', encoding='utf-8', newline='\n').write(sm)
print('ok', len(SETORES), 'setores')
