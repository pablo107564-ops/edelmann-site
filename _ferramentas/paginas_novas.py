# Gera as páginas novas do site Edelmann a partir do modelo da página de serviços.
import re, os, json, html

SITE = r'D:\projetos\edelmann-site'
BASE = 'https://edelmann.com.br'
shell = open(os.path.join(SITE, 'servicos', 'index.html'), encoding='utf-8').read()
I = shell.index('<main id="conteudo" tabindex="-1">') + len('<main id="conteudo" tabindex="-1">')
J = shell.index('</main>')
HEAD, TAIL = shell[:I], shell[J:]

WA = 'https://wa.me/5593981212924?text='
EXT = '<span class="sr"> (abre em nova aba)</span>'
ARROW = '<svg class="i" aria-hidden="true" focusable="false"><use href="#i-arrow"/></svg>'
ORG = {"@type": "ProfessionalService", "name": "Edelmann Tecnologia", "url": BASE + "/", "telephone": "+55-93-98121-2924",
       "email": "edelmann.tecnologia@gmail.com", "image": BASE + "/img/og.jpg",
       "address": {"@type": "PostalAddress", "addressLocality": "Itaituba", "addressRegion": "PA", "addressCountry": "BR"},
       "areaServed": {"@type": "City", "name": "Itaituba"}}

def wa(msg):
    from urllib.parse import quote
    return WA + quote(msg)

def crumbs(items):
    parts = []
    for name, href in items:
        parts.append(f'<a href="{href}">{name}</a>' if href else f'<span aria-current="page">{name}</span>')
    return '<nav class="crumbs" aria-label="Trilha">' + ' › '.join(parts) + '</nav>'

def breadcrumb_ld(items, path):
    out, pos = [], 1
    for name, href in items:
        out.append({"@type": "ListItem", "position": pos, "name": name, "item": BASE + (href or '/' + path)})
        pos += 1
    return {"@type": "BreadcrumbList", "itemListElement": out}

def faq_html(qas, title='Perguntas frequentes', eyebrow='Dúvidas', hid='faq'):
    items = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in qas)
    return f'''  <section class="section" aria-labelledby="{hid}-titulo">
    <div class="wrap">
      <div class="head reveal"><div><p class="eyebrow">{eyebrow}</p><h2 id="{hid}-titulo">{title}</h2></div></div>
      <div class="faq reveal">{items}</div>
    </div>
  </section>
'''

def faq_ld(qas):
    strip = lambda t: re.sub(r'<[^>]+>', '', t)
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qas]}

def cta(title='Precisa desse serviço em Itaituba?', msg='Olá! Vim pelo site da Edelmann Tecnologia.'):
    return f'''  <section class="section band cta-band" aria-labelledby="cta-titulo">
    <div class="wrap reveal">
      <h2 id="cta-titulo">{title}</h2>
      <p>Conte o que está acontecendo. Respondemos com os próximos passos e, quando for o caso, com um orçamento.</p>
      <div class="ctas">
        <a class="btn btn-primary" href="{wa(msg)}" target="_blank" rel="noopener">Chamar no WhatsApp{EXT}{ARROW}</a>
        <a class="btn btn-ghost" href="/contato/#orcamento">Pedir orçamento</a>
      </div>
    </div>
  </section>
'''

def hero(crumb_items, eyebrow, h1a, h1b, lead, buttons=True, msg='Olá! Vim pelo site da Edelmann Tecnologia.', meta=None):
    btns = f'''      <div class="ctas">
        <a class="btn btn-primary" href="{wa(msg)}" target="_blank" rel="noopener">Chamar no WhatsApp{EXT}{ARROW}</a>
        <a class="btn btn-ghost" href="/contato/#orcamento">Pedir orçamento</a>
      </div>
''' if buttons else ''
    m = f'      <p class="meta-line">{meta}</p>\n' if meta else ''
    return f'''
  <section class="hero" aria-labelledby="titulo">
    <div class="wrap">
      {crumbs(crumb_items)}
      <p class="eyebrow">{eyebrow}</p>
      <h1 id="titulo"><span>{h1a}</span> <em>{h1b}</em></h1>
      <p class="lead">{lead}</p>
{m}{btns}    </div>
  </section>
'''

def cards(items, eyebrow, title, sub, hid):
    lis = ''.join(f'''        <li class="service">
          <div class="service-top"><svg class="i" aria-hidden="true" focusable="false"><use href="#{ic}"/></svg></div>
          <h3>{t}</h3>
          <p>{d}</p>
        </li>
''' for ic, t, d in items)
    return f'''  <section class="section" aria-labelledby="{hid}-titulo">
    <div class="wrap">
      <div class="head reveal"><div><p class="eyebrow">{eyebrow}</p><h2 id="{hid}-titulo">{title}</h2></div><p class="sub">{sub}</p></div>
      <ul class="services reveal">
{lis}      </ul>
    </div>
  </section>
'''

STEPS = '''  <section class="section paper" aria-labelledby="como-titulo">
    <div class="wrap">
      <div class="head reveal"><div><p class="eyebrow">Como funciona</p><h2 id="como-titulo">Quatro etapas, nenhuma surpresa.</h2></div></div>
      <ol class="steps reveal">
        <li class="step"><h3>Solicitação</h3><p>Você descreve o que precisa pelo WhatsApp ou pelo formulário de orçamento.</p></li>
        <li class="step"><h3>Diagnóstico e orçamento</h3><p>Avaliamos o cenário e apresentamos a solução, com o valor, antes de começar.</p></li>
        <li class="step"><h3>Execução</h3><p>Realizamos o serviço no local, em Itaituba, ou a distância, conforme o caso.</p></li>
        <li class="step"><h3>Acompanhamento</h3><p>Conferimos o resultado e seguimos à disposição depois da entrega.</p></li>
      </ol>
    </div>
  </section>
'''

def page(path, title, desc, main, ld=None, current=None, og_type='website', noindex=False):
    h = HEAD
    h = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', h)
    esc = html.escape(desc, quote=True)
    h = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc, h)
    h = re.sub(r'(<meta (?:property="og:description"|name="twitter:description") content=")[^"]*', lambda m: m.group(1) + esc, h)
    short = html.escape(title.split(' | ')[0], quote=True)
    h = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*', lambda m: m.group(1) + short + ' | Edelmann Tecnologia', h)
    h = h.replace(f'{BASE}/servicos/', f'{BASE}/{path}')
    h = h.replace('<meta property="og:type" content="website">', f'<meta property="og:type" content="{og_type}">')
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', h, flags=re.S)
    if noindex:
        h = re.sub(r'<link rel="canonical"[^>]*>\n', '', h)
        h = h.replace('<meta name="theme-color"', '<meta name="robots" content="noindex">\n<meta name="theme-color"', 1)
    if ld:
        graph = {"@context": "https://schema.org", "@graph": ld}
        h = h.replace('<style>', '<script type="application/ld+json">\n' + json.dumps(graph, ensure_ascii=False, indent=1) + '\n</script>\n<style>', 1)
    h = h.replace('<li><a href="/servicos/" aria-current="page">', '<li><a href="/servicos/">')
    if current:
        h = h.replace(f'<li><a href="{current}">', f'<li><a href="{current}" aria-current="page">', 1)
    out = os.path.join(SITE, path.replace('/', os.sep), 'index.html') if path.endswith('/') else os.path.join(SITE, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8', newline='\n').write(h + '\n' + main + '\n' + TAIL)
    print(path, len((h + main + TAIL).encode()))

# ---------------------------------------------------------------- 404
page('404.html', 'Página não encontrada | Edelmann Tecnologia', 'O endereço que você abriu não existe ou mudou de lugar.',
     hero([('Início', '/'), ('Página não encontrada', None)], 'Erro 404', 'Esta página', 'não foi encontrada.',
          'O endereço pode ter sido digitado errado ou a página mudou de lugar. Veja abaixo os caminhos mais procurados.', buttons=False) +
     '''  <section class="section" aria-labelledby="caminhos-titulo">
    <div class="wrap">
      <div class="head"><div><p class="eyebrow">Caminhos</p><h2 id="caminhos-titulo">Para onde você quer ir?</h2></div></div>
      <ul class="svc-links">
        <li><a href="/">Página inicial''' + ARROW + '''</a></li>
        <li><a href="/servicos/">Serviços''' + ARROW + '''</a></li>
        <li><a href="/produtos/">Produtos''' + ARROW + '''</a></li>
        <li><a href="/dicas/">Dicas''' + ARROW + '''</a></li>
        <li><a href="/contato/">Contato''' + ARROW + '''</a></li>
      </ul>
    </div>
  </section>
''', noindex=True)

# ---------------------------------------------------------------- Privacidade
PRIV = '''  <section class="section" aria-labelledby="politica-titulo">
    <div class="wrap">
      <div class="prose">
        <h2 id="politica-titulo">Resumo</h2>
        <p>Este site não usa cookies, não tem contador de visitas e não guarda os dados que você digita. O formulário de orçamento só monta uma mensagem no seu próprio aparelho e abre o WhatsApp ou o seu e-mail para você enviar, se quiser.</p>

        <h2>Quem somos</h2>
        <p><strong>Edelmann Tecnologia</strong>, Itaituba, Pará, Brasil. Contato para assuntos de privacidade: <a href="mailto:edelmann.tecnologia@gmail.com?subject=Privacidade%20-%20Edelmann%20Tecnologia">edelmann.tecnologia@gmail.com</a> ou WhatsApp (93) 98121-2924.</p>

        <h2>Quais dados tratamos</h2>
        <ul>
          <li><strong>Mensagens que você nos envia</strong> por WhatsApp, e-mail ou telefone, com o que você decidir informar (nome, contato, descrição do problema). Usamos só para responder, fazer o orçamento e prestar o serviço contratado.</li>
          <li><strong>Formulário de orçamento:</strong> funciona apenas no seu navegador. Nada é enviado ao nosso site; a mensagem só sai quando você mesmo a envia pelo WhatsApp ou pelo e-mail.</li>
          <li><strong>Dados técnicos de acesso:</strong> o site é hospedado no GitHub Pages, que pode registrar o endereço IP de quem acessa para segurança e funcionamento do serviço, conforme a política de privacidade do GitHub. Não temos acesso a esses registros para identificar visitantes.</li>
        </ul>

        <h2>Serviços de terceiros</h2>
        <p>Ao clicar em botões de WhatsApp ou de e-mail, você passa a usar serviços de outras empresas (como o WhatsApp, da Meta, e o Gmail, do Google), que têm suas próprias políticas de privacidade. As fontes e imagens do site são servidas pelo próprio site, sem chamadas a outros servidores.</p>

        <h2>Por quanto tempo guardamos</h2>
        <p>As conversas e informações de atendimento ficam guardadas enquanto forem necessárias para o atendimento, a garantia do serviço e o cumprimento de obrigações legais. Você pode pedir a exclusão a qualquer momento, respeitadas essas obrigações.</p>

        <h2>Seus direitos (LGPD)</h2>
        <p>Pela Lei Geral de Proteção de Dados (Lei nº 13.709/2018), você pode pedir a confirmação de que tratamos seus dados, o acesso, a correção, a exclusão, a portabilidade e informações sobre compartilhamento, além de revogar o consentimento. Para isso, escreva para <a href="mailto:edelmann.tecnologia@gmail.com?subject=LGPD%20-%20Edelmann%20Tecnologia">edelmann.tecnologia@gmail.com</a>.</p>

        <h2>Aplicativos</h2>
        <p>O <a href="/leitor-de-bolso/privacidade.html">Leitor de Bolso</a> tem uma política de privacidade própria.</p>

        <h2>Mudanças nesta política</h2>
        <p>Se esta política mudar, a nova versão será publicada nesta página, com a data de atualização.</p>
        <p class="fine">Última atualização: 12 de outubro de 2026.</p>
      </div>
    </div>
  </section>
'''
page('privacidade/', 'Política de privacidade | Edelmann Tecnologia', 'Como a Edelmann Tecnologia trata dados pessoais no site e nos atendimentos, conforme a LGPD.',
     hero([('Início', '/'), ('Privacidade', None)], 'Privacidade', 'Política', 'de privacidade.',
          'Como tratamos as informações de quem visita o site e de quem fala conosco.', buttons=False) + PRIV,
     ld=[breadcrumb_ld([('Início', '/'), ('Privacidade', None)], 'privacidade/')])

# ---------------------------------------------------------------- Serviços detalhados
COMMON_FAQ = [
    ('Vocês atendem em casa ou na empresa?', 'Sim. Atendemos presencialmente em residências e empresas de Itaituba. Quando o problema permite, também resolvemos a distância, com acesso remoto seguro.'),
    ('Como funciona o orçamento?', 'Você descreve o que precisa; avaliamos o cenário e apresentamos a solução e o valor antes de começar. Nada é feito sem a sua aprovação.'),
    ('Atendem fora de Itaituba?', 'O atendimento presencial é em Itaituba. Para outras cidades, atendemos a distância sempre que o serviço permitir.'),
]

SERVICOS = [
    dict(slug='formatacao-e-manutencao', nome='Formatação e manutenção', h1a='Formatação e manutenção', h1b='de computadores em Itaituba.',
         title='Formatação e manutenção de computadores em Itaituba (PA)',
         desc='Formatação, limpeza, upgrade de SSD e memória e correção de lentidão em desktops e notebooks em Itaituba. Atendimento presencial e remoto.',
         lead='Desktops e notebooks lentos, travando ou com defeito: diagnosticamos a causa e resolvemos, em casa, na empresa ou a distância.',
         msg='Olá! Sou de Itaituba e preciso de formatação ou manutenção de computador.',
         itens=[('i-support', 'Formatação e reinstalação', 'Instalação limpa do sistema, drivers e programas essenciais, com os arquivos importantes preservados conforme combinado com você.'),
                ('i-support', 'Limpeza e manutenção', 'Limpeza interna para reduzir o aquecimento, que deixa o computador lento e desligando sozinho.'),
                ('i-server', 'Upgrade de SSD e memória', 'Troca do HD por SSD e ampliação da memória: a forma mais eficiente de dar vida nova a um computador antigo.'),
                ('i-shield', 'Vírus e lentidão', 'Remoção de vírus e programas indesejados e ajuste do que inicia junto com o sistema.'),
                ('i-code', 'Programas e configuração', 'Instalação e configuração de programas, impressoras e contas de e-mail.'),
                ('i-restore', 'Troca de peças', 'Diagnóstico de defeitos de hardware e troca de peças, com orçamento antes de qualquer compra.')],
         faq=[('Formatar apaga meus arquivos?', 'A formatação apaga o disco, por isso combinamos antes o que precisa ser salvo e fazemos a cópia dos arquivos importantes antes de começar.'),
              ('Vale a pena trocar o HD por SSD?', 'Na maioria dos computadores com HD, sim: o SSD deixa a inicialização e a abertura de programas muito mais rápidas. Avaliamos o seu equipamento e indicamos se compensa.')],
         dica=('/dicas/notebook-lento/', 'Notebook lento: 7 causas comuns e como resolver')),
    dict(slug='redes-e-wifi', nome='Redes e Wi-Fi', h1a='Redes e Wi-Fi', h1b='em Itaituba.',
         title='Redes e Wi-Fi em Itaituba (PA) para casa e empresa',
         desc='Projeto e configuração de Wi-Fi e redes cabeadas em Itaituba: sinal em todos os ambientes, roteadores MikroTik, fibra e VLANs para empresas.',
         lead='Wi-Fi que não chega em todos os cômodos, rede da empresa instável ou lenta: projetamos e configuramos a rede para funcionar de ponta a ponta.',
         msg='Olá! Sou de Itaituba e preciso de ajuda com rede ou Wi-Fi.',
         itens=[('i-wifi', 'Cobertura de Wi-Fi', 'Posicionamento e configuração de roteadores e pontos de acesso para o sinal chegar a todos os ambientes.'),
                ('i-wifi', 'Rede cabeada', 'Projeto e organização da rede cabeada de casas e empresas, para os pontos que precisam de mais estabilidade.'),
                ('i-server', 'Roteadores MikroTik', 'Configuração de roteadores MikroTik: controle de banda, redes separadas, acesso remoto e monitoramento.'),
                ('i-wifi', 'Fibra óptica', 'Configuração de equipamentos de fibra e da conexão com o provedor.'),
                ('i-shield', 'Redes separadas (VLANs)', 'Separação da rede de visitantes, câmeras e equipamentos da empresa, com mais segurança e organização.'),
                ('i-support', 'Diagnóstico de lentidão', 'Testes para descobrir se a lentidão está na internet, no roteador, no Wi-Fi ou nos aparelhos.')],
         faq=[('Repetidor resolve Wi-Fi fraco?', 'Às vezes, mas costuma reduzir a velocidade. Em muitos casos, mudar o roteador de lugar, usar um ponto de acesso cabeado ou um sistema mesh funciona melhor. Avaliamos o ambiente e indicamos a solução.'),
              ('Vocês configuram a rede de empresas?', 'Sim. Projetamos e configuramos redes de empresas, com redes separadas para visitantes e equipamentos, controle de acesso e acesso remoto seguro.')],
         dica=('/dicas/wifi-fraco/', 'Wi-Fi fraco em casa: como melhorar o sinal')),
    dict(slug='servidores', nome='Servidores', h1a='Servidores', h1b='para empresas em Itaituba.',
         title='Servidores Linux e Windows em Itaituba (PA)',
         desc='Instalação e manutenção de servidores Linux e Windows, máquinas virtuais, Docker e serviços 24 horas para empresas em Itaituba.',
         lead='Instalamos e mantemos os servidores que guardam os arquivos e os sistemas da sua empresa, funcionando com estabilidade.',
         msg='Olá! Sou de Itaituba e quero falar sobre servidor para empresa.',
         itens=[('i-server', 'Servidores Linux e Windows', 'Instalação, configuração e manutenção de servidores para arquivos, sistemas e serviços da empresa.'),
                ('i-server', 'Máquinas virtuais', 'Vários servidores num só equipamento, com melhor aproveitamento e mais facilidade de manutenção.'),
                ('i-code', 'Docker e serviços', 'Publicação de sistemas e serviços em contêineres, com atualização mais simples e segura.'),
                ('i-restore', 'Backup do servidor', 'Rotinas de cópia automáticas e plano para voltar a funcionar depois de uma falha.'),
                ('i-shield', 'Acesso remoto seguro', 'Acesso aos sistemas de fora da empresa sem expor o servidor a riscos desnecessários.'),
                ('i-support', 'Manutenção contínua', 'Atualizações, verificação de espaço e de funcionamento para evitar paradas inesperadas.')],
         faq=[('Minha empresa precisa de servidor?', 'Depende de quantas pessoas e sistemas usam os mesmos arquivos. Avaliamos o seu caso e indicamos se compensa um servidor local, a nuvem ou uma combinação dos dois.')],
         dica=('/dicas/backup-3-2-1/', 'Backup sem complicação: a regra 3-2-1')),
    dict(slug='seguranca-e-backup', nome='Segurança e backup', h1a='Segurança e backup', h1b='em Itaituba.',
         title='Segurança e backup em Itaituba (PA)',
         desc='Firewall, antivírus, acesso remoto seguro e rotinas de backup automáticas para casas e empresas em Itaituba.',
         lead='Protegemos computadores e redes contra invasões e vírus, e garantimos que seus arquivos tenham cópia para quando algo der errado.',
         msg='Olá! Sou de Itaituba e quero falar sobre segurança ou backup.',
         itens=[('i-shield', 'Firewall', 'Configuração de firewall no roteador e nos computadores para bloquear acessos indevidos.'),
                ('i-shield', 'Antivírus e proteção', 'Proteção contra vírus e programas maliciosos, com configuração adequada para cada equipamento.'),
                ('i-shield', 'Acesso remoto seguro', 'Acesso aos computadores e sistemas da empresa a distância, sem portas abertas desnecessárias.'),
                ('i-restore', 'Backup automático', 'Cópias programadas dos arquivos importantes, no próprio local e fora dele.'),
                ('i-restore', 'Plano de recuperação', 'Procedimento definido para voltar a funcionar rapidamente depois de uma falha ou ataque.'),
                ('i-support', 'Boas práticas', 'Orientação sobre senhas, atualizações e cuidados do dia a dia que evitam a maioria dos problemas.')],
         faq=[('O antivírus do Windows é suficiente?', 'Para uso doméstico, o Microsoft Defender, que já vem no Windows, oferece uma boa proteção quando está ativo e atualizado. Em empresas, avaliamos a rede como um todo: firewall, atualizações, acessos e backup.'),
              ('Com que frequência devo fazer backup?', 'Com a frequência com que seus arquivos mudam: para quem trabalha todo dia no computador, a cópia deve ser diária e automática.')],
         dica=('/dicas/backup-3-2-1/', 'Backup sem complicação: a regra 3-2-1')),
]

for sv in SERVICOS:
    crumb = [('Início', '/'), ('Serviços', '/servicos/'), (sv['nome'], None)]
    faq = sv['faq'] + COMMON_FAQ
    path = f"servicos/{sv['slug']}/"
    dica = f'''  <section class="section" aria-labelledby="leia-titulo">
    <div class="wrap">
      <div class="head reveal"><div><p class="eyebrow">Dicas</p><h2 id="leia-titulo">Leia também.</h2></div></div>
      <ul class="svc-links"><li><a href="{sv['dica'][0]}">{sv['dica'][1]}{ARROW}</a></li><li><a href="/servicos/">Todos os serviços{ARROW}</a></li></ul>
    </div>
  </section>
'''
    main = (hero(crumb, 'Itaituba · Pará', sv['h1a'], sv['h1b'], sv['lead'], msg=sv['msg']) +
            cards(sv['itens'], 'O que fazemos', 'Serviços incluídos.', 'Atendimento presencial em Itaituba e remoto quando o problema permite.', 'itens') +
            STEPS + faq_html(faq) + dica + cta(msg=sv['msg']))
    ld = [dict(**{"@type": "Service", "name": sv['title'].split(' | ')[0], "description": sv['desc'], "serviceType": sv['nome'],
                  "areaServed": {"@type": "City", "name": "Itaituba"}, "provider": ORG, "url": f"{BASE}/{path}"}),
          breadcrumb_ld(crumb, path), faq_ld(faq)]
    page(path, sv['title'] + ' | Edelmann Tecnologia', sv['desc'], main, ld=ld, current='/servicos/')

# ---------------------------------------------------------------- Dicas
ARTIGOS = [
 dict(slug='notebook-lento', titulo='Notebook lento: 7 causas comuns e como resolver', h1a='Notebook lento?', h1b='7 causas e como resolver.',
      desc='Por que o computador fica lento e o que fazer: HD antigo, pouca memória, programas na inicialização, vírus, aquecimento e mais.',
      resumo='HD antigo, pouca memória, vírus e aquecimento estão entre os motivos mais comuns. Veja como identificar cada um.',
      tempo='5 min de leitura', corpo='''
<p>Um computador que demora para ligar, trava ao abrir programas ou fica com o ventilador sempre alto quase sempre tem uma causa identificável. Antes de pensar em trocar de máquina, vale conferir os sete motivos mais comuns.</p>
<h2>1. O disco ainda é um HD</h2>
<p>Muitos notebooks vendidos até poucos anos atrás vêm com HD mecânico. Ele é bem mais lento que um <strong>SSD</strong> para ligar o sistema e abrir programas. Na prática, trocar o HD por um SSD costuma ser a melhoria mais perceptível que se pode fazer num computador antigo.</p>
<p><strong>Como saber:</strong> no Windows, abra o Gerenciador de Tarefas (Ctrl + Shift + Esc), vá em <em>Desempenho</em> e veja o tipo do disco. Se o disco fica em 100% de uso por muito tempo, ele provavelmente é o gargalo.</p>
<h2>2. Pouca memória RAM</h2>
<p>Com várias abas do navegador e programas abertos, a memória acaba e o sistema passa a usar o disco como reserva, o que deixa tudo lento. Para o uso atual com Windows, 8 GB é um mínimo confortável para tarefas do dia a dia.</p>
<p><strong>Como saber:</strong> no Gerenciador de Tarefas, veja se a memória fica perto de 90% ou mais durante o uso normal.</p>
<h2>3. Programas demais iniciando com o sistema</h2>
<p>Muitos programas se configuram para abrir junto com o Windows e ficam rodando em segundo plano sem necessidade.</p>
<p><strong>O que fazer:</strong> no Gerenciador de Tarefas, aba <em>Aplicativos de inicialização</em>, desative o que você não usa sempre. Não desative o antivírus nem itens que você não reconhece sem pesquisar antes.</p>
<h2>4. Vírus e programas indesejados</h2>
<p>Programas maliciosos, extensões de navegador suspeitas e "otimizadores" instalados sem querer consomem recursos e podem expor seus dados.</p>
<p><strong>O que fazer:</strong> mantenha o Microsoft Defender ativo e atualizado, faça uma verificação completa e revise as extensões do navegador.</p>
<h2>5. Aquecimento por poeira</h2>
<p>Com o tempo, a poeira acumula nas ventoinhas e dissipadores. O processador esquenta e reduz a própria velocidade para se proteger; em casos extremos, o computador desliga sozinho.</p>
<p><strong>Sinais:</strong> ventilador sempre alto, base do notebook muito quente, lentidão que piora depois de alguns minutos de uso. A solução é uma limpeza interna, com troca da pasta térmica quando necessário.</p>
<h2>6. Disco quase cheio</h2>
<p>Com pouco espaço livre, o sistema tem dificuldade para atualizar e trabalhar. Libere espaço com a ferramenta <em>Limpeza de Disco</em> ou em <em>Configurações › Sistema › Armazenamento</em>, e mova fotos e vídeos antigos para outro lugar (com backup).</p>
<h2>7. Sistema desatualizado ou danificado</h2>
<p>Atualizações pendentes, drivers antigos e anos de programas instalados e removidos podem deixar o sistema instável. Quando nada resolve, uma formatação com instalação limpa costuma devolver o desempenho, desde que os arquivos sejam salvos antes.</p>
<div class="note-box"><p><strong>Resumo:</strong> confira primeiro o tipo de disco, a memória e o aquecimento. Juntos, eles explicam a maioria dos casos de lentidão.</p></div>
''', links=[('/servicos/formatacao-e-manutencao/', 'Formatação e manutenção em Itaituba')]),
 dict(slug='wifi-fraco', titulo='Wi-Fi fraco em casa: como melhorar o sinal', h1a='Wi-Fi fraco em casa?', h1b='Como melhorar o sinal.',
      desc='Dicas práticas para melhorar o Wi-Fi: posição do roteador, 2,4 GHz e 5 GHz, interferência, repetidor, rede mesh e cabo.',
      resumo='Posição do roteador, frequência certa e menos interferência resolvem boa parte dos problemas. Veja quando vale um ponto de acesso ou mesh.',
      tempo='5 min de leitura', corpo='''
<p>Antes de trocar de plano de internet, vale descobrir se o problema é a internet ou o Wi-Fi. Muitas vezes a conexão chega bem até o roteador e se perde no caminho até o celular ou o notebook.</p>
<h2>1. Separe o problema: internet ou Wi-Fi?</h2>
<p>Faça um teste de velocidade com um computador ligado <strong>por cabo</strong> ao roteador e outro pelo Wi-Fi, perto do roteador. Se pelo cabo a velocidade está boa e pelo Wi-Fi não, o problema é a rede sem fio, não o plano.</p>
<h2>2. Mude o roteador de lugar</h2>
<p>O sinal se espalha em todas as direções e perde força ao atravessar paredes, lajes, espelhos e móveis de metal. O ideal é deixar o roteador:</p>
<ul>
<li>no ponto mais central da casa possível;</li>
<li>em lugar alto e aberto, fora de armários e de trás da TV;</li>
<li>longe de micro-ondas, aquários e superfícies metálicas.</li>
</ul>
<h2>3. Use a frequência certa</h2>
<p>A maioria dos roteadores atuais transmite em duas frequências:</p>
<ul>
<li><strong>2,4 GHz:</strong> alcança mais longe e atravessa melhor as paredes, mas é mais lenta e sofre mais interferência.</li>
<li><strong>5 GHz:</strong> é mais rápida e tem menos interferência, mas o alcance é menor.</li>
</ul>
<p>Para a TV e o computador perto do roteador, prefira 5 GHz. Para cômodos distantes, 2,4 GHz pode funcionar melhor.</p>
<h2>4. Fuja do canal congestionado</h2>
<p>Em prédios e ruas com muitas redes, vários roteadores podem usar o mesmo canal. Nas configurações do roteador, o canal automático costuma resolver; em alguns casos, escolher um canal menos ocupado melhora a estabilidade.</p>
<h2>5. Atualize ou troque o roteador</h2>
<p>Roteadores antigos ou muito simples não dão conta de muitos aparelhos ao mesmo tempo. Verifique se há atualização de firmware e, se o equipamento for muito antigo, um modelo com Wi-Fi 5 (802.11ac) ou Wi-Fi 6 (802.11ax) faz diferença.</p>
<h2>6. Repetidor, mesh ou cabo?</h2>
<ul>
<li><strong>Repetidor:</strong> barato, mas repete o sinal que já chega fraco e costuma reduzir a velocidade.</li>
<li><strong>Sistema mesh:</strong> vários aparelhos que formam uma rede única pela casa; mais caro, mas com cobertura bem mais uniforme.</li>
<li><strong>Ponto de acesso cabeado:</strong> um segundo aparelho ligado ao roteador por cabo. É a opção mais estável para cômodos distantes ou casas de mais de um andar.</li>
</ul>
<h2>7. Confira quem está conectado</h2>
<p>Use senha forte com WPA2 ou WPA3 e, no painel do roteador, veja a lista de aparelhos conectados. Vizinhos usando a sua rede também deixam tudo mais lento.</p>
<div class="note-box"><p><strong>Resumo:</strong> teste com cabo, mude o roteador de lugar e use 5 GHz quando estiver perto. Para cobrir a casa toda, um ponto de acesso cabeado ou um sistema mesh costuma ser melhor que o repetidor.</p></div>
''', links=[('/servicos/redes-e-wifi/', 'Redes e Wi-Fi em Itaituba')]),
 dict(slug='backup-3-2-1', titulo='Backup sem complicação: a regra 3-2-1', h1a='Backup sem complicação:', h1b='a regra 3-2-1.',
      desc='Entenda a regra 3-2-1 de backup: três cópias, dois tipos de mídia e uma fora de casa ou da empresa. Como automatizar e testar.',
      resumo='Três cópias, em dois tipos de mídia, com uma fora do local. A regra mais simples para não perder fotos, documentos e o trabalho da empresa.',
      tempo='4 min de leitura', corpo='''
<p>HD que queima, celular roubado, vírus que sequestra arquivos, notebook que cai no chão: qualquer um desses problemas vira só um susto quando existe backup. A regra 3-2-1 é a forma mais simples de organizar isso.</p>
<h2>O que é a regra 3-2-1</h2>
<ul>
<li><strong>3 cópias</strong> dos seus dados: o original e mais duas cópias.</li>
<li><strong>2 tipos de mídia</strong> diferentes, por exemplo o disco do computador e um HD externo.</li>
<li><strong>1 cópia fora do local</strong>, como um serviço de nuvem ou um HD guardado em outro endereço.</li>
</ul>
<p>Assim, um único problema (um defeito, um roubo, um incêndio) não leva todas as cópias de uma vez.</p>
<h2>O que entra no backup</h2>
<p>Documentos, fotos, planilhas, arquivos de trabalho, a base de dados dos sistemas da empresa e, quando for o caso, os e-mails. Programas e o sistema operacional podem ser reinstalados; os seus arquivos, não.</p>
<h2>Automatize</h2>
<p>Backup que depende de lembrar não acontece. Use rotinas automáticas: o Histórico de Arquivos do Windows com um HD externo, a sincronização com um serviço de nuvem ou, em empresas, um servidor ou NAS com cópia programada.</p>
<h2>Proteja contra vírus que sequestram arquivos</h2>
<p>Alguns vírus criptografam tudo o que encontram, inclusive o HD externo que estiver conectado. Por isso, mantenha pelo menos uma cópia <strong>desconectada</strong> ou com <strong>histórico de versões</strong>, que permite voltar a uma versão anterior aos arquivos danificados.</p>
<h2>Teste a restauração</h2>
<p>Um backup só vale se der para recuperar. De tempos em tempos, tente restaurar alguns arquivos para conferir que as cópias estão completas e funcionando.</p>
<div class="note-box"><p><strong>Resumo:</strong> três cópias, dois tipos de mídia, uma fora do local, tudo automático e testado de vez em quando.</p></div>
''', links=[('/servicos/seguranca-e-backup/', 'Segurança e backup em Itaituba'), ('/servicos/servidores/', 'Servidores para empresas')]),
]

for a in ARTIGOS:
    path = f"dicas/{a['slug']}/"
    crumb = [('Início', '/'), ('Dicas', '/dicas/'), (a['titulo'], None)]
    rel = ''.join(f'<li><a href="{h}">{t}{ARROW}</a></li>' for h, t in a['links'])
    others = ''.join(f'<li><a href="/dicas/{b["slug"]}/">{b["titulo"]}{ARROW}</a></li>' for b in ARTIGOS if b is not a)
    main = (hero(crumb, 'Dicas', a['h1a'], a['h1b'], a['resumo'], buttons=False, meta=f"Edelmann Tecnologia · 12 de outubro de 2026 · {a['tempo']}") +
            f'''  <section class="section" aria-label="Artigo">
    <div class="wrap">
      <article class="prose">{a['corpo']}</article>
    </div>
  </section>
  <section class="section paper" aria-labelledby="mais-titulo">
    <div class="wrap">
      <div class="head reveal"><div><p class="eyebrow">Continue</p><h2 id="mais-titulo">Leia também.</h2></div></div>
      <ul class="svc-links">{rel}{others}</ul>
    </div>
  </section>
''' + cta('Quer ajuda para resolver?', 'Olá! Li uma dica no site da Edelmann e quero ajuda.'))
    ld = [{"@type": "Article", "headline": a['titulo'], "description": a['desc'], "datePublished": "2026-10-12", "dateModified": "2026-10-12",
           "inLanguage": "pt-BR", "author": {"@type": "Organization", "name": "Edelmann Tecnologia", "url": BASE + "/"},
           "publisher": {"@type": "Organization", "name": "Edelmann Tecnologia", "logo": {"@type": "ImageObject", "url": BASE + "/img/icon-512.png"}},
           "image": BASE + "/img/og.jpg", "mainEntityOfPage": f"{BASE}/{path}"}, breadcrumb_ld(crumb, path)]
    page(path, a['titulo'] + ' | Edelmann Tecnologia', a['desc'], main, ld=ld, og_type='article')

lista = ''.join(f'''<li><a href="/dicas/{a['slug']}/"><p class="eyebrow">{a['tempo']}</p><h3>{a['titulo']}</h3><p>{a['resumo']}</p></a></li>''' for a in ARTIGOS)
page('dicas/', 'Dicas de tecnologia | Edelmann Tecnologia', 'Dicas práticas sobre computadores lentos, Wi-Fi, backup e segurança, da Edelmann Tecnologia, em Itaituba (PA).',
     hero([('Início', '/'), ('Dicas', None)], 'Dicas', 'Dicas de tecnologia', 'para o dia a dia.',
          'Explicações diretas para resolver os problemas mais comuns de computador e de rede, e para saber quando chamar um técnico.', buttons=False) +
     f'''  <section class="section" aria-labelledby="artigos-titulo">
    <div class="wrap">
      <div class="head reveal"><div><p class="eyebrow">Artigos</p><h2 id="artigos-titulo">Leituras rápidas.</h2></div></div>
      <ul class="post-list reveal">{lista}</ul>
    </div>
  </section>
''' + cta('Ficou com alguma dúvida?', 'Olá! Vim pelas dicas do site da Edelmann.'),
     ld=[breadcrumb_ld([('Início', '/'), ('Dicas', None)], 'dicas/')])
