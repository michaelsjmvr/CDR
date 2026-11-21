# Suíte de testes

> Atualizado em: 15/11/2026 21:54:32 (UTC−03:00).

Execute a suíte automatizada de regressão na raiz do projeto:

```powershell
python -m unittest discover -s tests -v
```

Os testes do cliente JavaScript são separados e requerem Node.js 20 ou superior,
além do Chromium gerenciado pelo Playwright. Na primeira execução:

```powershell
npm install
npx playwright install chromium
npm run test:js
```

Se o interpretador selecionado não tiver as dependências do projeto, instale-as
antes de executar:

```powershell
python -m pip install -r requirements.txt
```

A suíte usa o `unittest` do Python e os módulos reais do jogo. Os testes de
banco criam uma base SQLite temporária e isolada; não alteram a base de
desenvolvimento nem dados de jogadores.

## Cobertura

- Limiares de EXP, limite de nível, distribuição de EXP por fase, quantidade de
  inimigos e marcos de Pontos de Legado, incluindo a gravação ao subir de nível.
- Vida dos inimigos e dano recebido nos níveis 6/100/220/400, limite do nível
  400, metas calibradas de tempo para derrotar e projeção de EXP até o nível
  máximo.
- Simulação determinística ligada aos cálculos reais do servidor: dano,
  recargas, Vida, dano inimigo, distribuição de atributos e densidade das ondas.
  Mede comuns, semichefes, sobrevivência inicial, resistência elemental e
  pressão da horda parada.
- Migração idempotente de Pontos de Legado para personagens existentes,
  preservando saldos maiores que o crédito retroativo.
- As 12 árvores únicas de especialização, seus 714 Pontos de Legado somados,
  custos individuais de 58 ou 64 pontos, modificadores de combate e passivas.
- Desbloqueio e maestria próprios para cada habilidade suprema, maestrias para
  habilidades-base e assinaturas, e loadout de até três habilidades com no
  máximo uma suprema.
- Chance crítica e esquiva por Agilidade, acúmulo com talentos, limites e
  resultados determinísticos em eventos de combate.
- Conteúdo da página de talentos por classe, reembolso único de talentos v0.104,
  substituição da habilidade no talento principal e teste autenticado de cura
  do Necromante em combate.
- Tipos de dano, resistência elemental dos chefes, projéteis que só causam dano
  ao atingir, bônus de projétil/elemental, roubo de 5% de Vida e reflexão de 10%
  do dano, incluindo abates por reflexão e recompensas da onda.
- Impacto das habilidades supremas: alvos próximos atingidos por habilidades de
  área/encadeamento, atração e imobilização, repulsão, invocação temporária de
  sombras após um abate e limites de alvos.
- Catálogo de cartas: efeitos novos de projétil, dano elemental, Mana por abate
  e cura de habilidades; aumento de dano real e recomendações coerentes com a
  especialização, a passiva e a habilidade assinatura liberada.
- Missões P-048: desbloqueio em cascata de fases/dificuldades, crédito idempotente
  de moeda virtual, criação e resolução de staging com limite de inventário,
  autorização das rotas, bloqueio de ataques durante a contagem e conclusão
  pela última onda. Testes determinísticos percorrem os quatro perfis para Vida
  e dano em ondas comuns, semichefes e chefes, quantidade de inimigos, Ouro,
  bônus de fase/chefe, chances e pesos de raridade. Um teste de rota verifica o
  HTML dos quatro perfis candidatos no lobby. Os testes de rota confirmam a
  presença do modal e o bloqueio do retorno enquanto houver espólios; esses
  testes de rota não executam JavaScript nem navegador.
- JavaScript do cliente: `node --check` verifica todos os scripts first-party
  em `game_app/static/js/` (exclui arquivos vendorizados). Playwright executa
  dois fluxos com os scripts reais em Chromium: seleção de fase por dificuldade
  e diálogo/capacidade dos espólios. As páginas usam HTML mínimo de teste; não
  carregam os templates Flask, o backend ou Socket.IO e não são E2E completo.
- E2E Playwright adicional: servidor Flask/Socket.IO real, sessão autenticada e
  SQLite temporário; nos riscos Moderado, Alto e Extremo, valida contagem,
  movimento por teclado, Ataque básico e dano inimigo recebido na primeira
  onda. O progresso anterior é preparado para liberar os riscos; não percorre
  as dez ondas nem testa desbloqueio natural entre dificuldades.
- E2E de fase completa em v0.134: percorre as dez ondas da Fase 10 nos três
  riscos adicionais, derrota o chefe e alcança a tela pós-fase. O servidor usa
  SQLite temporário e ataques Socket.IO reais; o harness prepara progressão,
  nível 400, atributos no teto de 10.000 e coordenadas de alvo. O fluxo dura
  cerca de 66–80 s e recebe ataques inimigos, mas não é gameplay representativo
  nem mede sensação de dificuldade/recompensa. A decisão v0.135 estabelece
  170 como teto-alvo; o fixture 400 só valida integração e deverá ser revisto
  quando o novo balanceamento for implementado.
- E2E de inventário cheio: inicia com 30/30, abre os espólios reais, vende um
  item antigo, resgata o baú e confirma a ocupação atualizada. Não valida
  visualmente a apresentação nem calibra valor de venda ou recompensas.
- E2E do mapa da Fase 1: com Flask/Socket.IO e sessão real em banco temporário,
  inicia a missão, confirma o carregamento da imagem atual (1.200 × 896 px) no
  Canvas, o recorte desenhado na origem do viewport e que o jogador para em um
  colisor do mapa. O fluxo `/mapas/terminal-vilar-fase1` verifica a mesma arte,
  as dimensões do Canvas (2.400 × 1.800), retângulos, polígonos, paredes e o
  botão de depuração. `tests/test_terminal_vilar_map.py` testa
  os colisores aproximados e garante que os spawns da Fase 1 evitem os
  obstáculos. Para validar somente essa área, sem executar cenários de outras
  fases, use:

  ```powershell
  python -m unittest discover -s tests -p test_terminal_vilar_map.py -v
  node --check game_app\static\js\game.js
  node --test --test-name-pattern="phase one|Terminal de Vilar preview" tests\js\mission-app-e2e.test.cjs
  ```

  Esta cobertura é automatizada, não uma avaliação percentual de semelhança ou
  revisão visual manual. O artefato e os colisores continuam candidatos sem
  aprovação final; cada execução desta tarefa limitou-se à Fase 1.
  O editor local de colisores/limites e a integração de arte/efeitos v0.139
  ainda não têm cobertura automatizada específica. As asserções E2E foram
  atualizadas para a imagem e a interface atuais, mas não foram executadas a
  pedido do responsável; as evidências anteriores referem-se à versão
  precedente.
- Ouro P-048: formatação em valores inteiros, apresentação na carteira, crédito
  idempotente, venda e migração de dados do esquema legado sem perda dos valores.
- Campanha/lobby: os três grupos de fases cobrem Ato 1 (1–10), Ato 2 (11–20)
  e Ato 3 (21–30); a resposta do lobby não exibe saldo/ocupação, enquanto a
  página `/inventario` mostra Ouro da conta e capacidade.

Na validação de 15/11/2026 v0.124, a suíte automatizada passou com
**76 testes**, incluindo cinco testes focados em P-048. Os testes Python não
executam o JavaScript nem o navegador.

Na validação v0.126, a suíte completa passou com **78 testes**. O saldo agora
é Ouro inteiro por conta; a migração renomeia o esquema legado e preserva os
valores numéricos. O teste não valida calibração econômica nem pagamentos reais.

Na validação v0.127, a suíte completa passou com **78 testes** e `compileall`
concluiu sem erros. Os testes de rota cobrem os grupos de atos na Sala de
Espera e a exibição conjunta de saldo/ocupação em `/inventario`. Não foi feita
validação visual autenticada no navegador nesta rodada.

Na validação v0.128, a suíte completa passou com **82 testes** e
`python -m compileall -q game_app tests` concluiu sem erros. Os testes cobrem
deterministicamente as escalas dos quatro riscos em encontros comuns,
semichefes e chefes, as quantias/regras de recompensa e a renderização do painel
informativo no lobby. Esse teste verifica HTML gerado pelo Flask, não a
aparência em navegador. Não houve E2E visual autenticado nem calibração em
combate real nesta rodada.

Na validação v0.130, `npm run test:js` passou com **3 verificações** em Node.js
24.20.0 e Chromium: uma checagem agregada da sintaxe dos scripts first-party e
dois fluxos reais no navegador (seletor de fases e capacidade/diálogo de
espólios). Os fluxos passam pelos scripts de produção e exercitam eventos,
estado de controles e a interação com o diálogo nativo. Não carregam templates
reais nem servidor Flask, não exercitam Socket.IO, autenticação ou a missão
completa; também não equivalem a revisão visual manual.

A validação Python v0.130 permaneceu em **82 testes aprovados**. Não foi
executado novo E2E autenticado da missão completa nesta rodada.

Na validação v0.131, a suíte Python passou com **84 testes** e
`python -m compileall -q game_app tests` concluiu sem erros. Dois testes novos
garantem que a conta não inicie missões simultâneas em personagens diferentes
e que espólios pendentes suspendam uma run ativa em outra sessão. Nenhum valor
de balanceamento foi calibrado ou aprovado nesta validação.

Na validação documental v0.132, a suíte Python foi reexecutada e passou com
**84 testes**; `compileall` também concluiu sem erros. `npm run test:js` não
pôde ser executado porque Node.js/npm não estavam disponíveis nesta sessão.

Na validação v0.133, `npm run test:js` passou com **7 testes** em Node.js
24.20.0/Chromium: sintaxe agregada dos scripts first-party, dois fluxos isolados
em HTML mínimo, três cenários E2E Flask/Socket.IO nos riscos adicionais e um
E2E de inventário cheio. Node estava no cache WinGet, fora do PATH, e foi
chamado pelo caminho local; nenhum pacote foi instalado. A suíte Python passou
com **84 testes** e `python -m compileall -q game_app tests` concluiu sem erros.
Não houve alteração no código de gameplay.

Na validação v0.134, `npm run test:js` passou com **10 testes**, incluindo
execução completa da Fase 10 em Moderado, Alto e Extremo, da contagem até o
chefe e a tela pós-fase. Os cenários duraram 66–80 s e registraram ataques
inimigos. O harness semeou desbloqueios e usou nível 400, atributos no teto de
10.000 e coordenadas de alvo; não valida jogo natural nem sensação de
dificuldade. A suíte Python passou com **84 testes** e `compileall` sem erros.
`simulate_live_balance.py` foi reexecutado; seus resultados matemáticos não
representam combate manual nem aprovam parâmetros.

Na validação v0.136, `npm run test:js` passou com **12 testes** em Node.js
24.20.0/Chromium. Os dois novos E2E cobrem a integração visual da Fase 1 no
Canvas real da missão e a rota da prévia paramétrica. A suíte Python passou com
**84 testes** e `python -m compileall -q game_app tests` concluiu sem erros.
A prévia foi inspecionada visualmente; a composição integrada ainda precisa
de revisão visual e nada disso aprova a arte final.

Na validação focada v0.137, `python -m unittest discover -s tests -p
test_terminal_vilar_map.py -v` passou com **2 testes**; `node --check` passou
para `game.js` e `mission-app-e2e.test.cjs`; Playwright passou com **2 E2E**
selecionados pelo nome (missão Fase 1 e prévia); `compileall` passou nos módulos
Python alterados. Nenhuma fase além da Fase 1 foi exercitada. A prévia foi
inspecionada visualmente em servidor temporário; a cena de gameplay foi
verificada por automação, não por revisão visual manual. O teste comprova o
carregamento da imagem original, não um percentual de semelhança ou aprovação
da arte.

A E2E v0.125 (anterior às alterações monetárias e de interface v0.126–v0.127),
executada em navegador com banco descartável, percorreu a Fase 10 desde a Onda 1
até o chefe da Onda 10, usando ataques
Socket.IO reais; o modal foi exibido e três Baús de Recompensa foram resgatados.
O progresso das Fases 1–9 foi pré-carregado para liberar a Fase 10; atributos
elevados e coordenadas enviadas pelo harness aceleraram os ataques. Essa
execução não faz parte da suíte Python e não valida progressão natural,
movimento, mira manual, IA, ritmo representativo, equilíbrio das recompensas
ou aprovação dos parâmetros candidatos.
O navegador não foi revalidado após a troca do rótulo monetário por Ouro. A
interface v0.127 foi verificada por testes de rota, não por E2E visual. O painel
informativo dos quatro perfis v0.128 também foi verificado no HTML renderizado,
sem novo E2E visual autenticado. Os cenários v0.133 executam fluxos no navegador
autenticado, mas não fazem avaliação visual manual.

## Como ampliar

Ao alterar ou adicionar comportamento, crie um teste de regressão específico no
arquivo `test_*.py` correspondente antes de considerar a mudança concluída.
Crie um módulo quando o recurso pertencer a uma área distinta. Os testes devem
exercitar funções usadas pelo jogo, sem fórmulas copiadas, bancos reais,
serviços de rede ou etapas manuais. Depois, execute a suíte completa e corrija
as falhas; não ignore nem enfraqueça as verificações afetadas.

Ao alterar scripts JavaScript do cliente, atualize os casos em
`tests/js/browser-flows.test.cjs` e execute `npm run test:js`. Essa suíte roda
em Chromium, mas seus fluxos isolados não devem ser classificados como E2E do
aplicativo.

Quando um comportamento for difícil de automatizar, amplie o conjunto de testes
com um cliente de teste ou uma simulação determinística, em vez de pedir que a
pessoa responsável repita verificações manuais. Avaliação visual e sensação de
jogo devem ser registradas à parte; não substituem critérios automatizados.

Execute `python scripts/simulate_live_balance.py` para obter o relatório
completo por classe e marco. A simulação usa atributos automáticos, cadência
perfeita de ataques e nenhum equipamento, carta ou talento comprado. A pressão
da horda considera o personagem parado. O cenário com 50% de acertos é uma
prova de estresse, não uma previsão do movimento ativo nem uma recomendação
para ficar parado.
