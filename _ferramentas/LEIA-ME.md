# Ferramentas do site (não publicadas: o GitHub Pages ignora pastas que começam com "_")

Cada página do site é um HTML autocontido (CSS, cabeçalho e rodapé repetidos em todas). Os scripts usam a pasta do próprio site (a pasta acima desta), então funcionam em qualquer cópia.

Desde outubro de 2026 o site é de **consultoria**: não lista serviços, passa credibilidade e leva o cliente a **agendar uma conversa** (presencial de Itaituba a Santarém, indo até a empresa, ou por videochamada).

- `checar.py` — confere todas as páginas: links internos e âncoras, um h1 por página, títulos únicos, JSON-LD válido, ids duplicados, e se alguma página aponta para uma página removida (as que só redirecionam são ignoradas). Rodar antes de publicar.
- `consultoria.py` — monta o site atual (idempotente: pode rodar de novo). Refaz início, Itaituba, Sobre e Contato a partir dos trechos em `consultoria/*.html` (marcadores `{{FORM_DARK}}`, `{{PROOF}}`, `{{FAQ}}` etc. ficam no script); troca menu, rodapé e chamadas de todas as páginas; transforma Serviços (e subpáginas) em redirecionamentos para /suporte/ e Dicas em redirecionamentos para o início; põe o botão "Quero ver como funciona" nos cards de /produtos/ (os fechos de /balcao/, /agente-whatsapp/ e /chamados/ ficam só com o WhatsApp que já têm); atualiza sitemap e manifest. Para mudar um texto ou um estilo, edite o trecho ou o script e rode de novo (os blocos de CSS marcados com `/* ===== Nome ===== */` são substituídos, não duplicados).
- `acabamento.py` — aplica em todas as páginas (idempotente): fontes locais (`/fonts`), ícones e manifest, botão flutuante do WhatsApp, estilos extras (perguntas, formulário, artigos). Usa `fontface.css`.
- `artigos.py` — gera os 8 artigos e a lista /artigos/ (conclusão no topo, tabela, perguntas frequentes com FAQPage, "Sobre a Edelmann", "Leia também"). Os 5 comparativos (texto, FAQ, datas) ficam em `artigos_novos.json`; os 3 mais antigos estão no próprio script.
- `setores.py` — páginas de setor, com `FAQ_SETOR` (perguntas visíveis + FAQPage).
- `suporte.py` — página /suporte/ (suporte técnico e manutenção): casca de Sobre, texto em `suporte.json` (título, descrição, seções, FAQ visível + FAQPage, mensagem do WhatsApp), JSON-LD Service + BreadcrumbList e sitemap. O link "Suporte" não entra no menu do topo (quebra em duas linhas a 960px); fica no rodapé e na linha abaixo do topo da página inicial.

Ordem de geração (de uma pasta do site): `python _ferramentas/consultoria.py && python _ferramentas/artigos.py && python _ferramentas/setores.py && python _ferramentas/suporte.py && python _ferramentas/acabamento.py && python _ferramentas/checar.py` (o `suporte.py` roda antes do `acabamento.py`; o `checar.py` deve terminar em "problemas: nenhum").
- `og.html` — arte da imagem de prévia (`img/og.jpg`). Gerar: Chrome sem janela em 1200x800 e recortar 1200x630 do topo.

Publicar = `git add -A && git commit && git push` (o Pages atualiza em cerca de 1 minuto).
