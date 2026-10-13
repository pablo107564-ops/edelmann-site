# Galeria "Trabalhos realizados" com as fotos de img/trabalhos/ (tratadas: sem metadados, cortadas e desfocadas).
# Início: 3 fotos, depois de Áreas de atuação. Serviços: as 6, depois dos cards. Idempotente.
import os

SITE = r'D:\projetos\edelmann-site'
ARROW = '<svg class="i" aria-hidden="true" focusable="false"><use href="#i-arrow"/></svg>'
# arquivo, largura, altura, legenda, texto alternativo
FOTOS = [
    ('torre-enlace', 676, 1200, 'Enlace de rádio ponto a ponto em torre', 'Antena de enlace de rádio fixada em torre, com a cidade ao fundo'),
    ('rack', 676, 1200, 'Rack com switches, patch panels e distribuidor óptico', 'Rack de rede com switches, patch panels, conversores de mídia e distribuidores ópticos, com os cabos organizados'),
    ('bancada-fibra', 1200, 519, 'Fusão de fibra óptica e montagem de equipamento', 'Bancada com máquina de fusão de fibra óptica e um gravador aberto com dois discos rígidos'),
    ('manutencao-pc', 866, 1200, 'Manutenção de desktop', 'Gabinete aberto com placa-mãe, cooler, fonte e cabos durante a manutenção'),
    ('torre-fixacao', 676, 1200, 'Fixação e alinhamento da antena', 'Suporte metálico prendendo a antena de rádio à torre'),
    ('racks-parede', 1200, 676, 'Racks de parede para rede e equipamentos', 'Dois racks de parede instalados, um preto e um bege, com os cabos de rede chegando por eletrodutos'),
]
CSS = ('.gallery{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));grid-auto-rows:clamp(13rem,32vw,22rem);gap:.75rem;padding:0;list-style:none}\n'
       '@media (min-width:960px){.gallery{grid-template-columns:repeat(4,minmax(0,1fr))}}\n'
       '.gallery .wide{grid-column:span 2}\n'
       '.gallery figure{position:relative;height:100%;margin:0;overflow:hidden;border-radius:12px;background:var(--line)}\n'
       '.gallery img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .5s var(--ease)}\n'
       '.gallery li:hover img{transform:scale(1.03)}\n'
       '.gallery figcaption{position:absolute;inset:auto 0 0;padding:2.5rem 1rem .85rem;background:linear-gradient(transparent,rgba(6,12,24,.88));color:#fff;font:500 .875rem/1.35 var(--sans)}\n')

def items(fotos):
    out = []
    for nome, w, h, leg, alt in fotos:
        cls = ' class="wide"' if w > h else ''
        out.append(f'        <li{cls}><figure><img src="/img/trabalhos/{nome}.jpg" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async"><figcaption>{leg}</figcaption></figure></li>')
    return '\n'.join(out)

def secao(fotos, classe, mais=''):
    return f'''  <section class="section{classe}" id="trabalhos" aria-labelledby="trabalhos-titulo">
    <div class="wrap">
      <div class="head reveal">
        <div>
          <p class="eyebrow">Trabalhos</p>
          <h2 id="trabalhos-titulo">Trabalhos realizados.</h2>
        </div>
        <p class="sub">Algumas instalações e manutenções que realizamos.</p>
      </div>
      <ul class="gallery reveal">
{items(fotos)}
      </ul>{mais}
    </div>
  </section>

'''

def aplica(p, antes_de, html, trocas=()):
    f = os.path.join(SITE, p)
    s = open(f, encoding='utf-8').read()
    if 'id="trabalhos"' in s:
        print(p, 'já feito'); return
    i = s.index(antes_de)
    s = s[:i] + html + s[i:]
    s = s.replace('/* ===== Componentes extras ===== */', '/* ===== Componentes extras ===== */\n' + CSS, 1)
    for a, b in trocas:
        assert a in s, a
        s = s.replace(a, b, 1)
    open(f, 'w', encoding='utf-8', newline='\n').write(s)
    print(p, 'ok')

# Início (fundo escuro): entra entre Áreas de atuação e Atendimento; Atendimento e Por que trocam de fundo para alternar.
aplica('index.html', '  <section class="section alt" id="atendimento"',
       secao(FOTOS[:3], ' alt', f'\n      <p class="more reveal"><a class="link" href="/servicos/#trabalhos">Ver mais trabalhos{ARROW}</a></p>'),
       [('<section class="section alt" id="atendimento"', '<section class="section" id="atendimento"'),
        ('<section class="section" id="por-que"', '<section class="section alt" id="por-que"'),
        ('/* ===== Início: página de captação ===== */', '/* ===== Início: página de captação ===== */\n.home .gallery figure{background:#0E1B33}\n.home .link{color:#fff}')])
aplica('servicos/index.html', '  <section class="section" id="metodo"', secao(FOTOS, ' paper'))
