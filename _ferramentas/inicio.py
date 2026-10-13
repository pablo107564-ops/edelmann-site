# Página inicial no modelo de página de captação (fundo escuro, orçamento no topo, áreas de atuação, atendimento,
# "por que", faixa de chamada). Usa o index.html publicado como casca (cabeçalho, estilos, rodapé, scripts) e troca o <main>.
# Idempotente: se já tiver a classe "home", não faz nada.
import os, re

SITE = r'D:\projetos\edelmann-site'
AQUI = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(SITE, 'index.html')
s = open(f, encoding='utf-8').read()
if '<body class="home">' in s:
    raise SystemExit('já feito')

ICONS = '''    <symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.3"/></symbol>
    <symbol id="i-doc" viewBox="0 0 24 24"><path d="M7 3.5h7l4 4v13H7z"/><path d="M14 3.5v4h4M10 12h5M10 15.5h5"/></symbol>
    <symbol id="i-home" viewBox="0 0 24 24"><path d="M4 11 12 4l8 7"/><path d="M6.5 9.5V20h11V9.5"/></symbol>
    <symbol id="i-check" viewBox="0 0 24 24"><path d="m5 12.5 4.2 4.2L19 7"/></symbol>
'''

CSS = '''
/* ===== Início: página de captação ===== */
body.home{background:var(--night)}
.home main{color:var(--on-night)}
.home h2,.home h3{color:#fff}
.home .eyebrow,.home .eyebrow::before{color:var(--gold-soft)}
.home .sub{color:var(--on-night)}
.home .section{background:var(--night)}
.home .section.alt{background:#0A1428;border-block:1px solid rgba(255,255,255,.06)}
.home :focus-visible{outline-color:var(--gold-soft)}
.home h2 em{background:linear-gradient(90deg,#7FB2FF,#5FDDEC);-webkit-background-clip:text;background-clip:text;color:transparent}
.home .site-header{background:rgba(6,12,24,.9);border-bottom-color:rgba(255,255,255,.08)}
.home .brand,.home .brand b{color:#fff}
.home .brand small{color:var(--on-night)}
.home .menu a:not(.btn){color:#DCE2EC}
.home .menu a:not(.btn):hover{color:#fff}
.home .menu-toggle{border-color:rgba(255,255,255,.25);color:#fff}
@media (max-width:959.98px){
  .js .home .menu{background:var(--night);border-bottom-color:rgba(255,255,255,.08)}
  .js .home .menu a:not(.btn){color:#fff;border-bottom-color:rgba(255,255,255,.1)}
}
.home-hero{padding-block:clamp(3rem,7vw,6rem)}
.home-hero .hero-grid{align-items:center}
@media (min-width:960px){.home-hero .hero-grid{grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:4rem}}
.home-hero h1{font-size:clamp(2.4rem,1.3rem + 4vw,4.25rem)}
.home-hero .lead+.lead{margin-top:1rem}
.chip{display:inline-flex;margin-bottom:1.5rem;padding:.4rem .85rem;border:1px solid rgba(95,221,236,.45);border-radius:999px;font:500 .75rem/1.35 var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--gold-soft)}
.hero-links{margin-top:2rem}
.quote{position:relative;padding:clamp(1.25rem,3vw,2rem);background:#0E1B33;border:1px solid rgba(255,255,255,.1);border-radius:16px;box-shadow:0 40px 80px -40px rgba(0,0,0,.7)}
.quote h2{font-size:clamp(1.375rem,1.1rem + 1vw,1.75rem);text-align:center;color:var(--gold-soft)}
.quote>p{margin:.4rem 0 1.25rem;text-align:center;font-size:.9375rem}
.quote .form{padding:0;background:none;border:0}
.quote .form label{color:#DCE2EC}
.quote .form label small,.quote .fine{color:var(--on-night)}
.quote .fine a,.alt-send{color:#fff;text-decoration:underline;text-underline-offset:.2em}
.alt-send{padding:0;border:0;background:none;font:inherit;cursor:pointer}
.quote .btn-primary{width:100%;background:var(--gold-soft);color:var(--night);font-weight:600}
.quote .btn-primary:hover{background:#fff}
.proof{padding-block:1.75rem;background:#0A1428;border-block:1px solid rgba(255,255,255,.06)}
.proof ul{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem;padding:0;list-style:none}
@media (min-width:900px){.proof ul{grid-template-columns:repeat(4,minmax(0,1fr))}}
.proof li{display:flex;align-items:center;gap:.8rem;padding:1rem 1.15rem;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:12px;font:500 .9375rem/1.35 var(--sans);color:#fff}
.proof .i{width:22px;height:22px;color:var(--gold-soft)}
.pillars{display:grid;gap:2.5rem}
@media (min-width:900px){.pillars{grid-template-columns:repeat(2,minmax(0,1fr));grid-template-rows:auto auto}.pillars>div{display:grid;grid-row:span 2;grid-template-rows:subgrid}}
.pillar-card{padding:clamp(1.5rem,3vw,2.25rem);background:#0E1B33;border:1px solid rgba(95,221,236,.28);border-radius:14px;text-align:center}
.home .pillar-card h3{font-size:clamp(1.5rem,1.3rem + .8vw,1.875rem);color:var(--gold-soft)}
.pillar-card p{margin-top:.6rem;font-size:.9375rem}
.rows{display:grid;gap:.5rem;margin-top:1rem;padding:0;list-style:none}
.rows a{display:flex;justify-content:space-between;align-items:center;gap:1rem;padding:.9rem 1.15rem;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.09);border-radius:10px;color:#DCE2EC;font-size:.9375rem;text-decoration:none;transition:border-color .2s,background-color .2s,color .2s}
.rows a:hover{border-color:var(--gold-soft);background:rgba(95,221,236,.06);color:#fff}
.rows .i{width:18px;height:18px;color:var(--gold-soft);transition:transform .3s var(--ease)}
.rows a:hover .i{transform:translateX(4px)}
.modes{display:grid;gap:1.5rem}
@media (min-width:900px){.modes{grid-template-columns:repeat(2,minmax(0,1fr))}}
.mode{display:flex;flex-direction:column;overflow:hidden;background:#0E1B33;border:1px solid rgba(255,255,255,.1);border-radius:14px}
.home .mode h3{padding:1.4rem 1.75rem;background:linear-gradient(90deg,var(--gold-ink),#14869B);font-size:1.5rem}
.mode ul{display:grid;gap:.9rem;padding:1.6rem 1.75rem;list-style:none}
.mode li{display:flex;gap:.75rem;font-size:1rem;color:#DCE2EC}
.mode li .i{width:20px;height:20px;margin-top:.15rem;color:var(--gold-soft)}
.mode .btn{align-self:flex-start;margin:auto 1.75rem 1.75rem}
.why{display:grid;gap:3rem;align-items:center}
@media (min-width:960px){.why{grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:5rem}}
.why .map{justify-self:center}
.why-title{margin-bottom:2rem;font-size:var(--h2);line-height:1.08;letter-spacing:-.02em}
.home .faq details{background:#0E1B33;border-color:rgba(255,255,255,.1)}
.home .faq summary{color:#fff}
.home .faq summary::after{color:var(--gold-soft)}
.home .faq details p{color:var(--on-night)}
.cta-accent{padding-block:clamp(4rem,8vw,6.5rem);background:var(--gold-soft);text-align:center}
.home .cta-accent h2{max-width:40rem;margin-inline:auto;font-size:clamp(1.875rem,1.2rem + 2.6vw,3rem);line-height:1.1;color:var(--night)}
.cta-accent p{max-width:36rem;margin:1.25rem auto 0;color:#16314F}
.cta-accent .ctas{justify-content:center}
.cta-accent .btn-primary{background:var(--night);color:#fff}
.cta-accent .btn-primary:hover{background:var(--navy)}
.cta-accent .btn-ghost{border-color:rgba(6,12,24,.45);color:var(--night)}
.cta-accent .btn-ghost:hover{border-color:var(--night)}
.home .cta-accent :focus-visible{outline-color:var(--night)}
'''

JS = '''<script>
/* Orçamento do topo: monta a mensagem no navegador e abre WhatsApp ou e-mail. */
(function(){
  var f=document.getElementById('form-inicio'); if(!f)return;
  function msg(){
    var d=new FormData(f),l=['Olá! Quero um orçamento pela Edelmann Tecnologia.','','Nome: '+d.get('nome')];
    if(d.get('local'))l.push('Bairro/cidade: '+d.get('local'));
    l.push('Serviço: '+d.get('servico'),'Para: '+d.get('para'),'','Descrição: '+d.get('descricao'));
    return l.join('\\n');
  }
  f.addEventListener('submit',function(e){
    e.preventDefault(); if(!f.reportValidity())return;
    window.open('https://wa.me/5593981212924?text='+encodeURIComponent(msg()),'_blank','noopener');
  });
  document.getElementById('inicio-email').addEventListener('click',function(){
    if(!f.reportValidity())return;
    var a=document.createElement('a');
    a.href='mailto:edelmann.tecnologia@gmail.com?subject='+encodeURIComponent('Orçamento - '+new FormData(f).get('servico'))+'&body='+encodeURIComponent(msg());
    document.body.appendChild(a); a.click(); a.remove();
  });
})();
</script>
'''

main = open(os.path.join(AQUI, 'inicio_main.html'), encoding='utf-8').read().strip()
s = re.sub(r'<main id="conteudo" tabindex="-1">.*?</main>', lambda m: main, s, count=1, flags=re.S)
s = s.replace('<body>', '<body class="home">', 1)
s = s.replace('<meta name="color-scheme" content="light">', '<meta name="color-scheme" content="dark">', 1)
s = s.replace('  </defs>\n</svg>', ICONS + '  </defs>\n</svg>', 1)
s = s.replace('</style>', CSS + '</style>', 1)
s = s.replace('<a class="wa-float"', JS + '<a class="wa-float"', 1)
open(f, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
