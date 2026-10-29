# Reposiciona o site como consultoria (outubro de 2026): o site prova quem somos e leva o cliente a agendar uma conversa.
# - início, Sobre, Contato e Itaituba ganham conteúdo novo (trechos em consultoria/*.html, com marcadores {{...}});
# - menu, rodapé e chamadas de todas as páginas passam a convidar para "Agendar conversa";
# - Serviços e Dicas viram redirecionamentos para o início e saem do sitemap.
# Idempotente: pode rodar de novo (refaz as páginas a partir dos trechos e não duplica trocas).
import os, re, json, glob

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
os.chdir(SITE)

def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8', newline='\n').write(s)
def icon(n): return f'<svg class="i" aria-hidden="true" focusable="false"><use href="#i-{n}"/></svg>'
ARROW = icon('arrow')
WA = 'https://wa.me/5593981212924?text=Ol%C3%A1!%20Quero%20agendar%20uma%20conversa%20com%20a%20Edelmann%20Tecnologia.'

SYMBOLS = {
    'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    'coin': '<circle cx="12" cy="12" r="8.5"/><path d="M14.5 9.2c-.5-.8-1.4-1.2-2.5-1.2-1.4 0-2.5.8-2.5 1.9 0 2.6 5 1.4 5 4.1 0 1.1-1.1 2-2.5 2-1.2 0-2.2-.5-2.7-1.4M12 6.5V8M12 16v1.5"/>',
    'chart': '<path d="M4 20h16"/><path d="M7 16v-4M12 16V8M17 16v-7"/>',
}

# ---------- trechos repetidos ----------
CAMPOS = '''          <div class="row">
            <label>Seu nome<input name="nome" autocomplete="name" required pattern=".*\\S.*" title="Informe seu nome"></label>
            <label><span>Empresa <small>(opcional)</small></span><input name="empresa" autocomplete="organization"></label>
          </div>
          <label>Como prefere conversar?
            <select name="formato"><option>Presencial, de Itaituba a Santarém</option><option>Videochamada</option></select>
          </label>
          <label><span>O que mais pesa na empresa hoje? <small>(opcional)</small></span><textarea name="desafio" placeholder="Ex.: o que a empresa faz e o que você espera alcançar"></textarea></label>'''
NOSCRIPT = (f'<noscript><style>#form-agenda{{display:none}}</style><p class="fine">Para agendar, fale pelo <a href="{WA}">WhatsApp (93) 98121-2924</a> ou pelo '
            '<a href="mailto:edelmann.tecnologia@gmail.com?subject=Agendar%20conversa%20-%20Edelmann%20Tecnologia">e-mail</a>.</p></noscript>')
FORM_DARK = f'''      <div class="quote" id="agendar">
        <h2>Agende uma conversa.</h2>
        <form class="form" id="form-agenda">
{CAMPOS}
          <button class="btn btn-primary" type="submit">Agendar pelo WhatsApp<span class="sr"> (abre em nova aba)</span>{ARROW}</button>
          <p class="fine">Abre o WhatsApp com a mensagem pronta; por lá combinamos o dia e o horário. Prefere e-mail? <button class="alt-send" type="button" id="agenda-email">Enviar por e-mail</button>. Nada fica guardado no site. Veja a <a href="/privacidade/">política de privacidade</a>.</p>
          <p class="fine" id="agenda-status" role="status" aria-live="polite"></p>
        </form>
        {NOSCRIPT}
      </div>'''
FORM_CLARO = f'''      <form class="form" id="form-agenda">
{CAMPOS}
        <div class="actions">
          <button class="btn btn-primary" type="submit">Agendar pelo WhatsApp<span class="sr"> (abre em nova aba)</span>{ARROW}</button>
          <button class="btn btn-ghost" type="button" id="agenda-email">Enviar por e-mail</button>
        </div>
        <p class="fine">Ao enviar, abrimos o WhatsApp ou o e-mail com a mensagem pronta para você conferir. Por lá combinamos o dia e o horário. Veja a <a href="/privacidade/">política de privacidade</a>.</p>
        <p class="fine" id="agenda-status" role="status" aria-live="polite"></p>
      </form>
      {NOSCRIPT}'''
FORM_JS = '''<script>
/* Agendamento: monta a mensagem no navegador e abre WhatsApp ou e-mail. Nada é enviado ao site. */
(function(){
  var f=document.getElementById('form-agenda'); if(!f)return;
  var st=document.getElementById('agenda-status');
  function v(n){return String(new FormData(f).get(n)||'').trim()}
  function msg(){
    var l=['Olá! Quero agendar uma conversa com a Edelmann Tecnologia.','','Nome: '+v('nome')];
    if(v('empresa'))l.push('Empresa: '+v('empresa'));
    l.push('Formato: '+v('formato'));
    if(v('desafio'))l.push('','O que mais pesa hoje: '+v('desafio'));
    return l.join('\\n');
  }
  function aviso(antes,href,rotulo,depois){  /* texto + link de reserva, sem innerHTML */
    if(!st)return; st.textContent=antes;
    if(href){var a=document.createElement('a');a.href=href;a.target='_blank';a.rel='noopener';a.textContent=rotulo;st.appendChild(a)}
    if(depois)st.appendChild(document.createTextNode(depois));
  }
  f.addEventListener('submit',function(e){
    e.preventDefault(); if(!f.reportValidity())return;
    var u='https://wa.me/5593981212924?text='+encodeURIComponent(msg());
    window.open(u,'_blank','noopener');
    aviso('Se o WhatsApp não abriu, ',u,'toque aqui','.');
  });
  document.getElementById('agenda-email').addEventListener('click',function(){
    if(!f.reportValidity())return;
    var a=document.createElement('a');
    a.href='mailto:edelmann.tecnologia@gmail.com?subject='+encodeURIComponent('Agendar conversa - '+(v('empresa')||v('nome')))+'&body='+encodeURIComponent(msg());
    document.body.appendChild(a); a.click(); a.remove();
    aviso('Se o seu e-mail não abriu, escreva para edelmann.tecnologia@gmail.com.');
  });
})();
</script>
'''
WA_CHECK = 'https://wa.me/5593981212924?text=Ol%C3%A1!%20Quero%20receber%20o%20checklist%20%2210%20perguntas%20para%20descobrir%20onde%20a%20empresa%20perde%20dinheiro%22.%20Meu%20nome%20%C3%A9%20'
SINAIS_ITENS = [
    ('Retrabalho e tarefas repetidas', 'A equipe gasta horas fazendo à mão o que poderia ser rotina.'),
    ('Informação espalhada', 'Dados em planilhas, cadernos e conversas, e ninguém tem o número certo na hora de decidir.'),
    ('Tecnologia que não se paga', 'Sistemas, assinaturas e equipamentos que custam caro e não trazem retorno claro.'),
    ('Sistemas que não conversam', 'Cada setor com a sua ferramenta, e a mesma informação digitada mais de uma vez.'),
    ('Dependência de uma pessoa', 'Se alguém falta ou sai da empresa, parte do negócio para.'),
    ('Risco de parar', 'Uma falha, um ataque ou a perda de dados pode deixar a empresa sem operar.'),
]
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
SINAIS = f'''  <section class="section" id="sinais" aria-labelledby="sinais-titulo">
    <div class="wrap">
      <div class="head reveal">
        <div>
          <p class="eyebrow">Sinais</p>
          <h2 id="sinais-titulo">Isso acontece <em>na sua empresa?</em></h2>
        </div>
        <p class="sub">Situações comuns quando o negócio cresce e os processos não acompanham. Todas pesam no resultado.</p>
      </div>
      <ul class="signs reveal">
''' + '\n'.join(f'        <li><h3>{t}</h3><p>{d}</p></li>' for t, d in SINAIS_ITENS) + f'''
      </ul>
      <div class="signs-cta reveal">
        <div>
          <p>Se você reconheceu algum desses pontos, vale uma conversa. Ou comece pelo nosso checklist: 10 perguntas para descobrir onde a sua empresa perde dinheiro.</p>
          {CHECK_INFO}
        </div>
        <div class="ctas" style="margin:0">
          <a class="btn btn-primary" href="#agendar">Agendar conversa{ARROW}</a>
          <a class="btn btn-ghost" href="{WA_CHECK}" target="_blank" rel="noopener">Receber o checklist grátis<span class="sr"> (abre o WhatsApp em nova aba)</span></a>
        </div>
      </div>
    </div>
  </section>'''
STATS = '''      <ul class="stats reveal">
        <li><b>15+</b><span>anos de experiência em TI, em empresas de comércio, saúde, educação e outros setores</span></li>
        <li><b>Ponta a ponta</b><span>do diagnóstico à execução: planejamos, implantamos e acompanhamos junto com a sua equipe</span></li>
        <li><b>Rigor</b><span>a mesma exigência de prazo, documentação e prestação de contas dos contratos públicos</span></li>
      </ul>'''
# faixa logo abaixo do topo (início e Itaituba): os números da experiência
PROOF = f'''  <section class="proof" aria-label="A Edelmann em números">
    <div class="wrap">
{STATS}
    </div>
  </section>'''
def como_funciona(classe): return f'''  <section class="{classe}" id="como-funciona" aria-labelledby="como-funciona-titulo">
    <div class="wrap">
      <div class="head reveal">
        <div>
          <p class="eyebrow">Como funciona</p>
          <h2 id="como-funciona-titulo">Do primeiro contato <em>ao resultado.</em></h2>
        </div>
        <p class="sub">Em todas as fases da gestão: planejar, estruturar, operar e evoluir.</p>
      </div>
      <ol class="steps three reveal">
        <li class="step"><h3>Conversa</h3><p>Você conta como o negócio funciona e o que mais pesa hoje; nós ouvimos e perguntamos.</p></li>
        <li class="step"><h3>Diagnóstico e proposta</h3><p>Mostramos o que encontramos, as prioridades e o impacto esperado, com escopo e etapas. Você decide se e quando seguir.</p></li>
        <li class="step"><h3>Execução e acompanhamento</h3><p>Colocamos o plano em prática junto com a sua equipe e acompanhamos os resultados. Nada começa sem a sua aprovação.</p></li>
      </ol>
      <p class="more reveal"><a class="btn btn-primary" href="#agendar">Agendar conversa{ARROW}</a></p>
    </div>
  </section>'''
CTA_TXT = 'Um encontro, presencial ou por videochamada, para entender os seus objetivos e mostrar onde a tecnologia pode gerar resultado.'
WA_BTN = f'<a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">Falar no WhatsApp<span class="sr"> (abre em nova aba)</span></a>'
CHECK_BTN = f'<a class="btn btn-ghost" href="{WA_CHECK}" target="_blank" rel="noopener">Receber o checklist grátis<span class="sr"> (abre o WhatsApp em nova aba)</span></a>'
def cta(classe, alvo, final=False, titulo='Vamos conversar sobre o seu negócio?'):  # final: o último bloco da página abre o WhatsApp direto e oferece o checklist
    botoes = (f'<a class="btn btn-primary" href="{WA}" target="_blank" rel="noopener">Agendar pelo WhatsApp<span class="sr"> (abre em nova aba)</span>{ARROW}</a>\n        {CHECK_BTN}' if final
              else f'<a class="btn btn-primary" href="{alvo}">Agendar conversa{ARROW}</a>\n        {WA_BTN}')
    return f'''  <section class="{classe}" aria-labelledby="cta-titulo">
    <div class="wrap reveal">
      <h2 id="cta-titulo">{titulo}</h2>
      <p>{CTA_TXT}</p>
      <div class="ctas">
        {botoes}
      </div>
    </div>
  </section>'''
FAQ = [
    ('Como é a primeira conversa?', 'Um encontro presencial, indo até a sua empresa entre Itaituba e Santarém, ou por videochamada. Conversamos sobre o negócio, os objetivos e os principais desafios, e a partir daí indicamos os próximos passos.'),
    ('Vocês conhecem o meu ramo?', 'Sim. Já atendemos empresas de comércio, saúde e educação, entre outros setores, e também temos experiência com contratos públicos. A primeira conversa serve para entender como o seu negócio funciona; só depois propomos qualquer coisa.'),
    ('Vai atrapalhar a rotina da minha empresa?', 'Nada muda sem a sua aprovação. Cada etapa é combinada antes e conduzida junto com a sua equipe, respeitando a rotina da empresa.'),
    ('Preciso trocar os sistemas que já uso?', 'Recomendamos apenas o que traz retorno para o negócio, sempre explicando o motivo. Se o que você já usa atende, não há razão para trocar.'),
    ('Vocês atendem fora de Itaituba?', 'Sim. Vamos até a sua empresa em toda a região entre Itaituba e Santarém. Para projetos maiores, vamos presencialmente até onde for preciso, como Marabá. Nos demais casos, a conversa e o acompanhamento são por videochamada.'),
    ('Como é definido o valor?', 'Depois de entender o negócio, apresentamos uma proposta com o escopo, as etapas e o valor. Nada começa sem a sua aprovação.'),
]
FAQ_HTML = '      <div class="faq reveal">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + '</div>'
def ld(obj): return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=1) + '\n</script>\n'
FAQ_LD = ld({"@context": "https://schema.org", "@type": "FAQPage",
             "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]})
MARCAS = {'{{FORM_DARK}}': FORM_DARK, '{{FORM_CLARO}}': FORM_CLARO, '{{PROOF}}': PROOF, '{{SINAIS}}': SINAIS, '{{STATS}}': STATS,
          '{{COMO_FUNCIONA}}': como_funciona('section'), '{{COMO_FUNCIONA_ALT}}': como_funciona('section alt'),
          '{{CTA}}': cta('cta-accent', '#agendar', final=True), '{{CTA_CLARO}}': cta('section band cta-band', '/contato/#agendar', titulo='Conheceu a Edelmann. Agora conte sobre o seu negócio.'),
          '{{CTA_ITA}}': cta('cta-accent', '#agendar', final=True, titulo='Vamos conversar sobre a sua empresa em Itaituba?'),
          '{{CTA_WA}}': cta('section band cta-band', None, final=True), '{{WA_CHECK}}': WA_CHECK,
          '{{FAQ}}': FAQ_HTML, '{{ARROW}}': ARROW, '{{WA}}': WA}
def trecho(nome):
    s = rd(os.path.join(AQUI, 'consultoria', nome))
    for k, v in MARCAS.items(): s = s.replace(k, v)
    s = re.sub(r'\{\{I:([a-z-]+)\}\}', lambda m: icon(m.group(1)), s)
    assert '{{' not in s, nome
    return s.strip()

# ---------- ajudantes ----------
def troca_main(s, novo): return re.sub(r'<main id="conteudo" tabindex="-1">.*?</main>', lambda m: novo, s, count=1, flags=re.S)
def meta(s, chave, valor):
    return re.sub(r'(<meta (?:name|property)="' + re.escape(chave) + r'" content=")[^"]*(")', lambda m: m.group(1) + valor + m.group(2), s)
def titulo(s, t): return re.sub(r'<title>.*?</title>', f'<title>{t}</title>', s, count=1)
def titulo_todos(s, t):  # <title>, og:title e twitter:title iguais
    s = titulo(s, t)
    for k in ('og:title', 'twitter:title'): s = meta(s, k, t)
    return s
def descricao(s, d):
    for k in ('description', 'og:description', 'twitter:description'): s = meta(s, k, d)
    return s
def sem_ld(s, tipo):  # tira os blocos JSON-LD de um tipo
    return re.sub(r'<script type="application/ld\+json">(?:(?!</script>).)*?"@type": *"' + tipo + r'".*?</script>\n?', '', s, flags=re.S)
def com_ld(s, bloco): return s.replace('<style>', bloco + '<style>', 1)
def sem_js_form(s):  # tira os scripts antigos de formulário (orçamento) e o de agendamento, para pôr o atual
    return re.sub(r'<script>\n/\* (?:Orçamento do topo|Formulário de orçamento|Agendamento)[^\n]*\n.*?</script>\n', '', s, flags=re.S)
def com_js_form(s): return s.replace('<a class="wa-float"', FORM_JS + '<a class="wa-float"', 1)
def com_simbolos(s):
    novos = ''.join(f'    <symbol id="i-{n}" viewBox="0 0 24 24">{d}</symbol>\n' for n, d in SYMBOLS.items()
                    if f'#i-{n}"' in s and f'id="i-{n}"' not in s)
    s = s.replace('  </defs>\n</svg>', novos + '  </defs>\n</svg>', 1)
    for n in ('grid', 'doc', 'trend', 'pin', 'home', 'check'):  # ícones de versões anteriores que não são mais usados
        if f'#i-{n}"' not in s: s = re.sub(r'    <symbol id="i-' + n + r'".*?</symbol>\n', '', s)
    return s
def com_css(s, css, marca):  # põe o bloco de CSS no fim do <style>; se já existe, troca pelo atual
    marca = f'/* ===== {marca} ===== */'
    if marca in s:
        return re.sub(re.escape(marca) + r'\n.*?(?=\n/\* =====|</style>)', lambda m: marca + '\n' + css.rstrip('\n') + '\n', s, count=1, flags=re.S)
    return s.replace('</style>', f'\n{marca}\n{css}</style>', 1)

def menu(atual, cta_href):
    def li(href, txt):
        cur = ' aria-current="page"' if href == atual else ''
        return f'        <li><a href="{href}"{cur}>{txt}</a></li>'
    return '\n'.join(['<ul>', li('/#como-funciona', 'Como funciona'), li('/#setores', 'Setores'), li('/sobre/', 'Sobre'), li('/artigos/', 'Artigos'), li('/contato/', 'Contato'),
                      f'        <li class="menu-cta"><a class="btn btn-primary btn-sm" href="{cta_href}">Agendar conversa</a></li>', '      </ul>'])
RODAPE = '''<ul>
          <li><a href="/#como-funciona">Como funciona</a></li>
          <li><a href="/setores/comercio/">Para comércio</a></li>
          <li><a href="/setores/saude/">Para saúde</a></li>
          <li><a href="/setores/educacao/">Para educação</a></li>
          <li><a href="/itaituba/">Consultoria em TI em Itaituba</a></li>
          <li><a href="/sobre/">Sobre</a></li>
          <li><a href="/produtos/">Soluções</a></li>
          <li><a href="/artigos/">Artigos</a></li>
          <li><a href="/contato/">Contato</a></li>
          <li><a href="/privacidade/">Privacidade</a></li>
        </ul>'''

# a primeira tela e quem chega por âncora veem o conteúdo na hora, sem esperar a animação de entrada
CSS_REVELA = '.rv main>section:first-child .reveal,.rv :target .reveal,.rv .reveal:target{opacity:1;transform:none;transition:none}\n'
# alvos de toque de 44px no rodapé e nos links secundários (não vale para links no meio de frase)
CSS_TOQUE = '''.alt-send,.copy{position:relative}
.alt-send::after,.copy::after{content:"";position:absolute;inset:-12px -6px}
.site-footer nav a,.foot-mail,.legal>a{display:inline-flex;align-items:center;min-height:44px}
.site-footer nav ul{gap:0 1.5rem}
.more .link{min-height:44px}
'''
CSS_CAMPOS = '.form input,.form select,.form textarea{border-color:#7A8BA6}\n#agenda-status:empty{display:none}\n'

def comum(p, s):
    """Menu, botão do topo, rodapé e faixa de chamada genérica: iguais em todas as páginas."""
    atual = '/' + p.replace('index.html', '').replace('\\', '/') if p.endswith('index.html') else None
    cta_href = '#agendar' if p in ('index.html', 'itaituba/index.html') else '/contato/#agendar'
    s = re.sub(r'(<nav class="menu" id="menu" aria-label="Principal">\s*)<ul>.*?</ul>', lambda m: m.group(1) + menu(atual, cta_href), s, count=1, flags=re.S)
    s = re.sub(r'<a class="btn btn-primary btn-sm bar-cta" href="[^"]*"><span class="cta-l">[^<]*</span><span class="cta-s">[^<]*</span></a>',
               f'<a class="btn btn-primary btn-sm bar-cta" href="{cta_href}"><span class="cta-l">Agendar conversa</span><span class="cta-s">Agendar</span></a>', s, count=1)
    s = re.sub(r'(<nav aria-label="Rodapé">\s*)<ul>.*?</ul>', lambda m: m.group(1) + RODAPE, s, count=1, flags=re.S)
    s = s.replace('<p>Conte o que você precisa. Respondemos com os próximos passos e, quando for o caso, com um orçamento.</p>', f'<p>{CTA_TXT}</p>')
    s = s.replace('<h2 id="cta-titulo">Vamos conversar.</h2>', '<h2 id="cta-titulo">Vamos conversar sobre o seu negócio?</h2>')
    s = s.replace('<a class="btn btn-primary" href="/contato/">Solicitar orçamento', '<a class="btn btn-primary" href="/contato/#agendar">Agendar conversa')
    s = s.replace('subject=Or%C3%A7amento%20-%20Edelmann%20Tecnologia', 'subject=Agendar%20conversa%20-%20Edelmann%20Tecnologia')
    s = s.replace('computadores, redes e sistemas em mãos competentes', 'tecnologia a serviço do resultado do seu negócio')
    s = com_css(s, CSS_REVELA, 'Primeira tela sem atraso')
    s = com_css(s, CSS_TOQUE, 'Alvos de toque')
    if p == 'produtos/index.html':  # faixa final da página de soluções
        s = s.replace('Ol%C3%A1!%20Vim%20pelo%20site%20da%20Edelmann%20Tecnologia.', 'Ol%C3%A1!%20Quero%20agendar%20uma%20conversa%20com%20a%20Edelmann%20Tecnologia.')
        s = s.replace('<h2 id="cta-titulo">Vamos conversar sobre o seu negócio?</h2>', '<h2 id="cta-titulo">Qual dessas soluções faz sentido para a sua empresa?</h2>')
    return s

# ---------- CSS da página inicial (escura) ----------
CSS_INICIO = '''.impacts{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,15rem),1fr));padding:0;list-style:none}
.impact{padding:1.75rem;background:#0E1B33;border:1px solid rgba(255,255,255,.1);border-radius:14px}
.impact .i{width:30px;height:30px;margin-bottom:1.25rem;stroke-width:1.4;color:var(--gold-soft)}
.home .impact h3{margin-bottom:.5rem;font-size:1.375rem}
.impact p{font-size:.9375rem}
.home .step{border-top-color:rgba(255,255,255,.16)}
.home .step::before{color:var(--gold-soft)}
.home .step::after{background:var(--night);border-color:var(--gold-soft)}
.home .alt .step::after{background:#0A1428}
.home .step p{color:var(--on-night)}
@media (min-width:760px){.steps.three{grid-template-columns:repeat(3,1fr)}}
.head.exp{margin-bottom:0;align-items:start}
.exp-note{max-width:46rem;margin:1.5rem 0;padding:1.25rem 1.5rem;border-left:3px solid var(--gold-soft);border-radius:0 12px 12px 0;background:rgba(95,221,236,.06);color:#DCE2EC}
.sols{display:grid;gap:.75rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,15rem),1fr));padding:0;list-style:none}
.sols a{display:flex;flex-direction:column;gap:.4rem;height:100%;padding:1.25rem 1.35rem;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.09);border-radius:12px;color:#DCE2EC;text-decoration:none;transition:border-color .2s,background-color .2s}
.sols a:hover{border-color:var(--gold-soft);background:rgba(95,221,236,.06)}
.sols b{display:flex;justify-content:space-between;align-items:center;gap:.75rem;font:600 1.0625rem/1.3 var(--serif);color:#fff}
.sols .i{width:18px;height:18px;color:var(--gold-soft);transition:transform .3s var(--ease)}
.sols a:hover .i{transform:translateX(4px)}
.sols span{font-size:.9375rem;color:var(--on-night)}
.home-hero .crumbs{margin-bottom:1.25rem}
.signs{display:grid;gap:1px;grid-template-columns:minmax(0,1fr);padding:0;list-style:none;counter-reset:sg;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.09);border-radius:14px;overflow:hidden}
@media (min-width:640px){.signs{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:960px){.signs{grid-template-columns:repeat(3,minmax(0,1fr))}}
.signs li{padding:1.6rem 1.75rem;background:var(--night)}
.signs li::before{counter-increment:sg;content:counter(sg,decimal-leading-zero);content:counter(sg,decimal-leading-zero) / "";display:block;margin-bottom:1rem;font:500 .8125rem/1 var(--mono);color:var(--gold-soft)}
.home .signs h3{margin-bottom:.45rem;font-size:1.1875rem;line-height:1.25}
.signs p{font-size:.9375rem}
.signs-cta{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:1rem 2rem;margin-top:1.5rem;padding:1.5rem 1.75rem;border:1px solid rgba(95,221,236,.3);border-radius:14px;background:rgba(95,221,236,.06)}
.signs-cta p{max-width:34rem;font:600 1.125rem/1.35 var(--serif);color:#fff}
.signs-cta .btn-ghost{border-color:rgba(255,255,255,.28);color:#fff}
.signs-cta .btn-ghost:hover{border-color:#fff}
'''
CSS_CHECK = '''.signs-cta>div:first-child{flex:1 1 24rem}
.check-info{max-width:34rem;margin-top:1.1rem;text-align:left}
.check-info p{max-width:none;margin:0;font:400 .9375rem/1.5 var(--sans);color:var(--on-night)}
.check-info .check-t{margin-top:1rem;font:500 .75rem/1 var(--mono);letter-spacing:.04em;text-transform:uppercase;color:var(--gold-soft)}
.check-info .check-t:first-child{margin-top:0}
.check-info ul{display:grid;gap:.5rem;margin:.6rem 0 0;padding:0;list-style:none}
.check-info li{padding:.55rem .9rem;border-left:2px solid var(--gold-soft);border-radius:0 8px 8px 0;background:rgba(255,255,255,.04);font-size:.9375rem;line-height:1.4;color:#fff}
.cta-band .check-info{margin:1.75rem auto 0}
'''
CSS_INICIO += CSS_CHECK
# números da experiência: claro (Sobre) e escuro (início e Itaituba)
CSS_STATS = '''.stats{display:grid;gap:.75rem;grid-template-columns:minmax(0,1fr);margin-bottom:2.5rem;padding:0;list-style:none}
@media (min-width:900px){.stats{grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem}}
.stats li{padding:clamp(1.1rem,3vw,1.75rem);background:var(--paper);border:1px solid var(--line);border-radius:14px}
.stats b{display:block;margin-bottom:.75rem;font:600 clamp(1.625rem,1.2rem + 2vw,2.875rem)/1 var(--serif);letter-spacing:-.03em;color:var(--gold-ink)}
.stats span{display:block;font-size:.9375rem;line-height:1.5;color:var(--muted)}
.home .stats li{background:#0E1B33;border-color:rgba(255,255,255,.1)}
.home .stats b{color:var(--gold-soft)}
.home .stats span{color:var(--on-night)}
.proof .stats{margin:0}
'''
# celular de 320px: as colunas do topo podem encolher em vez de estourar a tela
CSS_INICIO += '.hero-grid>*,.quote .form>*{min-width:0}\n'
# botão primário único nas páginas escuras (as claras continuam com o azul)
CSS_INICIO += '''.home .btn-primary{background:var(--gold-soft);color:var(--night);font-weight:600}
.home .btn-primary:hover{background:#fff}
.home .cta-accent .btn-primary{background:var(--night);color:#fff}
.home .cta-accent .btn-primary:hover{background:var(--navy)}
'''
CSS_INICIO += CSS_STATS
# seções que saíram (áreas de atuação, atendimento, por que, galeria de fotos): o CSS delas sai junto
OBSOLETO = re.compile(r'^(?:@media[^{]*\{)?(?:\.home )?\.(?:pillars|pillar-card|rows|modes|mode|why|why-title|gallery)\b'
                      r'|^(?:@media[^{]*\{)?\.proof (?:ul|li|\.i)\b|^/\* ===== Galeria ===== \*/$')

AREA_SERVIDA = [{'@type': 'City', 'name': 'Itaituba'}, {'@type': 'City', 'name': 'Santarém'}, {'@type': 'State', 'name': 'Pará'}]
def ld_empresa(s):
    def f(m):
        o = json.loads(m.group(1))
        if o.get('@type') != 'ProfessionalService': return m.group(0)
        o['@id'] = 'https://edelmann.com.br/#empresa'
        o['image'] = 'https://edelmann.com.br/img/og.jpg'
        o['logo'] = 'https://edelmann.com.br/apple-touch-icon.png'
        o['description'] = ('Consultoria em tecnologia da informação para empresas de pequeno e médio porte: gestão e melhoria de processos '
                            'e soluções para todas as fases da gestão, com foco em resultado financeiro.')
        o['areaServed'] = AREA_SERVIDA
        o['knowsAbout'] = ['Consultoria em tecnologia da informação', 'Gestão de processos', 'Melhoria de processos', 'Transformação digital',
                           'Planejamento de TI', 'Contratos públicos', 'Segurança da informação', 'Desenvolvimento de sistemas']
        return '<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False, indent=2) + '\n</script>'
    return re.sub(r'<script type="application/ld\+json">\n(.*?)\n</script>', f, s, flags=re.S)

# ---------- 1. início ----------
s = rd('index.html')
s = troca_main(s, trecho('inicio.html'))
s = sem_js_form(s); s = com_js_form(s)
s = '\n'.join(l for l in s.split('\n') if not OBSOLETO.match(l))
s = com_css(s, CSS_INICIO, 'Consultoria')
s = com_css(s, CSS_CAMPOS, 'Campos do formulário')
s = titulo_todos(s, 'Consultoria em TI para empresas | Edelmann, Itaituba (PA)')
s = meta(s, 'description', 'Consultoria em TI para pequenas e médias empresas, de Itaituba a Santarém (PA). Mais de 15 anos em TI e melhoria de processos. Agende uma conversa.')
for k in ('og:description', 'twitter:description'):
    s = meta(s, k, 'Tecnologia a serviço do resultado do seu negócio. Consultoria em TI para empresas de pequeno e médio porte.')
s = meta(s, 'og:image:alt', 'Edelmann Tecnologia: tecnologia a serviço do resultado do seu negócio')
s = ld_empresa(s)
s = com_simbolos(comum('index.html', s))
wr('index.html', s)
inicio = s

# ---------- 2. Itaituba (versão local do início) ----------
s = troca_main(inicio, trecho('itaituba.html'))
s = titulo(s, 'Consultoria em TI em Itaituba (PA) | Edelmann Tecnologia')
s = descricao(s, 'Consultoria em TI para empresas de Itaituba a Santarém (PA): vamos até a sua empresa. Gestão e melhoria de processos, com mais de 15 anos de experiência em TI.')
for k in ('og:title', 'twitter:title'): s = meta(s, k, 'Consultoria em TI em Itaituba (PA) | Edelmann Tecnologia')
s = s.replace('<link rel="canonical" href="https://edelmann.com.br/">', '<link rel="canonical" href="https://edelmann.com.br/itaituba/">')
s = meta(s, 'og:url', 'https://edelmann.com.br/itaituba/')
s = com_ld(s, FAQ_LD + ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Início", "item": "https://edelmann.com.br/"},
    {"@type": "ListItem", "position": 2, "name": "Itaituba", "item": "https://edelmann.com.br/itaituba/"}]}))
wr('itaituba/index.html', com_simbolos(s))

# ---------- 3. Sobre ----------
s = rd('sobre/index.html')
s = troca_main(s, trecho('sobre.html'))
DESC_SOBRE = 'Consultoria em TI para pequenas e médias empresas, com mais de 15 anos de experiência em TI, em diversos setores e em contratos públicos.'
s = titulo_todos(s, 'Sobre a Edelmann | Consultoria em TI em Itaituba (PA)')
s = descricao(s, DESC_SOBRE)
s = sem_ld(s, 'AboutPage')
s = com_ld(s, ld({"@context": "https://schema.org", "@type": "AboutPage", "name": "Sobre a Edelmann", "url": "https://edelmann.com.br/sobre/",
                  "inLanguage": "pt-BR", "description": DESC_SOBRE, "about": {"@id": "https://edelmann.com.br/#empresa"}}))
s = '\n'.join(l for l in s.split('\n') if not OBSOLETO.match(l))
s = com_css(s, CSS_STATS, 'Experiência')
wr('sobre/index.html', com_simbolos(comum('sobre/index.html', s)))

# ---------- 4. Contato ----------
s = rd('contato/index.html')
s = troca_main(s, trecho('contato.html'))
s = sem_js_form(s); s = com_js_form(s)
s = sem_ld(s, 'FAQPage'); s = com_ld(s, FAQ_LD)
s = com_css(s, 'button.btn-ghost{background:transparent;font-family:inherit;cursor:pointer}\n', 'Botão de e-mail')
s = com_css(s, CSS_CAMPOS, 'Campos do formulário')
s = titulo_todos(s, 'Agende uma conversa em Itaituba | Edelmann Tecnologia')
s = descricao(s, 'Agende uma conversa com a Edelmann Tecnologia: presencial de Itaituba a Santarém ou por videochamada. WhatsApp (93) 98121-2924.')
wr('contato/index.html', com_simbolos(comum('contato/index.html', s)))

# ---------- 5. Soluções (antiga página de produtos) e páginas dos apps ----------
s = rd('produtos/index.html')
s = titulo_todos(s, 'Soluções próprias: PDV, agente de IA e chamados | Edelmann')
s = descricao(s, 'Agente de IA no WhatsApp, Balcão PDV e Sistema de Chamados: sistemas desenvolvidos pela Edelmann Tecnologia.')
s = re.sub(r'("description": ")Agente de IA no WhatsApp, Balcão PDV, Sistema de Chamados e Leitor de Bolso:', r'\1Agente de IA no WhatsApp, Balcão PDV e Sistema de Chamados:', s)
# o Leitor de Bolso não é mais listado como solução (as páginas dele continuam no ar)
s = re.sub(r'\n        <article class="app">(?:(?!<article|</article>).)*?/leitor-de-bolso/(?:(?!</article>).)*</article>', '', s, flags=re.S)
s = s.replace('vender, organizar o suporte e digitalizar documentos.', 'vender e organizar o suporte.')
if '<h2 class="sr">Nossas soluções</h2>' not in s:  # evita o salto h1 -> h3
    assert '<div class="apps reveal">' in s
    s = s.replace('<div class="apps reveal">', '<h2 class="sr">Nossas soluções</h2>\n      <div class="apps reveal">', 1)
s = sem_ld(s, 'CollectionPage')
s = com_ld(s, ld({"@context": "https://schema.org", "@type": "CollectionPage", "name": "Soluções", "url": "https://edelmann.com.br/produtos/",
                  "inLanguage": "pt-BR", "description": re.search(r'<meta name="description" content="([^"]*)"', s).group(1)}))
s = s.replace('<p class="eyebrow">Produtos</p>', '<p class="eyebrow">Soluções</p>', 1)
s = re.sub(r'(<h1[^>]*>)Produtos com a nossa assinatura\.', r'\1Soluções que desenvolvemos.', s, count=1)
s = s.replace('Além dos serviços, a Edelmann desenvolve ferramentas', 'A Edelmann desenvolve ferramentas próprias')
s = s.replace('>Conhecer o app<', '>Conhecer<')
s = com_css(s, '@media (min-width:1100px){.apps{grid-template-columns:repeat(3,minmax(0,1fr))}}\n', 'Soluções em 3 colunas')
wr('produtos/index.html', comum('produtos/index.html', s))

APPS = ['agente-whatsapp/index.html', 'balcao/index.html', 'chamados/index.html', 'leitor-de-bolso/index.html', 'leitor-de-bolso/privacidade.html']
for p in APPS + ['privacidade/index.html', '404.html']:
    s = rd(p)
    s = s.replace('<li><a href="/produtos/">Produtos</a></li>\n', '<li><a href="/produtos/">Soluções</a></li>\n')  # trilha
    s = re.sub(r'"name": *"Produtos"', '"name": "Soluções"', s)
    s = s.replace('presencial em Itaituba e região ou por videochamada', 'presencial de Itaituba a Santarém ou por videochamada')
    if not p.startswith('leitor-de-bolso'):  # o Leitor de Bolso não muda
        s = s.replace('Ver os outros produtos<', 'Ver as outras soluções<')
    s = s.replace('O formulário de orçamento só monta', 'O formulário de agendamento só monta')
    s = s.replace('(nome, contato, descrição do problema). Usamos só para responder, fazer o orçamento e prestar o serviço contratado.',
                  '(nome, empresa, contato, desafios do negócio). Usamos só para responder, agendar a conversa, preparar a proposta e prestar o serviço contratado.')
    s = re.sub(r'<a class="btn btn-primary" href="mailto:[^"]*">Solicitar orçamento', '<a class="btn btn-primary" href="/contato/#agendar">Agendar conversa', s)
    s = s.replace('Respondemos a cada pedido com os próximos passos e, quando for o caso, com um orçamento.',
                  'Marcamos uma conversa, presencial de Itaituba a Santarém ou por videochamada, para ver onde o agente pode gerar resultado no seu negócio.')
    s = s.replace('Respondemos com os próximos passos e, quando for o caso, com um orçamento.',
                  'Marcamos uma conversa, presencial de Itaituba a Santarém ou por videochamada, para ver onde isso pode gerar resultado.')
    if p in ('agente-whatsapp/index.html', 'chamados/index.html'):
        bloco = f'<div class="ctas"><a class="btn btn-primary" href="/contato/#agendar">Agendar conversa{ARROW}</a>{WA_BTN}</div>'
        if bloco not in s:
            assert '<a class="channel" href="mailto:' in s, p
            s = s.replace('<a class="channel" href="mailto:', bloco + '\n        <a class="channel" href="mailto:', 1)
    if p == 'privacidade/index.html':
        s = s.replace('<strong>Formulário de orçamento:</strong>', '<strong>Formulário de agendamento:</strong>')
        s = re.sub(r'Última atualização: [^<]*\.', 'Última atualização: 28 de outubro de 2026.', s)
    if p == '404.html':
        s = re.sub(r'<ul class="svc-links">.*?</ul>', lambda m: '<ul class="svc-links">\n' + '\n'.join(
            f'        <li><a href="{h}">{t}{ARROW}</a></li>' for h, t in [('/', 'Página inicial'), ('/#como-funciona', 'Como funciona'),
            ('/sobre/', 'Sobre'), ('/produtos/', 'Soluções'), ('/contato/', 'Agendar conversa')]) + '\n      </ul>', s, count=1, flags=re.S)
    wr(p, comum(p, s))

# ---------- 6. Serviços e Dicas: só redirecionam para o início ----------
REDIR = '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Edelmann Tecnologia</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="https://edelmann.com.br/">
<meta http-equiv="refresh" content="0; url=/">
</head>
<body>
<p><a href="/">Ir para a página inicial da Edelmann Tecnologia</a></p>
</body>
</html>
'''
removidas = sorted(glob.glob('servicos/**/index.html', recursive=True) + glob.glob('dicas/**/index.html', recursive=True))
for p in removidas: wr(p, REDIR)
wr('setores/index.html', REDIR.replace('url=/"', 'url=/#setores"'))  # /setores/ não dá 404: leva ao bloco de setores da home

# ---------- 7. sitemap e manifest ----------
s = rd('sitemap.xml')
s = re.sub(r'\n  <url><loc>https://edelmann\.com\.br/(?:servicos|dicas)/[^<]*</loc>.*?</url>', '', s)
for u in ('leitor-de-bolso/', 'leitor-de-bolso/privacidade.html', 'privacidade/', 'balcao/'):  # não mudaram em 29/10
    s = re.sub(r'(<loc>https://edelmann\.com\.br/' + re.escape(u) + r'</loc><lastmod>)[^<]*', r'\g<1>2026-10-28', s)
for u in ('', 'itaituba/', 'sobre/', 'contato/', 'produtos/', 'agente-whatsapp/', 'chamados/'):  # alteradas em 29/10
    s = re.sub(r'(<loc>https://edelmann\.com\.br/' + re.escape(u) + r'</loc><lastmod>)[^<]*', r'\g<1>2026-10-29', s)
wr('sitemap.xml', s)
m = json.loads(rd('manifest.webmanifest'))
m['description'] = 'Consultoria em TI para empresas de pequeno e médio porte. De Itaituba a Santarém (PA) e videochamada.'
wr('manifest.webmanifest', json.dumps(m, ensure_ascii=False, indent=2) + '\n')

print('ok:', len(removidas), 'redirecionamentos;', s.count('<url>'), 'URLs no sitemap')
