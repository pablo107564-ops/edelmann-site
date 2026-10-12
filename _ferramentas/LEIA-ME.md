# Ferramentas do site (não publicadas: o GitHub Pages ignora pastas que começam com "_")

Cada página do site é um HTML autocontido (CSS, cabeçalho e rodapé repetidos em todas).

- `checar.py` — confere todas as páginas: links internos e âncoras, um h1 por página, títulos únicos, JSON-LD válido, ids duplicados. Rodar antes de publicar.
- `acabamento.py` — aplica em todas as páginas (idempotente): fontes locais (`/fonts`), ícones/manifest, botão flutuante do WhatsApp, links Dicas/Privacidade no rodapé, estilos extras (FAQ, formulário, artigos). Usa `fontface.css`.
- `paginas_novas.py` — gera 404, /privacidade/, as 4 páginas /servicos/<serviço>/ e /dicas/ (+3 artigos) a partir do modelo `servicos/index.html`. Conteúdo dos artigos e serviços está no próprio script.
- `paginas_existentes.py` — inseriu formulário de orçamento + FAQ em /contato/, FAQ e links em /servicos/ e /itaituba/, links no resumo do início (idempotente: não repete).

Os scripts apontam para `D:\projetos\edelmann-site`. Publicar = `git add -A && git commit && git push` (o Pages atualiza em ~1 min).
