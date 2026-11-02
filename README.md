# Itadaki Street: Dragon Quest & Final Fantasy 30th Anniversary — Tradução PT-BR (fã)

Tradução não oficial de **いただきストリート ドラゴンクエスト＆ファイナルファンタジー 30th ANNIVERSARY** (PS Vita,
PCSG00932) para português do Brasil, feita sobre a tradução inglesa de fã
[fishyitadaki/itadakivitaeng](https://github.com/fishyitadaki/itadakivitaeng) (v1.2). Créditos da engenharia
original do patch (fonte, DLL, layout) são de lá.

- Falas de todos os personagens, menus, tutorial, cartas, descrições de mapas, músicas e museu (base + DLC de DQ11).
- Requer o jogo na **atualização 1.02**.

## Download e instalação

Baixe o `.zip` em [Releases](../../releases) e siga o `LEIA-ME.txt` dentro dele (Vita com rePatch reDux0 ou Vita3K).
Se aparecerem quadrados no lugar de letras acentuadas, use o zip `sem-acentos`.

## Estrutura

| Pasta / arquivo | Conteúdo |
|---|---|
| `pt/NNN.json` | A tradução: `{"<id>": "texto"}` |
| `tools/itd.py` | Leitura/escrita das tabelas de texto (Unity 5.4 TextAsset, UTF-16 em campos fixos) |
| `tools/extract.py` | Extrai o texto do patch inglês para `units.json` e `batches/` |
| `tools/check.py` | Valida um lote: ids, tags `<...>`, quebras de linha, tamanho do campo |
| `tools/build.py` | Gera `out/` (`--no-accents` remove acentos) |
| `BRIEF.md` | Guia de estilo, vozes e glossário |

## Gerar o patch

```
# extraia itadaki-eng-1.2-base.zip em src/base e itadaki-eng-1.2-DLC.zip em src/dlc
pip install UnityPy
python -I -X utf8 tools/extract.py
python -I -X utf8 tools/build.py        # gera out/base e out/dlc
```
