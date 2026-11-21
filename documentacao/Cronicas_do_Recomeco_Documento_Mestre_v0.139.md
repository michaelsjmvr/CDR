# Crônicas do Recomeço — Documento Mestre v0.139

> Atualizado em: 15/11/2026 21:54:32 (UTC−03:00), v0.139.

Este é o único índice mestre ativo da documentação. Leia-o primeiro e depois
abra os guias temáticos necessários. A base integral v0.55 está preservada em
`historico/Cronicas_do_Recomeco_Documento_Mestre_v0.55.md`; as decisões e
alterações das versões v0.61–v0.139 estão consolidadas em
`09_historico_e_regras_de_documentacao.md` e nos guias temáticos.

## Como escolher o documento

| Tarefa | Documento |
| --- | --- |
| Conceito, câmera, classes, ondas, chefes, combate | [Conceito e jogabilidade](01_conceito_e_jogabilidade.md) |
| Personagens, atributos, cartas, Legado e Talentos | [Personagens e progressão](02_progressao_e_personagens.md), [decisões aprovadas](balanceamento/decisoes_aprovadas.md), [base enviada](balanceamento/base_enviada_personagens.md) e [norte adaptado](balanceamento/norte_de_balanceamento.md) |
| Equipamentos, raridades, inventário, baú, moedas e loja | [Itens, inventário e economia](03_itens_e_economia.md), [base recebida de itens](balanceamento/base_enviada_itens_mu_online.md) |
| Sala de Espera, grupos, amigos, convites, trade e PvP | [Multiplayer e recursos sociais](04_multiplayer_e_sala_de_espera.md) |
| Direção de arte, paleta, HUD, menus e acessibilidade | [Arte e interface](05_arte_e_interface.md) |
| Flask, SQLite, Socket.IO, segurança e integridade | [Arquitetura e integridade](06_arquitetura_e_integridade.md) |
| Etapas, validação, ponto de retomada e próxima etapa | [Roadmap e estado atual](07_roadmap_e_estado_atual.md) |
| Questões sem resposta e decisões que precisam de aprovação | [Pendências e decisões](08_pendencias_e_decisoes.md) |
| Bugs observados, correções e regressões a retestar | [Registro de bugs e regressões](10_registro_de_bugs_e_regressoes.md) |
| História, lore, diálogos, mapas e temporadas | [Lore, história e mapas](11_lore_historia_e_mapas.md) |
| Auditoria, fórmulas candidatas e simulações de balanceamento | [Auditoria e primeira simulação](balanceamento/auditoria_e_primeira_simulacao.md), [norte adaptado](balanceamento/norte_de_balanceamento.md) e [decisões aprovadas](balanceamento/decisoes_aprovadas.md) |
| Registro completo de versões e como atualizar a documentação | [Histórico e regras](09_historico_e_regras_de_documentacao.md) |

## Regras de manutenção

- Atualize o guia temático afetado e o roadmap quando uma implementação mudar o estado de uma tarefa.
- Registre decisões aprovadas no guia temático e no histórico.
- Mantenha apenas um arquivo versionado `Cronicas_do_Recomeco_Documento_Mestre_vX.YY.md` na raiz de `documentacao/`. Ao atualizar a versão, renomeie o arquivo mestre existente e registre as mudanças no histórico; não mantenha cópias integrais de cada versão.
- Não converta ideias em regras aprovadas sem autorização do responsável.
- Preserve o histórico antigo; não apague decisões substituídas, registre a mudança e o motivo.
- Ao iniciar uma tarefa, leia este índice, o guia indicado e os arquivos de código relacionados.
- Antes de concluir uma mudança de comportamento, adicione ou atualize testes em `tests/` e execute `python -m unittest discover -s tests -v`. Para mudanças nos scripts JavaScript do cliente, execute também `npm run test:js`. Siga `../tests/README.md`; amplie as suítes para cobrir novas áreas em vez de pedir que o responsável repita testes manuais.

## Decisão de progressão — v0.135

O responsável decidiu alterar o teto-alvo para o nível 170 e rebalancear
experiência, Pontos de Legado e combate para a campanha de 30 fases. Esta é uma
direção de design registrada, ainda pendente de implementação e validação.
Nenhuma nova fórmula ou valor de balanceamento foi aprovado.

Até a implementação, o código continua com `MAX_LEVEL = 400`. A projeção antiga
de nível 170/26 PL ao fim da Fase 30 foi calculada sob a curva anterior e não é
uma meta final aprovada para o novo teto. As simulações e E2E anteriores que
usaram checkpoints ou personagem nível 400 continuam válidos apenas como
evidência do protótipo anterior/fluxo técnico, não como validação do novo
balanceamento.

## Mapa da Fase 1 — v0.139

A arte atual do Terminal de Vilar, extraída do HTML atualizado, mede 1.200 × 896
px e é servida por
`game_app/static/images/maps/terminal_vilar_fase1.jpg`. O Canvas da missão e a
prévia `/mapas/terminal-vilar-fase1` usam essa arte no mundo lógico fixo de
2.400 × 1.800 unidades. A imagem é recortada pela câmera no jogo; a projeção da
Fase 1 não aplica uma segunda compressão vertical. A arte ainda não tem
aprovação visual nem medição de semelhança percentual.

A integração v0.139 carrega também no gameplay os efeitos de ambiente da cena:
poças/reflexos, energia animada, iluminação, névoa, oclusão e chuva. A geometria
servida por `game_app/data/maps/terminal_vilar_fase1.json` inclui 23 colisores
retangulares, 16 polígonos sólidos, quatro paredes lineares e espessura de 13
unidades. Cliente e servidor consideram essas formas para movimento e
posicionamento na Fase 1; projéteis e linha de visão não são bloqueados. São
aproximações em unidades lógicas, não pixels nem escala física aprovada.

A prévia local mantém o editor de colisores retangulares e limites de movimento
e spawn, com gravação validada e atômica no JSON, restrita a conexões locais e
protegida por CSRF. O editor visual altera os retângulos e limites; polígonos e
paredes ficam fixos no painel e precisam ser editados na configuração do mapa.
Uma partida já aberta precisa ser recarregada para aplicar valores salvos.

**Validação v0.139:** a pedido do responsável, nenhum teste, checagem de
sintaxe, build ou inspeção no navegador foi executado. As verificações
automatizadas previamente registradas para a Fase 1 correspondem à arte e à
geometria anteriores, portanto não validam a integração atual. Outras fases não
foram testadas.

**Validação histórica v0.138:** nenhum teste, checagem de sintaxe, build ou
inspeção no navegador foi executado, a pedido do responsável. O editor daquela
versão também não foi exercitado.

## Mapa da Fase 1 — estado histórico v0.136 (superado)

Na v0.136, o Terminal era desenhado proceduralmente no Canvas e todos os
elementos eram cenográficos, sem colisão. A arte final atual e os obstáculos
aproximados foram introduzidos na v0.137; os resultados antigos de testes de
desenho procedural não validam a nova composição.

## Estado histórico — v0.134 (superado quanto à direção do teto)

O retrato abaixo documenta a implementação antes da decisão v0.135. Suas
referências ao teto 400, projeção 170/26 PL e simulações até 400 não são a
direção de balanceamento vigente; o código, porém, ainda conserva o limite 400
até a implementação da mudança.

- A Temporada 1 tem 30 fases, organizadas em três atos de dez fases, com dez
  ondas por fase. A onda 10 das fases 5/15/25 é de semichefe; a onda 10 das
  fases 10/20/30 é de chefe de ato. A Fase 30 encerra a temporada: não há
  avanço para a Fase 31.
- Há nove temas visuais agrupando as fases 1–3, 4–6, 7–10, 11–13, 14–16,
  17–20, 21–23, 24–26 e 27–30. Eles reutilizam a arena lógica atual de
  2.400 × 1.800; não são nove geometrias ou mapas físicos distintos. A Fase 1
  possui uma composição visual própria; no snapshot histórico v0.134 ainda
  não tinha alterações de colisão ou gameplay. A v0.137 adiciona arte e
  colisores aproximados somente à Fase 1; as demais fases ainda usam os
  tratamentos visuais genéricos. A
  narrativa detalhada disponível cobre somente as Fases 1–10. Temas visuais
  dos Atos 2 e 3 são provisórios, sem lore aprovada.
- A simulação de XP do modelo anterior projeta o fim da Fase 30 no nível 170 e
  com 26 Pontos de Legado; é uma projeção, não uma garantia de ritmo validada.
  Naquele snapshot, o teto 400 permanecia como direção futura, mas as fases
  além da 30 ainda não eram jogáveis. A extrapolação para a fase 69/70 não
  estende a campanha nem valida o ritmo real. A direção foi substituída em
  v0.135 e o recálculo do novo alvo 170 está pendente.
- Os nomes visíveis atuais são Guerreiro, Tecelão, Lâmina Arcana e Caçador.
  Os IDs internos existentes foram preservados para compatibilidade.
- Cada classe usa sua própria habilidade-base; a habilidade assinatura pode
  substituí-la após a evolução. Se a habilidade equipada estiver em recarga
  ou sem Mana, o fallback para Ataque básico vale para qualquer classe. Corte
  Rúnico é específico da Lâmina Arcana.
- Ao excluir um personagem, perdem-se dados e itens vinculados a ele, mas o
  saldo de Ouro compartilhado pela conta permanece. A regra de exclusão do
  Baú da Conta ao remover o último personagem não apaga a carteira da conta.
- Solo é a experiência padrão. A direção aprovada permite grupos de até três
  jogadores com qualquer combinação de classes; convites, presença,
  sincronização, reconexão e balanceamento cooperativo ainda não foram
  implementados.
- A migração marca como concluídos personagens já salvos além da Fase 30 sem
  reduzir fase, onda, nível, EXP, atributos ou Pontos de Legado.
- Em v0.134, a suíte Python passou com 84 testes, `compileall` concluiu sem
  erros e `npm run test:js` passou com 10 testes em Node.js 24.20.0/Chromium.
  `scripts/simulate_live_balance.py` também foi reexecutado; os resultados são
  matemáticos e não aprovam os parâmetros.
- A simulação baseline atual (sem equipamentos, cartas ou talentos comprados)
  mede TTK de 3,5–5,2 s para comuns, 20,1–35,0 s para semichefes e 61,4–111,0 s
  para chefes nos checkpoints 1/100/220/400.
- Dificuldades encadeadas, seleção e autorização de fase no backend, contagem
  regressiva de 5 segundos, crédito de Ouro inteiro por conta, baús por raridade e
  staging de espólios estão implementados. A Sala de Espera agora apresenta um
  painel recolhível com os perfis candidatos dos quatro riscos; o aviso deixa
  claro que eles não são regras finais. O inventário-protótipo tem limite
  candidato de 30 espaços, distinto do planejamento de mochila de 16 espaços.
  O orçamento total de XP por fase continua fixo e é redistribuído pela
  quantidade/peso dos inimigos da dificuldade escolhida.
- P-048 teve E2E anterior na Fase 10: a missão foi iniciada na
  Onda 1, os inimigos das dez ondas foram derrotados por ataques Socket.IO até
  o chefe de ato, o modal exibiu tempo/recompensa/saldo e os três baús foram
  resgatados antes do retorno ao lobby. A base descartável foi pré-carregada
  com conclusão das Fases 1–9 apenas para liberar a Fase 10; o personagem de
  teste recebeu atributos elevados e o harness enviou ataques com coordenadas
  do alvo, sem validar movimento, mira manual ou equilíbrio. O resultado
  comprova o fluxo do servidor e da interface até o resgate, não uma sessão
  representativa de gameplay. Em v0.133, E2E Playwright com Flask, Socket.IO e
  bancos temporários iniciou missões nos riscos Moderado, Alto e Extremo e
  cobriu movimento por teclado, Ataque básico e dano inimigo na primeira onda;
  o teste de inventário cheio cobriu venda e resgate.
  Em v0.134, três E2E adicionais percorreram a Fase 10 inteira nos riscos
  Moderado, Alto e Extremo, da contagem até o chefe e a tela pós-fase, com
  ataques reais pelo Socket.IO. Cada execução durou aproximadamente 66–80 s e
  confirmou dano recebido de inimigos durante o combate. Para desbloquear a
  fase, o progresso anterior foi semeado; o fixture usou nível 400, atributos
  no teto de 10.000 e coordenadas de alvo fornecidas pelo harness. É validação
  integrada/prolongada do fluxo e dos eventos, não progressão natural,
  movimentação/esquiva/mira humana, sensação de jogo ou balanceamento
  representativo. A avaliação manual do jogador e aprovação dos candidatos
  continuam pendentes. Como histórico, a v0.128 trouxe
  testes determinísticos das quatro escalas de dificuldade em encontros comuns,
  semichefes e chefes, quantidade de inimigos, Ouro, chances/pesos de raridade
  e o HTML do painel com os quatro perfis no lobby; na v0.131, a suíte Python
  passou com 84 testes. A suíte JavaScript v0.130 passou com três verificações:
  sintaxe dos scripts
  próprios do cliente e dois fluxos em Chromium com Playwright (seleção de fase
  e capacidade/modal de espólios). As páginas são fixtures HTML e não carregam
  templates Flask, backend, Socket.IO ou autenticação; isso não é E2E completo
  do aplicativo. Na v0.126, o crédito e a venda usam
  Ouro inteiro na carteira da conta; os números brutos anteriores foram
  mantidos como inteiros, sem taxa
  de câmbio. A migração renomeia as colunas/tabela antigas sem alterar saldos.
  Ouro não é dinheiro real, não é conversível e não participa de pagamentos;
  futuras vendas com dinheiro real devem usar fluxo separado. E2E de fase
  completa e combate automatizado prolongado nos outros riscos foram executados;
  avaliação manual e aprovação das quantias candidatas permanecem pendentes.
  Os testes isolados de HTML não equivalem a E2E completo do aplicativo nem a
  avaliação visual manual.
- A seleção na Sala de Espera agrupa fases em Ato 1 (1–10), Ato 2 (11–20) e
  Ato 3 (21–30). O resumo “Ouro da conta · Inventário” fica na página
  `/inventario`, não como texto solto no lobby. Isso altera apenas a
  apresentação; desbloqueios e validações de acesso continuam no backend.
- O protótipo distingue **Baú de Recompensa** (espólio de missão/chefe em
  staging e inventário) de **Baú da Conta** (armazenamento compartilhado
  planejado). São funções diferentes; Baús de Recompensa não são depósitos.
- O backend permite somente uma missão ativa por conta; a reserva é verificada
  dentro da transação de início. Qualquer espólio pendente da conta bloqueia
  novo início e suspende ações de combate em outras sessões/personagens até a
  resolução. Dados legados com mais de uma run ativa liberam ação apenas para
  a run mais recente; as demais ficam pausadas, sem descarte automático.
- Os valores de dificuldade, Ouro, raridade, capacidade e venda são candidatos
  do protótipo, não decisões finais. Ouro é virtual, inteiro e compartilhado
  pela conta, sem valor real, saque ou conversão. Diálogos permanecem [PENDENTE], com hooks de início
  da missão e encontro com chefe prontos para receber JSON futuro.
- A documentação vigente foi reconciliada com a campanha finita, a cadência
  real de encontros e o novo fluxo de missão. Fases posteriores à 30 não são
  conteúdo jogável; a extrapolação para a fase 69/70 é apenas matemática.
  A onda 9 é comum; encontros especiais ocorrem na onda 10 conforme a fase.

## Atualização documental e validação — v0.134

- E2E Playwright completou a Fase 10 nos riscos Moderado, Alto e Extremo no
  Flask/Socket.IO real, do lobby ao chefe e à tela pós-fase. Progresso de
  desbloqueio foi preparado no SQLite temporário; personagem em nível 400 e
  atributos no teto de 10.000, com posição do alvo enviada pelo harness.
- Os três fluxos duraram aproximadamente 66–80 s, geraram ataques recebidos de
  inimigos e exercitaram 10 ondas e o chefe. Isso não valida progressão natural,
  controle/mira/esquiva humana, equilíbrio ou sensação de jogo.
- `npm run test:js`: 10 testes aprovados; `python -m unittest discover -s
  tests -v`: 84 testes aprovados; `python -m compileall -q game_app tests`: sem
  erros. Node.js 24.20.0 foi usado do cache local do WinGet.
- `python scripts/simulate_live_balance.py` foi reexecutado. Nos checkpoints
  1/100/220/400, TTK de comuns 3,5–5,2 s, semichefes 20,1–35,0 s e chefes
  61,4–111,0 s; 12 builds no chefe teórico da fase 70 ficaram em 64,2–99,5 s.
  O modelo de horda estacionária a 50% de acertos termina em derrota nas quatro
  classes; é um cenário de estresse, não uma sessão com movimento ativo.
- Nenhum valor de dificuldade, recompensa, raridade ou capacidade foi alterado
  ou aprovado. A validação manual de gameplay e a decisão do responsável sobre
  os candidatos continuam pendentes.

## Atualização documental e validação — v0.133 (histórico, parcialmente superado)

- Criada uma suíte E2E Playwright contra Flask/Socket.IO reais, com servidor,
  sessão e SQLite descartáveis: três riscos adicionais percorrem lobby,
  contagem e combate ativo da primeira onda; outro fluxo resolve mochila cheia
  após venda de item antigo.
- `npm run test:js`: sete testes aprovados em Node.js 24.20.0/Chromium. O
  runtime já existia no cache do WinGet, fora do PATH, e foi executado por seu
  caminho local; nenhum pacote foi instalado.
- `python -m unittest discover -s tests -v`: 84 testes aprovados;
  `python -m compileall -q game_app tests`: sem erros.
- Não houve alteração de regras ou código de gameplay. Naquele snapshot, o E2E
  de risco percorria somente a primeira onda; fase completa nos outros riscos e
  combate prolongado ainda não tinham automação. A v0.134 superou essas duas
  lacunas com E2E da Fase 10 em Moderado, Alto e Extremo. Calibração manual e
  aprovação dos parâmetros continuam pendentes.

## Implementação e validação — v0.131

- O início da missão agora serializa a verificação de run ativa e staging
  pendente na conta. Não é permitido iniciar uma segunda missão em outro
  personagem; quando já existe espólio pendente, rotas e ações de combate
  suspendem missões ativas até a resolução.
- Dois testes de regressão cobrem o bloqueio de segunda run e a suspensão de
  uma run ativa quando outro personagem tem staging pendente.
- A suíte Python v0.131 passou com 84 testes; `compileall` passou. A suíte
  Playwright v0.130 permanece aprovada com três verificações em Chromium, sem
  E2E completo da missão.
- Multiplicadores, Ouro, raridades e limite de 30 espaços permanecem candidatos,
  sem calibração em combate ativo ou aprovação. Baús continuam registros de
  protótipo, não equipamentos reais. Esta rodada não altera nem aprova esses
  valores.
- Atualizados Documento Mestre v0.131, guias de missão/economia, multiplayer,
  arquitetura, roadmap, pendências, histórico, README e `tests/README.md`.
- E2E completo em outras dificuldades, inventário cheio, gameplay
  representativo e confirmação visual manual continuam pendentes. O percurso
  da Fase 10 em navegador usou progresso pré-carregado e harness acelerado.

## Estado histórico — v0.121 (superado pelas versões v0.122–v0.134)

- Progressão contínua até o nível 400; o Reset e a proposta de nível 1000
  foram retirados. A fórmula `nível // 10 + nível // 50 + nível // 25`
  concede 64 Pontos de Legado no nível 400.
- A migração concede retroativamente os marcos do nível atual e preserva os
  pontos/talentos existentes. O campo de banco `resets` permanece apenas para
  compatibilidade e crédito dos ciclos antigos.
- Vida máxima do personagem usa base 120; a curva de Vida de inimigos comuns,
  semichefes e chefes foi ajustada por faixa de nível para aproximar o TTK das
  metas. Dano recebido cresce 0,65 por nível e as escalas param no nível
  inimigo 400. A simulação `python scripts/simulate_live_balance.py` usa os
  helpers reais de combate e progressão.
- A simulação e os testes cobrem TTK por classe nos níveis 1/100/220/400:
  comuns 3,5–5,2 s, semichefes 20,1–31,6 s e chefes 63,2–130 s. O maior tempo
  é o Tecelão contra o chefe de Fogo; foi decidido manter a resistência de 30%
  como contrajogada. Personagens iniciais suportam 6,0–6,9 golpes comuns.
- Validação executada em 15/11/2026: `python -m unittest discover -s tests -v`
  passou com 65 testes. `python scripts/simulate_live_balance.py` foi repetido
  com uma matriz adicional das 12 árvores completas no nível 400. Todas custam
  58–64 PL, dentro dos 64 ganhos; o TTK no chefe da fase 69 ficou em 57,3–128,2
  s. A Lâmina Arcana ficou 2,7 s abaixo do alvo inferior de 60 s; os três
  caminhos do Tecelão ficaram entre 119,0 e 128,2 s, dentro da exceção aprovada
  de até 130 s contra o chefe de Fogo. A prova continua matemática, sem
  equipamentos/cartas nem validação subjetiva de combate ativo.
- O modelo parado da horda é um estresse, não uma previsão de movimento: com
  50% de acertos antes da esquiva, a onda 8 mata todas as classes. Foi decidido
  manter o desafio centrado em esquiva; movimento real, tempo da horda acima da
  faixa provisória, cooperação e recompensa de endgame seguem pendentes.
- A suíte de regressão em `tests/` cobre marcos de Legado, XP, densidade e
  orçamento por fase, curvas de inimigos, TTK, sobrevivência inicial, pressão
  da horda, limite de nível e migração idempotente. Use-a como verificação
  padrão e expanda-a junto de cada sistema; não confundir aprovação matemática
  com aprovação subjetiva de equilíbrio ou apresentação visual.

- A página `/jogo/atributos` agora envia distribuição manual e alternância VIP por Socket.IO; estimativas, pontos disponíveis e efeitos de combate atualizam sem recarga. A notificação de sucesso dura cinco segundos.
- Cada ponto de Agilidade concede 0,01 ponto percentual de chance crítica e 0,01 ponto percentual de esquiva. Esses bônus se somam aos talentos, passivas e cartas, com limites de 50% e 35%; o crítico causa 1,5× de dano e a esquiva anula o ataque.
- Ao ativar a distribuição automática VIP, os pontos livres acumulados são aplicados segundo pesos por classe; novos pontos de nível seguem os mesmos pesos. Desativar mantém os atributos já gastos.
- O contador de monstros foi movido para a barra superior, junto da fase e da onda, mantendo atualização Socket.IO.
- A EXP dos orbes de cartas permanece em 25 para conta comum e foi elevada provisoriamente a 40 para Premium/VIP, após o responsável informar que a fase terminava antes de surgir oportunidade suficiente para substituir cartas.
- O prazo de ativação automática de cartas Premium/VIP passou de 20 para 10 segundos por oferta. A recomendação e a substituição automática pontuam utilidade para a classe, especialização, passiva/habilidade assinatura e raridade, preservando a coleção se a nova carta for inferior à ativa menos útil.
- O catálogo foi ampliado para 36 cartas, incluindo bônus para projéteis, dano elemental, cura de habilidades e recuperação de Mana por abate. Recomendações agora consideram também a especialização, a passiva e a habilidade assinatura já liberada; o balanceamento desses bônus segue pendente.
- A página de atributos foi reorganizada em duas colunas para desktop. O resumo distingue pontos livres do próximo ganho: mostra a EXP que falta para subir de nível e receber mais 5 pontos. A barra superior da página identifica a classe; efeitos sem implementação própria aparecem explicitamente como indisponíveis.
- Em v0.117, a prévia das habilidades supremas preserva o JSON no HTML; o resumo de combate mantém os bônus da evolução após recarga. Números decimais da página de atributos agora usam vírgula tanto na resposta inicial quanto nas atualizações Socket.IO.
- A evolução de monstros combina densidade de horda (até +4 inimigos) e dificuldade por nível: Vida e dano aumentam progressivamente até o nível inimigo 400. A EXP total continua vinculada ao orçamento fixo da fase e é repartida entre as novas quantidades de inimigos.
- A árvore v0.105 tem três caminhos exclusivos por classe e talentos únicos para cada uma das 12 especializações. As 15 habilidades supremas têm nós individuais de desbloqueio e maestria; habilidades-base e assinaturas também podem ser aprimoradas. Nove caminhos custam 58 PL, três custam 64 PL, e a soma dos 12 é 714 PL. Cada personagem escolhe um caminho; os 64 PL até o nível 400 cobrem qualquer um deles. A fórmula é `nível // 10 + nível // 50 + nível // 25`. Os talentos v0.104 comprados são reembolsados uma vez ao abrir a nova árvore; v0.102/v0.103 continuam como legado.
- Opções da partida: Teclado + Mouse ou Apenas Teclado. Em ambos, todo ataque exige comando explícito. Tecla 1 sempre usa Ataque básico; teclas 2, 3 e 4 usam, respectivamente, as magias dos espaços 1, 2 e 3. Fileira superior e Numpad têm o mesmo mapeamento.
- Em Teclado + Mouse, o personagem olha para o cursor e o painel superior mostra o monstro sob ele. Em Apenas Teclado, olha na direção do último movimento e o painel mostra o alvo assistido à frente; essa assistência não dispara ataques. Os botões esquerdo e direito do mouse podem ser vinculados às magias dos espaços 2–4 no modo Teclado + Mouse.
- Se a habilidade da classe acionada por tecla ou mouse estiver em recarga ou sem Mana, o Ataque básico é usado como fallback, calculado e validado pelo servidor. A recarga básica também é respeitada.
- Ao escolher carta com todos os espaços preenchidos (6 comum/8 Premium/VIP), o primeiro clique abre imediatamente o seletor da carta ativa que sairá, sem Tab, segundo clique ou espera pelo Socket.IO. A escolha só é persistida e validada pelo servidor antes de liberar a confirmação da troca. Cada carta ativa mostra nome, raridade e descrição do efeito atual. O botão abaixo das três cartas permite manter as ativas e descartar as opções; elas não voltam a ser sorteadas durante a mesma onda, mas podem voltar em ondas futuras se não estiverem ativas. A decisão manual funciona também no VIP; o prazo VIP só escolhe automaticamente quando o jogador não iniciou uma escolha manual.
- A migração da conta preserva as magias equipadas, compacta-as nos espaços de magia 1–3 (teclas 2–4) e remapeia os botões do mouse para esses espaços. O marcador da versão de controle impede que os atalhos personalizados sejam alterados novamente no próximo reinício.
- A arena lógica é um retângulo de 2.400 × 1.800 unidades, com início do jogador no centro (1.200, 900). Desde v0.137, a Fase 1 usa a imagem fornecida e colisores aproximados; outras fases mantêm o tratamento genérico e o fator vertical `cos(58°)`. Consulte [Arquitetura e integridade](06_arquitetura_e_integridade.md) para a fonte dos obstáculos, regras de spawn, limites e conversões. As unidades não definem escala física aprovada.
- O guia oficial [Lore, história e mapas](11_lore_historia_e_mapas.md) integra a Temporada 1, Ato 1, Fases 1 a 10, com fichas de Level Design, roteiros e diretrizes para a IA. A estrutura de atos/fases e a composição visual da Fase 1 estão no jogo; cenas e diálogos são propostas, não conteúdo implementado. As Fases 11 a 30 ainda precisam de planejamento narrativo.
- Câmera Canvas configurada em projeção oblíqua 2.5D com pitch visual de 58° para baixo a partir do horizonte; a escala vertical do piso usa cosseno do ângulo, enquanto personagens e monstros permanecem eretos. O jogador fica como foco, o scroll interpola o zoom e os limites se adaptam ao mapa/tela. É uma aproximação afim 2.5D, não uma câmera 3D com perspectiva real. Parâmetros e conversão de mira ficam em `CAMERA_CONFIG` e nas funções de conversão em `game_app/static/js/game.js`.
- Cada classe tem uma habilidade-base; as 12 evoluções têm passiva e habilidade assinatura, e o catálogo inclui 15 habilidades supremas. As maestrias aumentam apenas o dano da habilidade correspondente. Habilidades supremas usam efeitos de área, encadeamento, atração/repulsão, imobilização, defesa, crítico e invocação temporária; alvos secundários são validados pelo servidor, embora suas posições sejam simuladas pelo cliente. “Erga-se” transforma um inimigo derrotado em soldado temporário das sombras: até três aliados ajudam por três ataques cada, por até 15 s. “Poço de Inércia” atrai e prende inimigos por 1,5 s.
- A proposta anterior de ataque automático Premium/VIP (P-035) está suspensa: nenhum ataque acontece só por proximidade, direção ou alvo assistido; reabrir apenas com nova aprovação.
- Testes automatizados em `tests/test_talents_and_abilities.py` cobrem árvores e passivas, custos/atributos, desbloqueio e maestria das habilidades supremas, loadout de três espaços, limite de uma suprema, efeitos de combate, chances crítica/esquiva, prévias por classe, persistência dos bônus da evolução, reembolso v0.104 e os fluxos de compra/bloqueio/troca VIP de talento nas quatro classes. Testes Socket.IO também cobrem alocação dos quatro atributos, distribuição automática VIP, persistência de controles e substituição/manutenção de coleção VIP 8/8. A suíte atual passou com 71 testes. A nova curva entrega 64 pontos no nível 400.
- `tests/test_cards.py` cobre os novos efeitos de carta, aumento real de dano de projéteis/elementos e recomendações coerentes com habilidades e passivas; o teste de combate também confirma o bônus de cura da habilidade assinatura.
- Foi criado `10_registro_de_bugs_e_regressoes.md`, separado do índice leve, para registrar sintomas, causas/hipóteses, correções, áreas de regressão e validações manuais pendentes.
- Corrigido o botão de desativação da distribuição automática VIP, que ficava desabilitado após a primeira resposta do servidor.
- Validação manual já informada como OK: alcance por contato nas classes e com carta; conta comum sem cronômetro; sequência de ofertas VIP; movimento do chefe; HUD anterior em telas grandes e pequenas.
- Na v0.119, a E2E em conta isolada mostrou notificações de atributos, persistência de controles, movimento/zoom e os fluxos de coleção VIP 8/8. Na ocasião, E2E de talentos e ataque/fallback ainda estavam pendentes; ver a validação v0.120 abaixo.
- Corrigido em v0.120 o travamento de ataques após telegráfico sem resolução: pedidos expirados agora são removidos antes de verificar pedidos pendentes; o cliente solta estados sem ACK após timeout e ao desconectar. O Avanço atravessa inimigos para evitar cerco sem saída, e o movimento normal pode deslizar pelos eixos livres.
- No jogo, a barra do rodapé foi removida e as coordenadas X/Y permanecem no canto inferior direito. Na página de atributos, o cartão de pontos livres agora fica dentro da coluna esquerda.
- E2E em navegador isolado v0.120: a árvore do Guardião foi exercitada no nível 100; escolha de Furioso, compra de talento por 2 PL, bloqueio visual do ramo Guardião, persistência após recarga e troca VIP para Guardião com reembolso dos 2 PL foram confirmados. Em rodada complementar com banco descartável, escolha, compra, bloqueio, troca VIP com reembolso e persistência após recarga foram confirmados para as outras três classes. Em combate, a falta de Mana acionou o Ataque básico (28 de dano ao alvo) e o Avanço atravessou o cerco (X 1250 → 1406). O layout dos pontos ficou na coluna esquerda em desktop e celular; a barra inferior não existe e X/Y continua visível.
- Pendências: mira com mouse, Numpad, validação do pitch em resoluções variadas, combate ativo prolongado/balanceamento de builds e detalhes/implementação do endgame. O nível 400 não tem Reset; a campanha atual termina na Fase 30 e conteúdo posterior ainda não foi definido. A direção híbrida (marcos cosméticos/recordes e equipamentos com poder limitado) foi aprovada; falta definir slots, regras dos itens, teto de poder e cadência dos marcos.
- Prioridade visual atual: desktop. Controles adaptados para tablets e celulares serão tratados posteriormente.
- A suíte automatizada é a forma padrão de validar mudanças. Pendências sem cobertura devem virar novos testes automatizados, não tarefas repetidas de validação manual.

## Integração documental — v0.121

Em 15/11/2026, foi integrado oficialmente o guia temático de lore, história e
mapas da Temporada 1, Ato 1 (Fases 1 a 10). O guia organiza o material original
de `temporario.md`, preserva seus roteiros e fichas de Level Design, explicita
as diretrizes autorais e separa intenções narrativas de mecânicas implementadas.
O planejamento das Fases 11 a 30 permanece pendente; o Ato 2 (Fases 11 a 20)
é a primeira parte desse escopo narrativo.

## Harmonização documental — v0.123

Em 15/11/2026, foi revisada a documentação vigente após a implementação da
campanha de 30 fases. Os guias de conceito, progressão, roadmap e pendências
agora distinguem conteúdo jogável de extrapolações; a onda 10 segue a cadência
de encontro por fase, e não há fases infinitas implementadas. Resultados de
65 testes e a matriz que tratava a fase 69 como chefe permanecem apenas como
registros históricos. O Documento Mestre foi renomeado para v0.123 e os
documentos vigentes passaram a apontar para ele.

## Sistema de missões e atualização documental — v0.124 (histórico; moeda atualizada em v0.126)

Em 15/11/2026, foi implementado o fluxo protótipo de dificuldade, seleção e
conclusão de missões, moeda virtual (à época descrita como R$; especificação
superada em v0.126 por Ouro inteiro por conta), baús e resolução obrigatória dos
espólios no inventário. O backend valida progressão e acesso; valores de
balanceamento continuam candidatos. Hooks de diálogo foram adicionados com
status [PENDENTE]. A suíte completa passou com 76 testes, incluindo cinco
testes focados no sistema de missões. Smoke test manual em navegador temporário
exercitou lobby, countdown/freeze, modal e descarte de staging; a sequência
completa iniciada por abate não foi E2E. Não houve validação em combate ativo.

## Próxima retomada

1. **Revisar visualmente o Terminal de Vilar** no jogo e na prévia, em
   resoluções representativas; comparar a imagem de referência, avaliar
   escala/legibilidade e confirmar manualmente as rotas ao redor dos colisores.
   A meta subjetiva de 90% ainda não foi medida nem aprovada.
2. **Validar o núcleo jogável:** completar E2E de mira/controles no P-045 e
   testar movimento, esquiva, horda e builds em combate ativo no P-031/P-043/
   P-047; separar esses resultados das simulações.
3. **Aprovar o balanceamento de P-048:** manualmente avaliar desafio/recompensa
   e decidir os parâmetros candidatos depois do rebalanceamento da meta de
   nível 170.
4. **Planejar a narrativa restante da Temporada 1:** desenvolver Fases 11–30,
   começando pelo Ato 2 (11–20), alinhando ritmo, encontros e recompensas às
   regras atuais de progressão.
5. **Construir dependências de poder:** ampliar o inventário de staging para
   equipamentos e consumíveis persistentes, definir economia aprovada e concluir
   as regras de cooperação antes da calibração integrada.
