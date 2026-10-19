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
            <label>Seu nome<input name="nome" autocomplete="name" required></label>
            <label>Empresa<input name="empresa" autocomplete="organization" required></label>
          </div>
          <div class="row">
            <label><span>Segmento <small>(opcional)</small></span><input name="segmento" placeholder="Ex.: comércio, saúde"></label>
            <label><span>Cidade <small>(opcional)</small></span><input name="cidade" autocomplete="address-level2"></label>
          </div>
          <div class="row">
            <label>Formato
              <select name="formato"><option>Presencial</option><option>Videochamada</option></select>
            </label>
            <label>Melhor período
              <select name="periodo"><option>Qualquer horário</option><option>Manhã</option><option>Tarde</option></select>
            </label>
          </div>
          <label><span>Qual o principal desafio do negócio hoje? <small>(opcional)</small></span><textarea name="desafio"></textarea></label>'''
NOSCRIPT = '<noscript><p class="fine">Para agendar, use o WhatsApp (93) 98121-2924 ou o e-mail edelmann.tecnologia@gmail.com.</p></noscript>'
FORM_DARK = f'''      <div class="quote" id="agendar">
        <h2>Agende uma conversa.</h2>
        <p>Presencial em Itaituba e região, ou por videochamada.</p>
        <form class="form" id="form-agenda">
{CAMPOS}
          <button class="btn btn-primary" type="submit">Agendar pelo WhatsApp{ARROW}</button>
          <p class="fine">Prefere e-mail? <button class="alt-send" type="button" id="agenda-email">Enviar por e-mail</button>. Nada fica guardado no site. Veja a <a href="/privacidade/">política de privacidade</a>.</p>
        </form>
        {NOSCRIPT}
      </div>'''
FORM_CLARO = f'''      <form class="form" id="form-agenda">
{CAMPOS}
        <div class="actions">
          <button class="btn btn-primary" type="submit">Agendar pelo WhatsApp{ARROW}</button>
          <button class="btn btn-ghost" type="button" id="agenda-email">Enviar por e-mail</button>
        </div>
        <p class="fine">Ao enviar, abrimos o WhatsApp ou o e-mail com a mensagem pronta para você conferir. Veja a <a href="/privacidade/">política de privacidade</a>.</p>
      </form>
      {NOSCRIPT}'''
FORM_JS = '''<script>
/* Agendamento: monta a mensagem no navegador e abre WhatsApp ou e-mail. Nada é enviado ao site. */
(function(){
  var f=document.getElementById('form-agenda'); if(!f)return;
  function msg(){
    var d=new FormData(f),l=['Olá! Quero agendar uma conversa com a Edelmann Tecnologia.','','Nome: '+d.get('nome'),'Empresa: '+d.get('empresa')];
    if(d.get('segmento'))l.push('Segmento: '+d.get('segmento'));
    if(d.get('cidade'))l.push('Cidade: '+d.get('cidade'));
    l.push('Formato: '+d.get('formato'),'Melhor período: '+d.get('periodo'));
    if(d.get('desafio'))l.push('','Principal desafio: '+d.get('desafio'));
    return l.join('\\n');
  }
  f.addEventListener('submit',function(e){
    e.preventDefault(); if(!f.reportValidity())return;
    window.open('https://wa.me/5593981212924?text='+encodeURIComponent(msg()),'_blank','noopener');
  });
  document.getElementById('agenda-email').addEventListener('click',function(){
    if(!f.reportValidity())return;
    var a=document.createElement('a');
    a.href='mailto:edelmann.tecnologia@gmail.com?subject='+encodeURIComponent('Agendar conversa - '+new FormData(f).get('empresa'))+'&body='+encodeURIComponent(msg());
    document.body.appendChild(a); a.click(); a.remove();
  });
})();
</script>
'''
WA_CHECK = 'https://wa.me/5593981212924?text=Ol%C3%A1!%20Quero%20receber%20o%20checklist%20%2210%20perguntas%20para%20descobrir%20onde%20a%20empresa%20perde%20dinheiro%22.'
SINAIS_ITENS = [
    ('Retrabalho e tarefas repetidas', 'A equipe gasta horas fazendo à mão o que poderia ser rotina.'),
    ('Informação espalhada', 'Dados em planilhas, cadernos e conversas, e ninguém tem o número certo na hora de decidir.'),
    ('Tecnologia que não se paga', 'Sistemas, assinaturas e equipamentos que custam caro e não trazem retorno claro.'),
    ('Sistemas que não conversam', 'Cada setor com a sua ferramenta, e a mesma informação digitada mais de uma vez.'),
    ('Dependência de uma pessoa', 'Se alguém falta ou sai da empresa, parte do negócio para.'),
    ('Risco de parar', 'Uma falha, um ataque ou a perda de dados pode deixar a empresa sem operar.'),
]
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
        <p>Se você reconheceu algum desses pontos, vale uma conversa. Ou comece pelo nosso checklist: 10 perguntas para descobrir onde a sua empresa perde dinheiro.</p>
        <div class="ctas" style="margin:0">
          <a class="btn btn-primary" href="#agendar">Agendar conversa{ARROW}</a>
          <a class="btn btn-ghost" href="{WA_CHECK}" target="_blank" rel="noopener">Receber o checklist grátis<span class="sr"> (abre o WhatsApp em nova aba)</span></a>
        </div>
      </div>
    </div>
  </section>'''
STATS = '''      <ul class="stats reveal">
        <li><b>15+</b><span>anos de experiência em tecnologia da informação</span></li>
        <li><b>Diversos</b><span>setores atendidos ao longo da nossa trajetória</span></li>
        <li><b>Público</b><span>experiência com contratos do setor público</span></li>
        <li><b>4</b><span>soluções próprias desenvolvidas por nós</span></li>
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
          <h2 id="como-funciona-titulo">Tudo começa <em>com uma conversa.</em></h2>
        </div>
        <p class="sub">Presencial em Itaituba e região, ou por videochamada.</p>
      </div>
      <ol class="steps three reveal">
        <li class="step"><h3>Conversa</h3><p>Nos encontramos para entender o seu negócio, os seus objetivos e o que hoje impede o crescimento.</p></li>
        <li class="step"><h3>Diagnóstico e proposta</h3><p>Apresentamos as prioridades, o caminho e o impacto esperado para o negócio.</p></li>
        <li class="step"><h3>Execução e acompanhamento</h3><p>Colocamos o plano em prática junto com a sua equipe e acompanhamos os resultados.</p></li>
      </ol>
      <p class="more reveal"><a class="btn btn-primary" href="#agendar">Agendar conversa{ARROW}</a></p>
    </div>
  </section>'''
CTA_TXT = 'Um encontro, presencial ou por videochamada, para entender os seus objetivos e mostrar onde a tecnologia pode gerar resultado.'
WA_BTN = f'<a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">Falar no WhatsApp<span class="sr"> (abre em nova aba)</span></a>'
def cta(classe, alvo):
    return f'''  <section class="{classe}" aria-labelledby="cta-titulo">
    <div class="wrap reveal">
      <h2 id="cta-titulo">Vamos conversar sobre o seu negócio?</h2>
      <p>{CTA_TXT}</p>
      <div class="ctas">
        <a class="btn btn-primary" href="{alvo}">Agendar conversa{ARROW}</a>
        {WA_BTN}
      </div>
    </div>
  </section>'''
FAQ = [
    ('Como é a primeira conversa?', 'Um encontro presencial, em Itaituba e região, ou por videochamada. Conversamos sobre o negócio, os objetivos e os principais desafios, e a partir daí indicamos os próximos passos.'),
    ('Que tipo de empresa vocês atendem?', 'Empresas de pequeno e médio porte dos mais diversos setores. Também temos experiência com contratos públicos.'),
    ('Vocês atendem fora de Itaituba?', 'Sim. Os encontros presenciais acontecem em Itaituba e região; para outras cidades, conversamos por videochamada.'),
    ('Como é definido o valor?', 'Depois de entender o negócio, apresentamos uma proposta com o escopo, as etapas e o valor. Nada começa sem a sua aprovação.'),
    ('Qual a forma mais rápida de falar com vocês?', 'O WhatsApp (93) 98121-2924. Também respondemos pelo e-mail edelmann.tecnologia@gmail.com.'),
]
FAQ_HTML = '      <div class="faq reveal">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + '</div>'
def ld(obj): return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=1) + '\n</script>\n'
FAQ_LD = ld({"@context": "https://schema.org", "@type": "FAQPage",
             "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]})
MARCAS = {'{{FORM_DARK}}': FORM_DARK, '{{FORM_CLARO}}': FORM_CLARO, '{{PROOF}}': PROOF, '{{SINAIS}}': SINAIS, '{{STATS}}': STATS,
          '{{COMO_FUNCIONA}}': como_funciona('section'), '{{COMO_FUNCIONA_ALT}}': como_funciona('section alt'),
          '{{CTA}}': cta('cta-accent', '#agendar'), '{{CTA_CLARO}}': cta('section band cta-band', '/contato/#agendar'),
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
    return '\n'.join(['<ul>', li('/#como-atuamos', 'Como atuamos'), li('/sobre/', 'Sobre'), li('/contato/', 'Contato'),
                      f'        <li class="menu-cta"><a class="btn btn-primary btn-sm" href="{cta_href}">Agendar conversa</a></li>', '      </ul>'])
RODAPE = '''<ul>
          <li><a href="/#como-atuamos">Como atuamos</a></li>
          <li><a href="/sobre/">Sobre</a></li>
          <li><a href="/produtos/">Soluções</a></li>
          <li><a href="/contato/">Contato</a></li>
          <li><a href="/privacidade/">Privacidade</a></li>
        </ul>'''

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
# números da experiência: claro (Sobre) e escuro (início e Itaituba)
CSS_STATS = '''.stats{display:grid;gap:.75rem;grid-template-columns:repeat(2,minmax(0,1fr));margin-bottom:2.5rem;padding:0;list-style:none}
@media (min-width:900px){.stats{grid-template-columns:repeat(4,minmax(0,1fr));gap:1rem}}
.stats li{padding:clamp(1.1rem,3vw,1.75rem);background:var(--paper);border:1px solid var(--line);border-radius:14px}
.stats b{display:block;margin-bottom:.75rem;font:600 clamp(1.625rem,1.2rem + 2vw,2.875rem)/1 var(--serif);letter-spacing:-.03em;color:var(--gold-ink)}
.stats span{display:block;font-size:.9375rem;line-height:1.5;color:var(--muted)}
.home .stats li{background:#0E1B33;border-color:rgba(255,255,255,.1)}
.home .stats b{color:var(--gold-soft)}
.home .stats span{color:var(--on-night)}
.proof .stats{margin:0}
'''
CSS_INICIO += CSS_STATS
# seções que saíram (áreas de atuação, atendimento, por que, galeria de fotos): o CSS delas sai junto
OBSOLETO = re.compile(r'^(?:@media[^{]*\{)?(?:\.home )?\.(?:pillars|pillar-card|rows|modes|mode|why|why-title|gallery)\b'
                      r'|^(?:@media[^{]*\{)?\.proof (?:ul|li|\.i)\b|^/\* ===== Galeria ===== \*/$')

def ld_empresa(s):
    def f(m):
        o = json.loads(m.group(1))
        if o.get('@type') != 'ProfessionalService': return m.group(0)
        o['description'] = ('Consultoria em tecnologia da informação para empresas de pequeno e médio porte: gestão e melhoria de processos '
                            'e soluções para todas as fases da gestão, com foco em resultado financeiro.')
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
s = titulo(s, 'Edelmann Tecnologia | Consultoria em TI para empresas')
s = meta(s, 'description', 'Consultoria em TI para empresas de pequeno e médio porte. Há mais de 15 anos apoiamos os mais diversos setores a organizar processos, reduzir custos e crescer. Itaituba (PA) e videochamada.')
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
s = descricao(s, 'Consultoria em TI para empresas de Itaituba e região: gestão e melhoria de processos, redução de custos e tecnologia para cada fase do negócio. Mais de 15 anos de experiência.')
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
s = descricao(s, 'A Edelmann Tecnologia é uma consultoria em TI para empresas de pequeno e médio porte, com mais de 15 anos de experiência nos mais diversos setores e em contratos públicos.')
s = '\n'.join(l for l in s.split('\n') if not OBSOLETO.match(l))
s = com_css(s, CSS_STATS, 'Experiência')
wr('sobre/index.html', com_simbolos(comum('sobre/index.html', s)))

# ---------- 4. Contato ----------
s = rd('contato/index.html')
s = troca_main(s, trecho('contato.html'))
s = sem_js_form(s); s = com_js_form(s)
s = sem_ld(s, 'FAQPage'); s = com_ld(s, FAQ_LD)
s = com_css(s, 'button.btn-ghost{background:transparent;font-family:inherit;cursor:pointer}\n', 'Botão de e-mail')
s = descricao(s, 'Agende uma conversa com a Edelmann Tecnologia, presencial em Itaituba e região ou por videochamada. WhatsApp (93) 98121-2924 e e-mail edelmann.tecnologia@gmail.com.')
wr('contato/index.html', com_simbolos(comum('contato/index.html', s)))

# ---------- 5. Soluções (antiga página de produtos) e páginas dos apps ----------
s = rd('produtos/index.html')
s = titulo(s, 'Soluções | Edelmann Tecnologia')
s = s.replace('<p class="eyebrow">Produtos</p>', '<p class="eyebrow">Soluções</p>', 1)
s = re.sub(r'(<h1[^>]*>)Produtos com a nossa assinatura\.', r'\1Soluções que desenvolvemos.', s, count=1)
s = s.replace('Além dos serviços, a Edelmann desenvolve ferramentas', 'A Edelmann desenvolve ferramentas próprias')
wr('produtos/index.html', comum('produtos/index.html', s))

APPS = ['agente-whatsapp/index.html', 'balcao/index.html', 'chamados/index.html', 'leitor-de-bolso/index.html', 'leitor-de-bolso/privacidade.html']
for p in APPS + ['privacidade/index.html', '404.html']:
    s = rd(p)
    s = s.replace('<li><a href="/produtos/">Produtos</a></li>\n', '<li><a href="/produtos/">Soluções</a></li>\n')  # trilha
    s = re.sub(r'"name": *"Produtos"', '"name": "Soluções"', s)
    s = s.replace('O formulário de orçamento só monta', 'O formulário de agendamento só monta')
    s = s.replace('(nome, contato, descrição do problema). Usamos só para responder, fazer o orçamento e prestar o serviço contratado.',
                  '(nome, empresa, contato, desafios do negócio). Usamos só para responder, agendar a conversa, preparar a proposta e prestar o serviço contratado.')
    if p == '404.html':
        s = re.sub(r'<ul class="svc-links">.*?</ul>', lambda m: '<ul class="svc-links">\n' + '\n'.join(
            f'        <li><a href="{h}">{t}{ARROW}</a></li>' for h, t in [('/', 'Página inicial'), ('/#como-atuamos', 'Como atuamos'),
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

# ---------- 7. sitemap e manifest ----------
s = rd('sitemap.xml')
s = re.sub(r'\n  <url><loc>https://edelmann\.com\.br/(?:servicos|dicas)/[^<]*</loc>.*?</url>', '', s)
for u in ('', 'itaituba/', 'sobre/', 'contato/', 'produtos/'):
    s = re.sub(r'(<loc>https://edelmann\.com\.br/' + re.escape(u) + r'</loc><lastmod>)[^<]*', r'\g<1>2026-10-16', s)
wr('sitemap.xml', s)
m = json.loads(rd('manifest.webmanifest'))
m['description'] = 'Consultoria em TI para empresas de pequeno e médio porte. Itaituba (PA) e videochamada.'
wr('manifest.webmanifest', json.dumps(m, ensure_ascii=False, indent=2) + '\n')

print('ok:', len(removidas), 'redirecionamentos;', s.count('<url>'), 'URLs no sitemap')
