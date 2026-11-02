# Brief de tradução — Itadaki Street: Dragon Quest & Final Fantasy 30th Anniversary (EN → PT-BR)

Jogo de tabuleiro (PS Vita, 2017) no estilo "Banco Imobiliário com ações": os jogadores rolam o dado, compram
lojas, investem nelas, compram ações das áreas, juntam os quatro naipes e voltam ao Castelo do Banco para subir de
nível e receber salário. Vence quem chega ao Castelo do Banco com o patrimônio-meta. Personagens de Dragon Quest e
Final Fantasy disputam as partidas e comentam tudo (provocam, comemoram, reclamam). A base é a tradução inglesa de
fã (v1.2); o texto em inglês é a referência.

## Fluxo

- Entrada: `batches/NNN.json` = `{ "<arquivo> | <quem fala>": { "<id>": "English", ... }, ... }`.
- Saída: `pt/NNN.json` = `{ "<id>": "PT-BR", ... }` — objeto plano, **todas** as ids do lote, nada a mais.
- `python -I -X utf8 tools/check.py NNN` valida. Corrigir até "0 problems".
- "quem fala" é o personagem que diz a frase (arquivos talk*/outercharacter*). Use o gênero e a voz dele.

## Preservar exatamente (o validador confere)

- Tags `<...>`: copiar idênticas. As de emoção no começo (`<通常>`, `<喜>`, `<怒>`, `<哀>`, `<考>`, `<特>`, `<激>`,
  `<黙>`, `<口止>`, `<左>`, `<右>`) ficam **no começo**, antes do texto. Variáveis: `<p>` e `<player>` = nome de um
  jogador, `<monster>`, `<n>`, `<任意文字:0>` (valor qualquer: nome, número), `<金額:0>` (quantia),
  `<プレイヤー:0>`, `<アイコン:...>` (ícone de botão), `<文字色:赤>`…`<文字色:終了>` (texto em vermelho). Coloque a
  variável na posição natural da frase em português.
- Quebras de linha `\n`: **mesmo número** que o inglês, em ponto natural. Em textos com `\n` cada linha pode ter no
  máximo ~15% a mais que a linha mais longa do inglês (as caixas são pequenas). Sem `\n` o jogo quebra sozinho.
- Caracteres NUL (`\u0000`) e espaços no começo/fim de botões (`" Buy "`): manter.
- Limite de tamanho: cada string tem um máximo fixo (o validador avisa). Mire em até ~10% a mais que o inglês;
  descrições longas (cartas, monstros) já estão quase no limite — condense sem perder informação.
- Strings só com nome próprio, número, sigla ou símbolo: copiar.
- Não resumir, não juntar, não inventar. Cada string é independente (algumas frases do tutorial são continuação da
  anterior: "The marks are: Spade" → "Os naipes são: Espadas", depois "Espadas, Copas"...).

## Estilo

- Português do Brasil natural, informal-padrão, como uma localização oficial (Nintendo/Square Enix PT-BR). Nada de
  gíria regional forte. Humor, trocadilhos e tiques de cada personagem preservados (adaptar trocadilho se precisar).
- "você" entre todos; nobres/servos: "Vossa Alteza", "Majestade", "princesa", "milady", "senhor(a)" como no inglês.
- O jogador (`<p>`) pode ser homem ou mulher: frases dirigidas a ele/ela sem adjetivo marcado ("Você tem talento",
  não "Você é talentoso"). Quando impossível, masculino.
- Falas de rival dirigidas a outro personagem (`<player>`) idem: neutro.
- Gênero de quem fala (concordância "obrigado/obrigada", "cansado/cansada"):
  - Feminino: Alena, Nera, Bianca, Maribel, Jessica, Ricka, Anlucia, Yuna, Lightning, Minfilia.
  - Masculino: Kiryl, Terry, Carver, Angelo, Nelgel, Sylvando, Golbez, Gilgamesh, Kefka, Cloud, Sephiroth, Squall,
    Zidane, Tidus, Balthier, Noctis, Torneko, Healix (slime curandeiro, apresentador), Moogle (apresentador, "kupo").
- Vozes: Kiryl (clérigo, formal, devotado à princesa Alena); Alena (princesa moleca, impulsiva, adora lutar); Nera
  (doce, gentil); Bianca (calorosa, decidida); Terry (frio, orgulhoso, espadachim); Carver (brutão, empolgado,
  "parceiro"); Maribel (mimada, mandona, língua afiada); Jessica (confiante, provocadora); Angelo (galanteador,
  irônico, ex-templário); Ricka (menina estalajadeira, educada e animada); Anlucia (princesa determinada); Nelgel
  (vilão grandioso, "insetos", arrogante); Sylvando (artista flamboyant, otimista, teatral, "querido(a)");
  Golbez (sombrio, solene); Gilgamesh (canastrão espadachim, gritado, colecionador de espadas); Kefka (palhaço
  insano, risadas, cruel e infantil); Cloud (lacônico, "Não me interessa"); Sephiroth (frio, superior, ameaçador);
  Squall (seco, "...Tanto faz."); Zidane (ladrão brincalhão, flerta com garotas); Yuna (educada, suave); Tidus
  (animado, jovem, esporte blitzball); Balthier (pirata do céu galã, "protagonista", refinado e irônico); Lightning
  (direta, fria, militar); Minfilia (gentil, serena, fala dos Scions); Noctis (príncipe preguiçoso e descontraído);
  Healix e Moogle (apresentadores animados do jogo; Moogle termina frases com "kupo" — manter "kupo").
- Interjeições: Hmph → Hmpf; Whoa → Uau; Phew/Whew → Ufa; Geez → Puxa/Credo; Damn/Dammit → Droga/Maldição;
  Ugh/Argh → Argh; Hehe, Hahaha, Ufufu, Kuku, Fufu, Kyaa, Fwah, Hyah ficam; Yeah → É!/Isso!; Alright → Certo/Beleza.

## Nomes

- Personagens, lugares, monstros, magias e itens dos jogos DQ/FF: **nome oficial em inglês** (Slime, Metal Slime,
  Cactuar, Whack, Fuddle, Zanmato, Gysahl Greens, Alexandria, Santeem, Spira, Shinra, Scions, Sin, aeon → éon).
  Lugares compostos: traduz a parte genérica, mantém o nome (Trodain Castle → Castelo de Trodain; Ghost Ship →
  Navio Fantasma; Kingdom of Lucis → Reino de Lucis; Alltrades Abbey → Abadia de Alltrades).
- Títulos e epítetos traduzem: Princess → Princesa; Your Highness → Vossa Alteza; the Destroyer → o Destruidor;
  Demon Lord → Lorde Demônio; Dragonlord fica; Legendary Hero → Herói Lendário; Warriors of Light → Guerreiros da
  Luz; Demon Lord's Darkness → Trevas do Lorde Demônio; 30th Anniversary → 30º Aniversário.
- "DQ VIII", "FF X", "From: DQ II" → "DQ VIII", "FF X", "De: DQ II".
- Nomes de lojas do tabuleiro traduzem (Item Shop → Loja de Itens; Weapon Shop → Loja de Armas; Armor Shop → Loja de
  Armaduras; Inn → Estalagem; Restaurant → Restaurante; Apothecary → Boticário; Magic Shop → Loja de Magia...).
  Nomes de bairros/distritos que são nomes próprios ficam.

## Glossário fixo

| EN | PT-BR |
|---|---|
| Itadaki Street | Itadaki Street |
| Bank Castle | Castelo do Banco |
| shop / your shop | loja / sua loja |
| shop charge(s) | taxa (da loja) / taxas |
| shop value / shop price | valor da loja / preço da loja |
| invest / investment / reinvest | investir / investimento / reinvestir |
| area | área |
| stock(s) / share(s) / shareholder / stock price | ação/ações / ação/ações / acionista / cotação |
| buy / sell stocks; stockbroker / Brokerage | comprar / vender ações; corretora / Corretora |
| dividend | dividendo |
| cash / total assets / net worth / estate | dinheiro / patrimônio total / patrimônio / imóveis |
| target / target amount | meta / valor-meta |
| bankrupt / bankruptcy | falir / falência |
| level / level up / salary / promotion | nível / subir de nível / salário / promoção |
| Spade / Heart / Diamond / Club / mark(s) | Espadas / Copas / Ouros / Paus / naipe(s) |
| Changing Mark | Naipe Coringa |
| Chance / Chance Card | Sorte / Carta da Sorte |
| Lucky / Super Lucky | Sortudo / Supersortudo |
| Vacant Lot / Land Lot | Terreno Vazio / Terreno |
| Land Office | Imobiliária |
| Checkpoint / Circus Tent / Circus / Airship / Airship Dock / Shrine / Tavern | Pedágio / Tenda de Circo / Circo / Aeronave / Doca da Aeronave / Santuário / Taverna |
| Paper / Straw / Wood / Brick / Iron / Orichalcum Shop | Loja de Papel / Palha / Madeira / Tijolo / Ferro / Oricalco |
| Grand Cross | Grand Cross |
| space / square | casa |
| Dice / Dice Square / Casino / Holiday / Magic Door / Cannon / Warp | dado / Casa do Dado / Cassino / Folga / Porta Mágica / Canhão / teleporte |
| auction / Sell Shop / Buy Shop / Swap Shop | leilão / Vender Loja / Comprar Loja / Trocar Loja |
| Relief (hand control to CPU) | Piloto automático |
| Anyone Welcome / Friends Only | Todos Bem-vindos / Só Amigos |
| Itadaki Coins / Itadaki Spotlight / Prize Exchange | Moedas Itadaki / Holofote Itadaki / Troca de Prêmios |
| Wealth Climax | Clímax da Fortuna |
| Monopoly / monopolize | Monopólio / monopolizar |
| Quick Rules / Easy Mode | Regras Rápidas / Modo Fácil |
| G (money) | G |
| CPU / the computer | CPU / o computador |
| Save / Load / Settings / Back | Salvar / Carregar / Configurações / Voltar |
| Yes / No | Sim / Não |
| 1st / 2nd / 3rd / 4th | 1º / 2º / 3º / 4º |
