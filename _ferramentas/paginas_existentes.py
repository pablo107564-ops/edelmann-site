# Acrescenta formulário de orçamento, perguntas frequentes e links das páginas de serviço às páginas existentes (idempotente).
import re, os, json

SITE = r'D:\projetos\edelmann-site'
ARROW = '<svg class="i" aria-hidden="true" focusable="false"><use href="#i-arrow"/></svg>'

def rd(p): return open(os.path.join(SITE, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(SITE, p), 'w', encoding='utf-8', newline='\n').write(s)

def faq_html(qas, hid='faq'):
    items = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in qas)
    return f'''  <section class="section" id="{hid}" aria-labelledby="{hid}-titulo">
    <div class="wrap">
      <div class="head reveal"><div><p class="eyebrow">Dúvidas</p><h2 id="{hid}-titulo">Perguntas frequentes</h2></div></div>
      <div class="faq reveal">{items}</div>
    </div>
  </section>
'''

def faq_ld(qas):
    strip = lambda t: re.sub(r'<[^>]+>', '', t)
    return '<script type="application/ld+json">\n' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qas]},
        ensure_ascii=False, indent=1) + '\n</script>\n'

FAQ = [
    ('Vocês atendem em casa ou na empresa?', 'Sim. Atendemos presencialmente em residências e empresas de Itaituba. Quando o problema permite, também resolvemos a distância, com acesso remoto seguro.'),
    ('Como funciona o orçamento?', 'Você descreve o que precisa pelo WhatsApp, por e-mail ou pelo formulário; avaliamos o cenário e apresentamos a solução e o valor antes de começar. Nada é feito sem a sua aprovação.'),
    ('Atendem fora de Itaituba?', 'O atendimento presencial é em Itaituba. Para outras cidades, atendemos a distância sempre que o serviço permitir.'),
    ('Atendem empresas?', 'Sim. Além do suporte, cuidamos de redes, servidores, segurança e backup de empresas, e oferecemos sistemas como o Balcão PDV e o Agente de IA no WhatsApp.'),
    ('Qual a forma mais rápida de falar com vocês?', 'O WhatsApp (93) 98121-2924. Também respondemos pelo e-mail edelmann.tecnologia@gmail.com.'),
]

SVC_LINKS = f'''      <ul class="svc-links reveal">
        <li><a href="/servicos/formatacao-e-manutencao/">Formatação e manutenção{ARROW}</a></li>
        <li><a href="/servicos/redes-e-wifi/">Redes e Wi-Fi{ARROW}</a></li>
        <li><a href="/servicos/servidores/">Servidores{ARROW}</a></li>
        <li><a href="/servicos/seguranca-e-backup/">Segurança e backup{ARROW}</a></li>
      </ul>
'''

FORM = '''  <section class="section" id="orcamento" aria-labelledby="orcamento-titulo">
    <div class="wrap">
      <div class="head reveal"><div><p class="eyebrow">Orçamento</p><h2 id="orcamento-titulo">Peça um orçamento.</h2></div><p class="sub">Preencha e envie pelo WhatsApp ou por e-mail. Nada fica guardado no site: a mensagem sai pronta no seu aplicativo.</p></div>
      <form class="form" id="form-orcamento">
        <div class="row">
          <label>Seu nome<input name="nome" autocomplete="name" required></label>
          <label>Bairro ou cidade <small>(opcional)</small><input name="local" autocomplete="address-level2"></label>
        </div>
        <div class="row">
          <label>Serviço
            <select name="servico" required>
              <option value="">Escolha uma opção</option>
              <option>Formatação e manutenção</option>
              <option>Redes e Wi-Fi</option>
              <option>Servidores</option>
              <option>Segurança e backup</option>
              <option>Sistemas sob medida</option>
              <option>Balcão PDV</option>
              <option>Agente de IA no WhatsApp</option>
              <option>Sistema de Chamados</option>
              <option>Leitor de Bolso</option>
              <option>Outro</option>
            </select>
          </label>
          <fieldset><legend>É para</legend>
            <label><input type="radio" name="para" value="Residência" checked> Residência</label>
            <label><input type="radio" name="para" value="Empresa"> Empresa</label>
          </fieldset>
        </div>
        <fieldset><legend>Atendimento preferido</legend>
          <label><input type="radio" name="atendimento" value="Presencial"> Presencial</label>
          <label><input type="radio" name="atendimento" value="A distância"> A distância</label>
          <label><input type="radio" name="atendimento" value="Tanto faz" checked> Tanto faz</label>
        </fieldset>
        <label>O que está acontecendo ou o que você precisa<textarea name="descricao" required></textarea></label>
        <div class="actions">
          <button class="btn btn-primary" type="submit">Enviar pelo WhatsApp''' + ARROW + '''</button>
          <button class="btn btn-ghost" type="button" id="orcamento-email">Enviar por e-mail</button>
        </div>
        <p class="fine">Ao enviar, abrimos o WhatsApp ou o e-mail com a mensagem pronta para você conferir. Veja a <a href="/privacidade/">política de privacidade</a>.</p>
      </form>
      <noscript><p class="fine">Para enviar o pedido, use o WhatsApp (93) 98121-2924 ou o e-mail edelmann.tecnologia@gmail.com.</p></noscript>
    </div>
  </section>
'''

FORM_JS = '''<script>
/* Formulário de orçamento: monta a mensagem no próprio navegador e abre WhatsApp ou e-mail. */
(function(){
  var f=document.getElementById('form-orcamento'); if(!f)return;
  function msg(){
    var d=new FormData(f),l=['Olá! Quero um orçamento pela Edelmann Tecnologia.','','Nome: '+d.get('nome')];
    if(d.get('local'))l.push('Bairro/cidade: '+d.get('local'));
    l.push('Serviço: '+d.get('servico'),'Para: '+d.get('para'),'Atendimento: '+d.get('atendimento'),'','Descrição: '+d.get('descricao'));
    return l.join('\\n');
  }
  f.addEventListener('submit',function(e){
    e.preventDefault(); if(!f.reportValidity())return;
    window.open('https://wa.me/5593981212924?text='+encodeURIComponent(msg()),'_blank','noopener');
  });
  document.getElementById('orcamento-email').addEventListener('click',function(){
    if(!f.reportValidity())return;
    var a=document.createElement('a');
    a.href='mailto:edelmann.tecnologia@gmail.com?subject='+encodeURIComponent('Orçamento - '+new FormData(f).get('servico'))+'&body='+encodeURIComponent(msg());
    document.body.appendChild(a); a.click(); a.remove();
  });
})();
</script>
'''

# ---- Contato: formulário + FAQ
s = rd('contato/index.html')
if 'id="form-orcamento"' not in s:
    i = s.index('</main>')
    s = s[:i] + FORM + '\n' + faq_html(FAQ) + s[i:]
    s = s.replace('</body>', FORM_JS + '</body>', 1)
    s = s.replace('<style>', faq_ld(FAQ) + '<style>', 1)
    wr('contato/index.html', s); print('contato ok')

# ---- Serviços: links das páginas detalhadas + FAQ
s = rd('servicos/index.html')
if 'href="/servicos/redes-e-wifi/"' not in s:
    # depois da lista de serviços (primeira seção)
    i = s.index('</ul>', s.index('<ul class="services')) + len('</ul>')
    s = s[:i] + '\n      <p class="sub reveal" style="margin-top:2.5rem">Veja cada serviço em detalhe:</p>\n' + SVC_LINKS + s[i:]
    j = s.index('<section class="section band cta-band"')
    s = s[:j] + faq_html(FAQ).lstrip() + '\n  ' + s[j:]
    s = s.replace('<style>', faq_ld(FAQ) + '<style>', 1)
    wr('servicos/index.html', s); print('servicos ok')

# ---- Itaituba: links + FAQ
s = rd('itaituba/index.html')
if 'href="/servicos/redes-e-wifi/"' not in s:
    i = s.index('</ul>', s.index('<ul class="services')) + len('</ul>')
    s = s[:i] + '\n      <p class="sub reveal" style="margin-top:2.5rem">Veja cada serviço em detalhe:</p>\n' + SVC_LINKS + s[i:]
    j = s.index('<section class="section band cta-band"')
    s = s[:j] + faq_html(FAQ).lstrip() + '\n  ' + s[j:]
    s = s.replace('<style>', faq_ld(FAQ) + '<style>', 1)
    wr('itaituba/index.html', s); print('itaituba ok')

# ---- Início: itens do resumo de serviços viram links
s = rd('index.html')
MAP = {'Suporte técnico': '/servicos/formatacao-e-manutencao/', 'Redes e Wi-Fi': '/servicos/redes-e-wifi/', 'Servidores': '/servicos/servidores/',
       'Segurança': '/servicos/seguranca-e-backup/', 'Sistemas sob medida': '/produtos/', 'Backup': '/servicos/seguranca-e-backup/'}
if 'class="svc-mini-link"' not in s:
    for t, h in MAP.items():
        s = re.sub(r'<li>(<svg class="i" aria-hidden="true" focusable="false"><use href="#i-[a-z]+"/></svg>)' + re.escape(t) + '</li>',
                   lambda m: f'<li><a class="svc-mini-link" href="{h}">{m.group(1)}{t}</a></li>', s, count=1)
    s = s.replace('/* ===== Componentes extras ===== */', '/* ===== Componentes extras ===== */\n.svc-mini li{padding:0}\n.svc-mini-link{display:flex;align-items:center;gap:1rem;width:100%;padding:1.5rem 1.75rem;color:inherit;text-decoration:none;transition:background-color .2s}\n.svc-mini-link:hover{background:var(--paper)}', 1)
    wr('index.html', s); print('inicio ok', s.count('svc-mini-link'))
