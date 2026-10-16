# Dados e HTML da galeria "Trabalhos realizados" (fotos tratadas em img/trabalhos/: sem metadados, cortadas e desfocadas).
# Usado por consultoria.py (início com 3 fotos, Sobre com as 6).

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
