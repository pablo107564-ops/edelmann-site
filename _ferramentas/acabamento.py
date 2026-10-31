# Acabamento comum a todas as páginas do site Edelmann (idempotente: pode rodar de novo).
# Fontes locais, ícones/manifest, botão flutuante do WhatsApp, links novos no rodapé e estilos extras.
import re, glob, os, sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # pasta do site
FONTFACE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fontface.css'), encoding='utf-8').read()

WA = 'https://wa.me/5593981212924?text=Ol%C3%A1!%20Quero%20agendar%20uma%20conversa%20com%20a%20Edelmann%20Tecnologia.'
WA_ICON = ('<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
           '<path fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round" d="M16 3.5C9.1 3.5 3.5 8.9 3.5 15.6c0 2.4.7 4.6 2 6.5L4 28l6-1.6c1.8 1 3.9 1.6 6 1.6 6.9 0 12.5-5.4 12.5-12.1S22.9 3.5 16 3.5z"/>'
           '<path fill="currentColor" d="M12.2 9.8c.3 0 .6 0 .8.6l1 2.5c.1.3.1.6-.1.8l-.8 1c-.2.2-.2.5 0 .8.9 1.5 2.1 2.6 3.6 3.5.3.2.6.1.8-.1l1-1.1c.2-.3.5-.3.8-.2l2.5 1.1c.3.1.5.4.5.7 0 1.6-1.4 2.9-3 2.8-4.7-.4-8.5-4.2-8.9-8.8-.1-1.6 1-2.8 1.8-2.8z"/></svg>')
FLOAT = (f'<a class="wa-float" href="{WA}" target="_blank" rel="noopener">{WA_ICON}'
         '<span>WhatsApp</span><span class="sr"> (abre em nova aba)</span></a>\n')

CSS = '''
/* ===== Componentes extras ===== */
''' + FONTFACE + '''
.crumbs{margin-bottom:1.75rem;font-size:.8125rem}
.crumbs a{text-decoration:none}
.wa-float{position:fixed;right:max(16px,env(safe-area-inset-right));bottom:max(16px,env(safe-area-inset-bottom));z-index:60;display:inline-flex;align-items:center;gap:.55rem;min-height:3.25rem;padding:.7rem 1.15rem .7rem .95rem;border-radius:999px;background:#0B7A3E;color:#fff;font:600 .9375rem/1 var(--sans);text-decoration:none;box-shadow:0 14px 32px -12px rgba(6,12,24,.55);transition:background-color .2s,transform .2s}
.wa-float svg{width:1.6rem;height:1.6rem;flex:none}
.wa-float:hover{background:#0C6E3D;transform:translateY(-2px)}
.wa-float:focus-visible{outline:3px solid var(--gold-soft);outline-offset:3px}
@media (max-width:559.98px){.wa-float{width:3.5rem;height:3.5rem;padding:0;justify-content:center}.wa-float span:not(.sr){position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}
@media print{.wa-float{display:none}}
.site-footer{padding-bottom:5.5rem}
.faq{display:grid;gap:.75rem;max-width:52rem}
.faq details{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:0 1.25rem}
.faq summary{display:flex;justify-content:space-between;align-items:center;gap:1rem;padding:1.1rem 0;font:600 1.0625rem/1.35 var(--serif);color:var(--ink);cursor:pointer;list-style:none}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";flex:none;font:500 1.4rem/1 var(--mono);color:var(--gold-ink)}
.faq details[open] summary::after{content:"\\2212"}
.faq details p{padding:0 0 1.15rem;color:var(--muted)}
.prose{max-width:46rem}
.prose h2{margin:2.5rem 0 .9rem;font-size:clamp(1.5rem,1.25rem + 1vw,2rem);line-height:1.15}
.prose h3{margin:1.75rem 0 .6rem;font-size:1.25rem}
.prose p,.prose ul,.prose ol{margin:0 0 1.1rem;color:var(--text)}
.prose ul,.prose ol{padding-left:1.25rem}
.prose li{margin:.35rem 0}
.prose strong{color:var(--ink)}
.prose a{color:var(--gold-ink)}
.note-box{margin:2rem 0;padding:1.25rem 1.4rem;border-left:3px solid var(--gold);background:var(--sand);border-radius:0 10px 10px 0}
.meta-line{margin-top:1rem;font:500 .8125rem/1.4 var(--mono);color:var(--on-night)}
.post-list{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,19rem),1fr));padding:0;list-style:none}
.post-list a{display:block;height:100%;padding:1.5rem;background:var(--paper);border:1px solid var(--line);border-radius:14px;text-decoration:none;color:inherit;transition:border-color .2s,transform .2s}
.post-list a:hover{border-color:var(--gold);transform:translateY(-2px)}
.post-list h3{margin:.5rem 0 .5rem;font-size:1.25rem;line-height:1.2}
.post-list p{color:var(--muted);font-size:.9375rem}
.post-list .eyebrow{margin:0}
.form{display:grid;gap:1rem;padding:clamp(1.25rem,3vw,2rem);background:var(--paper);border:1px solid var(--line);border-radius:14px}
.form .row{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,14rem),1fr))}
.form label{display:grid;gap:.4rem;font:600 .875rem/1.3 var(--sans);color:var(--ink)}
.form label small{font-weight:400;color:var(--muted)}
.form input,.form select,.form textarea{width:100%;min-height:3rem;padding:.7rem .85rem;border:1px solid #7A8BA6;border-radius:8px;background:#fff;font:400 1rem/1.4 var(--sans);color:var(--ink)}
.form textarea{min-height:7.5rem;resize:vertical}
.form input:focus,.form select:focus,.form textarea:focus{outline:2px solid var(--gold);outline-offset:1px;border-color:var(--gold)}
.form fieldset{display:flex;flex-wrap:wrap;gap:.5rem 1.25rem;margin:0;padding:0;border:0}
.form legend{margin-bottom:.5rem;font:600 .875rem/1.3 var(--sans);color:var(--ink)}
.form fieldset label{display:inline-flex;align-items:center;gap:.45rem;font-weight:400}
.form fieldset input{width:auto;min-height:0}
.form .actions{display:flex;flex-wrap:wrap;gap:.75rem;align-items:center}
.form .fine{font-size:.8125rem;color:var(--muted)}
@media (max-width:400px){.channel-value{font-size:1rem}.channel{min-width:0}}
.svc-links{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,13rem),1fr));margin-top:2rem;padding:0;list-style:none}
.svc-links a{display:flex;justify-content:space-between;align-items:center;gap:1rem;padding:1.1rem 1.25rem;background:var(--paper);border:1px solid var(--line);border-radius:12px;font-weight:600;color:var(--ink);text-decoration:none}
.svc-links a:hover{border-color:var(--gold)}
'''

# o botão some enquanto o formulário de agendamento está na tela (só nas páginas que têm o formulário)
CSS_AUTO = '''/* ===== wa-float auto-ocultar ===== */
.wa-float{transition:opacity .2s,visibility .2s,background-color .2s,transform .2s}
.wa-float.is-off{opacity:0;visibility:hidden;pointer-events:none}
'''
JS_AUTO = '''<script>
/* wa-float auto-ocultar */
(function(){var f=document.getElementById('form-agenda'),w=document.querySelector('.wa-float');
if(f&&w&&'IntersectionObserver' in window){new IntersectionObserver(function(e){w.classList.toggle('is-off',e[e.length-1].isIntersecting)}).observe(f)}})();
</script>
'''

# contador de visitas (GoatCounter, sem cookies); se tirar, atualizar /privacidade/ (ver LEIA-ME)
GOAT = '<script data-goatcounter="https://edelmann.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>'

FOOTER_ADD = '<li><a href="/dicas/">Dicas</a></li>\n          <li><a href="/privacidade/">Privacidade</a></li>'

def pages():
    fs = glob.glob(os.path.join(SITE, '**', '*.html'), recursive=True)
    return [f for f in fs if os.path.basename(f) != os.path.basename('google2e5f17acf4dcb527.html') and 'fonts' not in f and '_ferramentas' not in f]

def process(f):
    s = open(f, encoding='utf-8').read()
    if 'http-equiv="refresh"' in s: return False, False, True, False  # redirecionamento: sem estilo, rodapé nem botão
    o = s
    # 1. fontes locais
    s = re.sub(r'<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"[^>]*>\n?', '', s)
    s = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2[^"]*">\n?',
               '<link rel="preload" href="/fonts/space-grotesk.woff2" as="font" type="font/woff2" crossorigin>\n'
               '<link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>\n', s)
    # 2. ícones e manifest
    if 'rel="apple-touch-icon"' not in s:
        s = re.sub(r'(<link rel="icon" type="image/svg\+xml" href="[^"]*">)',
                   lambda m: '<link rel="icon" href="/favicon.ico" sizes="any">\n' + m.group(1) +
                   '\n<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n<link rel="manifest" href="/manifest.webmanifest">', s, count=1)
    # 3. estilos extras
    if '/* ===== Componentes extras ===== */' not in s:
        i = s.index('</style>')
        s = s[:i] + CSS + s[i:]
    # 4. botão do WhatsApp
    if 'class="wa-float"' not in s:
        s = s.replace('</body>', FLOAT + '</body>', 1)
    # 4b. botão com a mesma mensagem dos outros botões e auto-ocultar onde há formulário
    s = re.sub(r'(<a class="wa-float" href=")[^"]*"', lambda m: m.group(1) + WA + '"', s, count=1)
    if 'id="form-agenda"' in s and '/* ===== wa-float auto-ocultar ===== */' not in s:
        s = s.replace('</style>', '\n' + CSS_AUTO + '</style>', 1)
    s = s.replace('e[0].isIntersecting', 'e[e.length-1].isIntersecting')  # páginas geradas antes da correção
    if 'id="form-agenda"' in s and '/* wa-float auto-ocultar */' not in s:
        s = s.replace('</body>', JS_AUTO + '</body>', 1)
    # 5. rodapé: Dicas e Privacidade
    if 'href="/privacidade/"' not in s:
        s = re.sub(r'(<li><a href="/contato/"[^>]*>Contato</a></li>)(\s*</ul>\s*</nav>\s*<a class="foot-mail")',
                   lambda m: m.group(1) + '\n          ' + FOOTER_ADD + m.group(2), s, count=1)
    # 6. contador de visitas (menos a política do app, que diz não usar ferramentas de análise)
    if 'gc.zgo.at/count.js' not in s and not f.endswith('privacidade.html'):
        s = s.replace('</body>', GOAT + '</body>', 1)
    if s != o:
        open(f, 'w', encoding='utf-8', newline='\n').write(s)
    return s != o, ('fonts.googleapis' in s), ('href="/privacidade/"' in s), ('class="wa-float"' in s)

if __name__ == '__main__':
    for f in sorted(pages()):
        print(os.path.relpath(f, SITE), process(f))
