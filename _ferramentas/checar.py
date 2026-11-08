# © 2026 Edelmann Tecnologia — edelmann.com.br
# Todos os direitos reservados. Proibido copiar, modificar, distribuir ou fazer engenharia reversa
# deste código sem autorização por escrito da Edelmann Tecnologia.
import re,os,json,glob
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # pasta do site
bad=[];titles={}
fs=[f.replace(os.sep,'/') for f in glob.glob('**/*.html',recursive=True) if 'google2e5' not in f and not f.startswith('_')]
# páginas que só redirecionam (conteúdo removido): não são checadas, e nenhuma página deve apontar para elas
redir={f for f in fs if 'http-equiv="refresh"' in open(f,encoding='utf-8').read()}
fs=[f for f in fs if f not in redir]
VIS=open('_ferramentas/visual.css',encoding='utf-8').read()  # o bloco Visual tem de ser igual ao arquivo e o último do <style>
BASE='https://edelmann.com.br/'
SM=set(re.findall(r'<loc>(.*?)</loc>',open('sitemap.xml',encoding='utf-8').read()))
def url_de(f): return BASE+(f[:-10] if f.endswith('index.html') else f)  # pasta/index.html -> pasta/
for f in sorted(fs):
    s=open(f,encoding='utf-8').read(); d=os.path.dirname(f); idl=re.findall(r'id="([^"]+)"',s); ids=set(idl)
    if '<style>' in s and s.split('/* ===== Visual ===== */\n',1)[-1].split('</style>',1)[0]!=VIS: bad.append((f,'bloco Visual ausente, diferente do visual.css ou fora do fim do <style>'))
    h1=s.count('<h1')
    if h1!=1: bad.append((f,'h1=',h1))
    hs=[int(x) for x in re.findall(r'<h([1-6])[\s>]',s)]
    if any(b>a+1 for a,b in zip(hs,hs[1:])): bad.append((f,'salto de nivel de titulo',hs))
    m=re.search(r'<title>(.*?)</title>',s)
    if m: titles.setdefault(m.group(1),[]).append(f)
    else: bad.append((f,'sem <title>'))
    if f!='404.html':  # canonical e og:url têm de apontar para a própria página (as derivadas trocam por replace, que falha calado), e toda página fica no sitemap
        u=url_de(f)
        for rotulo,pad in (('canonical',r'<link rel="canonical" href="([^"]*)"'),('og:url',r'<meta property="og:url" content="([^"]*)"')):
            m=re.search(pad,s)
            if not m or m.group(1)!=u: bad.append((f,rotulo,m.group(1) if m else 'ausente','devia ser',u))
        if u not in SM: bad.append((f,'fora do sitemap.xml'))
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):
        try: json.loads(m)
        except Exception as e: bad.append((f,'jsonld',str(e)[:60]))
    if len(idl)!=len(ids): bad.append((f,'ids duplicados',[i for i in ids if idl.count(i)>1]))
    for u in re.findall(r'(?:href|src)="([^"]+)"',s):
        if u.startswith(('http','mailto:','tel:','data:')): continue
        if u.startswith('#'):
            if len(u)>1 and u[1:] not in ids: bad.append((f,u))
            continue
        path,_,frag=u.partition('#'); path=path.split('?')[0]
        tgt=path.lstrip('/') if path.startswith('/') else os.path.normpath(os.path.join(d,path))
        tgt=tgt or '.'
        if os.path.isdir(tgt): tgt=os.path.join(tgt,'index.html')
        if not os.path.exists(tgt): bad.append((f,u)); continue
        if tgt.replace(os.sep,'/') in redir: bad.append((f,u,'aponta para página removida')); continue
        if frag and tgt.endswith('.html') and f'id="{frag}"' not in open(tgt,encoding='utf-8').read(): bad.append((f,u))
for t,l in titles.items():
    if len(l)>1: bad.append(('titulo repetido',t,l))
for u in SM-{url_de(f) for f in fs}:
    bad.append(('sitemap',u,'sem página ou é redirecionamento'))
print(len(fs),'paginas,',len(redir),'redirecionamentos'); print('problemas:',bad or 'nenhum')
