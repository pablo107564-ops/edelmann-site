# Avisa o Bing (IndexNow) das páginas do sitemap.xml e de URLs extras (ex.: páginas removidas, que viram 404).
# Uso, depois de publicar: python _ferramentas/indexnow.py [url_removida ...]
# A chave é o nome do arquivo <32 hex>.txt na raiz do site (o Pages precisa já estar servindo esse arquivo).
import os, re, sys, json, urllib.request, urllib.error
AQUI = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.dirname(AQUI)
HOST = 'edelmann.com.br'
chaves = [f[:-4] for f in os.listdir(SITE) if re.fullmatch(r'[0-9a-f]{32}\.txt', f)]
assert len(chaves) == 1, f'esperava 1 arquivo de chave na raiz, achei {len(chaves)}'
chave = chaves[0]
urls = re.findall(r'<loc>(.*?)</loc>', open(os.path.join(SITE, 'sitemap.xml'), encoding='utf-8').read()) + sys.argv[1:]
corpo = json.dumps({'host': HOST, 'key': chave, 'keyLocation': f'https://{HOST}/{chave}.txt', 'urlList': urls}).encode()
req = urllib.request.Request('https://api.indexnow.org/indexnow', corpo, {'Content-Type': 'application/json; charset=utf-8'})
try:
    with urllib.request.urlopen(req, timeout=30) as r: print(len(urls), 'URLs enviadas; HTTP', r.status, '(200/202 = aceito)')
except urllib.error.HTTPError as e:
    print(len(urls), 'URLs enviadas; HTTP', e.code, e.read().decode(errors='replace'))
