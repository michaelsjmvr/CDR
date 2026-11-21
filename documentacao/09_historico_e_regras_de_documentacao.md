# Histórico e regras de documentação

> Guia temático iniciado a partir do Documento Mestre v0.55 e atualizado com decisões posteriores. Consulte `Cronicas_do_Recomeco_Documento_Mestre_v0.139.md` para navegar entre assuntos.
>
> Atualizado em: 15/11/2026 21:54:32 (UTC−03:00).

## 21. Histórico de versões

### v0.139 — integração da arte atualizada, efeitos e geometria da Fase 1

**Tipo:** integração na missão da nova cena recebida em
`terminal_vilar_fase1.html`; mantém o escopo exclusivamente na Fase 1.

**O que mudou:**
- A arte embutida no HTML foi extraída para
  `game_app/static/images/maps/terminal_vilar_fase1.jpg` (1.200 × 896 px) e
  conectada ao Canvas principal. A URL versionada evita reutilizar imagem antiga
  em cache.
- Os efeitos de poças/reflexos, energia animada, luzes, névoa, oclusão e chuva
  foram separados em `terminal-vilar-effects.js`, carregado antes de `game.js`.
- `terminal_vilar_fase1.json` passou a conter 16 polígonos sólidos, quatro
  paredes lineares (espessura 13) e os retângulos editáveis atuais. A validação
  e colisão do servidor em `map_geometry.py`, o cliente e a prévia usam essa
  configuração; o painel local continua editando retângulos e limites, não
  polígonos ou paredes.
- A prévia Flask foi ligada novamente ao editor e ao bridge de renderização; os
  controles de projeção ausentes foram tratados como opcionais. As asserções
  E2E existentes foram atualizadas para a dimensão atual e a interface vigente.

**Validação:** nenhum teste, checagem de sintaxe, build ou inspeção no navegador
foi executado, a pedido do responsável. As asserções atualizadas não foram
executadas e a evidência v0.137 não valida os arquivos ou a geometria desta
integração. Nenhuma outra fase foi testada.

**Seções atualizadas:** Documento Mestre v0.139, README, `tests/README.md`,
arquitetura, roadmap, pendências, lore e este histórico. A arte segue sem
aprovação visual e a meta de semelhança percentual não foi medida.

### v0.138 — editor local de colisores e limites da Fase 1

**Tipo:** ferramenta local para editar colisores e limites do Terminal de Vilar;
não amplia o escopo além da Fase 1 nem altera o tamanho-base do mundo.

**O que mudou:**
- A prévia `/mapas/terminal-vilar-fase1` ganhou o painel **Editar mapa**,
  disponível somente para conexões loopback. Permite adicionar, selecionar,
  mover, redimensionar, rotacionar e remover colisores retangulares, além de
  ajustar limites de movimento e spawn.
- `game_app/data/maps/terminal_vilar_fase1.json` passou a ser a configuração
  persistente. `map_geometry.py` valida os dados e grava por substituição
  atômica; a rota POST local exige token CSRF. As alterações atualizam os
  valores usados pelo servidor e são servidas ao cliente ao carregar a página.
- O mundo lógico permanece fixo em 2.400 × 1.800. Spawn deve ficar dentro do
  limite de movimento, que deve incluir o início do jogador (1.200, 900).
  Páginas de jogo já abertas precisam ser recarregadas.
- Ajustes de UX marcam alterações ainda inválidas como não salvas e informam
  que páginas de jogo abertas precisam ser recarregadas.

**Validação:** nenhum teste, checagem de sintaxe, build ou inspeção no navegador
foi executado, a pedido do responsável. A ferramenta foi implementada, mas
continua não validada; a cobertura v0.137 da Fase 1 refere-se ao código anterior
do mapa, não ao editor.

**Seções atualizadas:** Documento Mestre v0.138, README, `tests/README.md`,
guias de arquitetura, lore, roadmap, pendências, histórico e notas de estado
de balanceamento. Não foram executados testes de outras fases.

### v0.137 — arte de referência e colisões aproximadas na Fase 1

**Tipo:** integração da ilustração fornecida ao mapa de gameplay, colisores
aproximados e validação focada na Fase 1; não altera conteúdo de outras fases.

**O que mudou:**
- A imagem de 1.029 × 768 px foi copiada sem alteração para
  `game_app/static/images/maps/terminal_vilar_fase1.jpg`; o SHA-256 da cópia
  foi comparado com o arquivo fornecido.
- O Canvas da missão desenha a arte na proporção 4:3 do mundo lógico e não
  aplica compressão vertical 2.5D uma segunda vez. O recorte desenhado segue a
  origem e a área visível da câmera; o ajuste da imagem 1.3398:1 ao mundo 4:3
  comprime sua largura em aproximadamente 0,49%. A prévia usa a mesma arte como
  padrão e mantém a alternativa procedural.
- `game_app/map_geometry.py` tornou-se a fonte única dos proxies de colisão
  para ônibus, colunas e bancos. Movimento, navegação/spawn de inimigos e
  deslocamento de repulsão/atração respeitam esses obstáculos na Fase 1.
  Projéteis e linha de visão não são bloqueados; unidades são aproximadas e
  não representam escala física aprovada.
- Nenhuma outra fase foi testada. A imagem carregou na missão E2E e a prévia
  foi inspecionada visualmente, mas não houve revisão manual da cena de
  gameplay nem medição objetiva de semelhança percentual; a arte não está
  aprovada.

**Validação focada:** dois testes Python em `test_terminal_vilar_map.py`;
`node --check` nos scripts JavaScript alterados; dois E2E Playwright restritos
ao nome dos testes da Fase 1/prévia, incluindo a verificação do recorte de
câmera; `compileall` nos módulos Python alterados. Todos passaram. Nenhuma
suíte ampla ou cenário de outra fase foi executado.

**Seções atualizadas:** Documento Mestre v0.137, README, `tests/README.md`,
guias de conceito, arte, arquitetura, roadmap, pendências, lore e referências
vigentes do índice. P-027 continua parcial porque movimento autoritativo e
sincronização multiplayer seguem pendentes.

### v0.136 — mapa da Fase 1 integrado e prévia acessível (histórico; superado pela v0.137)

**Tipo:** snapshot histórico da integração visual do mapa do Terminal de Vilar na missão, rota de
prévia e documentação; não altera regras de combate, movimento ou balanceamento.

**O que mudou:**
- A Fase 1 usa o mapa visual Terminal de Vilar no Canvas do jogo; a plataforma
  central, o letreiro, seis ônibus, pilares, poças, postes, rachaduras, detritos
  e fendas são cenografia, sem colisões ou efeitos de gameplay.
- A rota `/mapas/terminal-vilar-fase1` serve a prévia paramétrica independente,
  com projeção 2.5D/planta e controle de grade/limites.
- A câmera, os limites do mundo, o spawn e a área lógica continuam inalterados.
  O guia de arquitetura descreve a geometria; a lore inclui instruções para
  reutilizar o `MAP_CONFIG` e editar a proposta com IA. A prévia e o
  renderizador do jogo eram implementações separadas, sem sincronização
  automática entre suas configurações. A afirmação de ausência de colisões foi
  superada na Fase 1 pela v0.137.
- P-008 passa a Parcial apenas quanto ao fluxo de uso/edição por IA deste mapa;
  a política geral de produção visual segue pendente. P-007 e a aprovação da
  arte final também continuam pendentes.

**Validação:** `npm run test:js`: 12 testes aprovados em Node.js 24.20.0 e Chromium,
incluindo E2E Flask/Socket.IO da Fase 1 (letreiro, plataforma central,
movimento e sem erros de JavaScript) e da prévia (dimensões, projeções e
depuração). A suíte Python
passou com 84 testes e `python -m compileall -q game_app tests` concluiu sem
erros. A prévia independente foi inspecionada visualmente no navegador; a
composição integrada durante gameplay não recebeu revisão visual manual, e a
arte final continua sem aprovação.

**Seções atualizadas:** Documento Mestre v0.136, README, `tests/README.md`,
guias temáticos, Roadmap, Pendências, Registro de Bugs, índice histórico e
esta entrada. Nenhuma regra de gameplay ou valor candidato foi aprovado.

### v0.135 — teto-alvo 170 e rebalanceamento pendente

**Tipo:** registro documental de direção de design; sem alteração de código,
fórmulas ou parâmetros ativos.

- O responsável decidiu que o teto-alvo será 170 e que XP, Pontos de Legado e
  combate devem ser rebalanceados para a campanha de 30 fases.
- A implementação ainda mantém `MAX_LEVEL = 400`. A projeção anterior de
  nível 170/26 PL ao fim da Fase 30 é resultado do modelo antigo, não a
  especificação final do novo teto.
- Recalcular a curva e o orçamento de XP, a concessão de PL e as escalas de
  inimigos/combate; adicionar testes e validar em gameplay representativo são
  pendências. Não há valores novos aprovados.
- Os E2E v0.134 usam nível 400 por fixture e comprovam fluxo integrado, não
  equilíbrio para o teto-alvo 170.

**Seções atualizadas:** Documento Mestre v0.135, README, `tests/README.md`,
guias temáticos, Roadmap, Pendências, Registro de Bugs, Lore, decisões
aprovadas e notas de balanceamento/referência.

### v0.134 — conclusão E2E nas dificuldades adicionais

**Tipo:** expansão da automação e atualização das evidências; sem mudança do
código de gameplay, dos valores de balanceamento ou da sua aprovação.

**O que mudou:**
- E2E Playwright completou a Fase 10 em Moderado, Alto e Extremo, da contagem
  até o chefe e a tela pós-fase, com Flask/Socket.IO e SQLite temporário reais.
  Cada execução durou aproximadamente 66–80 segundos e observou dano inimigo.
- O teste semeia desbloqueios, usa nível 400, atributos no teto de 10.000 e
  posição do alvo pelo harness. É automação integrada/prolongada do fluxo, não
  avaliação representativa com movimento, esquiva ou mira humana.
- `npm run test:js`: 10 testes aprovados; `python -m unittest discover -s
  tests -v`: 84 testes aprovados; `compileall`: sem erros.
- `scripts/simulate_live_balance.py` foi reexecutado. Os resultados continuam
  matemáticos; não foram usados para aprovar valores. Avaliação manual e
  decisão de balanceamento permanecem com o responsável.

**Seções atualizadas:** Documento Mestre v0.134, README, `tests/README.md`,
Roadmap, Pendências, Registro de Bugs, guias temáticos com referência ao índice
vigente e auditoria de balanceamento.

### v0.133 — E2E de riscos e inventário cheio (snapshot parcialmente superado)

**Tipo:** expansão da automação do cliente e documentação; sem alteração das
regras ou do código de gameplay e sem aprovação de parâmetros de balanceamento.

**O que mudou:**
- `npm run test:js` passou com sete testes em Node.js 24.20.0/Chromium. O
  runtime já existia no cache do WinGet, fora do PATH, e foi executado pelo
  caminho local; nenhum pacote foi instalado.
- Foram adicionados E2E Playwright contra Flask/Socket.IO reais usando sessão
  autenticada e SQLite temporário. Moderado, Alto e Extremo validam contagem,
  movimento por teclado, Ataque básico e dano recebido na primeira onda.
- Outro E2E começa com inventário 30/30, vende item antigo, resgata o espólio e
  confirma a ocupação atualizada. O teste prepara o contexto de missão; não
  substitui uma execução completa.
- `python -m unittest discover -s tests -v`: 84 testes aprovados;
  `python -m compileall -q game_app tests`: sem erros.
- Naquele snapshot, permaneciam pendentes fase completa nos outros riscos,
  combate prolongado e avaliação manual. Os dois primeiros pontos foram
  cobertos pela automação v0.134; a avaliação manual e aprovação de parâmetros
  continuam pendentes.

**Seções atualizadas:** Documento Mestre v0.133, README, `tests/README.md`,
Roadmap, Pendências, Registro de Bugs, guias temáticos com referência ao índice
vigente e notas de estado dos guias de balanceamento.

### v0.132 — auditoria e reconciliação documental

**Tipo:** correções de consistência documental; sem alteração de código ou
aprovação de parâmetros de balanceamento.

**O que mudou:**
- A regra de exclusão de personagem agora distingue itens/progresso do
  personagem do Ouro compartilhado pela conta.
- A descrição das ondas foi alinhada ao código: as ondas 1–9 são comuns; os
  encontros especiais ocorrem na onda 10 conforme a fase.
- O fallback de combate e os círculos de alcance deixaram de usar Corte Rúnico
  como nome genérico; a documentação agora identifica a habilidade atual da
  classe/especialização.
- E2E de talentos, pendências P-031 e totais da suíte foram reconciliados.
  Snapshots v0.126 e o Documento Mestre v0.55 receberam indicação explícita de
  estado histórico.
- O índice mestre foi renomeado para v0.132 e os links vigentes atualizados.

**Validação:** `python -m unittest discover -s tests -v`: 84 testes aprovados;
`python -m compileall -q game_app tests`: sem erros;
`python scripts/simulate_live_balance.py`: executado. O verificador encontrou
18 arquivos Markdown e nenhum link relativo quebrado. `npm run test:js` não
foi executado porque Node.js/npm não estão disponíveis nesta sessão. Não houve
E2E novo nem validação de combate ativo; esses itens permanecem pendentes.

**Seções atualizadas:** Documento Mestre v0.132, README, `tests/README.md`,
guias 01–11, Roadmap, Pendências, fontes de balanceamento v0.126 e aviso do
arquivo histórico v0.55.

### v0.131 — isolamento de missões e espólios por conta

**Tipo:** proteção de integridade para sessões simultâneas; os parâmetros de
balanceamento e as regras de itens não foram alterados.

**O que mudou:**
- O início da missão verifica, sob `BEGIN IMMEDIATE`, que a conta não tenha
  outra run ativa nem espólios pendentes. Uma segunda sessão/personagem não
  consegue iniciar uma missão concorrente.
- A aplicação só libera ações para a run ativa mais recente da conta; staging
  pendente suspende a entrada e as ações de combate em outras sessões até os
  espólios serem resolvidos. Runs antigas não são apagadas automaticamente.
- Índice por conta/status e dois testes de regressão cobrem início concorrente
  em personagens diferentes e a suspensão de uma run ativa por staging alheio.
- Multiplicadores, moeda, raridades e limite de 30 espaços seguem candidatos,
  sem aprovação ou calibração em combate ativo. Baús continuam registros de
  protótipo, não equipamentos reais.
- Atualizados Documento Mestre v0.131, guias de economia, multiplayer,
  arquitetura, roadmap, pendências, README e `tests/README.md`.

**Validação:** `python -m unittest discover -s tests -v`: 84 testes aprovados;
`python -m compileall -q game_app tests`: sem erros. A suíte Playwright
JavaScript v0.130 não foi afetada. Não houve novo E2E autenticado nem calibração
em combate ativo.

### v0.130 — testes JavaScript em Chromium

**Tipo:** ampliação da validação automatizada do cliente; sem alteração das
regras de jogo ou dos valores candidatos.

**O que mudou:**
- A suíte JavaScript foi migrada de DOM simulado para Playwright em Chromium.
  Continua verificando a sintaxe dos scripts first-party e agora executa dois
  fluxos dos scripts reais: seleção de fase por dificuldade e interação com o
  diálogo de conclusão/capacidade dos espólios.
- Os testes usam HTML mínimo, sem renderizar templates Flask ou conectar ao
  backend/Socket.IO; não são E2E completo da missão nem avaliação visual manual.
- Playwright foi adicionado como dependência de desenvolvimento, com lockfile.
  A execução requer Node.js 20 ou superior e Chromium instalado.
- Atualizados Documento Mestre v0.130, guias com links ao índice, arquitetura,
  Sala de Espera, interface, roadmap, pendências, README e `tests/README.md`.

**Validação:** `npm run test:js`: 3 verificações aprovadas em Node.js 24.20.0 e
Chromium; `python -m unittest discover -s tests -v`: 82 testes aprovados. Não
foi executado novo E2E autenticado da missão completa.

### v0.129 — testes automatizados de sintaxe e fluxos JavaScript (histórico; fluxo migrado em v0.130)

**Tipo:** infraestrutura de teste e regressões do cliente; sem alteração das
regras de jogo ou dos valores candidatos.

**O que mudou:**
- Adicionado `package.json` com comando `npm run test:js`, sem dependências
  externas, para Node.js 18 ou superior.
- A suíte valida sintaxe de todos os scripts first-party em
  `game_app/static/js/`, excluindo arquivos vendorizados, e executa dois fluxos
  dos scripts reais usando Node `vm` e DOM simulado: disponibilidade de fases
  por dificuldade e conclusão/capacidade de espólios.
- A validação automatizada não substitui E2E em navegador: não valida
  renderização, integração Socket.IO, interação visual ou gameplay.
- Atualizados Documento Mestre v0.129, guias de arquitetura, Sala de Espera,
  interface, roadmap, pendências, README e `tests/README.md`.

**Validação:** `npm run test:js`: 3 verificações aprovadas em Node.js 24.20.0;
`python -m unittest discover -s tests -v`: 82 testes aprovados. Não foi
executado novo E2E visual.

### v0.128 — cobertura dos quatro riscos e perfis no lobby

**Tipo:** ampliação da cobertura automatizada e apresentação informativa dos
parâmetros candidatos; sem alteração dos valores de balanceamento.

**O que mudou:**
- A Sala de Espera apresenta um painel recolhível com escalas de Vida/dano,
  inimigos adicionais, recompensas de Ouro e probabilidades/pesos de Baús de
  Recompensa para os quatro riscos. A interface os identifica como candidatos.
- Testes determinísticos cobrem os valores de Vida/dano em ondas comuns,
  semichefes e chefes, contagem de inimigos, Ouro por abate, bônus da fase e
  bônus de chefe, chance de terceiro baú e pesos de raridade. Também verificam
  as chances de raridade em fases comuns/semichefes e o HTML renderizado dos
  quatro perfis.
- Atualizados Documento Mestre v0.128, guias de economia, Sala de Espera,
  interface, roadmap, pendências, README e `tests/README.md`; referências dos
  demais guias apontam para o novo índice mestre ativo.
- A validação do HTML não é E2E visual em navegador nem calibração de combate.
  Fluxos completos nas outras dificuldades, visualização autenticada e
  balanceamento em jogo permanecem pendentes.

**Validação:** suíte completa com 82 testes aprovada; `python -m compileall -q
game_app tests` concluído sem erros; Pylance não encontrou erros de sintaxe nos
módulos Python alterados. Não foi realizado E2E visual autenticado nesta rodada.

### v0.127 — seleção por atos e resumo de conta no inventário

**Tipo:** ajuste de interface, apresentação de dados da conta e reconciliação
da lore com a estrutura implementada da campanha.

**O que mudou:**
- A lista de fases da Sala de Espera agora apresenta grupos separados por ato:
  Fases 1–10, 11–20 e 21–30. As opções e os bloqueios continuam seguindo o
  progresso por dificuldade validado no backend.
- A linha de saldo de Ouro e quantidade de itens foi removida do lobby e
  consolidada no topo de `/inventario`. O cartão de serviço do Inventário
  continua como link, sem repetir saldo ou ocupação.
- A lore relaciona os três atos aos nove grupos visuais configurados no código
  e diferencia estrutura/cadência implementadas de cenas, nomes de chefes e
  setores provisórios. O roteiro dos Atos 2 e 3 continua pendente; não foi
  inventada lore para apresentá-la como conteúdo existente.
- Atualizados Documento Mestre v0.127, README, testes/README, roadmap e guias
  de inventário, Sala de Espera, interface e lore.

**Validação:** `python -m unittest discover -s tests -v`: 78 testes aprovados;
`python -m compileall -q game_app tests` concluído. A verificação Pylance não
encontrou erros de sintaxe nos módulos Python alterados. O navegador integrado
redirecionou a rota para login; a interface foi verificada por testes de rota,
sem E2E visual autenticado.

### v0.126 — moeda virtual renomeada para Ouro

**Tipo:** ajuste de código e alinhamento documental; sem conversão dos valores
numéricos legados e sem aprovação de parâmetros econômicos.

**O que mudou:**
- A moeda virtual do protótipo agora é denominada **Ouro**, armazenada como
  inteiro em saldo compartilhado por conta (`users.wallet_gold`). Não há
  centavos, taxa de câmbio, saque, conversão ou integração com pagamentos reais.
- A migração renomeia as colunas legadas terminadas em `_cents` para `_gold`
  e `wallet_ledger` para `gold_ledger`, mantendo os valores inteiros existentes
  sem conversão. Os números de recompensa continuam candidatos, não aprovados.
- Crédito de missão, venda, saldo e interfaces usam Ouro; pagamentos futuros
  com dinheiro real deverão ter fluxo, ledger e apresentação separados.
- Atualizados o Documento Mestre para v0.126, README, testes/README, guias de
  economia, sala, interface, arquitetura, roadmap, pendências, bugs, lore e
  referências de balanceamento. Menções a R$ em versões anteriores são
  históricas e não representam a especificação vigente.

**Validação:** `python -m unittest discover -s tests -v`: 78 testes aprovados;
`python -m compileall -q game_app tests` concluído. A migração preservando
valores foi coberta por teste. O E2E de navegador documentado em v0.125 ocorreu
antes da troca de rótulo e não foi reexecutado; a apresentação monetária no
navegador após a mudança permanece sem validação E2E.

### v0.125 — E2E da missão e distinção entre baús

**Tipo:** validação integrada em navegador e reconciliação documental; sem
alteração de código ou de parâmetros aprovados.

**O que mudou:**
- E2E em banco descartável percorreu a Fase 10 desde a Onda 1 até a derrota
  do chefe na Onda 10, usando ataques Socket.IO reais. O modal apresentou
  duração, recompensa/saldo virtual e raridades; três Baús de Recompensa foram
  resgatados antes do retorno ao lobby.
- A base descartável teve a conclusão das Fases 1–9 pré-carregada apenas para
  liberar a Fase 10. Atributos altos e coordenadas do alvo fornecidas pelo
  harness aceleraram os combates; isso não valida progressão natural,
  movimento, mira manual, IA ou balanceamento representativo.
- A execução confirmou o fluxo integrado no navegador, não gameplay manual.
  Inventário cheio, outras dificuldades, combate humano/IA e calibração dos
  valores candidatos permanecem pendentes. A suíte v0.124 já havia passado com
  76 testes, cinco focados em P-048; a E2E não foi adicionada como teste
  automatizado da suíte Python.
- Formalizada a distinção: Baú de Recompensa é espólio de missão/chefe em
  staging e inventário; Baú da Conta é armazenamento compartilhado planejado.
  `account_stashes` existe apenas como registro-base, sem operações de
  armazenamento de itens.
- Atualizados Mestre v0.125, guias afetados, README, testes/README, bugs e
  referências de balanceamento. A versão v0.124 permanece como registro
  histórico da implementação.

**Validação:** E2E em navegador, com banco SQLite descartável, concluído na
Fase 10; saldo, run, progresso e itens conferidos no banco temporário. Nenhum
save real foi usado. Nenhum teste automatizado de código foi executado nesta
rodada documental.

### v0.124 — progressão de dificuldades e fluxo pós-missão (histórico; R$ superado em v0.126)

**Tipo:** implementação do fluxo de missões, recompensas virtuais e resolução
de espólios; atualização da documentação e do índice mestre.

**O que mudou:**
- Adicionadas migrações para dificuldade/progresso por usuário, runs de missão,
  carteira virtual em centavos, ledger idempotente, inventário simples e staging.
- O lobby passou a selecionar dificuldade/fase com bloqueio em cascata e
  validação no backend. A missão inicia com contagem de 5 segundos; ataques são
  bloqueados e cliente congela movimento/IA até o início oficial da run.
- A conclusão do último inimigo da fase fecha a run, credita a recompensa,
  salva progresso e gera baús com raridade no staging. A tela de conclusão
  apresenta tempo, valor da run e saldo virtual em modal; resgate/venda/descarte
  respeitam capacidade. O retorno ao lobby é bloqueado até resolver os espólios.
- Hooks para diálogo de início e encontro com chefe foram adicionados com
  status `[PENDENTE]`; nenhum texto/JSON de diálogo foi criado ou testado.
- Valores de multiplicadores, recompensas, pesos, vendas e capacidade de 30
  espaços são candidatos ainda sem aprovação. A moeda R$ é virtual, sem valor
  monetário real ou saque. O limite de 30 espaços não substitui os 16 espaços
  planejados para a futura mochila.
- `python -m unittest discover -s tests -v`: 76 testes aprovados. Cinco testes
  focados cobrem desbloqueio, crédito idempotente, capacidade, autorização,
  contagem regressiva e conclusão da última onda. Não foi feito E2E integral
  da missão nem calibração em combate ativo. Smoke test manual em navegador e banco
  descartáveis confirmou lobby, contagem com movimento congelado, modal de
  conclusão, descarte de staging e retorno ao lobby. A conclusão por abate
  real e o fluxo integral permanecem sem E2E.

**Seções atualizadas:** Documento Mestre v0.124, README, testes/README, guias
01–11, referências de balanceamento e este histórico.

### v0.123 — harmonização documental da campanha

**Tipo:** revisão documental, sem alteração de código ou de regras de jogo.

**O que mudou:**
- Corrigidas especificações ativas que ainda descreviam fases infinitas,
  semichefe na onda 9 ou chefe em toda onda 10. A Temporada 1 termina na Fase
  30 e só as fases 5/15/25 e 10/20/30 têm encontros especiais na onda 10.
- Sincronizados o estado de validação com 71 testes e a simulação mais recente
  das 12 builds completas no chefe teórico da fase 70 (64,2–99,5 s).
- Registros da matriz v0.119, benchmark da fase 69 e 65 testes foram mantidos
  como históricos, sem serem tratados como estado vigente.
- Atualizado o ponto de retomada para priorizar combate ativo e E2E do núcleo,
  seguido do planejamento narrativo das Fases 11–30.
- Renomeado o Documento Mestre para v0.123 e atualizados seus links vigentes.

**Validação:** em 15/11/2026, `python -m unittest discover -s tests -v`
passou com 71 testes; `python scripts/simulate_live_balance.py` foi executado.
O baseline atual ficou em 3,5–5,2 s para comuns, 20,1–35,0 s para semichefes
e 61,4–111,0 s para chefes; as 12 builds completas no chefe teórico da fase 70
ficaram em 64,2–99,5 s. São simulações, não testes de combate ativo.

**Seções atualizadas:** Documento Mestre v0.123, README, guias 01–11,
referências de balanceamento e este histórico.

### v0.122 — Temporada 1 jogável (campanha de 30 fases)

**Tipo:** implementação da campanha histórica em código e sincronização da
documentação de escopo, progressão, mapa e pendências.

**O que mudou:**
- Implementadas três atos de dez fases, dez ondas por fase, nove agrupamentos
  visuais e encontros de semichefe/chefe na cadência aprovada.
- A Fase 30 encerra a Temporada 1 sem avançar para a 31; o encerramento é
  persistido. Migrações marcam personagens já além do limite como concluídos,
  preservando seu progresso.
- A campanha projeta nível 170 e 26 Pontos de Legado ao final da Fase 30.
  Trata-se de simulação, não de validação subjetiva de ritmo.
- Atualizados os nomes visíveis das classes sem alterar seus IDs internos.
- Explicitado que a geometria permanece uma arena única; temas dos Atos 2 e 3
  são provisórios, e sua narrativa ainda não foi escrita.
- Solo permanece funcional; cooperação de até três jogadores com qualquer
  combinação de classes é direção aprovada, mas segue sem implementação.
- Incluídos testes de regressão para encerramento da Fase 30, migração de
  progresso além do limite e nomes de classes.
- `python -m unittest discover -s tests -v`: 71 testes aprovados.
- `python scripts/simulate_live_balance.py`: as 12 builds completas ficaram
  em 64,2–99,5 s contra o chefe teórico da fase 70, sem equipamento/cartas.
- Smoke test em navegador, com banco descartável: classe visível, lobby
  informando corretamente que cooperação está em desenvolvimento e tela de
  conclusão da Fase 30 persistida após recarga; sem erros JavaScript de página.

**Seções atualizadas:** Documento Mestre v0.122, README, guias 01, 02, 04–11,
decisões aprovadas e referências de balanceamento.

### v0.121 — 15/11/2026

**Tipo:** integração documental da lore, história e mapas da Temporada 1.

**O que mudou:**
- Criado `11_lore_historia_e_mapas.md` com os dez mapas, fichas de Level
  Design, roteiros e diálogos do Ato 1.
- Registradas diretrizes de tom, quebra da quarta parede, ficcionalização e
  compatibilidade obrigatória entre história, XP, níveis e balanceamento.
- A documentação distingue explicitamente o material de Level Design e as
  mecânicas narradas do estado implementado no protótipo.
- O Documento Mestre foi atualizado para v0.121 e aponta as Fases 11 a 20
  como próxima etapa de planejamento.

**Impacto no projeto:** nenhuma mecânica, recompensa ou regra de progressão foi
alterada; conteúdo de jogo e propostas de balanceamento ainda exigem aprovação
e validação próprias.

**Seções atualizadas:** Documento Mestre v0.121, guia de lore, README, guias
temáticos 01–10 (referência à versão ativa) e este histórico.

### v0.120 — 15/11/2026

**Tipo:** correção de telegráficos de inimigos travados, fluxo de fuga de
cerco, ajustes na HUD e validação E2E de talentos/combate.

**O que mudou:**
- Ataques inimigos expirados são removidos antes da checagem que bloqueava
  novos pedidos; o cliente libera pedidos sem resposta após timeout e ao
  desconectar.
- Avanço agora atravessa inimigos e o movimento normal desliza pelo eixo livre.
- Removida a barra inferior da tela do jogo; coordenadas X/Y continuam visíveis.
  Cartão de pontos livres movido para a coluna esquerda da página de atributos.
- `python -m unittest discover -s tests -v`: 65 testes aprovados.
- E2E isolado confirmou compra/bloqueio/persistência/troca VIP de talento no
  Guardião, fallback de Ataque básico sem Mana, dano e fuga com Avanço.
- Nesta rodada, E2E em navegador com banco descartável confirmou os mesmos
  fluxos de escolha, compra, bloqueio, troca VIP com reembolso e persistência
  após recarga nas outras três classes.
- A geometria atual da arena foi documentada a partir do código: dimensões
  lógicas, limites, spawn, adornos, colisões, alcances e projeção 2.5D. A
  manutenção da documentação foi formalizada como obrigação para agentes de IA.

**Impacto no projeto:** o BUG-015 tem correção e teste de regressão; a validação
em save real ainda fica pendente. P-042 foi validado no navegador para as quatro
classes, sem incluir calibração de magnitudes. P-045
continua pendente para mira por mouse, Numpad e pitch em resoluções variadas.
P-003 registra direção híbrida aprovada pelo responsável: títulos/cosméticos e
recordes, mais equipamentos com poder limitado. A implementação foi adiada
porque inventário/equipamentos ainda não existem e faltam definir slots, limites
de atributos, cadência e conteúdo das recompensas.

**Seções atualizadas:** Documento Mestre v0.120, README, `AGENTS.md`, conceito,
arte e interface, arquitetura, roadmap, pendências, registro de bugs e este
histórico.

### v0.119 — 15/11/2026

**Tipo:** E2E de notificações, controles/câmera e cartas; matriz completa de
talentos e progressão.

**O que mudou:**
- A suíte passou com 63 testes. Foram acrescentados testes de persistência das
  opções de controle, troca e manutenção de coleção VIP 8/8, além de uma
  regressão de balanceamento para os 12 caminhos completos no nível 400.
- No navegador, os avisos de alocação manual e automática de atributos foram
  exibidos. O modo de controle, espaços e botões persistiram após recarga;
  movimento alterou Y de 900 para 779 em 450 ms, e o zoom alcançou os limites
  1,6 e aproximadamente 0,932 na viewport de teste.
- Coleção VIP 8/8: substituição e manutenção manual foram feitas no navegador,
  mantiveram oito cartas e persistiram após recarga.
- O simulador inclui as 12 árvores completas. Todos os caminhos custam 58–64
  dos 64 PL disponíveis; o TTK no chefe da fase 69 ficou em 57,3–128,2 s.
  Lâmina Arcana ficou 2,7 s abaixo do alvo inferior de 60 s; os três caminhos
  do Tecelão ficaram entre 119,0 e 128,2 s, abaixo da exceção aprovada de 130 s.

**Impacto no projeto:** validações visuais solicitadas foram executadas em
navegador e os resultados de servidor ficaram repetíveis. A simulação identificou
um desvio pequeno na Lâmina Arcana; nenhum parâmetro foi alterado sem validação
de builds intermediárias, itens/cartas e combate ativo.

**Seções atualizadas:** Documento Mestre v0.119, roadmap, pendências,
auditoria de balanceamento e este histórico.

**Pendências criadas ou resolvidas:** P-041 visual e P-046 fluxo 8/8 concluídos;
ataques/mira/fallback, E2E de talentos no navegador, revisão do TTK da Lâmina
Arcana, validação em combate ativo e recompensas de endgame permanecem abertos.

### v0.118 — 15/11/2026

**Tipo:** automação integrada dos fluxos de talentos e atributos.

**O que mudou:**
- A suíte completa passou com 59 testes; os três novos testes cobrem os fluxos
  de talentos e atributos solicitados.
- Compra de talento, bloqueio de ramo, recusa de troca sem o benefício
  especial, troca VIP com reembolso e persistência após nova consulta foram
  automatizados para as quatro classes.
- Socket.IO foi validado para Força, Agilidade, Vitalidade e Energia, incluindo
  efeitos no resumo de combate, mensagens, eventos de atualização e erros por
  saldo insuficiente.
- Distribuição automática VIP foi validada para as quatro classes, incluindo
  pesos por classe, ativação/desativação, persistência e recusa sem VIP.

**Impacto no projeto:** os fluxos de integração do servidor deixam de depender
apenas de validação manual. Ainda faltam E2E de navegador para a apresentação
visual das notificações, fluxos de controles/cartas e validação de equilíbrio
em jogo.

**Seções atualizadas:** Documento Mestre v0.118, roadmap, pendências e este
histórico.

**Pendências criadas ou resolvidas:** automação de servidor para os fluxos
solicitados concluída; E2E visual, controles/cartas, equilíbrio e endgame
permanecem pendentes.

### v0.117 — 15/11/2026

**Tipo:** validação integrada de talentos, atributos, controles/câmera e cartas;
correção de localização pt-BR no resumo de combate.

**O que mudou:**
- A suíte completa passou com 56 testes. O simulador de balanceamento não foi
  repetido porque esta rodada não alterou fórmulas ou parâmetros de combate.
- No navegador, foram validados para o Guardião a escolha de evolução no nível
  100, compra de talento, bloqueio dos outros ramos e troca VIP com reembolso
  de 2 Pontos de Legado.
- A alocação de Força atualizou o dano estimado de 31,0 para 31,5 em tempo real;
  o mesmo valor persistiu após recarga. A câmera aproximou com a rodinha e WASD
  moveu o personagem durante a preparação.
- Uma carta foi substituída numa coleção VIP 8/8 e persistiu após recarga; a
  recomendação de uma oferta posterior foi ativada automaticamente pelo prazo
  VIP, mantendo oito cartas.
- O resumo de combate passou a usar vírgula decimal na resposta inicial e nas
  atualizações Socket.IO. Regressões cobrem a prévia de habilidades supremas e
  a preservação dos bônus da evolução após recarga.

**Por que mudou:** o responsável pediu a validação integrada dos fluxos pendentes
antes de receber a lista atualizada do que falta.

**Impacto no projeto:** os fluxos exercitados estão documentados como validação
manual; isso não substitui automação repetível de navegador nem validação de
combate ativo, cooperação ou balanceamento subjetivo.

**Seções atualizadas:** Documento Mestre v0.117, roadmap, pendências, registro
de bugs e este histórico.

**Pendências criadas ou resolvidas:** alocação manual, substituição VIP 8/8,
escolha automática VIP e uso básico de movimento/zoom foram validados
manualmente. Persistem testes E2E automatizados, fluxos para todas as classes,
movimento em combate ativo, cooperação e balanceamento de endgame.

### v0.116 — 15/11/2026

**Tipo:** registro das validações automatizadas de progressão, combate e
habilidades supremas.

**O que mudou:**
- Executada novamente a suíte completa: 55 testes aprovados.
- Executado `scripts/simulate_live_balance.py`: TTK medido de 3,5–5,2 s para
  inimigos comuns, 20,1–31,6 s para semichefes e 63,2–130 s para chefes nos
  marcos 1/100/220/400.
- A simulação estacionária confirmou que a horda mata todas as classes quando
  parada; isso é estresse, não validação de movimento.
- Atualizados os estados de P-031, P-043 e P-047, mantendo pendentes combate
  ativo, cooperação, integração web/VIP e recompensas de endgame.

**Por que mudou:** o responsável pediu executar as validações antes de atualizar
a lista do que falta fazer.

**Impacto no projeto:** resultados automatizados e limites do que demonstram
foram registrados sem declarar validados fluxos que não foram exercitados.

**Seções atualizadas:** Documento Mestre v0.116, roadmap, pendências e este
histórico.

**Pendências criadas ou resolvidas:** regressões automatizadas e simulação
determinística executadas sem falhas; P-031/P-043/P-047 continuam parciais
enquanto faltarem validação em movimento ativo, builds e endgame.

### v0.115 — 15/11/2026

**Tipo:** integração das habilidades supremas à Árvore de Talentos, ao loadout
e ao combate; rebalanceamento da curva de Pontos de Legado.

**O que mudou:** - As 12 especializações receberam desbloqueio e maestria
individuais para suas 15 habilidades supremas; habilidades-base e assinaturas
também têm nós de maestria. - O loadout aceita até três habilidades disponíveis,
com no máximo uma suprema, e o servidor valida os espaços. - Efeitos de área,
encadeamento, atração/repulsão, imobilização, defesa e crítico supremos foram
integrados ao combate. - “Erga-se” transforma um inimigo derrotado em soldado
temporário das sombras que auxilia os próximos ataques. - O custo passou a 58
ou 64 PL por caminho (714 PL somando as 12
especializações); a fórmula `nível // 10 + nível // 50 + nível // 25` concede
64 PL no nível 400. - A interface chama essas habilidades de “supremas”, em
português do Brasil. - “Erga-se” convoca até três sombras por três ataques
cada (máximo de 15 segundos); “Poço de Inércia” imobiliza alvos por 1,5 segundo.

**Por que mudou:** o responsável pediu que todas as habilidades pudessem ser
equipadas e aprimoradas por talentos, sem exigir Reset, com custo que permita
concluir qualquer especialização no nível máximo.

**Impacto no projeto:** o jogador pode evoluir uma habilidade desbloqueada sem
comprar todas as outras; o saldo ao nível 400 cobre qualquer caminho individual.
A migração retroativa é idempotente e preserva saldos superiores ao mínimo.

**Seções atualizadas:** progressão, arquitetura, roadmap, pendências,
`tests/README.md` e Documento Mestre v0.115.

**Pendências criadas ou resolvidas:** P-023 permanece parcialmente pendente
para integração web/VIP e validação em fluxo completo. Os testes direcionados
das habilidades passaram; a suíte completa terminou com 55 testes aprovados.
O simulador de balanceamento também foi executado; o cenário de horda parada
continua sendo uma prova de estresse, conforme P-031/P-047.

### v0.114 — 15/11/2026

**Tipo:** atualização das cartas para integrar habilidades, passivas e atributos
de combate recentes.

**O que mudou:** - O catálogo passou de 32 para 36 cartas, adicionando bônus
para dano de projéteis e elemental, recuperação de Mana por abate e cura de
habilidades. - As recomendações agora consideram a especialização, a passiva e
a habilidade assinatura liberada. - A cura concedida por habilidades é aplicada
no combate pelo servidor.

**Por que mudou:** - O responsável pediu que as cartas acompanhassem as novas
habilidades, passivas e efeitos de combate.

**Impacto no projeto:** - Novas cartas estão conectadas às fórmulas e eventos
reais de combate. Os valores ainda aguardam calibração de equilíbrio.

**Seções atualizadas:** - Seções 6.3, 18 e 20; `tests/README.md`.

**Pendências criadas ou resolvidas:** - P-022 continua parcialmente pendente
para calibração e validação em partida. Testes automatizados cobrem os novos
efeitos e recomendações.

### v0.27 --- 13/11/2026

**Tipo:** correção da validação incompatível com o ímã dos orbes.

**O que mudou:** - Removida a comparação entre a posição local do orbe atraído e a posição original salva no banco. A coleta continua limitada a orbes não coletados pertencentes ao personagem ativo.

**Por que mudou:** - O ímã move o orbe apenas no cliente; o servidor comparava com a posição original persistida, causando a mensagem mesmo após a atração.

**Impacto no projeto:** - Corrige o falso erro. A validação de distância real depende de movimentação autoritativa no servidor, ainda não implementada no protótipo.

**Seções atualizadas:** - Seções 1, 18.1 e 21.

**Pendências criadas ou resolvidas:** - Causa corrigida; validação manual pendente. A tentativa da v0.26 foi registrada como falha para não ser repetida.

### v0.26 --- 13/11/2026

**Tipo:** correção da coleta dos orbes e ajuste da atração magnética.

**O que mudou:** - A validação de proximidade usa agora a posição do orbe
após o ímã atraí-lo, eliminando a discrepância com a posição do personagem
em movimento. - A velocidade de atração aumenta conforme o orbe se aproxima.

**Por que mudou:** - O responsável relatou que correr enquanto o orbe era
atraído causava uma mensagem de distância incorreta ao coletá-lo e pediu
absorção mais rápida.

**Impacto no projeto:** - Coleta e atração continuam via Socket.IO; requer
validação manual no navegador.

**Seções atualizadas:** - Seções 1, 18.1 e 21.

**Pendências criadas ou resolvidas:** - A validação manual desta correção
permanece pendente.

### v0.25 --- 13/11/2026

**Tipo:** atualização em tempo real do protótipo e inclusão de pets e
montarias no escopo planejado.

**O que mudou:** - Adicionado Socket.IO ao servidor e ao cliente local. -
Coleta de orbes, atualização da EXP, escolhas/substituições de cartas e
conclusão simulada de ondas passam a atualizar a sala sem recarregá-la. -
Orbes recebem atração suave quando o personagem se aproxima. - Registrados
pets como companheiros e montarias como recurso de deslocamento, com regras
específicas ainda pendentes.

**Por que mudou:** - O responsável pediu comunicação em tempo real para
evitar recarregar a página ao coletar orbes, solicitou uma atração leve e
incluiu pets e montarias no escopo do jogo.

**Impacto no projeto:** - `python app.py` passa a iniciar por Socket.IO;
dependência Flask-SocketIO e cliente JavaScript compatível são adicionados.
Eventos ainda precisam de validação manual no navegador. Pets e montarias
estão planejados, sem implementação de gameplay.

**Seções atualizadas:** - Seções 1, 9.3, 16, 18, 18.1, 20 e 21.

**Pendências criadas ou resolvidas:** - A validação de Socket.IO e atração
de orbes permanece aberta. Criada P-024 para definir tipos, obtenção,
habilidades e efeitos de pets e montarias.

### v0.24 --- 13/11/2026

**Tipo:** mudança no ritmo de aquisição de cartas temporárias e início da
coleta de orbes de EXP.

**O que mudou:** - Substituída a oferta automática de cartas a cada onda por
orbes coletáveis que enchem a barra de EXP da coleção. - Ao completar 100
EXP, o jogador recebe uma oferta de 3 cartas para adicionar ou substituir;
cada orbe concede 25 EXP no protótipo. - Confirmado que cartas não terão
níveis individuais. - Implementada persistência de EXP, escolhas pendentes,
orbes por personagem e desenho/coleta de orbes no cenário.

**Por que mudou:** - O responsável pediu que as cartas não precisassem ser
adicionadas ou trocadas ao final de toda onda e definiu que EXP coletável
deve liberar a escolha.

**Impacto no projeto:** - Valores de EXP e posicionamento dos orbes são
provisórios. O fluxo aguarda validação manual; cartas ainda não aplicam
efeitos ao combate.

**Seções atualizadas:** - Seções 1, 6.3, 18, 18.1, 20 e 21.

**Pendências criadas ou resolvidas:** - P-022 continua parcialmente
pendente para validação manual, aplicação dos efeitos e balanceamento.

### v0.23 --- 13/11/2026

**Tipo:** descrição das cartas ativas e registro de validação da
progressão.

**O que mudou:** - Adicionada descrição acessível ao passar o mouse ou
focar uma carta ativa; ela explica seu efeito. - Registrado que o
responsável testou e validou a exibição/manutenção/troca das cartas e a
subida de nível.

**Por que mudou:** - O responsável solicitou a explicação do efeito ao
inspecionar uma carta e informou que validou o fluxo de cartas e nível.

**Impacto no projeto:** - A descrição usa o texto do catálogo. Os efeitos
continuam sem aplicação mecânica até a implementação de atributos e
combate.

**Seções atualizadas:** - Seções 1, 6.3, 18.1 e 21.

**Pendências criadas ou resolvidas:** - Fluxo de cartas e subida de nível
marcados como validados pelo responsável. A interação de tooltip foi
implementada e aguarda validação manual.

### v0.22 --- 13/11/2026

**Tipo:** protótipo de Árvore de Talentos por classe.

**O que mudou:** - Criadas quatro árvores originais, uma para cada classe,
cada qual com três trilhas ramificadas e nós com pré-requisitos. - A nova
tela mostra saldo de Pontos de Legado, custos, efeitos, conexões e estado
de cada nó. - Compras são protegidas por sessão/CSRF, validadas no
servidor e persistidas no personagem. - Adicionado acesso à árvore pelo
topo da sala.

**Por que mudou:** - O responsável pediu uma árvore com navegação visual
de ARPG, inspirada na legibilidade de Diablo IV, mas usando classes,
atributos e vantagens próprias do projeto.

**Impacto no projeto:** - A árvore muda conforme a classe vinculada ao
personagem. Os custos de 1/2/3 Pontos de Legado e os efeitos são valores
iniciais de protótipo; efeitos ainda não modificam atributos ou combate.
Como a recompensa de fim de partida (P-003) não está definida, contas
atuais podem não ter pontos para comprar nós. Nenhum saldo artificial foi
adicionado.

**Seções atualizadas:** - Seções 1, 3.2, 6.4, 15.1, 18, 19, 20 e 21.

**Pendências criadas ou resolvidas:** - Criada P-023 para integração e
balanceamento dos efeitos e definição de redistribuição/reembolso. A
interface e persistência por personagem estão prototipadas.

### v0.21 --- 13/11/2026

**Tipo:** primeira simulação de progressão, ondas e cartas.

**O que mudou:** - Criados módulos separados para catálogo/sorteio de
cartas e progressão provisória. - A conta recebe 3 ofertas de cartas por
onda, pode ativar uma, manter até 6 (padrão) ou 8 (Premium/VIP), e pode
substituir uma carta ativa ou recusar a troca. - O catálogo inicial tem
30 cartas com raridade e descrições de efeitos. - A conclusão simulada
de onda concede experiência e avança até a quinta onda, tratada como
chefe de teste; concluir essa onda inicia a próxima fase.

**Por que mudou:** - Iniciar a próxima etapa definida no painel e tornar
testáveis a progressão, a coleção e as regras de Reset já decididas.

**Impacto no projeto:** - Fórmulas de experiência e 5 ondas por fase são
valores provisórios. Não há inimigos nem combate real; o botão de concluir
onda simula o resultado. Os efeitos das cartas ainda são descritivos e
não mudam atributos ou habilidades. O Reset pode ser alcançado na
simulação, mas precisa de validação manual.

**Seções atualizadas:** - Seções 1, 5, 6.1, 6.3, 18, 19, 20 e 21.

**Pendências criadas ou resolvidas:** - Implementada primeira versão de
progressão e ofertas; P-004 permanece aberto sobre o número final de
ondas. P-022 tem catálogo prototipado e aguarda integração/balanceamento
dos efeitos. Combate e XP real por inimigo continuam pendentes.

### v0.20 --- 13/11/2026

**Tipo:** retorno de cartas não ativas ao sorteio.

**O que mudou:** - Cartas não escolhidas e cartas removidas por
substituição podem aparecer em ondas futuras, desde que não estejam
ativas na coleção. - Mantida a regra contra duplicatas na oferta atual e
na coleção ativa.

**Por que mudou:** - O responsável definiu a política de retorno das
cartas ao sorteio.

**Impacto no projeto:** - O conjunto pode continuar oferecendo escolhas
ao longo da progressão infinita sem permitir cópias simultâneas da mesma
carta na coleção.

**Seções atualizadas:** - Seções 1, 6.3, 19 e 21.

**Pendências criadas ou resolvidas:** - Resolvida a política de retorno
ao sorteio em P-022. Falta criar o catálogo inicial de pelo menos 30
cartas com seus efeitos e raridades.

### v0.19 --- 13/11/2026

**Tipo:** regras de raridade, unicidade e duração da coleção temporária.

**O que mudou:** - Definidos pesos iniciais: Comum 50%, Incomum/Mágico
25%, Raro 14%, Excelente 7%, Épico/Ancestral 3% e Lendário/Mítico 1%.
- A coleção de cartas é removida ao encerrar a partida. - As 3 cartas
oferecidas na mesma onda são distintas e não se pode ativar uma segunda
cópia de uma carta que já esteja ativa.

**Por que mudou:** - O responsável delegou o balanceamento inicial dos
pesos e definiu que a coleção é temporária e não deve ter cartas iguais.

**Impacto no projeto:** - A regra de retorno ao sorteio ainda aguardava a
decisão do responsável, registrada depois em v0.20. O conjunto inicial
de pelo menos 30 cartas ainda precisa ser criado.

**Seções atualizadas:** - Seções 1, 6.3, 18, 19, 20 e 21.

**Pendências criadas ou resolvidas:** - Pesos de raridade e limpeza ao fim
da partida definidos. P-022 continua parcial para retorno ao sorteio e
catálogo de cartas.

### v0.18 --- 13/11/2026

**Tipo:** regra de substituição de cartas ativas.

**O que mudou:** - Quando a coleção está cheia, o jogador escolhe uma
carta das 3 ofertas e depois pode escolher uma carta ativa para
substituir. - A substituição é opcional; se recusá-la, a coleção
permanece igual e a nova carta não é ativada.

**Por que mudou:** - O responsável definiu como tratar a escolha de cartas
quando todos os espaços ativos estão ocupados.

**Impacto no projeto:** - O limite de coleção não é ultrapassado e o
jogador mantém controle sobre suas cartas ativas. A interface ainda será
implementada com o sistema de cartas.

**Seções atualizadas:** - Seções 1, 6.3, 19 e 21.

**Pendências criadas ou resolvidas:** - P-022 parcialmente resolvida;
comportamento de coleção cheia definido. Sorteio e persistência no fim da
partida continuam pendentes.

### v0.17 --- 13/11/2026

**Tipo:** definição das cartas temporárias da partida.

**O que mudou:** - Registrado que cada onda oferece 3 cartas sorteadas e
o jogador ativa 1 na coleção temporária. - A coleção comporta 6 cartas
ativas em contas padrão e 8 em Premium/VIP. - A biblioteca inicial terá
no mínimo 30 cartas distintas, com efeitos em atributos/habilidades e
raridade visível pela escala de 6 níveis existente.

**Por que mudou:** - O responsável definiu a escolha de melhorias por
cartas, limites ativos, tamanho mínimo da biblioteca e exibição de
raridade.

**Impacto no projeto:** - O sistema ainda não foi implementado. A regra
de Reset já remove as melhorias temporárias; a implementação futura deve
limpar também a coleção ativa. Probabilidades de raridade, repetições,
escolhas com coleção cheia e comportamento ao fim da partida continuam
em aberto.

**Seções atualizadas:** - Seções 1, 6.3, 12, 18, 19, 20 e 21.

**Pendências criadas ou resolvidas:** - Criada P-022, parcialmente
definida. Conteúdo do conjunto inicial (30 cartas) está especificado;
detalhes do sorteio e do limite ativo permanecem pendentes.

### v0.16 --- 13/11/2026

**Tipo:** preparação técnica do Reset.

**O que mudou:** - O modelo SQLite foi preparado para experiência,
fase/onda, Ouro, Pontos de Legado e melhorias temporárias. - Adicionada a
confirmação do Reset, disponível apenas a partir do nível 400; a rota
revalida o nível no servidor e transaciona a alteração. - O Reset mantém
a fase e o Ouro, volta à primeira onda da fase, retorna ao nível 1 com
experiência zero, incrementa o contador de Resets e remove melhorias
temporárias.

**Por que mudou:** - Aplicar as regras definidas pelo responsável e
preparar a integração com o sistema de progressão.

**Impacto no projeto:** - O protótipo atual não tem ganho de experiência,
combate, ondas ou chefes; portanto, ainda não é possível chegar ao nível
400 nem validar manualmente o Reset completo. A concessão de Pontos de
Legado permanece aguardando P-003.

**Seções atualizadas:** - Seções 1, 18.1 e 21.

**Pendências criadas ou resolvidas:** - Implementação do Reset iniciada
(parcial). A progressão e validação manual continuam pendentes.

### v0.15 --- 13/11/2026

**Tipo:** definição das regras centrais do Reset e da progressão por
fases.

**O que mudou:** - Definido que a progressão de fases é infinita e que
cada fase termina em chefe; derrotá-lo avança à fase seguinte. - No
Reset, o personagem volta ao nível 1 com experiência reiniciada, mantém
a fase atual e retorna à primeira onda dela; melhorias temporárias são
perdidas. - Ouro, equipamentos e demais itens persistentes permanecem
com o personagem. - Os Resets contribuem para Pontos de Legado usados na
Árvore de Talentos para atributos e vantagens permanentes.

**Por que mudou:** - O responsável definiu o comportamento do Reset, a
persistência do Ouro e o uso dos Pontos de Legado.

**Impacto no projeto:** - P-002 foi resolvida no nível de regras. A
implementação depende da base de experiência, níveis, fases, ondas e
chefes. Quantidade de ondas por fase permanece em P-004; fórmula e
quantidade dos Pontos de Legado permanecem em P-003.

**Seções atualizadas:** - Seções 1, 5, 7, 11, 18, 19, 20 e 21.

**Pendências criadas ou resolvidas:** - P-002 concluída. P-003 e P-004
continuam pendentes.

### v0.14 --- 13/11/2026

**Tipo:** validação do fluxo de troca de personagem e avanço do ponto de
retomada.

**O que mudou:** - Registrado que o responsável validou a tela de seleção
e o botão **Trocar Personagem**. - Atualizado o painel para iniciar a
definição das regras do Reset (P-002), preservando o que já está decidido
sobre persistência de itens.

**Por que mudou:** - O responsável confirmou o funcionamento e autorizou
seguir para a próxima etapa.

**Impacto no projeto:** - A próxima implementação de gameplay depende de
fechar as regras ainda pendentes do Reset.

**Seções atualizadas:** - Seções 1, 18.1 e 21.

**Pendências criadas ou resolvidas:** - Fluxo de troca validado. P-002
permanece pendente até a definição do comportamento de partida e do
benefício permanente.

### v0.13 --- 13/11/2026

**Tipo:** retorno à seleção de personagens a partir da sala.

**O que mudou:** - Adicionado o botão **Trocar Personagem** ao topo da
sala, com estilo alinhado à paleta. - O botão abre a seleção da conta sem
encerrar a sessão; outro personagem pode ser selecionado e iniciado pelo
botão **Jogar**.

**Por que mudou:** - O responsável solicitou uma forma de trocar de
personagem depois de entrar no jogo.

**Impacto no projeto:** - A rota existente de seleção mantém a sessão e
continua protegida pela autenticação. O responsável validou manualmente o
fluxo com troca de personagem.

**Seções atualizadas:** - Seções 1, 15.1, 18.1 e 21.

**Pendências criadas ou resolvidas:** - Implementado e validado pelo
responsável.

### v0.12 --- 13/11/2026

**Tipo:** atualização da interface de seleção de personagens.

**O que mudou:** - A tela foi reorganizada em três zonas sobre cenário
noturno. - A área central mostra uma prévia SVG grande com animação idle,
caixa translúcida com os dados do personagem e botão **Jogar**. - O painel
à direita lista slots verticais, destaca o ativo com Bronze `#B48A3E`,
exibe nível/classe/Resets, apresenta a criação em slot livre e posiciona
**Deletar** e **Voltar** na parte inferior. - O layout também se adapta a
telas estreitas.

**Por que mudou:** - Implementar a composição visual solicitada pelo
responsável, respeitando a paleta já aprovada no documento.

**Impacto no projeto:** - A seleção continua a usar o fluxo e os dados já
implementados. A prévia é provisória e aguarda avaliação visual no
navegador; não substitui a arte final das classes. **Voltar** encerra a
sessão e retorna à tela de acesso enquanto não há menu principal.

**Seções atualizadas:** - Seções 15.1, 18.1 e 21.

**Pendências criadas ou resolvidas:** - Layout visual implementado, falta
validação manual. P-021 permanece parcialmente pendente para arte final,
regras de nome e progressão.

### v0.11 --- 13/11/2026

**Tipo:** implementação do fluxo de personagens.

**O que mudou:** - Criadas rotas e armazenamento de personagens por conta.
- Após login, o jogador passa à tela de personagens; pode criar com nome
globalmente disponível, escolher uma das quatro classes, selecionar,
jogar e deletar. - Cartões exibem retrato provisório, nome, classe, nível
e quantidade de Resets. - Aplicados limites de 4 personagens padrão e 6
Premium/VIP. - Adicionada confirmação de exclusão com aviso diferente
quando se trata do último personagem. - Criado registro de Baú da Conta
que permanece com personagens ativos e é removido junto ao último.

**Por que mudou:** - Implementar o fluxo definido pelo responsável e
refletir as regras de limite e exclusão no protótipo.

**Impacto no projeto:** - O novo fluxo está implementado, mas aguarda
validação manual do responsável. - Os nomes são globalmente únicos como
premissa inicial; regras finais de nomes, arte de retrato e persistência
de nível/Resets permanecem pendentes.

**Seções atualizadas:** - Seções 1 (Controle do documento), 4.1
(Personagens), 10.2 (Baú), 12 (Premium/VIP), 15.1 (UI/UX), 18 (Etapas e
painel), 19 (Pendências), 20 (Decisões consolidadas) e 21 (Histórico).

**Pendências criadas ou resolvidas:** - P-021 parcialmente resolvida;
modelo e fluxo básico implementados. - Aguardando validação manual antes
de marcar a tarefa como concluída.

### v0.10 --- 13/11/2026

**Tipo:** definição de regras de personagens e autorização do próximo
fluxo de implementação.

**O que mudou:** - Definido limite de 4 personagens por conta padrão e 6
por conta Premium/VIP. - Definido o aviso e a perda de dados vinculados
ao deletar qualquer personagem. - Definido que o Baú da Conta permanece
com pelo menos um personagem ativo e é perdido ao deletar o último.
- Registrado que após login o jogador seleciona/cria personagem e usa
**Jogar** para entrar na sala. - Atualizada a próxima tarefa para
implementação do modelo e tela de personagens.

**Por que mudou:** - Incorporar as regras informadas pelo responsável e
deixar o fluxo pronto para implementação sem perder as decisões sobre
persistência da conta e do baú.

**Impacto no projeto:** - O cadastro/login passa a encaminhar para a tela
de personagens. - A conta permanece separada dos personagens; deletar o
último personagem remove o baú e os dados associados, após confirmação.
- O nome globalmente único é uma regra provisória do protótipo.

**Seções atualizadas:** - Seções 1 (Controle do documento), 4.1
(Personagens), 10.2 (Baú), 12 (Premium/VIP), 15.1 (UI/UX), 18 (Etapas e
painel), 19 (Pendências), 20 (Decisões consolidadas) e 21 (Histórico).

**Pendências criadas ou resolvidas:** - P-021 parcialmente resolvida;
limite e regra de exclusão definidos. - Permanecem pendentes nomes,
persistência de nível/Resets, arte dos retratos, troca de classe e
expiração Premium/VIP.

### v0.9 --- 13/11/2026

**Tipo:** registro de proposta de seleção e gestão de personagens.

**O que mudou:** - Registrada a proposta de mostrar a seleção de
personagens após o login. - Incluídos os fluxos de criar, selecionar,
jogar e deletar, e os dados do cartão: retrato, nome, classe, nível e
quantidade de Resets. - Reconfirmado que o Baú da Conta é compartilhado
entre personagens. - Criada a pendência P-021 para limites, nomes,
exclusão e persistência.

**Por que mudou:** - Registrar a ideia do responsável e separar os
detalhes que precisam ser definidos antes de implementar um fluxo que
cria e exclui dados persistentes.

**Impacto no projeto:** - A tela proposta passa a ser o próximo item de
planejamento. - A exclusão deve respeitar a regra existente de persistência
de equipamentos, Ouro e joias. - Nenhum código de personagens foi
implementado nesta atualização.

**Seções atualizadas:** - Seções 1 (Controle do documento), 4.1
(Seleção e criação), 15.1 (UI/UX), 18 (Etapas e painel), 19 (Pendências)
e 21 (Histórico de versões).

**Pendências criadas ou resolvidas:** - P-021 criada. - P-001 continua
resolvida; P-002 permanece pendente para a etapa seguinte.

### v0.8 --- 13/11/2026

**Tipo:** validação de funcionalidades e definição das classes iniciais.

**O que mudou:** - Registrado que o responsável testou e aprovou cadastro,
login, logout, bloqueio de `/jogo` sem sessão e movimentação. - Definidas
quatro classes iniciais: Guardião do Umbral, Tecelão de Cinzas, Vigia do
Ermo e Lâmina Rúnica, baseadas nos arquétipos solicitados pelo
responsável. - Atualizado o painel para indicar P-002 (Reset) como próxima
decisão.

**Por que mudou:** - Incorporar o resultado dos testes do responsável e
registrar os arquétipos e nomes das classes autorizados por ele.

**Impacto no projeto:** - P-001 foi concluída. - A implementação de
classes no jogo permanece pendente; atributos e habilidades continuam
sem definição.

**Seções atualizadas:** - Seções 1 (Controle do documento), 4 (Classes),
18 (Escopo e painel), 19 (Pendências), 20 (Decisões consolidadas) e 21
(Histórico de versões).

**Pendências criadas ou resolvidas:** - P-001 resolvida. - P-002 passa a
ser a próxima decisão de projeto.

### v0.7 --- 13/11/2026

**Tipo:** validação de protótipo e preparação da próxima decisão.

**O que mudou:** - Registrado que o responsável testou e aprovou o fluxo
de cadastro, login e movimentação. - Marcadas essas entregas como
concluídas no roteiro. - Mantidos logout e proteção de `/jogo` sem sessão
como implementados, mas ainda sem confirmação. - Adicionada à Seção 4
uma proposta de quatro classes iniciais, claramente identificada como
não aprovada. - Atualizado o ponto de retomada para a decisão P-001.

**Por que mudou:** - Refletir o teste feito pelo responsável e preparar
uma proposta concreta para a primeira pendência de definição do jogo,
sem transformar a proposta em decisão oficial.

**Impacto no projeto:** - A próxima decisão é aprovar ou revisar os nomes
e arquétipos propostos para as classes. - Nenhuma classe deve ser
implementada antes dessa aprovação.

**Seções atualizadas:** - Seções 1 (Controle do documento), 4 (Classes),
18 (Escopo e painel), 19 (Pendências) e 21 (Histórico de versões).

**Pendências criadas ou resolvidas:** - P-001 recebeu uma proposta e
aguarda decisão do responsável. - Nenhuma pendência foi encerrada.

### v0.6 --- 13/11/2026

**Tipo:** expansão do acompanhamento e do processo de continuidade.

**O que mudou:** - Criado o painel de andamento da Seção 18.1 com itens
implementados, em andamento, não validados e próximos passos. - Adicionada
uma legenda uniforme para os estados das tarefas. - Registrado que a
correção e reorganização recentes ainda precisam ser iniciadas e
validadas. - Definido que cada sessão de trabalho deve deixar atualizado
o ponto de retomada.

**Por que mudou:** - Manter uma visão clara do que já foi feito, do que
falta, do que está em curso e da próxima ação, permitindo retomar o
projeto sem reconstruir o contexto pelas conversas.

**Impacto no projeto:** - O painel da Seção 18.1 passa a ser o resumo
operacional prioritário; a Seção 19 continua sendo a lista oficial de
decisões pendentes.

**Seções atualizadas:** - Seções 1.1 (Uso do documento), 18 (Escopo por
etapas), 18.1 (Painel de andamento), 21 (Histórico de versões) e 23
(Instrução permanente).

**Pendências criadas ou resolvidas:** - Nenhuma decisão P-001 a P-020 foi
fechada. - Foi explicitado o próximo passo de validação manual no painel.

### v0.5 --- 12/11/2026

**Tipo:** correção e organização da estrutura do projeto.

**O que mudou:** - Corrigido o erro de indentação que impedia o servidor
Flask de iniciar. - Separado o código em módulos para autenticação,
banco de dados, segurança e rotas do jogo. - Movidos templates e arquivos
estáticos para pastas próprias. - Atualizado o README com a estrutura e
as instruções de execução.

**Por que mudou:** - Corrigir o erro reportado e facilitar manutenção,
localização de funcionalidades e futuras atualizações.

**Impacto no projeto:** - O ponto de entrada permanece `app.py`; as
funcionalidades agora vivem em `game_app/`. - O banco e a chave de sessão
locais são criados em `game_app/instance/`.

**Seções atualizadas:** - Seções 1 (Controle do documento) e 21
(Histórico de versões).

**Pendências criadas ou resolvidas:** - Nenhuma pendência de gameplay ou
arquitetura para produção foi fechada.

### v0.4 --- 12/11/2026

**Tipo:** expansão do protótipo e início da autenticação.

**O que mudou:** - Criada uma página inicial com formulários de login e
cadastro. - Adicionado servidor Flask com rotas de autenticação e acesso
à sala protegido por sessão. - Criado armazenamento local SQLite para
usuários; senhas são armazenadas usando hash. - Adicionadas validação
básica, tokens CSRF, opção de sair e arquivos de execução/dependências.

**Por que mudou:** - O responsável definiu que o usuário deve entrar ou
criar uma conta antes de acessar o jogo.

**Impacto no projeto:** - A sala de movimentação agora é servida em
`/jogo` somente após autenticação. - SQLite é usado apenas como escolha
provisória deste protótipo. - A implementação não resolve ainda
recuperação de senha, proteção contra tentativas automatizadas,
permissões ou requisitos de produção.

**Seções atualizadas:** - Seções 1 (Controle do documento), 16.3
(Banco de dados), 16.5 (Segurança e integridade), 18 (Escopo por etapas)
e 21 (Histórico de versões).

**Pendências criadas ou resolvidas:** - P-009 permanece pendente; a
autenticação e o modelo final de contas também continuam pendentes para
produção.

### v0.3 --- 12/11/2026

**Tipo:** autorização de implementação e início de protótipo.

**O que mudou:** - O responsável autorizou explicitamente o início do
desenvolvimento nesta conversa. - Criado um protótipo de navegador com
uma sala visual de teste, movimentação por teclado e câmera que acompanha
o personagem. - Canvas 2D foi usado como escolha técnica provisória do
protótipo.

**Por que mudou:** - Iniciar a etapa prática do projeto com o primeiro
item previsto no escopo do protótipo, preservando como pendentes as
decisões de gameplay que ainda não foram aprovadas.

**Impacto no projeto:** - A Etapa 3 está em andamento. - A escolha entre
Canvas e WebGL para o jogo continua pendente; a implementação atual não
fecha essa decisão. - Não foram definidos classe, combate, inimigos,
ondas ou balanceamento.

**Seções atualizadas:** - Seção 1 (Controle do documento), Seção 18
(Escopo por etapas) e Seção 21 (Histórico de versões).

**Pendências criadas ou resolvidas:** - Nenhuma pendência P-001 a P-020
foi fechada.

### v0.2 --- 12/11/2026

**Tipo:** nova decisão e expansão de UI/UX.

**O que mudou:** - Adicionada a tabela oficial de **6 níveis de raridade e cores de borda** (Comum, Incomum/Mágico, Raro, Excelente, Épico/Ancestral e Lendário/Mítico) aplicável a todos os itens (armaduras, armas, asas, anéis, colares/pendentes, joias e consumíveis). - Definida a separação visual entre a **borda externa do slot** (indica raridade) e o **brilho interno / aura sobre o ícone** (indica nível de aprimoramento `+0` a `+11+`). - Atualizada a paleta de cores na Seção 14.2 e as regras de slots/tooltips na Seção 15.2.

**Por que mudou:** - Evitar ambiguidade visual entre a raridade base de um item e seu nível de aprimoramento, garantindo leitura rápida no inventário, baú e drops no chão.

**Impacto no projeto:** - Padroniza o design de interface (Tailwind CSS) de todos os slots de equipamentos, mochila, baú, loja, forja e janela de trade.

**Seções atualizadas:** - Seção 1 (Controle do documento), Seção 8 (Itens, equipamentos, raridades e aprimoramentos), Seção 14.2 (Paleta de cores), Seção 15.2 (Slots e tooltips), Seção 18 (Etapa 1) e Seção 20 (Decisões consolidadas).

**Pendências criadas ou resolvidas:** - Nenhuma pendência da tabela P-001 a P-020 foi fechada; nova diretriz visual incorporada como **Definido**.

### v0.1 --- 12/11/2026

**Tipo:** consolidação inicial do planejamento.

**O que foi feito:** - Reunidas as ideias enviadas em uma estrutura
única. - Removidas repetições sobre Reset, ondas, itens persistentes,
inventário, direção de arte e tecnologias. - Separadas decisões já
informadas de propostas e assuntos ainda pendentes. - Organizados os
sistemas em seções para facilitar futuras atualizações. - Criada uma
lista de pendências identificadas. - Criado um roteiro inicial de etapas
do projeto.

**Por que foi feito:** - Evitar que informações importantes fiquem
espalhadas em conversas. - Reduzir contradições e repetição de
contexto. - Permitir que futuras conversas consultem este documento como
referência central. - Evitar que uma IA trate ideias ainda não aprovadas
como funcionalidades confirmadas.

**O que não foi feito:** - Nenhum código foi implementado. - Nenhum
banco de dados foi criado. - Nenhuma arte ou sprite foi produzido. -
Nenhuma decisão pendente foi tomada em nome do responsável pelo projeto.

------------------------------------------------------------------------

## 22. Modelo para próximas atualizações

Sempre que uma nova decisão for tomada, registrar neste formato:

### vX.Y --- DD/MM/AAAA

**Tipo:** nova decisão / correção / expansão / remoção.

**O que mudou:** - Descrever objetivamente a alteração.

**Por que mudou:** - Registrar o motivo da decisão.

**Impacto no projeto:** - Informar quais sistemas, regras ou etapas
foram afetados.

**Seções atualizadas:** - Listar as seções alteradas.

**Pendências criadas ou resolvidas:** - Informar os IDs correspondentes.

------------------------------------------------------------------------

## 23. Instrução permanente para futuras sessões

Antes de continuar o projeto, consultar a versão mais recente deste
Documento Mestre.

**Obrigação de entrega:** documentação é parte do trabalho, não um extra
opcional. Antes de alterar comportamento, fórmulas, dados, arquitetura ou UX,
ler o Documento Mestre e os guias temáticos envolvidos. Na mesma tarefa,
atualizar os documentos afetados sempre que houver mudança de comportamento,
bug, decisão, regra, parâmetro, teste, validação, risco, status ou próxima ação.
Isso vale também para correções pequenas e validações sem alteração de código.

Ao final de cada tarefa, conferir a coerência entre a fonte técnica, o guia
temático, o Roadmap, Pendências, Registro de Bugs e Documento Mestre, conforme
o impacto real; não copiar conteúdo para documentos sem relação. Registrar
separadamente implementação, teste automatizado, simulação, E2E, validação
manual e balanceamento. Não transformar evidência de uma categoria em prova de
outra nem marcar como concluído o que ainda não foi exercitado.

Atualizar data e hora (UTC−03:00) em cada documento modificado. Distinguir
decisões aprovadas de parâmetros candidatos e retratos históricos; ao mudar o
estado atual, marcar as afirmações antigas como superadas em vez de deixá-las
parecer vigentes. Se uma regra conflitar com outra, consultar as fontes mais
recentes e pedir decisão quando não houver evidência suficiente. Não declarar
teste, leitura ou validação que não tenha sido executado.

Ao final da sessão, atualizar a seção de retomada do Documento Mestre para
registrar o que foi concluído, o que continua em andamento, o que falta, o
estado de validação e a próxima ação concreta. Só marcar uma tarefa como `[x]`
quando estiver concluída e validada; usar `[~]` para código implementado ou
trabalho em andamento que ainda precise de validação ou conclusão. Manter o
histórico de versões atualizado quando o estado do projeto ou uma decisão mudar.

Agentes de IA devem tratar também as instruções de [`AGENTS.md`](../AGENTS.md)
como requisitos obrigatórios do projeto.

Ao receber uma nova ideia: 1. Verificar se ela já existe no documento.
2. Se já existir, complementar ou corrigir sem duplicar. 3. Se for nova,
identificar a seção correta. 4. Se houver conflito, explicar o conflito
e pedir decisão antes de substituir uma regra definida. 5. Atualizar a
seção correspondente. 6. Atualizar o histórico de versões e a lista de
pendências, quando aplicável. 7. Entregar a versão completa e atualizada
do arquivo `.md` quando for solicitada uma atualização do documento.

**Este documento representa o estado atual do planejamento, não uma
autorização automática para iniciar a implementação.**



### v0.28 --- 13/11/2026

Iniciado o combate básico: inimigos persistidos por personagem/onda, colisão local para impedir atravessá-los, ataque por Espaço e concessão provisória de 35 EXP por derrota. Vida 100 e dano 35 são parâmetros de teste. Convivência/colisão entre jogadores permanece sem implementação porque o protótipo ainda não possui salas de partida/multiplayer (Etapa 5). A primeira parte aguarda validação manual.



### v0.29 --- 13/11/2026

Avanço automático de onda após derrotar o último inimigo via Socket.IO; inimigos seguintes são carregados sem recarregar a página. Removido o botão de conclusão manual. A transição aguarda validação do responsável. Valores de combate e XP continuam provisórios. Colisão entre jogadores permanece futura, condicionada ao multiplayer.\r\n


### v0.30 --- 13/11/2026

Corrigida a inicialização de inimigos: a sala verifica inimigos vivos, não apenas registros existentes, e restaura o grupo da onda atual se todos estiverem derrotados mas a onda não tiver avançado. Assim, reiniciar o servidor não deixa uma onda vazia. Compilação Python aprovada; validar no navegador.



### v0.31 --- 13/11/2026

A coleta Socket.IO de orbes agora é idempotente: requisições simultâneas para um orbe já coletado retornam sucesso silencioso, evitando aviso vermelho em abas/eventos concorrentes. Compilação Python aprovada; aguarda validação manual.



### v0.32 --- 13/11/2026

HUD provisória de Vida/Mana e barra de duas habilidades do guerreiro adicionadas. Ataque básico e habilidades usam Socket.IO; servidor valida mana e cooldown. Dano causado aparece sobre inimigos e contato com inimigos reduz Vida e mostra dano recebido. Valores de combate são provisórios e aguarda validação manual.



### v0.33 --- 13/11/2026

Corrigida a HUD de Vida/Mana: as larguras das barras agora são renderizadas a partir dos valores persistidos do personagem, em vez de iniciar visualmente em 100%. A persistência no servidor já existia; após recarga, a apresentação estava incorreta. Compilação Python e templates verificados.



### v0.34 --- 13/11/2026

Regras registradas: Vida zerada retorna o personagem à onda 1 mantendo a fase; monstro deve mostrar nome e nível; mudança de onda/fase recebe destaque central; capítulos narrativos a cada 10 fases, com história específica por classe; missões, conquistas e bestiário de eliminações; autopotion de Vida/Mana posicionadas nas laterais da barra de combate. Histórias, missões, conquistas e bestiário ficam planejados para implementação futura. Autopotões estão representadas visualmente como controles de protótipo.


### v0.35 --- 13/11/2026

**Tipo:** controle de direção por mouse no combate.

**O que mudou:** o personagem agora gira para acompanhar o cursor; ataques
e habilidades selecionam um inimigo próximo alinhado à mira. WASD e setas
continuam movimentando o personagem. Os textos de controle foram
atualizados.

**Por que mudou:** o responsável definiu que o personagem deve olhar para
onde o jogador aponta e usar habilidades nessa direção.

**Impacto no projeto:** implementado no cliente do protótipo. O ataque
continua emitido ao servidor por Socket.IO; alcance e seleção direcional
são parâmetros provisórios do cliente.

**Seções atualizadas:** Seções 1, 15.4, 18.1 e 21.

**Pendências:** validar visualmente a direção e a seleção dos ataques no
navegador.


### v0.36 --- 13/11/2026

**Tipo:** atualização dos controles do combate.

**O que mudou:** botão esquerdo do mouse executa o ataque básico; botão
direito usa Corte Rúnico. Impacto do Umbral, a terceira ação de combate
da barra, foi removido. Movimento continua em WASD/setas e o mouse mantém
a mira.

**Por que mudou:** o responsável definiu os botões do mouse como controles
de ataque e pediu a remoção da terceira habilidade.

**Impacto no projeto:** controles aplicados na sala de combate; poções
continuam representadas na interface. Aguarda validação manual.

**Seções atualizadas:** Seções 1, 15.4, 18.1 e 21.

**Pendências:** validar os dois botões do mouse e confirmar a remoção da
terceira ação no navegador.


### v0.37 --- 13/11/2026

**Tipo:** avanço rápido direcional (dash).

**O que mudou:** Espaço inicia um dash na direção da mira, com duração
inicial de 0,2 s, velocidade de 720 unidades/s e recarga de 1,2 s. O dash
para ao colidir com um inimigo, mantém os limites do cenário e mostra a
recarga no HUD. Os controles da tela foram atualizados.

**Por que mudou:** o responsável pediu que Espaço avance na direção para
onde o mouse estiver apontando.

**Impacto no projeto:** movimento do dash é local no cliente, seguindo o
modelo provisório da movimentação atual. Os parâmetros são ajustáveis e
aguardam validação manual.

**Seções atualizadas:** Seções 1, 15.4, 18.1 e 21.

**Pendências:** validar direção, bloqueio por colisão e sensação do dash no
navegador; ajustar duração/velocidade/recarga após o teste.


### v0.38 --- 13/11/2026

**Tipo:** transições de ondas e apresentação de chefes.

**O que mudou:** ao carregar a onda final, o servidor prepara um chefe
individual com vida/recompensa próprias; a mesma regra vale ao abrir a sala
diretamente nessa onda. O cliente destaca a nova onda ou chefe no centro,
atualiza a apresentação do chefe e mantém nome/nível dos inimigos após as
transições Socket.IO. Mudanças de fase exibem o início da nova fase; a cada
10 fases, um destaque genérico de capítulo aparece, sem história específica
implementada ainda.

**Por que mudou:** o Documento Mestre já previa destaque ao iniciar ondas,
chefes na última onda e capítulos a cada 10 fases. Este é o próximo ponto
de implementação após a validação dos controles de combate.

**Impacto no projeto:** transições continuam em tempo real via Socket.IO.
IA de perseguição e ataque dos monstros ainda está pendente. A validação
manual deste fluxo permanece aberta.

**Seções atualizadas:** Seções 1, 18, 18.1 e 21.

**Pendências:** validar a transição e a onda de chefe no navegador; depois
implementar IA dos inimigos.


### v0.39 --- 13/11/2026

**Tipo:** exibição única da introdução de capítulo.

**O que mudou:** introduções de capítulo agora aparecem na faixa narrativa
superior da sala somente uma vez por personagem/capítulo, com o registro
guardado no navegador. A faixa desaparece após a apresentação. As transições
de onda deixam de repetir o capítulo e mostram fase/onda ou chefe no destaque
central; quando começa um novo capítulo, sua introdução aparece primeiro e
depois surge a fase/onda.

**Por que mudou:** o responsável relatou que o capítulo estava reaparecendo
durante as ondas e pediu que fosse mostrado apenas uma vez na área indicada
na imagem.

**Impacto no projeto:** o registro de exibição é local ao navegador; histórias
específicas por classe ainda serão produzidas em etapa futura.

**Seções atualizadas:** Seções 1, 15.4, 18.1 e 21.

**Pendências:** validar visualmente o ciclo capítulo → fase/onda e as
transições de chefe.


### v0.40 --- 13/11/2026

**Tipo:** recuperação de Vida e Mana ao morrer.

**O que mudou:** a morte restaura Vida e Mana aos valores máximos, persiste
ambos no banco e envia os valores no evento Socket.IO. O cliente atualiza
as duas barras imediatamente ao receber a morte; a fase é mantida e a onda
volta para 1.

**Por que mudou:** o responsável definiu que Vida e Mana devem voltar
completas quando o personagem morrer.

**Impacto no projeto:** restauração fica no servidor e sobrevive a recargas
da página. A regra de encerramento definitivo e recompensa da partida segue
pendente em P-003/P-019.

**Seções atualizadas:** Seções 1, 7.2, 18.1 e 21.

**Pendências:** validar manualmente as barras de Vida/Mana e a persistência
após a morte.


### v0.41 --- 13/11/2026

**Tipo:** primeira IA de perseguição e ataque dos monstros.

**O que mudou:** inimigos vivos perseguem o personagem no cenário, mantêm
colisão com o personagem e entre si, e causam dano ao alcançar distância de
contato. O cliente regula as solicitações e o servidor também aplica uma
recarga por personagem, verifica que há inimigos ativos, persiste Vida/Mana
e transmite o resultado via Socket.IO. Fluxos de capítulo/onda/chefe e morte
foram marcados como validados após confirmação do responsável.

**Por que mudou:** após confirmar a etapa anterior, o responsável pediu
para avançar ao próximo item pendente do Documento Mestre: IA dos monstros.

**Impacto no projeto:** a movimentação dos inimigos é local no cliente neste
protótipo individual; a aplicação de dano e os atributos de Vida/Mana são
servidor/sessão persistidos. Sincronização de movimento entre jogadores
depende da futura implementação de salas multiplayer.

**Seções atualizadas:** Seções 1, 18, 18.1 e 21.

**Pendências:** validar perseguição, colisão, frequência/dano de contato e
persistência após a morte; balancear os parâmetros antes de ampliar a IA.


### v0.42 --- 13/11/2026

**Tipo:** recuperação de Vida/Mana ao iniciar uma fase.

**O que mudou:** derrotar o chefe e avançar para uma fase nova restaura
Vida e Mana máximas no banco e atualiza ambas as barras em tempo real. O
avanço entre ondas normais mantém os valores atuais. O fluxo simulado de
conclusão de onda segue a mesma regra.

**Por que mudou:** o responsável pediu que recursos sejam restaurados ao
iniciar uma fase, mas somente ao iniciar fase ou após morrer.

**Impacto no projeto:** a restauração ocorre no servidor tanto no combate
real quanto no fluxo simulado; a recuperação por morte permanece igual.

**Seções atualizadas:** Seções 1, 7.2, 18.1 e 21.

**Pendências:** validar fase nova com Vida/Mana reduzidas e confirmar que
uma onda comum não restaura os valores.


### v0.43 --- 13/11/2026

**Tipo:** controles contínuos, preparação de fase e informações de combate.

**O que mudou:** a sala impede seleção/arraste de texto; manter os botões
do mouse repete ataques dentro das recargas e manter Espaço repete o dash
quando disponível. Ataque básico ganhou recarga curta de 0,45 s, aplicada
no cliente e servidor. O HUD mostra a contagem de monstros restantes. Ao
começar fase nova após chefe, inicia uma preparação de 30 segundos,
persistida no banco, durante a qual os monstros não se movem nem podem
causar dano.

**Por que mudou:** o responsável pediu correções de interação, ataques
contínuos e tempo para preparar a próxima fase, além da contagem de inimigos.

**Impacto no projeto:** movimentos/contagem atualizam no cliente; servidor
valida recarga de ataques, bloqueia dano durante a preparação e persiste o
fim do intervalo. O painel avançado do chefe e o hub de capítulo não estão
implementados, pois dependem de regras/conteúdo e dos sistemas de
Inventário/Baú.

**Seções atualizadas:** Seções 1, 7.2, 15.4, 18, 18.1, 19, 20 e 21.

**Pendências:** validar controles segurados, cooldown básico, contador e
preparação. P-025 registra painel/estados do chefe; P-026 registra pausa e
hub ao fim de capítulo.


### v0.44 --- 13/11/2026

**Tipo:** contenção de gravações concorrentes do SQLite.

**O que mudou:** SQLite agora usa journal WAL e `busy_timeout` de 15 s.
Os eventos Socket.IO que iniciam transações usam um helper que converte uma
contenção persistente em retorno controlado ao cliente. O cliente permite
apenas um ataque em andamento por vez para evitar rajadas sobrepostas ao
segurar o mouse.

**Por que mudou:** foi relatado `sqlite3.OperationalError: database is
locked` no início de `attack_enemy`, durante gravações em paralelo no modo
threading do Socket.IO. O padrão anterior deixava o timeout no valor padrão
e não tratava a falha de início de transação.

**Impacto no projeto:** transações continuam protegidas por `BEGIN IMMEDIATE`;
WAL e espera de bloqueio reduzem conflitos entre leitores/escritores. Se a
contenção superar 15 s, o evento responde com erro em vez de propagar
traceback. Gravações de múltiplos processos continuam limitadas pelo SQLite.

**Seções atualizadas:** Seções 1, 16, 18, 18.1 e 21.

**Pendências:** validar ataques segurados e coleta simultânea de orbes no
navegador; observar se o erro reaparece sob uso contínuo.


### v0.45 --- 13/11/2026

**Tipo:** preparação de fase, coleta de cartas e IA dos monstros.

**O que mudou:** orbes agora podem ser coletados durante os 30 segundos de
preparação, e cartas liberadas pela experiência podem ser escolhidas ali.
O painel de preparação oferece acesso direto à árvore de Talentos. O dano
por contato passou a usar recarga individual por monstro, com validação do
ID do inimigo no servidor. A IA agora busca ângulos alternativos e tenta
contornar aliados que bloqueiam sua aproximação.

**Por que mudou:** a preparação bloqueava também a coleta de orbes, deixando
cartas disponíveis somente depois do cronômetro. Além disso, uma única
recarga global limitava o ataque de toda a horda; os inimigos também paravam
ao colidir entre si e acumulavam-se em fila.

**Impacto no projeto:** cartas e talentos podem ser preparados sem atualizar
a página. Cada contato é conferido contra um inimigo vivo da fase/onda atual.
Inventário, Baú, atributos e configuração de habilidades ainda não existem;
quando implementados, estarão disponíveis na preparação conforme P-026.

**Seções atualizadas:** Seções 7.2, 15.4, 18, 18.1, 19 e 21.

**Pendências:** validar manualmente coleta e escolha de carta durante a
preparação, além de observar se vários inimigos conseguem contornar aliados
e causar dano sem ficarem agrupados. P-027 registra a validação da IA.


### v0.46 --- 13/11/2026

**Tipo:** cooldowns por Agilidade, sala de espera, morte, transição de fase e estrutura
de ondas.

**O que mudou:** ataque básico (1 s), Corte Rúnico (6 s) e Avanço (3 s)
começam com recargas mais longas e Agilidade reduz o tempo. A seleção de
personagem agora leva à Sala de Espera-base. A morte pausa a sala e oferece reiniciar
a fase ou ir à Sala de Espera. Após a onda 10, o jogador escolhe entre sala de espera e
próxima fase; a coleção temporária é apagada. Cada fase passa a ter 10 ondas,
com semichefe na 9 e chefe na 10.

**Por que mudou:** o responsável pediu recargas iniciais mais deliberadas,
decisão de recuperação após morte, uma sala de espera antes do combate e
uma estrutura de fase mais longa com dois encontros especiais.

**Impacto no projeto:** cooldowns são validados no servidor para ataques e
Avanço. A tela-base da Sala de Espera mostra o personagem, três espaços de grupo e
atalho para Talentos; convites, amigos, cooperação, Inventário, Baú, Máquina
do Caos e trade continuam pendentes. A distribuição comum de pontos em
Agilidade também continua pendente; talentos de Agilidade já modificam as
recargas.

**Seções atualizadas:** Seções 1, 5, 7.2, 13, 15.4, 18, 18.1, 19, 20 e 21.

**Pendências:** validar manualmente os fluxos de morte, sala de espera, chefe, ondas 9
e 10, limpeza das cartas e efeito de Agilidade. P-028 reúne os recursos
sociais e serviços ainda não implementados.


### v0.47 --- 13/11/2026

**Tipo:** correção de transição de ondas e padronização de idioma.

**O que mudou:** ao criar a próxima onda, registros antigos de inimigos
agora são atualizados e reativados com vida cheia antes de o servidor
notificar o cliente. O nome da área foi padronizado como “Sala de Espera”
nos textos visíveis do jogo.

**Por que mudou:** algumas ondas existentes no banco continuavam marcadas
como derrotadas quando eram alcançadas novamente. O cliente recebia a
contagem da nova onda, mas seus monstros só voltavam após recarregar a sala.
Também foi pedido que toda a interface do jogo permaneça em português.

**Impacto no projeto:** a transição Socket.IO atualiza a posição, vida,
vida máxima, estado ativo e recompensa dos inimigos reaproveitados; a
quantidade enviada corresponde à horda reativada. Nomes internos de funções
e arquivos podem permanecer em inglês como identificadores do código.

**Seções atualizadas:** Seções 1, 18, 18.1 e 21.

**Pendências:** validar manualmente várias transições de ondas sem atualizar
a página e confirmar a tradução da interface no navegador.


### v0.48 --- 13/11/2026

**Tipo:** rolagem da Sala de Espera e localização da rota.

**O que mudou:** a página permite rolagem vertical no documento inteiro,
incluindo a raiz HTML, para alcançar o conteúdo abaixo da área visível. A
rota pública passou de `/lobby` para `/sala-de-espera`, e o envio de início
de partida passou para `/sala-de-espera/iniciar`.

**Por que mudou:** as regras globais mantinham a rolagem da página bloqueada
mesmo quando o conteúdo excedia a altura da tela. Também foi solicitado que
a URL visível da sala de espera estivesse em português.

**Impacto no projeto:** links gerados por `url_for` acompanham as rotas
atualizadas; os nomes Python internos permanecem estáveis.

**Seções atualizadas:** Seções 1, 13 e 21.

**Pendências:** conferir a rolagem e a URL em resoluções menores no navegador.


### v0.49 --- 13/11/2026

**Tipo:** posição e apresentação visual dos orbes de EXP de cartas.

**O que mudou:** orbes de EXP agora aparecem na posição em que o monstro
morre, usando a posição atual enviada pelo cliente no golpe final e salva
no estado do inimigo/orbe. Removidos os orbes artificiais em coordenadas
fixas que eram gerados ao concluir ondas de teste, e limpos os registros
antigos desses drops simulados. O desenho agora tem uma aura mais intensa e
difusa, brilhos ao redor e núcleo branco/dourado maior, com pulsação suave.

**Por que mudou:** o responsável pediu que o drop acompanhasse a morte real
do monstro e que a luz fosse intensa, respirasse suavemente e deixasse o
núcleo claramente visível.

**Impacto no projeto:** o cliente envia a posição atual do inimigo no ataque;
quando derrotado, o servidor persiste essa posição e transmite o orbe via
Socket.IO. A pulsação é desenhada no Canvas sem recarregar a página.

**Seções atualizadas:** Seções 1, 6.3, 18, 18.1 e 21.

**Pendências:** validar no navegador a posição de drops em monstros que se
movem e a legibilidade do núcleo/brilho em diferentes fundos do cenário.


### v0.50 --- 13/11/2026

**Tipo:** reorganização visual da Sala de Espera.

**O que mudou:** a tela agora apresenta cabeçalho com identidade do jogo e
atalho para trocar personagem, chamada de preparação, coluna do grupo com
três slots e painel de chat, e coluna de personagem/progresso, serviços e
botão principal de partida. O personagem local recebe um retrato Canvas
provisório com paleta por classe. A Árvore de Talentos continua acessível;
os serviços ainda não implementados estão identificados.

**Por que mudou:** aproximar a sala do layout de referência solicitado,
reservando a área para formar grupo e conversar sem esconder o progresso
do personagem e os acessos de preparação.

**Impacto no projeto:** novos estilos responsivos da sala ficam agrupados
em `styles.css`, e o retrato de classe é desenhado por `static/js/lobby.js`.
O painel de chat e os espaços de amigos são apenas apresentação: salas,
convites e mensagens Socket.IO dependem da implementação futura de grupo.

**Seções atualizadas:** Seções 1, 13.1, 18 e 21; README.

**Pendências:** validar visualmente em desktop e celular; implementar grupo,
convites e chat Socket.IO quando a etapa de multiplayer social for iniciada.


### v0.51 --- 13/11/2026

**Tipo:** ajustes de grupo e preparação na Sala de Espera.

**O que mudou:** o botão de início agora diz **Começar!** e aparece ao lado
da caixa de busca, com maior peso visual. O cartão com retrato do personagem
mostra também seus resets. Os slots vazios abrem um seletor de amigos; foi
adicionado o painel de lista com contador e área rolável preparada para
mostrar cinco amigos por vez.

**Por que mudou:** melhorar a hierarquia visual do início solo e preparar a
interface para encontrar perfis e convidar amigos tanto pelos espaços do
grupo quanto pela lista.

**Impacto no projeto:** a interface apresenta esses caminhos, mas busca,
lista persistida e envio de convites estão desabilitados porque a camada
social ainda não foi implementada. A tela não inventa amigos: exibe zero até
existirem registros reais.

**Seções atualizadas:** Seções 1, 13.1, 18 e 21; README.

**Pendências:** definir e implementar amizades/perfis, convites de sala,
presença online e integração com grupos Socket.IO.


### v0.52 --- 13/11/2026

**Tipo:** refinamento de hierarquia e distribuição da Sala de Espera.

**O que mudou:** busca de perfil foi movida para a barra superior e reduzida
para um campo fino. A lista social foi movida para a coluna direita, abaixo
dos serviços. Removido o painel de personagem selecionado que repetia nome,
classe, nível e resets já visíveis no cartão do grupo. O progresso de fase e
onda permanece junto ao título do grupo. **Começar!** fica alinhado no canto
inferior do painel, com largura controlada e sem ultrapassar seus limites.

**Por que mudou:** reduzir repetição de informações e organizar melhor o
espaço, conforme a referência visual fornecida.

**Impacto no projeto:** somente apresentação e CSS responsivo foram alterados;
busca e lista social continuam desabilitadas até existir a camada de amizades.

**Seções atualizadas:** Seções 1, 13.1, 18 e 21; README.

**Pendências:** implementar busca de perfis, amizades, convites e presença.


### v0.53 --- 13/11/2026

**Tipo:** compactação do painel de grupo para ampliar o Chat da Sala.

**O que mudou:** o aviso de fase concluída ou de retomada após derrota agora
fica na mesma linha do botão **Começar!**; em telas estreitas, ele se ajusta
acima do botão.

**Por que mudou:** reduzir a altura ocupada pelo painel do grupo e liberar
mais espaço vertical para a área de chat.

**Impacto no projeto:** mudança responsiva de layout, sem alteração no fluxo
de progressão ou no envio do formulário.

**Seções atualizadas:** Seções 1, 13.1 e 21; README.

**Pendências:** validar a composição visual em telas largas e estreitas.


### v0.54 --- 13/11/2026

**Tipo:** consolidação das regras de Reset, preparação e interface do jogo.

**O que mudou:** cada Reset agora concede 1 Ponto de Legado, implementado
junto à atualização do personagem. Na preparação da fase, foi removido o
atalho para Talentos da caixa de contagem regressiva. A mensagem técnica
sobre remoção de cartas ao fim da fase foi substituída por uma orientação
voltada ao jogador. A busca na Sala de Espera passou a usar o texto
“Buscar perfil de jogador”. O aviso de fase concluída/retomada ocupa a
mesma linha do botão **Começar!** em telas largas e fica acima dele em telas
estreitas.

**Decisões e pendências:** o responsável adiou o balanceamento de atributos,
efeitos e limites de nível da Árvore de Talentos até a etapa de balanceamento
do personagem, para que ambos sejam feitos juntos. A redistribuição será
gratuita para VIP e custará Ouro para contas comuns; o valor do custo ainda
precisa ser definido. Busca de perfis, lista de amigos e convites continuam
sem backend.

**Próxima etapa:** iniciar P-025, especificando e implementando a apresentação
de elemento/resistências do chefe e estados (quebra de escudo, sangramento,
paralisia e queimadura), com parâmetros provisórios sujeitos a balanceamento.

**Seções atualizadas:** Seções 1, 6.2, 7, 13.1, 18, 19 e 21; README.


### v0.55 --- 13/11/2026 — Consolidação de andamento

Este registro consolida alterações feitas após a v0.53 e corrige o ponto de
retomada para refletir as decisões mais recentes do responsável.

**Implementado desde a v0.53:**

-   Cada Reset concede 1 Ponto de Legado, salvo junto ao Reset e informado
    ao jogador.
-   Removido o atalho de Talentos da caixa de contagem regressiva de fase.
-   A mensagem de conclusão foi reescrita para o jogador, sem detalhes
    técnicos sobre limpeza de cartas.
-   Na Sala de Espera, a busca diz “Buscar perfil de jogador” e o aviso de
    fase concluída/retomada fica junto ao botão Começar. Busca, lista social
    e convites ainda não têm backend.

**Decisões confirmadas, ainda sem implementação completa:**

-   Redistribuição de talentos grátis para VIP; contas comuns pagarão Ouro.
    O custo ainda precisa ser definido.
-   A árvore poderá ter níveis múltiplos por talento, mas efeitos e limites
    serão definidos junto ao balanceamento dos atributos do personagem.
-   O responsável adiou esse balanceamento conjunto; não inventar bônus ou
    limites provisórios para os talentos antes dessa etapa.

**Próximas pendências:** P-025 (elementos/resistências e estados dos chefes);
P-029 (atributos e balanceamento conjunto dos talentos); P-016/P-026
(inventário e hub de preparação); P-028 (amizades, grupos, convites e chat
em tempo real).

**Validação:** o responsável informa que os recursos implementados até aqui
foram testados e aprovados. As pendências acima ainda não foram validadas.


### v0.57 --- 13/11/2026 — P-025 iniciado

**Implementado:** afinidade elemental provisória de chefes em ciclo Fogo,
Gelo, Raio e Umbral; resistência de 30% ao próprio elemento; exibição do
elemento e resistência no Canvas; redução de dano do Corte Rúnico contra
chefes Umbral. Perfil calculado no servidor.

**Falta:** escudo quebrado, sangramento, paralisia, queimadura, estados
sincronizados em tempo real, validação do responsável e balanceamento dos
valores elementais. P-025 permanece em andamento.


### v0.60 --- 13/11/2026 — Direção de progressão aprovada

O responsável aprovou o modelo de nível máximo 400 por ciclo, fases infinitas
como endgame sem níveis acima do teto, 5 pontos por nível para todas as classes,
Reset opcional que retorna aos atributos-base e concede 1 Ponto de Legado.
Pontos de atributo gastos não se acumulam através de Reset; Ouro, itens e fase
permanecem, a onda retorna a 1 e cartas temporárias são limpas.

Foi descartada a proposta de 7 pontos por nível e bloqueio da classe híbrida no
nível 220: não há justificativa implementada para vantagem extra/desbloqueio.
As fórmulas enviadas são referências para proporções, não valores que possam
ser misturados diretamente à escala atual. Atributos, jogador e monstros serão
migrados e balanceados em etapas coordenadas. Próximo: persistência e alocação
de pontos por nível sem alterar ainda dano e inimigos.


### v0.59 --- 13/11/2026 — Norte de balanceamento de personagens

O material de fórmulas enviado pelo responsável foi analisado e preservado
como referência. Criado `balanceamento/norte_de_balanceamento.md` com uma
proposta adaptada à escala e aos sistemas atuais: princípios de clareza,
tabela candidata de atributos/pontos, metas de duração de combate, faixas de
monstros para simulação e ordem segura de implementação.

Os números são propostas; nenhuma fórmula foi aplicada ao combate. Próxima
ação: revisar a tabela e decidir persistência dos atributos no Reset; depois
implementar armazenamento e distribuição, antes de migrar dano e monstros.
P-025 permanece em andamento, mas o balanceamento numérico de chefes aguarda
a calibração do personagem.


### v0.61 --- 13/11/2026 — Primeira etapa de atributos

Implementados atributos-base candidatos por classe no modelo SQLite e
migração de personagens existentes; pontos livres; concessão de 5 pontos por
nível ganho nos caminhos de progressão de teste e combate; página protegida
`/jogo/atributos`; validação de saldo e teto 32.767 no servidor; contador no
menu atualizado por Socket.IO ao subir de nível. Reset retorna aos valores-base,
zera pontos livres, mantém bônus de Agilidade de talentos comprados e concede
1 Ponto de Legado. Os atributos ainda não alteram as fórmulas de combate.

`python -m compileall -q game_app` concluiu sem erros. Falta validar
manualmente criação/migração, distribuição, atualização dinâmica e Reset.


### v0.62 --- 13/11/2026 — Persistência de atributos e recalibração de EXP

Após avaliar o impacto de manter uma fase avançada com atributos reiniciados,
a regra do Reset foi revisada: atributos investidos permanecem, pontos livres
não gastos são zerados, a fase permanece e a onda volta a 1. O limite por
atributo foi reduzido de 32.767 para 10.000 como teto técnico provisório. A EXP
de monstros passou a escalar com o nível (`20 + 6 × nível`), semichefe 3x e
chefe 5x; com a curva atual de nível (`100 + 25 × nível`), a projeção é cerca
de 63 fases até o nível 400. Foi implementada a opção VIP de distribuição
automática, por pesos de classe, mantendo a alocação manual. As novas regras
aguardam validação manual do responsável.


### v0.63 --- 13/11/2026 — Referências de arte procedural e revisão do Reset

Registradas no guia de Arte opções futuras de SVG para vetores e UI, Canvas e
matrizes para sprites, animação por tempo, tilemaps procedurais e partículas
para magias. São referências técnicas; a escolha de arte final permanece
pendente. O responsável reabriu P-002 para analisar se o Reset deve reiniciar
fase e onda em 1 mantendo atributos e itens persistentes. A regra atual no
código não foi alterada. A análise de riscos e a recomendação de balanceamento
estão no guia de Personagens e Progressão.


### v0.64 --- 13/11/2026 — Reset por ciclo aprovado e base de itens

O responsável aprovou o Reset retornar nível, fase e onda a 1, mantendo
atributos gastos, Ouro e itens persistentes, removendo pontos livres não gastos
e cartas temporárias, e concedendo 1 Ponto de Legado. Também aprovou como
princípio que os inimigos escalem pela quantidade de Resets; a fórmula e as
recompensas dessa escala continuam pendentes de balanceamento, e a mudança no
código ainda falta.

Recebido e documentado o material comparativo sobre armas, armaduras, escudos,
asas, pets, montarias, anéis e pendentes inspirado em MU Online. Criado
`balanceamento/base_enviada_itens_mu_online.md` com a referência e análise de
empilhamento, limites e adaptação à escala do projeto. Nenhum valor numérico do
material foi adotado. O guia de itens e o norte de balanceamento foram
atualizados para considerar equipamentos nos testes futuros.


### v0.65 --- 13/11/2026 — Dano elemental e roubo de Vida no escopo de balanceamento

O responsável acrescentou dano elemental causado e roubo de Vida à lista de
fatores obrigatórios para a futura calibração. A documentação distingue dano
elemental de resistência/estados e roubo de Vida de regeneração passiva e cura
por eliminação. Registradas perguntas futuras para fontes, cálculo, limites e
interações com chefes, dano em área, efeitos contínuos, escudos, equipamentos e
outras curas. Nenhuma fórmula ou valor foi definido. Atualizados o material de
referência de itens, o norte de balanceamento, progressão, pendências e o
roadmap. O próximo balanceamento deve considerar esses sistemas em conjunto.


### v0.66 --- 13/11/2026 — Auditoria dos documentos de balanceamento

Revisados todos os documentos do diretório `balanceamento/`. Corrigidas
informações antigas sobre 7 pontos por nível e bloqueio da Lâmina Rúnica no
nível 220; a regra vigente é 5 pontos por nível e classe disponível desde o
início. O documento de base de personagens agora separa os números enviados
das regras atuais e do próximo trabalho.

O norte de balanceamento passou a listar lacunas adicionais: ordem de resolução
de dano/cura, restauração de recursos e recargas no Reset, requisitos de nível
dos itens que persistem, Mana em combate, poções, solo/dupla/trio, teto de
atributos ao longo de vários Resets, progressão após nível 400 sem Reset e
economia completa. Criada a pendência P-031 para fechar o modelo integrado de
combate. Os valores continuam pendentes; nenhuma fórmula de balanceamento foi
adotada nesta auditoria.
Também foi registrada a divergência entre a hipótese antiga de um nível de
inimigo por fase e o mapeamento provisório atual do código (`5 × fase + onda`);
a projeção de XP de 63 fases usa apenas o mapeamento atual, antes de Reset,
equipamentos e escala para grupos.
Os pesos atuais de distribuição automática VIP foram registrados como
protótipos a validar contra builds manuais, para que sejam conveniência e não
vantagem exclusiva de poder.


### v0.67 --- 13/11/2026 — Auto-poções VIP e adaptação do modelo de itens

Implementadas auto-poções opcionais de Vida e Mana para contas Premium/VIP,
com ativação independente por personagem, validação server-side e atualização
em tempo real. Como ainda não existe estoque de consumíveis, o comportamento
usa limites, restaurações e recargas provisórios e não gasta itens; isso está
documentado em P-032 e não representa balanceamento final.

A referência MU Online foi revista e traduzida em papéis adequados ao projeto:
arma como identidade de dano; armadura/escudo para sobrevivência; asas com
orçamento ofensivo/defensivo combinado; acessórios com escolhas distintas;
pet voltado a função de combate e montaria a mobilidade. Também foram
reforçados os limites contra empilhamento de porcentagens e a calibração em
ondas e grupos de até três. Nenhum valor da referência foi importado como
atributo final. Os itens, pets, montarias, asas, dano elemental, roubo de Vida,
poções, atributos e Reset seguem no balanceamento integrado P-031.


### v0.68 --- 13/11/2026 — Câmera oblíqua futura e alcance de coleta

Registrada a direção de revisar a câmera, depois de concluir 100% do
balanceamento integrado, para uma perspectiva oblíqua 2.5D que mostre melhor
personagem, armas, pets, montarias, asas e profundidade do cenário. Cerca de
25° foi anotado apenas como referência inicial de prototipagem; movimento,
mira, colisão e alcance continuarão em coordenadas do mundo.

Analisada a coleta futura de drops: usando o raio de personagem de 13 e o
alcance atual dos orbes (24 unidades), propusemos 24 sem pet, 72 com pet e
108 para Premium/VIP com pet. Isso representa 3x alcance com pet e mais 50%
para Premium/VIP. Valores são propostas para simulação, não aprovados nem
implementados. Itens ainda não possuem sistema de drop; somente orbes de EXP
de cartas existem (atração em até 155 e coleta a cerca de 24). A coleta futura
deve validar distância e propriedade no servidor, e o saque em grupo precisa
definir propriedade/compartilhamento. Criadas P-033 e P-034.


### v0.69 --- 13/11/2026 — Zoom controlado pela roda do mouse

Adicionada à proposta de câmera P-033 a opção de aproximar/afastar pelo scroll
do mouse, com o personagem como foco. Escala padrão inicial de 1,0x e limites
propostos de 0,85x a 1,15x, com transição suave e sem alterar movimento, mira,
alcances ou colisões. O zoom deve preservar a leitura do personagem e dos
perigos e não revelar áreas fora do mapa. Será avaliado junto da câmera 2.5D,
após o balanceamento completo; ainda não implementado.


### v0.70 --- 13/11/2026 — Proposta de auto-ataque Premium/VIP

Registrada a proposta de oferecer auto-ataque opcional contra monstros PvE
para Premium/VIP, além do modo automático desbloqueável pela Árvore de
Talentos. O recurso deverá respeitar dano, velocidade, alcance, Mana, recargas
e demais regras do combate manual, sem bônus numérico por assinatura. Pendente
definir se o VIP fornece acesso alternativo ao talento ou apenas libera o
botão após o desbloqueio. Não implementado; registrado em P-035 para avaliar
progressão, equilíbrio por classe e impacto no cooperativo.


### v0.71 --- 13/11/2026 — Auto-ataque fora da Árvore de Talentos

Correção da proposta registrada na v0.70 após esclarecimento do responsável:
o auto-ataque não estará disponível na Árvore de Talentos. A proposta vigente
é tratá-lo como opção Premium/VIP separada contra monstros PvE. Removida a
pendência de decidir a relação do benefício com o talento; P-035 continua
aberta para definir funcionamento, controles e equilíbrio. A função não foi
implementada.


### v0.72 --- 13/11/2026 — Auditoria e primeira simulação de balanceamento

Auditados os documentos de decisão, referências de personagem/itens, norte,
pendências, roadmap e fórmulas existentes no código. Confirmadas lacunas que
impedem declarar o balanceamento integrado concluído: atributos ainda não
afetam o combate, faltam habilidades para três classes, escala por Reset,
equipamentos, efeitos de talentos/cartas, elementos/estados, cura/roubo de
Vida, poções com estoque, economia e escala cooperativa.

Criados `balanceamento/auditoria_e_primeira_simulacao.md` e
`scripts/simulate_balance_model.py`. O simulador calcula checkpoints das quatro
classes com as fórmulas recebidas e os pesos VIP atuais, além da projeção de XP.
Resultados apontam faixas de Vida/Mana/Dano muito diferentes entre classes e
redução de recarga por Agilidade que chega ao teto atual até o nível 100. A
curva de XP chega ao nível 400 na fase 63 após cerca de 1.637 eliminações.
Nenhuma fórmula candidata foi conectada ao combate; P-031 passou a Em andamento

O simulador passou a comparar também distribuições manuais representativas.
A recarga básica candidata foi elevada de 1,0 s para 1,15 s para manter a build
de Agilidade no alvo de duração de inimigo comum. Os dois perfis simulados
permanecem dentro dos alvos iniciais de TTK/sobrevivência nessa primeira rodada
de ataque básico.

A etapa seguinte adicionou uma rotação candidata para cada classe e simulou
inimigos comuns, semichefes e chefes. O dano básico foi recalibrado no simulador
para `10 + 0,50 Força + 0,20 Agilidade` (Guardião), `20 + 0,35 Energia + 0,20
Agilidade` (Tecelão), `10 + 0,35 Agilidade + 0,20 Força` (Vigia) e `10 + 0,40
Força + 0,40 Energia + 0,10 Agilidade` (Lâmina). A rotação usa recargas
independentes e Mana inicial finita, sem regeneração. O TTK dos comuns ficou em
3,0–5,7 s. Surgiram desvios pequenos nos alvos de semichefe e chefe: Guardião
manual no nível 1 e Tecelão VIP no nível 400. Foram registrados para a próxima
calibração; não houve mudança no combate ativo.

### v0.73 --- 13/11/2026 — Primeiras rotações de habilidade por classe

Atualizada a auditoria com uma proposta inicial de habilidade ativa por classe
e rotações com recargas independentes, Mana finita e sem regeneração. O
simulador compara ataques básicos, semichefes e chefes nos níveis 1/100/220/400
para builds VIP e manuais. O TTK de inimigos comuns ficou entre 3,0 e 5,7 s.
Os resultados de semichefe/chefe ficaram próximos das metas, com desvios
pequenos do Guardião manual no nível 1 e do Tecelão VIP no nível 400. Parâmetros
e limitações permanecem propostas; nenhum valor foi ligado ao combate do jogo.
Atualizados P-031, roadmap e Documento Mestre para v0.73. Próxima ação: ajustar
esses desvios e definir comportamento, elementos e áreas das habilidades antes
da integração.

### v0.74 --- 13/11/2026 — Ataques telegráficos de monstros

Implementado P-036: monstros comuns alternam papéis de ataque corpo a corpo e
à distância; o semichefe e o chefe alternam dois padrões especiais cada. Áreas
de perigo e contagem regressiva são desenhadas no chão, projéteis incluem
sombra/posição de queda, e o dano só é resolvido ao fim do aviso. Socket.IO
transmite os avisos e o servidor valida o ataque ativo, sua janela, área e dano
antes de atualizar Vida. Contato sem aviso foi removido como fonte de dano para
que os ataques corpo a corpo também possam ser esquivados. Padrões, danos,
recargas e raios são provisórios; validação manual no navegador continua
pendente. A posição do jogador ainda é simulada no cliente. Conceito, arquitetura,
roadmap e pendências foram atualizados; o índice passou a v0.74.

### v0.75 --- 13/11/2026 — Correção do ataque do jogador

Corrigido o bloqueio que impedia o guerreiro de atacar após a implementação dos
novos tipos de monstros. `attackWith` filtra alvos por `attackReady`, mas
`prepareEnemy` havia deixado de inicializar essa propriedade ao ser ampliado
para os papéis melee/ranged e elites. O preparo agora marca cada inimigo vivo
como pronto para receber ataque. O combate continua aguardando validação manual
no navegador. Roadmap e Documento Mestre foram atualizados para v0.75.

### v0.76 --- 13/11/2026 — Atributos nos serviços da Sala de Espera

A página de distribuição de atributos foi adicionada aos Serviços da Sala de
Espera. O atalho leva à tela existente, que consulta os quatro atributos,
investe pontos com validação do servidor e mantém a opção automática exclusiva
Premium/VIP. O cabeçalho e o botão de retorno da página agora voltam à Sala de
Espera. Nenhuma fórmula de combate foi alterada; os efeitos dos atributos seguem
pendentes do balanceamento conjunto. Roadmap e índice do Documento Mestre foram
atualizados para v0.76.

### v0.77 --- 13/11/2026 — Alinhamento da página de Atributos

Após a captura de tela mostrar a interface encostada à esquerda e uma grande
área vazia à direita, o contêiner da página de Atributos recebeu largura
responsiva limitada e margens automáticas para centralização. A paleta e os
componentes internos foram preservados. Guia de Arte, roadmap e índice do
Documento Mestre foram atualizados para v0.77.

### v0.78 --- 13/11/2026 — Avisos de pontos e navegação da Sala de Espera

A tela de Atributos agora calcula e exibe a estimativa do valor final durante a
digitação, avisa sobre pontos insuficientes ou teto e desativa envios inválidos;
validação do servidor continua ativa. A Sala de Espera calcula corretamente o
saldo de Pontos de Legado após compras e sinaliza com um ponto dourado os
serviços de Atributos/Talentos com pontos disponíveis. Removidos do menu de jogo
os atalhos de Atributos, Talentos e Trocar Personagem. Adicionado o botão Sair
ao lado de Trocar personagem na Sala de Espera, usando POST e CSRF. Guias de
progressão, interface, Sala de Espera, roadmap e índice foram atualizados para
v0.78. Os endpoints de visualização/compra de talentos e distribuição de
atributos também verificam a marca de Sala de Espera armazenada na sessão.

### v0.79 --- 13/11/2026 — Indicadores sobre os ícones dos serviços

Reposicionados os indicadores dourados de pontos pendentes para o canto
superior direito dos ícones de Atributos e Árvore de Talentos na Sala de
Espera. A condição que mostra/oculta cada indicador permanece vinculada aos
pontos livres correspondentes. Guia de Arte e Documento Mestre atualizados
para v0.79.

### v0.80 --- 13/11/2026 — Segundo passe de balanceamento de combate

O simulador recebeu pesos VIP candidatos separados dos pesos ativos e avaliou
builds espelhadas das distribuições manuais representativas. Foram ajustados,
apenas no modelo, o multiplicador de Vida de semichefe (6,5× para 6,7×) e a
fórmula-base do Vigia, que reduziu o TTK comum inicial de 6,8 s para 5,7 s.
As builds candidatas ficaram dentro das metas solo nos checkpoints 1/100/220/400
e igualaram os cenários manuais correspondentes. Nenhum valor foi conectado ao
jogo; pesos com zero exigirão suporte explícito no alocador caso sejam aprovados.
Corrigida também a atribuição do resultado de 19,4 s do semichefe nível 1: era
do Tecelão, não do Guardião. Como gatilhos de estados ainda dependem da definição
de habilidades em P-031 e a movimentação não é autoritativa, P-025 foi ordenado
depois dessa calibração. Relatório, roadmap e índice atualizados para v0.80.

### v0.81 --- 13/11/2026 — Perfis candidatos de habilidades e estados

Registrados no simulador e na auditoria perfis provisórios para as quatro
classes, com alvo/área, elemento, estado, chance e duração. Dano contínuo
esperado é 6% por aplicação completa de queimadura e 2,1% em valor esperado
para sangramento. Quebra de escudo e paralisia seguem como utilidades sem dano
equivalente; as dependências foram registradas. Nenhum perfil foi ligado ao
combate. A simulação de grupo (três inimigos) deu 8,9–16,0 s e a de chefe nas
quatro afinidades 60,9–95,4 s nos níveis 1/100/220/400. Área pressupõe
alinhamento ideal; DoT usa valor esperado e quebra de escudo/paralisia não foram
convertidos em dano. Próximo passo P-031: avaliar o valor tático desses estados,
composição de grupo, equipamento, recursos e escala por Reset. A documentação
usa “distribuição automática Premium/VIP” em vez de “build VIP”. Nenhum valor foi
aplicado ao combate. Índice e roadmap atualizados para v0.81.

#### Complemento v0.81 — Posicionamento e grupos

O quarto passe do P-031 passou a informar quantos inimigos a área realmente
alcança: em três comuns, Tecelão cai de 11,9–16,6 s com um alvo para 8,9–11,1 s
com três; Vigia cai de 12,1–15,9 s para 9,1–12,2 s. Habilidades de alvo único
não mudam. Foi incluído um baseline de dano cooperativo contra a Vida atual do
chefe solo: dupla Guardião + Tecelão 30,8–39,3 s e trios 20,8–25,1 s. Não há
escala cooperativa, utilidade, sobrevivência ou itens nesses resultados. A
próxima definição é a escala de inimigos e regras de alvo em dupla/trio, antes
de equipamento, recursos e Reset. Nenhum dado foi aplicado ao combate.

### v0.82 --- 13/11/2026 — Posição dos monstros e pressão das hordas

Substituída a concentração dos monstros no centro por posições pseudoaleatórias
distribuídas pelo mapa, afastadas do ponto de entrada do jogador e umas das
outras. A próxima onda considera a posição enviada no último golpe e a mesma
onda conserva os pontos ao recarregar. Os limites aguardam validação manual; os
efeitos visuais de entrada continuam planejados. A estimativa de pressão agora
para de contar ataques de monstros eliminados, mas ainda é um limite superior
porque não calcula aproximação, alcance nem esquiva. Próxima missão P-031:
modelar esses fatores e então calibrar número e ritmo das ondas. Código, guia,
auditoria, roadmap e índice atualizados para v0.82.

### v0.83 --- 13/11/2026 — Simulação de aproximação e revisão da pressão

O simulador passou a obter o nível de entrada real por onda pelo orçamento fixo
de EXP, usar a Vida dos inimigos conforme a fase/onda e estimar aproximação,
alcance, aviso e recarga com os pontos de surgimento do protótipo. No cenário
Guardião solo, a onda 8 estimou 86 s e derrota no início do ciclo (entrada no
nível 4); perto do nível 100, 61 s e derrota sob a hipótese de jogador parado e
50% de ataques recebidos. Isso aponta um risco, não uma dificuldade validada:
movimento, colisão, esquiva real e escolhas do jogador ainda faltam. Nenhum
parâmetro foi alterado no combate. Registrado que eventos dinâmicos usam
Socket.IO. Um candidato de simulação (45% da Vida comum/25% do dano comum)
reduziu a onda 8 inicial de 86 para 42 s e melhorou a sobrevivência nas quatro
classes; no nível 400 três classes ficaram abaixo da meta provisória de 30 s.
Candidato não aplicado. Próxima missão: ajustar a escala por fase/nível e depois
incluir builds manuais, equipamento, elementos, chefes, recursos e Reset. Índice,
guias, auditoria e roadmap atualizados para v0.83.

### v0.84 --- 13/11/2026 — Correção da consulta de inicialização do jogo

Corrigido `GET /jogo`, que acessava `phase_xp_budget` sem selecionar o campo na
consulta de personagens. A consulta de inimigos também seleciona `enemy_index`,
necessário ao reposicionar inimigos agrupados de versões anteriores. A causa
era acessar chaves ausentes na linha SQLite, não uma migração ausente no banco.
Roadmap e Documento Mestre atualizados para v0.84.

### v0.85 --- 14/11/2026 — Restauração de recursos e passivas das cartas

Ao ganhar um ou mais níveis, o personagem agora recebe Vida e Mana máximas
novamente no mesmo evento de combate. O cliente atualiza os medidores pelo
Socket.IO. Os orbes de EXP de cartas gravam e exibem as mesmas coordenadas da
posição final do inimigo morto. As 30 cartas agora aplicam passivas concretas
no servidor, incluindo dano, defesa, críticos, esquiva, recarga, alcance,
movimento e recuperação entre ondas; descrições foram ajustadas para refletir
os efeitos implementados. Os valores continuam provisórios para P-022.

Ao morrer, cartas ativas, EXP temporária, ofertas pendentes e orbes são removidos
na mesma transação que restaura Vida/Mana e retorna à onda 1 da fase atual. O
HUD recebe esse reset em tempo real. A barra continua acumulando EXP quando a
coleção está cheia; a oferta permite substituir uma carta ou manter as atuais.
Selecionar cartas recalcula os máximos e limita recursos ao novo teto quando um
efeito de Vida/Mana máxima sai da coleção.

Na transição de fase, os orbes antigos são limpos com a coleção; o orbe do
chefe recém-derrotado permanece no ponto do abate para coleta na preparação
da fase seguinte. A coleção continua zerada e sem cartas ativas.

**Validação técnica:** `python -m compileall -q game_app` passou. A validação
manual no navegador/combate continua pendente; o responsável deverá confirmar
subida de nível, posição do orbe, passivas, morte e troca/manutenção com coleção
cheia. Índice v0.85, guia de progressão, arquitetura, roadmap e P-022 atualizados.

### v0.86 --- 14/11/2026 — Efeitos dos atributos visíveis e Agilidade

Auditada a distribuição de Força, Agilidade, Vitalidade e Energia. Os pontos
eram salvos e lidos pelas fórmulas de combate, mas a página de atributos não
mostrava os valores derivados, e Agilidade ainda não alterava o movimento como
sua descrição prometia. A tela agora mostra dano básico/habilidade, máximos de
Vida/Mana, recargas e bônus de movimento. Vitalidade concede +2 Vida máxima por
ponto; Energia concede +1,5 Mana máxima; ao investir nesses atributos, o aumento
dos máximos também é somado aos recursos atuais. Agilidade acrescenta +0,1% de
movimento por ponto, com teto de 25%, além da redução de recarga já existente
(0,5% por ponto, teto de 50%). Força agora também escala levemente o dano do
Tecelão de Cinzas (+0,1 por ponto). Coeficientes são provisórios e continuam no
balanceamento conjunto. Sintaxe Python/JavaScript e cálculo de impacto foram
verificados; teste manual de combate pendente.

### v0.87 --- 14/11/2026 — Inicialização correta de recursos e auditoria dos atributos

Na revisão do efeito dos atributos foi encontrada uma inconsistência adicional:
personagens novos recebiam os padrões fixos de 1.000 Vida/200 Mana, em vez dos
máximos derivados de classe, nível e atributos. A criação agora inicializa os
recursos com os valores derivados. Personagens antigos com recursos acima do
máximo são limitados ao máximo ao entrar em `/jogo`, e o padrão de fallback do
banco foi ajustado. O investimento em Vitalidade/Energia preserva apenas os
recursos válidos antes de aplicar o ganho do novo máximo, evitando cura indevida
em dados antigos. A tela também exibe o dano-base decimal antes do arredondamento
do golpe e recargas com três casas para tornar incrementos pequenos visíveis.
Atualizados os status e fórmulas na tela de Atributos, o
roadmap, guia de progressão, README e índice leve. Sintaxe e verificações locais
de rotas/fórmulas passaram; validação manual no navegador permanece pendente.

### v0.88 --- 14/11/2026 — Recolher e reabrir seleção de cartas durante o combate

Ao liberar uma oferta, a seleção de cartas aparece automaticamente. Foi
adicionado botão para exibir/ocultar as cartas e a tecla Tab como atalho. Tab é
interceptado enquanto houver escolha pendente, sem avançar o foco dos controles
do navegador. Com o painel oculto, movimento e combate voltam a responder; com
ele aberto, entradas do jogador ficam suspensas enquanto os inimigos continuam
agindo. A coleta automática de orbes fica suspensa até a escolha ser resolvida,
evitando tentativas recusadas pelo servidor. O fluxo funciona também na troca
de carta quando a coleção está cheia. Sintaxe Python/JavaScript e template
verificados; validação manual no navegador pendente.

### v0.89 --- 14/11/2026 — Movimento liberado com as cartas abertas

O responsável esclareceu que a seleção de cartas não deve travar o personagem.
Corrigido o controle: enquanto o painel está aberto, WASD/setas continuam
movendo o personagem e Espaço ainda permite usar Avanço; os ataques permanecem
suspensos para evitar ações acidentais na interface. Com o painel recolhido, o
combate volta integralmente. O jogador não perde a possibilidade de se deslocar
até uma área segura antes de ler e escolher. Documentação de progressão,
roadmap e Documento Mestre atualizados; sintaxe JavaScript e template
verificados, teste manual no navegador pendente.

### v0.90 --- 14/11/2026 — Cartas ocultas por padrão com aviso no Tab

O responsável definiu que as ofertas de cartas não devem cobrir o cenário por
padrão: quando uma escolha ficar disponível, o painel permanece oculto e o
botão Tab se destaca com “Nova carta” enquanto a seleção está oculta. O botão e
a tecla Tab abrem/recolhem a seleção, e o destaque reaparece quando ela é
recolhida enquanto a escolha segue pendente. Movimentação e
Avanço continuam disponíveis com a seleção aberta; ataques ficam suspensos
nesse estado. O botão também informa a ação por leitor de tela. Atualizados o
Documento Mestre, o guia de progressão, o roadmap, o histórico e README.

### v0.91 --- 14/11/2026 — Coleta de orbes e EXP com cartas pendentes

Investigado o relato de que o orbe seguia o personagem sem aumentar a EXP. O
cliente bloqueava a coleta quando `pendingCardChoices > 0` ou a seleção estava
aberta, e o servidor também recusava coletas enquanto havia escolha/oferta
pendente. A aura continuava sendo atraída localmente, criando a impressão de
coleta sem recompensa. Removidas as travas redundantes: orbes agora podem ser
recolhidos durante uma escolha e EXP/ofertas adicionais acumulam na fila. As
coletas são serializadas para evitar rajadas concorrentes no SQLite; o ACK do
Socket.IO atualiza barra/coleção diretamente e o broadcast é deduplicado. Se o
banco estiver ocupado, o cliente tenta novamente após breve intervalo, soltando
o orbe visualmente até a confirmação. Progressão, roadmap, Documento Mestre,
README e histórico atualizados. Validação manual no navegador pendente.


### v0.92 --- 14/11/2026 — Clique para selecionar cartas

Investigado o relato de que clicar em uma carta não produzia ação. A oferta
inicial era renderizada como formulário e dependia de `event.submitter`; ofertas
criadas depois da carga usavam botões com um caminho próprio. Isso deixava a
seleção inicial dependente do comportamento de submissão do navegador e sem um
retorno claro quando a ação não era aceita. As duas ofertas agora usam botões
`type="button"` com delegação de clique e enviam `card:choose` por Socket.IO.
Falhas de conexão ou validação exibem mensagem e reabilitam o botão. A URL do
script foi versionada como `0.92` para invalidar a cópia antiga em cache. Atualizados
os guias de progressão, arquitetura, roadmap, o índice Documento Mestre e README.
Validação manual no navegador ainda pendente.


### v0.93 --- 14/11/2026 — Sincronização de ofertas de cartas

Investigado o aviso intermitente de que uma carta clicada não pertencia à oferta.
A coleta de orbes podia transmitir um estado atrasado com uma oferta anterior;
o cliente usava esse estado para a interface enquanto o servidor já havia
resolvido a oferta e criado outra. As escolhas agora carregam o ID exato da oferta,
validado no servidor, e cada personagem mantém uma revisão monotônica própria.
Estados de ofertas mais antigas são ignorados, a coleta
de orbes atualiza somente a EXP, e cada oferta é sincronizada por `card:state`.
Cliques concorrentes são impedidos. Em caso de ID desatualizado, o servidor
retorna a oferta atual para atualizar a interface em vez de rejeitar a carta
como indisponível. Script versionado como `0.93`.

O responsável definiu que não quer testes automatizados. Não criar nem executar
testes automatizados; funcionamento e interface são validados manualmente pelo
responsável, jogando e usando os fluxos. As alterações aguardam essa validação.

### v0.94 --- 14/11/2026 — Painel de alvo e recomendação de carta

Implementado o P-037: ao apontar para um monstro, um painel superior central
mostra retrato procedural desenhado em Canvas, nome, nível, Vida/barra, elemento,
resistência e ponto fraco. Os nomes sobre os monstros permanecem, mas nível e
afinidade saíram dos rótulos do cenário. Fraqueza não definida aparece como
“Ainda não identificado”; não foi alterada a fórmula de dano elemental.

Cada oferta de três cartas passa a destacar uma sugestão determinística baseada
na classe, nos efeitos e na situação da run. Após 20 segundos, um evento Socket.IO
pede ao servidor para ativar a carta recomendada; o servidor valida a oferta e o
prazo persistido no SQLite, que não reinicia ao recarregar a página. Se a coleção
estiver cheia, a sugestão não substitui uma carta sem decisão do jogador. Também
foi garantida a apresentação de uma escolha inicial ao iniciar com coleção vazia.
Script versionado como `0.94`; Documento Mestre, guias temáticos, roadmap e README
atualizados.

Não foram adicionados nem executados testes automatizados, conforme a regra do
responsável. A validação visual e funcional de P-037 permanece manual e pendente.

### v0.95 --- 14/11/2026 — Alcance visual por classe e escolhas de carta por categoria de conta

O responsável confirmou manualmente os itens de P-037 marcados como OK:
retrato/dados do monstro, valores e barra de Vida, elemento/resistência/ponto
fraco, troca de alvo, atualização de Vida em tempo real, afinidades de
semichefe/chefe, recomendação visível, escolha manual antes do prazo, escolha
automática após 20 segundos, prazo preservado após atualizar a página, fluxo da
coleção cheia e escolha inicial. A frase sobre nenhuma carta ativa ser removida
sem decisão não recebeu marcação OK explícita, por isso não foi registrada como
validada.

Nova regra: contas comuns podem escolher qualquer uma das três cartas e a
recomendação fica apenas como destaque; o fim do contador não escolhe por elas.
Premium/VIP ativa a recomendada após 20 segundos, se ainda não tiver escolhido.
Com coleção cheia, contas comuns escolhem manualmente entre substituir e manter.
Premium/VIP substitui uma carta ativa da menor raridade pela carta escolhida ou
recomendada, mas mantém a coleção se ela for inferior a todas as cartas ativas.
Empate de raridade remove a carta mais antiga. A permissão, o prazo e a raridade
são verificados no servidor, e as mudanças de coleção permanecem transacionais.

Adicionado um círculo dourado suave ao redor do personagem, dimensionado pelo
alcance visual-base provisório de cada classe. O círculo é apenas indicativo e
não altera o alcance de combate. Estes novos comportamentos e os valores visuais
aguardam validação manual do responsável. Script versionado como `0.95`.
Nenhum teste automatizado foi criado ou executado.

### v0.96 --- 14/11/2026 — Saída da pausa entre fases, dois alcances e alternância VIP de teste

Investigado o relato de personagem preso ao atingir o fim da fase enquanto o
jogador se movimentava ou estava escolhendo carta. A conclusão de fase já é uma
pausa intencional até o jogador escolher preparar a seguinte ou voltar à Sala de
Espera; o cliente, porém, podia conservar teclas/botões pressionados e uma
interface de cartas pendente. Agora a transição limpa as entradas mantidas,
encerra o temporizador e remove a oferta da tela, e o painel de decisão explica
como sair da pausa. Validar manualmente o cenário relatado.

O círculo único foi separado em dois: dourado contínuo para o ataque básico e
azul tracejado para Corte Rúnico, com raios visuais próprios por classe. As
caixas das ações no HUD usam as mesmas cores. Os valores são visuais e
provisórios, sem mudar o alcance de combate.

Adicionado botão flutuante para ativar/desativar Premium/VIP da própria conta
durante os testes. O evento Socket.IO verifica sessão e CSRF e grava a alteração
no servidor; após a confirmação, a página recarrega para aplicar capacidades e
benefícios. A ferramenta fica ativa por padrão no protótipo e pode ser escondida
e bloqueada com `CRONICAS_ENABLE_PREMIUM_TEST_TOGGLE=0`; deverá ser removida antes
do lançamento.

Atualizados os guias, roadmap, pendências, README e Documento Mestre v0.96.
Nenhum teste automatizado foi criado ou executado; mudanças aguardam validação
manual do responsável.

### v0.97 --- 14/11/2026 — Movimento preservado durante a seleção de cartas

O responsável esclareceu que o personagem precisa continuar andando enquanto a
oferta de cartas está aberta, pois os monstros continuam atacando. A interface já
permitia WASD/setas e Avanço no fluxo normal, mas a pausa global podia sobrepor o
estado do modal na transição de fase. A pausa agora é derivada apenas das telas de
morte e da decisão de fim de fase; abrir ou escolher carta não pausa o mundo.
Estados atrasados de ofertas são ignorados quando uma dessas pausas está aberta.

Ao concluir a fase, a seleção pendente é fechada e teclas/botões mantidos são
limpos. A partida permanece pausada até o jogador escolher preparar a próxima
fase ou voltar à Sala de Espera, conforme o fluxo aprovado. O caso prático
relatado pelo responsável aguarda validação manual. Recursos versionados como
`0.97`; nenhum teste automatizado foi criado ou executado.

### v0.98 --- 14/11/2026 — Alcance efetivo alinhado aos círculos

O responsável observou que acertar um monstro na borda do círculo não causava
dano. A seleção do alvo ainda usava alcances fixos de 100/150 unidades, embora
os círculos variassem por classe. O ataque básico agora usa `base_attack_range`
da classe e Corte Rúnico usa `base_skill_range`; multiplicadores de cartas
afetam os círculos e o alcance selecionável na mesma proporção. O servidor
confere a distância recebida antes de aplicar dano e rejeita golpes além do
limite. Os valores continuam candidatos de balanceamento; validar bordas,
classes e cartas de alcance manualmente.

Atualizados os guias de combate, arte, arquitetura, roadmap, pendências, README e
Documento Mestre v0.98. JavaScript/CSS versionados como `0.98`. Não foram
adicionados nem executados testes automatizados.

### v0.99 --- 14/11/2026 — Alcance por contato, escolhas VIP e HUD compacto

O limite de ataque agora considera o contato do contorno do monstro com o
círculo: cliente e servidor permitem a distância entre centros até o alcance da
classe/carta somado ao raio do inimigo (17 comum, 24 semichefe, 28 chefe). O
alvo continua precisando estar na direção da mira e o servidor confere o mesmo
limite antes de causar dano.

Contas comuns escolhem cartas sem cronômetro e não recebem prazo salvo; ao
ativar Premium/VIP com uma oferta aberta, o servidor inicia um prazo novo de
20 segundos. Apenas Premium/VIP vê a contagem regressiva em destaque. Ao confirmar uma escolha automática, o cliente aplica o
estado mais recente retornado pelo servidor, preservando a próxima oferta e seu
próprio prazo de 20 segundos. O servidor também resolve a raridade se uma oferta
já tiver uma carta escolhida aguardando substituição. Orbes passam a conceder
25 EXP para contas comuns e 30 EXP (+20%) para Premium/VIP. Os parâmetros são
provisórios para testar mais oportunidades de escolha/substituição VIP.

O chefe passa a circular e se reposicionar em torno do jogador enquanto ataca,
em vez de parar apenas por entrar no grande alcance de ataque. Movimento e
posição seguem simulados pelo cliente.

A caixa inferior agora combina o retrato Canvas compartilhado, nível/limite,
barra de EXP para o próximo nível, Resets, Vida, Mana e habilidades. A contagem
de monstros fica em uma caixa compacta separada no canto superior esquerdo. O
novo `portrait.js` centraliza os retratos usados na Sala de Espera e no jogo.

Roadmap registra como já validados os fluxos anteriores informados pelo
responsável. A lista de validação manual pendente contém somente: contato e
alcance com carta; fluxo comum sem cronômetro; contagem sequencial VIP,
substituição por raridade e regra de manter coleção; bônus de EXP VIP; movimento
do chefe; e nova disposição compacta da HUD. Movimento com cartas abertas, fim
de fase e alternância do Premium/VIP permanecem como validados. Nenhum teste
automatizado foi criado ou executado.

Atualizados os guias temáticos, o roadmap, as pendências, o README e o Documento
Mestre v0.99. Recursos estáticos da partida e retratos recebem versão `0.99`.

### v0.100 — 14/11/2026 — Atributos em tempo real e barra superior

A tela `/jogo/atributos` agora envia a distribuição manual por Socket.IO e
atualiza o valor do atributo, os pontos restantes e os efeitos derivados de
combate sem recarregar a página. A descrição dos pontos informa quantos aguardam
distribuição, sem exibir o teto técnico. As notificações dessa tela desaparecem
após cinco segundos.

A automação Premium/VIP agora pode ser ativada e desativada pelo botão usando
Socket.IO. Ao ativar, distribui também os pontos livres acumulados pelos pesos
da classe do personagem; os novos pontos ganhos seguem a mesma regra. Ao
desativar, mantém os atributos já gastos e interrompe a automação futura.

A contagem de monstros saiu da caixa separada no canto superior esquerdo e foi
integrada à barra superior junto de fase e onda. O contador continua atualizado
por Socket.IO sem reconstruir a barra ou perder o indicador de conexão.

Depois que o responsável informou que a partida acabava antes de abrir escolhas
suficientes para testar substituição VIP, a EXP por orbe Premium/VIP foi elevada
provisoriamente de 30 para 40; conta comum permanece em 25. Roadmap, guias e
Documento Mestre registram a calibração pendente.

Validações manuais informadas como OK: alcance por contato e carta de alcance,
conta comum sem cronômetro, ofertas VIP sequenciais, chefe em movimento e HUD
anterior em telas grandes e pequenas. Permanecem pendentes: coleção VIP cheia e
ritmo da EXP 25/40; tela de atributos em tempo real e automação por classe; aviso
de cinco segundos; nova posição da contagem no topo. Prioridade visual atual:
desktop. Controles adaptados para tablets e celulares ficam para depois. Não
foram adicionados nem executados testes automatizados.

### v0.101 — 14/11/2026 — Cartas VIP, tela de atributos, hordas e especializações

O prazo automático de cartas Premium/VIP foi reduzido de 20 para 10 segundos
por oferta. Uma versão de timer persistida permite migrar ofertas antigas uma
única vez, preservando a contagem ao atualizar a página. A recomendação usa
utilidade para a classe, situação da run e raridade; a raridade pesa menos que
um ganho claro de classe. Com coleção cheia, o servidor substitui a carta ativa
de menor utilidade, considerando efeitos e raridade, e mantém a coleção quando
a carta nova é inferior a todas as ativas.

A página de atributos ganhou duas colunas para desktop e identifica a classe no
topo. O cartão menor mostra a EXP que falta para o próximo nível e os cinco
pontos que virão com ele, sem repetir os pontos livres. A área de combate passou
a exibir críticos, cura crítica, esquiva, alcance básico e de habilidade,
reduções, recargas, Vida/Mana e velocidade. Roubo de Vida, dano de projétil do
jogador, dano refletido e dano elemental ainda não têm fórmula própria e são
marcados como não implementados. A automação VIP teve o botão de desativação
reativado após o ACK do Socket.IO.

A árvore preserva os nós anteriores e ganhou quatro caminhos de atributos com
três níveis: cada nó de atributo abre novas opções conectadas, e os novos bônus
são aplicados aos valores permanentes do personagem com validação de teto e
recursos derivados. Uma escolha de especialização aparece no nível 100 e é
salva permanentemente em coluna própria, sem substituir a classe base. Foram
cadastradas as três opções informadas para Guardião, Vigia do Ermo, Tecelão de
Cinzas e Lâmina Rúnica. As habilidades e bônus de combate das especializações
continuam aguardando balanceamento, sem efeitos inventados.

Ondas comuns passam a adicionar um inimigo por onda a cada quatro fases, com
limite de quatro adicionais; semichefe e chefe continuam únicos. Vida escala
3% por fase e 2,5% por onda até +100%; o dano recebido escala 2% por fase e 1%
por onda até +50%. O orçamento fixo de EXP da fase é redistribuído de acordo
com as quantidades novas, sem aumentar o total concedido por fase. Os valores
aguardam validação manual quanto à dificuldade e à duração.

Os guias de progressão, interface, arquitetura, pendências e roadmap foram
atualizados; o índice leve passou a v0.101. Validação manual pendente: timer e
recomendação VIP; troca por utilidade/raridade; EXP 25/40; nova tela de atributos
e toggle VIP; caminhos e bônus da árvore; escolha permanente no nível 100; e
ritmo de quantidade, dificuldade e EXP das hordas. Nenhum teste automatizado foi
adicionado ou executado.

### v0.102 — 14/11/2026 — Árvore de talentos em grafo radial

A representação anterior da árvore como caminhos hierárquicos foi substituída
por um grafo não direcionado com coordenadas X/Y e lista de adjacência. O mapa
tem um ponto central e seis origens setoriais, seis setores conectados por
estradas circulares e radiais, rodas de cinco nós pequenos convergindo para
Notáveis, Keystones externos e Encaixes laterais. Cada personagem escolhe uma
origem sem custo; ela pode ser alterada até o primeiro investimento.

A compra verifica no servidor se uma aresta liga o nó a um nó já ativado desde
a origem. Os bônus de Pequenos e Notáveis são aplicados aos atributos
permanentes; as afinidades desses nós variam de acordo com a classe. Keystones
e Encaixes estão representados e bloqueados até o balanceamento dos efeitos e
a integração dos modificadores de item. Especializações permanecem disponíveis
no nível 100 como escolha separada.

Personagens que já possuíam investimentos na estrutura antiga mantêm os
registros e os custos contabilizados; a página mostra esses registros numa
seção de legado. Foi adicionada a coluna persistente `talent_root_id`, com
migração automática para bancos existentes. O guia de progressão, roadmap,
pendências, índice e README apontam para v0.102. Validação manual pendente:
origens, conexões entre setores, clusters, bônus, bloqueios e persistência.
Nenhum teste automatizado foi adicionado ou executado.

### v0.103 — 14/11/2026 — Árvores exclusivas por classe e evolução no nível 100

As opções genéricas de ponto de partida foram substituídas por seis trilhas
temáticas para cada classe, com núcleo central, nomes, descrições e atributos
principais/secundários próprios: Guardião, Vigia/Arqueiro, Tecelão de Cinzas/
Mago e Lâmina Rúnica/Gladiador Mágico. A tela agora apresenta “Ponto de
partida · Escolha uma trilha da sua classe”. Os nomes genéricos anteriores
permanecem apenas na estrutura v0.102 preservada para históricos e compras
legadas.

No nível 100, a árvore apresenta um botão destacado; ao acioná-lo, abre uma
caixa com três caminhos de evolução da classe. As opções e descrições aprovadas
permanecem: Berserker/Guardião-Bastião/Senhor da Guerra; Atirador de
Elite/Domador de Feras/Arqueiro Arcano; Arquimago/Necromante/Sábio-Erudito;
Lâmina Arcana/Gladiador Etéreo/Forjador de Almas. A escolha é única, permanente
e persistida no personagem. Efeitos de combate das evoluções continuam
pendentes de balanceamento, junto dos Keystones e Encaixes.

README, índice e guias de progressão, interface, arquitetura, roadmap e
pendências apontam para v0.103. A validação manual está pendente para as quatro
árvores, seus atributos, conectividade e compras, e para o botão/caixa de
especialização no nível 100. Nenhum teste automatizado foi adicionado ou
executado.

### v0.104 — 14/11/2026 — Três evoluções exclusivas e troca Premium/VIP

Correção da interpretação v0.103: as seis trilhas adicionais não eram
evoluções aprovadas e foram removidas do mapa atual. Cada classe oferece
exatamente três caminhos, conforme os nomes e descrições definidos pelo
responsável. Ao nível 100, o jogador escolhe um único caminho; somente o ramo
escolhido aceita investimentos, e os outros dois ficam bloqueados.

Conta comum mantém a escolha. Premium/VIP ativo pode trocar o caminho a
qualquer momento, mesmo após o personagem voltar ao nível 1 por Reset. A troca
é transacional: remove os talentos do ramo v0.104 ativo, devolve os custos em
Pontos de Legado e subtrai os atributos desses nós. Ao fim do VIP, o caminho
escolhido continua ativo, mas a troca é bloqueada até reativar o benefício.
Investimentos v0.102/v0.103 foram mantidos como legado e não aparecem como
novos caminhos.

Foi criado `10_registro_de_bugs_e_regressoes.md` para armazenar relatos,
correções, áreas relacionadas e validações manuais pendentes; o índice leve
aponta para ele. Índice, README, roadmap, pendências e guias apontam para v0.104.
Falta validação manual das quatro classes, exclusividade dos ramos e troca VIP.
Nenhum teste automatizado foi adicionado ou executado.

### v0.105 — 14/11/2026 — Controles configuráveis, fallback de combate e câmera

Adicionada à partida a tela de Opções com esquemas **Teclado + Mouse** e
**Apenas Teclado**, quatro espaços de ação editáveis e vínculos configuráveis
dos botões esquerdo/direito. As preferências são persistidas na conta por
migração incremental da tabela `users` e gravadas/sincronizadas por Socket.IO.
As ações únicas existentes permanecem Ataque básico e Corte Rúnico; os espaços
1/3 e 2/4 começam como atalhos duplicados, e o catálogo de novas habilidades
por classe continua pendente em P-018.

As teclas da fileira superior e do Numpad 1–4 usam os espaços correspondentes.
No modo Apenas Teclado, a direção segue o último movimento e o painel superior
acompanha o inimigo mais próximo no alcance/direção; a mira assistida não
dispara sem ação do jogador. Corte Rúnico sem Mana ou em recarga cai para
Ataque básico; servidor valida recarga, distância e dano e comunica o resultado
via Socket.IO.

A câmera recebeu compressão vertical 2.5D e zoom suave na rodinha, com limites
calculados a partir do tamanho da tela e das bordas do mapa. Os parâmetros
ficam no `CAMERA_CONFIG` de `game.js`; a correção de mira/alcance com projeção
requer validação manual P-045. O ângulo e os sprites finais continuam sujeitos
à revisão pós-balanceamento P-033.

README, índice e guias de conceito, interface, arquitetura, roadmap, pendências
e bugs apontam para v0.105. O responsável ainda precisa validar manualmente
esquemas, remapeamentos, Numpad, fallback, alvo e zoom. Nenhum teste
automatizado foi adicionado ou executado.

### v0.106 — 14/11/2026 — Ataque automático no esquema Apenas Teclado

O responsável pediu que, no modo Apenas Teclado, o personagem ataque
automaticamente o inimigo elegível mais próximo à frente. `game.js` agora
consulta o alvo no alcance básico e tenta o Ataque básico conforme a direção do
último movimento, respeitando a recarga local e a validação existente de
`combat:attack`; as habilidades 1–4 seguem manuais. Teclado + Mouse permanece
controlado pelo jogador. A opção Premium/VIP de auto-ataque P-035 continua
separada e pendente para os demais esquemas.

O painel de alvo do modo Apenas Teclado usa o alcance básico. Esta regra foi
substituída em v0.107: o painel continua sendo assistência visual, sem disparar
ataques. Persistência das opções, fallback de magia, atalhos, mira, hitbox e
câmera seguem a validação manual P-045. Nenhum teste automatizado foi adicionado
ou executado.

### v0.107 — 14/11/2026 — Comandos explícitos de combate e substituição manual de cartas

O responsável pediu para remover o ataque básico automático por direção/alvo
assistido. Agora os dois esquemas só atacam após comando do jogador. A tecla 1
sempre executa Ataque básico; 2, 3 e 4 usam as magias dos espaços 1, 2 e 3,
igualmente pela fileira superior e pelo Numpad. Teclado + Mouse permite vincular
os botões esquerdo/direito às magias nos espaços 2–4. Magia em recarga ou sem
Mana mantém o fallback para Ataque básico. P-035, antiga proposta de automação
VIP, fica suspensa até nova aprovação. Migração de banco preserva magias
equipadas e remapeia os vínculos de mouse uma única vez, sem sobrescrever
atalhos personalizados nos reinícios seguintes.

Com a coleção cheia, escolher uma oferta agora abre um passo explícito para
marcar qual carta ativa será removida e confirmar a troca. O destaque visual
marca a carta ativa selecionada. Um botão abaixo das três ofertas permite
manter as cartas atuais e descartar a oferta aberta. Esta escolha manual se
aplica também ao Premium/VIP; a escolha automática por prazo continua separada
e só segue sem intervenção do jogador. As cartas exibidas ficam registradas e
não voltam a ser sorteadas durante a mesma onda; em ondas futuras podem voltar
se continuarem inativas, conforme regra já aprovada.

P-045 e P-046 aguardam validação manual pelo responsável. Atualizados os guias
de conceito, interface, arquitetura, roadmap, pendências, índice e registro de
bugs. Nenhum teste automatizado foi adicionado ou executado.

### v0.108 — 14/11/2026 — Projeção oblíqua e substituição imediata de cartas

A câmera Canvas passou a usar pitch visual de 58° para baixo a partir do
horizonte, aproximado pela escala vertical `cos(58°)`. Piso e efeitos de chão
seguem a inclinação, enquanto personagens, inimigos, nomes e barras permanecem
eretos. O enquadramento mantém o jogador como foco, suaviza o scroll e limita o
zoom para não mostrar fora das bordas do mapa. A projeção é afim 2.5D;
perspectiva 3D real e arte com
profundidade permanecem etapas visuais futuras. P-045 aguarda validação manual
de leitura do personagem/piso, mira, círculos, zoom e limites.

Com a coleção cheia, o primeiro clique numa das três ofertas abre o seletor de
substituição no mesmo quadro, antes da resposta do Socket.IO. A solicitação
continua sendo validada e persistida pelo servidor; até o ACK, a interface
mostra o seletor e mantém desabilitados os botões de confirmação. A lista de
cartas ativas agora mostra nome, raridade e descrição do efeito que será
removido. A escolha de substituir ou manter/descartar continua explícita.
P-046 aguarda validação manual pelo responsável. Atualizados README, índice,
guias de interface/arquitetura, roadmap, pendências e registro de bugs. Nenhum
teste automatizado foi adicionado ou executado.

### v0.109 — 14/11/2026 — Progressão contínua até o nível 400

O responsável aprovou manter o nível máximo em 400, retirar o Reset e não
adotar o nível 1000. A Árvore de Talentos passa a receber 1 Ponto de Legado a
cada 10 níveis e 1 ponto adicional a cada 50 níveis, totalizando 48 no nível
400. O servidor aplica os pontos ao ganhar nível; a migração de personagens
existentes é idempotente, considera nível e Resets históricos e preserva
qualquer saldo/talento já existente.

A rota, o botão, a tela, os indicadores e os textos de Reset foram removidos.
O campo `characters.resets` permanece apenas para compatibilidade dos bancos e
reconstrução de pontos históricos. A Vida dos inimigos cresce 6% por nível
inimigo acima do nível 6 e o dano recebido aumenta 0,65 por nível; ambos param
no nível inimigo 400. A validação manual do ritmo de XP, dificuldade e marcos
permanece pendente em P-047. Não foram criados nem executados testes
automatizados.

Atualizados os guias de progressão, conceito, economia, interface, decisões,
roadmap e pendências. As regras anteriores de Reset permanecem somente como
histórico substituído.

### v0.110 — 14/11/2026 — Passivas, habilidades e prévia de evoluções

A tela `/talentos` agora explica as escolhas por hover e foco de teclado, com
atributos ganhos no ramo, passiva aplicada imediatamente e comparação entre a
habilidade-base e a habilidade assinatura. O caminho completo custa 14 PL:
10 nos nós de atributo e 4 no Keystone. O Keystone já é comprável e substitui a
habilidade-base no espaço salvo do personagem; Encaixes continuam bloqueados.

As quatro classes receberam habilidades-base e cada uma das 12 evoluções ganhou
passiva e habilidade funcional. A passiva modifica as estatísticas reais; o
servidor valida a habilidade ativa e calcula dano, Mana, recarga e efeitos de
cura/retorno de Mana. O espaço do jogador continua salvo na conta, mas a
habilidade selecionada é determinada pelo personagem, evitando incompatibilidade
entre classes.

Adicionados testes unitários e de página para as quatro classes, os 12 caminhos,
custos, atributos, ativação/substituição no Keystone e um ataque de Necromante.
A suíte completa passou com 18 testes. Atualizados README, testes, documentação
de progressão/arquitetura, roadmap e pendências. Os números são candidatos de
balanceamento; escolha/transação, troca VIP e compras web ainda precisam de
testes de integração.

### v0.111 — 14/11/2026 — Árvores únicas e rebalanceamento de Legado

Os 12 caminhos receberam nomes, descrições e modificadores próprios, ligados
aos atributos, passivas, habilidades, dano de projéteis e dano elemental. O
aprimoramento lateral antes indisponível agora é um talento funcional. Cada
caminho custa 48 Pontos de Legado: 42 em atributos, 2 em combate e 4 no talento
principal. Cada classe soma 144 pontos nos três caminhos, mas o personagem só
pode investir no caminho escolhido.

A fórmula permanece `nível // 10 + nível // 50`: 12 pontos no nível 100, 14 no
120 e 48 no 400. Portanto, o ganho atual é suficiente para concluir um caminho,
sem alteração da curva. Na primeira abertura da árvore nova, os talentos
v0.104 comprados são reembolsados uma única vez, incluindo seus custos e
atributos; os nós v0.102/v0.103 continuam registrados como legado.

Atualizados os guias de progressão, arquitetura, interface, decisões aprovadas,
README e instruções da suíte. Os testes cobrem unicidade, custos, modificadores
reais no combate, migração v0.104 e dano elemental/de projéteis. A calibração
subjetiva dos valores continua pendente.

### v0.113 — 15/11/2026 — Calibração de combate e progressão

A Vida-base do personagem foi elevada de 100 para 120 para que todas as classes
iniciais resistam a pelo menos seis golpes comuns. A Vida de comuns, semichefes
e chefes recebeu escalas progressivas em `enemy_max_health`, calibradas com uma
simulação que usa os cálculos de dano compartilhados pelo servidor. Todas as
classes ficaram dentro das metas individuais de TTK nos checkpoints 1/100/220/
400, exceto o Tecelão contra o chefe de Fogo no nível 400: 130 s devido à
resistência de 30%. O responsável escolheu manter essa contrajogada elemental.

Foi criado `scripts/simulate_live_balance.py` e a suíte agora verifica TTK,
sobrevivência inicial, pressão determinística da onda 8, limite de nível e
projeção de XP até o nível 400 (fase 69/5.585 eliminações). O responsável
escolheu manter a horda como desafio de esquiva: o cenário estacionário de 50%
de acertos é letal e exige evitar mais de 90% dos ataques; não se reduziram
densidade, dano ou frequência. Movimento real, duração da horda acima da janela
provisória, builds manuais, cooperação, equipamento e recompensas de endgame
continuam pendentes. A suíte completa passou com 40 testes. Atualizados testes,
guias de progressão/balanceamento, roadmap, pendências e Documento Mestre v0.113.

### v0.112 — 15/11/2026 — Agilidade, crítico e esquiva

Agilidade agora concede 0,01 ponto percentual de chance crítica e 0,01 ponto
percentual de esquiva por ponto. Os bônus são somados aos de talentos, passivas
e cartas antes dos limites de 50% de crítico e 35% de esquiva. A página de
atributos explica esses ganhos e mostra as chances resultantes. O combate já
usava chance crítica para multiplicar o dano por 1,5 e esquiva para anular um
ataque; testes de combate determinísticos agora verificam esses dois caminhos.

O custo da árvore permanece em 48 PL por especialização (42 em atributos, 2 em
aprimoramento de combate e 4 no talento principal). O jogador recebe 48 PL no
nível 400 e pode completar um caminho; as 12 especializações totalizam 576 PL
apenas como soma agregada. Não foram criados novos nós e a fórmula de Legado
não mudou. Atualizados os guias de progressão, decisões aprovadas, roadmap,
README, instruções de testes e Documento Mestre v0.112. Os percentuais ainda
precisam de validação de equilíbrio no jogo.

### Consolidação do Documento Mestre v0.61–v0.110

Em 14/11/2026, os snapshots versionados v0.61 a v0.109 foram consolidados no
único índice mestre ativo v0.110. O histórico individual de todas essas
versões permanece registrado nesta seção; o conteúdo temático está nos guias
01–10 e nos arquivos de balanceamento. A fonte integral v0.55 continua em
`historico/`. Atualizações futuras devem renomear o índice mestre existente e
registrar a mudança aqui, sem deixar uma cópia do índice para cada versão.

### Diretriz atual de testes automatizados — 14/11/2026

Esta decisão substitui a orientação anterior de não criar nem executar testes
automatizados. A suíte ativa fica em `../tests/` e é executada da raiz do
projeto com `python -m unittest discover -s tests -v`. As instruções para a IA
estão em `../tests/README.md`: toda mudança de comportamento deve incluir ou
atualizar testes de regressão, e o conjunto completo deve passar antes de
concluir a tarefa. Se uma área ainda não puder ser testada, amplie o harness
com testes de integração ou simulações determinísticas em vez de solicitar que
o responsável repita verificações manuais.

A cobertura inicial verifica XP, limites de nível, densidade e orçamento de XP
por fase, Pontos de Legado, curva de Vida/dano inimigo e migração idempotente.
Os testes de integração de controles, câmera, talentos, atributos e cartas
permanecem pendentes e devem ser adicionados à mesma suíte; os registros em
`07_roadmap_e_estado_atual.md` e `08_pendencias_e_decisoes.md` acompanham essa
expansão. A aprovação matemática não substitui critérios objetivos de
balanceamento nem a avaliação subjetiva de apresentação visual.
