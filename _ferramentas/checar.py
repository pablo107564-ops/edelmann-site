import re,os,json,glob
os.chdir(r'D:\projetos\edelmann-site')
bad=[];titles={}
fs=[f.replace(os.sep,'/') for f in glob.glob('**/*.html',recursive=True) if 'google2e5' not in f]
for f in sorted(fs):
    s=open(f,encoding='utf-8').read(); d=os.path.dirname(f); idl=re.findall(r'id="([^"]+)"',s); ids=set(idl)
    h1=s.count('<h1')
    if h1!=1: bad.append((f,'h1=',h1))
    t=re.search(r'<title>(.*?)</title>',s).group(1); titles.setdefault(t,[]).append(f)
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
        if frag and tgt.endswith('.html') and f'id="{frag}"' not in open(tgt,encoding='utf-8').read(): bad.append((f,u))
for t,l in titles.items():
    if len(l)>1: bad.append(('titulo repetido',t,l))
print(len(fs),'paginas'); print('problemas:',bad or 'nenhum')
