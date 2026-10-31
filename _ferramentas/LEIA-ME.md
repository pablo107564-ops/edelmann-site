# Ferramentas do site (não publicadas: o GitHub Pages ignora pastas que começam com "_")

Cada página do site é um HTML autocontido (CSS, cabeçalho e rodapé repetidos em todas). Os scripts usam a pasta do próprio site (a pasta acima desta), então funcionam em qualquer cópia.

Desde outubro de 2026 o site é de **consultoria**: não lista serviços, passa credibilidade e leva o cliente a **agendar uma conversa** (presencial de Itaituba a Santarém, indo até a empresa, ou por videochamada).

- `checar.py` — confere todas as páginas: links internos e âncoras, um h1 por página, títulos únicos, JSON-LD válido, ids duplicados, e se alguma página aponta para uma página removida (as que só redirecionam são ignoradas). Rodar antes de publicar.
- `consultoria.py` — monta o site atual (idempotente: pode rodar de novo). Refaz início, Itaituba, Sobre e Contato a partir dos trechos em `consultoria/*.html` (marcadores `{{FORM_DARK}}`, `{{PROOF}}`, `{{FAQ}}` etc. ficam no script); troca menu, rodapé e chamadas de todas as páginas; põe o botão flutuante do WhatsApp com a mensagem de agendar; atualiza as datas do sitemap. Os redirecionamentos de /servicos/, /dicas/ e /setores/, os cards de /produtos/ e o restante do reposicionamento já estão nos HTML: o script não os regrava mais. Para mudar um texto ou um estilo, edite o trecho ou o script e rode de novo (os blocos de CSS marcados com `/* ===== Nome ===== */` são substituídos, não duplicados).
- O formulário de agendamento também avisa a Edelmann por e-mail, via Google Apps Script (código em `edelmann-divulgacao/notificacao/`). Trocar a URL do script é em `FORM_JS`, em `consultoria.py`.
- Contador de visitas GoatCounter (`edelmann.goatcounter.com`, sem cookies): o script está antes de `</body>` em todas as páginas (menos redirecionamentos e a política do Leitor de Bolso); as páginas novas herdam da casca (Sobre). Ao removê-lo, atualizar a /privacidade/.
- `artigos.py` — gera os 8 artigos e a lista /artigos/ (conclusão no topo, tabela, perguntas frequentes com FAQPage, "Sobre a Edelmann", "Leia também"). Os 8 artigos (texto, FAQ e as datas `publicado` e `atualizado`) ficam em `artigos_novos.json`; a ordem da lista e os "Leia também" ficam no script.
- `setores.py` — páginas de setor, com `FAQ_SETOR` (perguntas visíveis + FAQPage).
- `suporte.py` — página /suporte/ (suporte técnico e manutenção): casca de Sobre, texto em `suporte.json` (título, descrição, seções, FAQ visível + FAQPage, mensagem do WhatsApp), JSON-LD Service + BreadcrumbList e sitemap. O link "Suporte" não entra no menu do topo (quebra em duas linhas a 960px); fica no rodapé e na linha abaixo do topo da página inicial.
- `comum.py` — trechos usados por `artigos.py`, `setores.py` e `suporte.py` (casca da página nova a partir de Sobre, trilha, FAQPage, entrada no sitemap, constantes do site e do WhatsApp). Não gera nada ao ser importado.

Datas fixas: `publicado`/`atualizado` no `artigos_novos.json`; o lastmod do sitemap em `artigos.py` (lista), `setores.py` e `suporte.py` (`sitemap_add` sempre regrava a data do script, então um lastmod ajustado à mão no `sitemap.xml` se perde na próxima geração). Atualizar à mão ao mudar texto.

Ordem de geração (de uma pasta do site): `python _ferramentas/consultoria.py && python _ferramentas/artigos.py && python _ferramentas/setores.py && python _ferramentas/suporte.py && python _ferramentas/checar.py` (o `checar.py` deve terminar em "problemas: nenhum").
- `og.html` — arte da imagem de prévia (`img/og.jpg`). Gerar: Chrome sem janela em 1200x800 e recortar 1200x630 do topo.

Publicar = `git add -A && git commit && git push` (o Pages atualiza em cerca de 1 minuto).
- `indexnow.py` — depois de publicar, rodar `python _ferramentas/indexnow.py` para avisar o Bing (IndexNow) das URLs do `sitemap.xml`; páginas removidas vão como argumentos (ex.: `python _ferramentas/indexnow.py https://edelmann.com.br/cal-as`). A chave é o arquivo `<32 hex>.txt` na raiz.
