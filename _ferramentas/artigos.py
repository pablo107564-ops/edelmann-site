# Artigos de consultoria (/artigos/): textos que o dono de empresa procura no Google, cada um levando a "Agendar conversa".
# Usa sobre/index.html como casca (cabeçalho, estilos, rodapé). Rodar depois do consultoria.py. Idempotente.
import os, re, json
AQUI = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.dirname(AQUI); os.chdir(SITE)
URL = 'https://edelmann.com.br'
WA = 'https://wa.me/5593981212924?text=Ol%C3%A1!%20Quero%20agendar%20uma%20conversa%20com%20a%20Edelmann%20Tecnologia.'
ARROW = '<svg class="i" aria-hidden="true" focusable="false"><use href="#i-arrow"/></svg>'

ARTIGOS = [
  ('planilha-ou-sistema', 'Planilha ou sistema: quando vale a pena mudar',
   'Planilha resolve no começo, mas cobra caro quando a empresa cresce. Veja os sinais de que chegou a hora de um sistema e como fazer a mudança sem parar o negócio.',
   '''<p>Toda empresa começa na planilha, e está tudo bem. Ela é barata, flexível e todo mundo sabe usar. O problema aparece quando o negócio cresce e a planilha continua sendo o centro de tudo.</p>
<h2>Sinais de que a planilha já está custando caro</h2>
<ul>
<li><strong>Mais de uma versão do mesmo arquivo.</strong> "Planilha final", "final 2", "a do João". Ninguém sabe qual está certa.</li>
<li><strong>Informação digitada duas vezes.</strong> A venda vai para a planilha e depois para o financeiro, para o estoque, para a nota.</li>
<li><strong>Só uma pessoa entende o arquivo.</strong> Se ela falta, ninguém fecha o mês.</li>
<li><strong>Erros que só aparecem tarde.</strong> Uma fórmula quebrada pode distorcer meses de números sem ninguém perceber.</li>
<li><strong>Demora para responder perguntas simples.</strong> "Quanto vendemos este mês?" vira meia hora de trabalho.</li>
</ul>
<h2>Sistema não é sinônimo de gastar muito</h2>
<p>O erro mais comum é comprar o sistema mais completo do mercado e usar 10% dele. O caminho certo é o contrário: entender o processo da empresa primeiro e escolher a ferramenta que resolve aquele processo, nem mais nem menos.</p>
<div class="note-box">A pergunta certa não é "qual o melhor sistema?", e sim "qual problema da minha empresa o sistema precisa resolver?".</div>
<h2>Como mudar sem parar a empresa</h2>
<ol>
<li><strong>Mapeie o processo atual</strong>, mesmo que seja bagunçado. É ele que o sistema vai substituir.</li>
<li><strong>Comece pelo ponto que mais dói</strong>: normalmente vendas, estoque ou financeiro.</li>
<li><strong>Rode os dois juntos por um período curto</strong>, para conferir os números.</li>
<li><strong>Treine quem usa no dia a dia</strong>, não só quem decide.</li>
</ol>
<p>Feita com método, a troca se paga em tempo economizado e em decisões tomadas com o número certo na mão.</p>'''),
  ('gastos-com-tecnologia', 'Como saber se a sua empresa está gastando demais com tecnologia',
   'Assinaturas esquecidas, equipamento parado e sistemas que não conversam: um roteiro simples para descobrir onde a tecnologia está pesando no caixa da sua empresa.',
   '''<p>Tecnologia deveria economizar dinheiro. Quando ninguém olha para ela com calma, acontece o contrário: os gastos se acumulam em silêncio, um pouco a cada mês.</p>
<h2>Faça o levantamento em uma tarde</h2>
<p>Liste tudo o que a empresa paga em tecnologia: sistemas, assinaturas, internet, telefonia, licenças, manutenção e equipamentos alugados. Para cada item, responda três perguntas:</p>
<ol>
<li><strong>Quem usa?</strong> Se ninguém sabe responder, provavelmente ninguém usa.</li>
<li><strong>Para quê?</strong> Qual tarefa ele resolve no dia a dia?</li>
<li><strong>Existe outro item que faz a mesma coisa?</strong> Ferramentas repetidas são mais comuns do que parece.</li>
</ol>
<h2>Onde o dinheiro costuma escapar</h2>
<ul>
<li><strong>Assinaturas esquecidas</strong> de testes que viraram cobrança mensal.</li>
<li><strong>Licenças a mais</strong> para funcionários que já saíram.</li>
<li><strong>Sistemas que não conversam</strong>, obrigando alguém a redigitar informação.</li>
<li><strong>Paradas não planejadas</strong>: um computador ou a internet fora do ar no horário de maior venda.</li>
<li><strong>Falta de cópia de segurança</strong>: o custo só aparece no dia em que se perde tudo.</li>
</ul>
<div class="note-box">O gasto mais caro com tecnologia nem sempre está na fatura. Muitas vezes está no tempo da equipe e na venda que não aconteceu.</div>
<h2>E depois do levantamento?</h2>
<p>Corte o que não é usado, junte o que está repetido e invista onde a tecnologia gera retorno claro: menos retrabalho, informação na hora certa e uma operação que não para.</p>'''),
]

casca = open('sobre/index.html', encoding='utf-8').read()

def pagina(slug, titulo, desc, h1, corpo, extra_ld=None):
    url = f'{URL}/artigos/{slug}/' if slug else f'{URL}/artigos/'
    s = re.sub(r'<title>.*?</title>', f'<title>{titulo} | Edelmann Tecnologia</title>', casca, count=1)
    for k in ('description', 'og:description', 'twitter:description'):
        s = re.sub(r'(<meta (?:name|property)="' + k + r'" content=")[^"]*', lambda m: m.group(1) + desc, s)
    for k in ('og:title', 'twitter:title'):
        s = re.sub(r'(<meta (?:name|property)="' + k + r'" content=")[^"]*', lambda m: m.group(1) + titulo, s)
    s = s.replace('<link rel="canonical" href="https://edelmann.com.br/sobre/">', f'<link rel="canonical" href="{url}">')
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, s)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', s, flags=re.S)
    if extra_ld:
        s = s.replace('<style>', '<script type="application/ld+json">\n' + json.dumps(extra_ld, ensure_ascii=False, indent=1) + '\n</script>\n<style>', 1)
    s = s.replace('<a href="/sobre/" aria-current="page">Sobre</a>', '<a href="/sobre/">Sobre</a>')
    s = s.replace('<li><a href="/artigos/">Artigos</a></li>\n        <li><a href="/contato/"', '<li><a href="/artigos/" aria-current="page">Artigos</a></li>\n        <li><a href="/contato/"', 1)  # menu do topo
    trilha = '<nav class="crumbs" aria-label="Trilha"><a href="/">Início</a> › <a href="/artigos/">Artigos</a></nav>' if slug else '<nav class="crumbs" aria-label="Trilha"><a href="/">Início</a> › <span aria-current="page">Artigos</span></nav>'
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
    pagina(slug, t, desc, t, corpo, {"@context": "https://schema.org", "@type": "Article", "headline": t, "description": desc,
           "inLanguage": "pt-BR", "author": {"@type": "Organization", "name": "Edelmann Tecnologia"},
           "publisher": {"@type": "Organization", "name": "Edelmann Tecnologia"}, "mainEntityOfPage": f"{URL}/artigos/{slug}/"})
lista = '<ul class="post-list">' + ''.join(f'<li><a href="/artigos/{s}/"><p class="eyebrow">Artigo</p><h3>{t}</h3><p>{d}</p></a></li>' for s, t, d, _ in ARTIGOS) + '</ul>'
pagina('', 'Artigos sobre gestão e tecnologia', 'Artigos da Edelmann Tecnologia para donos de empresa: gestão, processos e tecnologia que gera resultado.', 'Gestão e tecnologia, <em>sem complicação.</em>', lista)

# sitemap
sm = open('sitemap.xml', encoding='utf-8').read()
for u in ['/artigos/'] + [f'/artigos/{s}/' for s, *_ in ARTIGOS]:
    if f'<loc>{URL}{u}</loc>' not in sm:
        sm = sm.replace('</urlset>', f'  <url><loc>{URL}{u}</loc><lastmod>2026-10-18</lastmod></url>\n</urlset>')
open('sitemap.xml', 'w', encoding='utf-8', newline='\n').write(sm)
print('ok', len(ARTIGOS), 'artigos')
