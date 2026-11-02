# Instruções para o agente tradutor

Você traduz lotes da tradução PT-BR de Itadaki Street: Dragon Quest & Final Fantasy 30th Anniversary (inglês →
português do Brasil). Pasta do projeto: C:\Users\soste\Documents\itadaki-pt-br

1. Leia BRIEF.md inteiro (estilo, vozes, gênero de cada personagem, glossário, o que preservar).
2. Para cada lote NNN que recebeu: leia batches\NNN.json ({"<arquivo> | <quem fala>": {"<id>": "English"}}) inteiro
   antes de traduzir, e escreva pt\NNN.json como objeto plano {"<id>": "PT-BR"} com TODAS as ids do lote e nenhuma a
   mais. UTF-8, ensure_ascii=False, indent=1. Não toque em outros arquivos. Lote grande: escreva em partes (vários
   arquivos temporários pt\NNN.partK.json e junte num só com um script Python curto no fim; apague as partes).
3. Rode `python -I -X utf8 tools\check.py NNN` para cada lote; tem que terminar em "0 problems". Corrija e repita.
4. Responda só com: a saída final do check de cada lote e até 10 termos recorrentes novos que você fixou (EN → PT).

Regras essenciais:
- Tags `<...>` idênticas; a tag de emoção do início (`<通常>`, `<喜>`...) continua no início.
- Mesmo número de `\n`; respeite o limite de tamanho (validador avisa).
- Use a voz e o gênero gramatical de quem fala (BRIEF.md). Frases dirigidas ao jogador `<p>`: neutras quanto a gênero.
- Tradução completa e natural, sem resumir nem inventar. Nomes oficiais em inglês de personagens, lugares, monstros,
  magias e itens; termos de jogo pelo glossário.
