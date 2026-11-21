# Registro de bugs e regressões

> Registro vivo de falhas observadas, correções e validações manuais. Consulte
> o [Documento Mestre v0.139](Cronicas_do_Recomeco_Documento_Mestre_v0.139.md)
> e o guia temático indicado antes de alterar uma área afetada.
>
> Atualizado em: 15/11/2026 21:54:32 (UTC−03:00).

Este arquivo mantém um histórico consultável para evitar repetir tentativas,
perder a causa de uma regressão ou corrigir um sistema sem rever seus efeitos
nos sistemas ligados a ele. Registra relatos do responsável; não substitui o
roadmap de funcionalidades.

## Como registrar e revisar

Para cada ocorrência, anotar: ID, data/versão, tela ou sistema, passos para
reproduzir, resultado esperado, resultado observado, causa confirmada ou
hipótese, correção, áreas que podem regredir e resultado do teste manual feito
pelo responsável. Se a causa for hipótese, identificá-la como hipótese.

Usar estes estados:

- **Aberto:** ainda ocorre ou não foi investigado.
- **Corrigido — validação pendente:** alteração feita; falta o responsável
  reproduzir o cenário manualmente.
- **Resolvido — validado manualmente:** o responsável confirmou a correção.
- **Monitorar:** houve correção ou mitigação, mas falta reteste específico ou
  observação suficiente para encerrar.

Ao corrigir um bug, revisar efeitos colaterais nos serviços relacionados e
atualizar este registro, o guia técnico e o roadmap. Cada correção deve incluir
ou atualizar um teste de regressão em `tests/`; execute
`python -m unittest discover -s tests -v` antes de encerrar a correção. Se a
falha ainda não puder ser reproduzida automaticamente, estenda a suíte em vez
de pedir repetição manual ao responsável.

## Ocorrências registradas

### BUG-001 — Opções de evolução excediam os três caminhos aprovados

- **Área/versão:** Árvore de Talentos, v0.103.
- **Relato:** a tela apresentava seis trilhas extras por classe além das três
  evoluções aprovadas, dando a entender que havia várias classes/caminhos a
  escolher.
- **Esperado:** cada classe tem exatamente três evoluções. O personagem escolhe
  uma; as outras duas ficam fechadas.
- **Correção v0.104:** o mapa agora contém somente esses três ramos. A escolha
  ocorre uma vez ao alcançar o nível 100; só o ramo selecionado aceita pontos.
  Uma conta Premium/VIP ativa pode trocar de ramo. A troca remove os talentos
  comprados no ramo atual e devolve seus Pontos de Legado e atributos.
- **Áreas de regressão:** saldo de Pontos de Legado, atributos derivados, Vida,
  Mana, persistência da especialização, interface VIP e nós antigos preservados
  como legado.
- **Cobertura automatizada:** testes de integração cobrem compra, bloqueio,
  recusa sem VIP, troca VIP com reembolso e persistência nas quatro classes.
- **E2E em navegador v0.120:** escolha, compra, bloqueio visual do ramo
  incompatível, persistência após recarga e troca VIP com reembolso foram
  confirmados nas quatro classes, usando conta e banco descartáveis.
- **Estado:** integração e E2E cobrem as quatro classes. A calibração das
  magnitudes não faz parte deste reteste; permanece em P-042/P-047.

### BUG-002 — Orbe acompanhava o personagem sem conceder EXP / mensagem de distância

- **Área:** coleta de orbes e atualização da coleção por Socket.IO.
- **Relato:** após atrair o orbe e correr, a coleta podia exibir “Chegue mais
  perto”; também houve caso do orbe seguir sob o personagem sem conceder EXP.
- **Correção relatada:** ajuste do alcance/posição de coleta, velocidade de
  atração e identificação da coleta; o responsável depois informou que estava
  funcionando corretamente.
- **Áreas relacionadas:** posição de morte do monstro, estado de coleta no
  servidor, EXP de cartas, ofertas e sincronização Socket.IO.
- **Estado:** resolvido — validação manual informada pelo responsável.

### BUG-003 — Carta clicada era recusada como indisponível

- **Área:** seleção de ofertas de cartas.
- **Relato:** clicar numa oferta podia retornar que a carta não estava
  disponível, mesmo aparecendo na tela.
- **Correção relatada:** sincronização da oferta/estado selecionado entre cliente
  e servidor foi ajustada durante as correções de cartas.
- **Áreas relacionadas:** ofertas acumuladas, troca com coleção cheia, prazo VIP,
  atualização da página e ACK Socket.IO.
- **Estado:** monitorar; a correção foi implementada, mas falta confirmação
  manual específica após a última ocorrência.

### BUG-004 — Contagem mostrava monstros restantes depois de a onda terminar

- **Área:** transição de ondas e contagem de inimigos em tempo real.
- **Relato:** a próxima onda podia mostrar inimigos restantes sem monstros na
  arena; eles só apareciam após atualizar a página.
- **Correção relatada:** sincronização da criação da próxima horda e da contagem
  pelo servidor/Socket.IO foi ajustada.
- **Áreas relacionadas:** persistência de inimigos, transição da onda, HUD e
  recuperação após recarga.
- **Estado:** monitorar; não há reteste manual específico registrado para a
  última alteração.

### BUG-005 — SQLite ocupado durante ataques concorrentes

- **Área:** gravação de combate em `game_app/socket_events.py`.
- **Relato:** `sqlite3.OperationalError: database is locked` em
  `attack_enemy` ao iniciar uma transação.
- **Mitigação registrada:** SQLite em WAL com espera por gravações concorrentes
  de até 15 segundos.
- **Áreas relacionadas:** ataque, movimento, dano recebido, orbes, EXP e
  transições persistidas por Socket.IO.
- **Estado:** monitorar; falta observar combate prolongado e confirmar que o
  erro não volta em uso manual.

### BUG-006 — `/jogo` falhava quando o banco não tinha `phase_xp_budget`

- **Área:** compatibilidade do estado de fase ao abrir a sala.
- **Relato:** `IndexError: No item with that key` ao ler
  `character["phase_xp_budget"]` em banco antigo.
- **Correção relatada:** leitura/migração do campo foi adaptada para estado
  anterior do banco.
- **Áreas relacionadas:** início/retomada de fase, orçamento de EXP e migrações
  SQLite.
- **Estado:** monitorar; não houve nova ocorrência relatada, mas falta reteste
  manual com o banco local atualizado e uma retomada de fase.

### BUG-007 — Movimento ficava preso ao terminar a fase com cartas abertas

- **Área:** controles e transição para a pausa de fim de fase.
- **Relato:** ao continuar andando com ofertas abertas perto do fim da horda,
  o personagem podia ficar preso depois de escolher uma carta.
- **Correção relatada:** limpar entradas mantidas na transição, sem pausar o
  mundo ao abrir cartas; movimento com cartas abertas permaneceu liberado.
- **Áreas relacionadas:** WASD/setas, Avanço, ofertas, chefe, pausa e botões de
  preparar a próxima fase/voltar à Sala de Espera.
- **Estado:** resolvido — o responsável marcou o teste manual de movimento com
  cartas abertas e de fim de fase como OK.

### BUG-008 — Pontos de atributo pareciam não alterar o personagem

- **Área:** distribuição de atributos e estatísticas reais de combate.
- **Relato:** pontos eram distribuídos sem diferença perceptível em Força,
  Agilidade, Vitalidade ou Energia.
- **Correção registrada:** atributos foram conectados às fórmulas de dano,
  Vida, Mana, recarga e movimento; a tela passou a exibir efeitos derivados.
- **Áreas relacionadas:** atributos, talentos, nível, equipamentos e HUD de
  combate.
- **Estado:** Força foi validada manualmente: o dano mudou de 31,0 para 31,5 em
  tempo real e continuou igual após recarga. Testes automatizados agora cobrem
  alocação dos quatro atributos, distribuição automática VIP nas classes,
  persistência e eventos Socket.IO; a E2E também confirmou notificações. Isso
  valida os fluxos, não o balanceamento dos atributos em combate ativo. As
  magnitudes e a experiência de combate continuam pendentes de calibração em
  P-031/P-047.

### BUG-009 — O servidor Flask não iniciava por erro de indentação

- **Área/versão:** inicialização de `app.py`, no começo do projeto.
- **Relato:** Python encerrava a execução com `IndentationError` em uma rota.
- **Correção relatada:** organização do código e arquivos por módulos corrigiu
  a indentação.
- **Validação informada:** cadastro e login foram testados pelo responsável.
- **Estado:** resolvido — validação manual informada.

### BUG-010 — Vida e Mana voltavam cheias ao atualizar a partida

- **Área:** persistência de estado do personagem e HUD.
- **Relato:** após receber dano e gastar Mana, atualizar a página mostrava
  recursos cheios; a falta de Mana só era percebida ao tentar conjurar e a Vida
  anterior aparecia depois de outro golpe.
- **Correção relatada:** Vida/Mana atuais são persistidas no servidor e a tela
  carrega os valores salvos; atualizações de combate usam Socket.IO.
- **Áreas relacionadas:** dano, habilidades, recarga, morte, nível e
  restauração de recursos.
- **Estado:** monitorar; retestar manualmente após dano, gasto de Mana e recarga
  da página.

### BUG-011 — Partida retomada sem monstros após reiniciar o servidor

- **Área:** carregamento e reconstrução da horda persistida.
- **Relato:** ao abrir a onda 1 depois de reiniciar `app.py`, a arena aparecia
  vazia.
- **Correção relatada:** o fluxo de carregamento/criação de inimigos foi
  ajustado; o responsável prosseguiu jogando depois da correção.
- **Áreas relacionadas:** transição de onda, reinício de fase, persistência e
  contador de inimigos.
- **Estado:** monitorar; reproduzir manualmente após reiniciar o servidor.

### BUG-012 — Chefe permanecia parado durante o combate

- **Área:** movimento e reposicionamento do chefe.
- **Relato:** o chefe atacava sem se deslocar.
- **Correção relatada:** comportamento de movimento e reposicionamento foi
  implementado; o responsável informou que confirmou o movimento do chefe.
- **Áreas relacionadas:** IA, telegráficos de ataque, colisão e leitura de
  padrões.
- **Estado:** resolvido — validação manual informada.

### BUG-013 — Prévia de evolução falhava com habilidades supremas

- **Área/versão:** prévia da Árvore de Talentos, v0.117.
- **Relato:** abrir a prévia de evolução lançava erro ao interpretar a lista de
  habilidades supremas.
- **Causa confirmada:** o JSON no atributo HTML não preservava corretamente as
  aspas delimitadoras.
- **Correção:** escapar a saída JSON no atributo e adicionar teste de regressão.
- **Áreas relacionadas:** seleção de evolução, nomes de habilidades supremas e
  prévias das classes.
- **Estado:** resolvido — teste de regressão aprovado e fluxo de evolução
  exercitado no navegador.

### BUG-014 — Resumo de combate perdia bônus da evolução após recarga

- **Área/versão:** página de atributos, v0.117.
- **Relato:** o resumo de combate após recarga divergia do valor mostrado após
  uma atualização de atributo em tempo real.
- **Causa confirmada:** consultas da tela e da distribuição não carregavam
  `specialization_id`, omitindo efeitos da evolução.
- **Correção:** incluir a evolução ativa nas consultas; unificar a vírgula
  decimal entre HTML inicial e atualizações Socket.IO; adicionar regressão.
- **Áreas relacionadas:** atributos, especializações, talentos, bônus de carta
  e apresentação de números pt-BR.
- **Estado:** resolvido — testes aprovados e valor conferido antes/depois da
  recarga no navegador.

### REG-013 — Integração de controles, alvo, fallback e zoom

- **Tipo:** conjunto de regressões a observar; nenhum defeito foi relatado ainda.
- **Área/versão:** controles de combate e câmera Canvas, regra atualizada em v0.108.
- **Mudanças relacionadas:** esquema Teclado + Mouse/Apenas Teclado,
  teclas Digit/Numpad 1–4, atalhos do mouse, fallback para ataque básico,
  alvo assistido e projeção/zoom da câmera.
- **Riscos de regressão:** mudança de zoom pode deslocar mira, hitbox, círculos
  de alcance, seleção pelo cursor e labels de dano; opção pode perder
  persistência/estado entre abas; entradas de movimento não devem atacar sem
  comando; tecla 1 não pode deixar de ser Ataque básico; teclas 2–4 precisam
  apontar para magia 1–3; fallback não pode aplicar dano/recarga incorretos;
  transições com cartas abertas podem reter entradas.
- **Validação manual parcial:** opções e atalhos do mouse persistiram após
  recarga; WASD moveu o personagem durante a preparação e o scroll aproximou a
  câmera. Ainda seguir os cenários restantes de P-045 em
  `07_roadmap_e_estado_atual.md`: ataques, Numpad, alvo, fallback, pitch,
  limites e diferentes resoluções.
- **Estado:** parcialmente validado; não tratar como bug confirmado.

### REG-014 — Confirmação de substituição e descarte de oferta de cartas

- **Tipo:** conjunto de regressões a observar; nenhum defeito foi relatado ainda.
- **Área/versão:** ofertas Socket.IO, coleção temporária, v0.108 (P-046).
- **Mudanças relacionadas:** selecionar uma carta com coleção cheia abre
  imediatamente o seletor local e envia a intenção ao servidor; cada carta
  ativa mostra nome, raridade e descrição do efeito atual; a confirmação só
  é liberada após a validação do servidor. O botão abaixo das três ofertas
  mantém a coleção e descarta a oferta corrente.
- **Riscos de regressão:** equipar a oferta antes de selecionar/confirmar a
  remoção; remover carta diferente da marcada; descartar oferta e também perder
  carta ativa; repetir opções já mostradas durante a mesma onda; timer VIP
  competir com escolha manual; submit duplicado ou divergência entre ACK e
  evento de estado.
- **Validação manual parcial:** numa coleção VIP 8/8, uma substituição explícita
  foi confirmada e permaneceu após recarga; a oferta seguinte escolheu a
  recomendação automaticamente pelo prazo, mantendo oito cartas. Ainda testar
  coleção comum, descarte, opções repetidas e ofertas sequenciais. Ver P-046 em
  `07_roadmap_e_estado_atual.md`.
- **Estado:** parcialmente validado; não tratar como bug confirmado.

### BUG-015 — Inimigos paravam de atacar após pedidos telegráficos expirados

- **Área/versão:** ciclo de ataques inimigos por Socket.IO, v0.120.
- **Relato:** após morrer repetidas vezes e voltar à partida, os monstros
  cercavam o personagem, mas em algum momento paravam de atacar.
- **Causa confirmada:** o servidor verificava se já havia ataque pendente antes
  de limpar ataques expirados. Como o pedido expirado continuava marcado como
  pendente, novos pedidos do mesmo inimigo eram bloqueados indefinidamente.
  No cliente, a ausência de ACK também podia deixar o pedido marcado como ativo.
- **Correção:** limpar registros expirados antes da checagem de bloqueio; liberar
  o estado do pedido no cliente após 5 segundos sem resposta e ao desconectar;
  ignorar callbacks atrasados e aplicar intervalo curto quando o servidor
  informa que ainda há ataque pendente.
- **Correção relacionada à fuga do cerco:** Avanço atravessa inimigos, e o
  movimento comum desliza no eixo não bloqueado. Isso não altera a colisão
  normal nem permite atravessar inimigos com movimento comum.
- **Áreas de regressão:** telegráficos, ACK Socket.IO, timeout, reconexão,
  ataques repetidos, colisão, movimento e Avanço.
- **Validação:** teste de regressão reproduziu o bloqueio antes da correção e
  passou após a alteração; suíte completa v0.120 passou com 65 testes. E2E em
  servidor e banco descartáveis confirmou que inimigos voltaram a atacar após
  reiniciar e que o personagem conseguiu atravessar o cerco com Avanço. Não foi
  alterado o save real do responsável.
- **Estado:** corrigido; validação em save real após disponibilização ao
  responsável permanece pendente.

### BUG-016 — A tela da missão falhava ao carregar o JavaScript do jogo

- **Área/versão:** inicialização de `game.js`, fluxo de missões P-048, v0.124.
- **Sintoma observado:** ao iniciar uma missão no navegador, o script lançava
  `ReferenceError: state is not defined` antes de registrar os eventos Socket.IO.
- **Causa confirmada:** o redirecionamento de missão concluída lia `state` no
  escopo global, fora do callback que recebe o estado do servidor.
- **Correção:** mover a checagem de conclusão para o callback
  `combat:enemy_updated`, onde o estado recebido existe, e retornar após iniciar
  a navegação para a tela pós-fase.
- **Áreas de regressão:** carregamento do jogo, conexão Socket.IO, contagem
  regressiva, transições de onda/fase e redirecionamento de conclusão.
- **Validação:** reproduzido na primeira abertura de `/jogo`; após a correção,
  recarga no navegador isolado conectou ao Socket.IO e não emitiu `pageerror`.
  A suíte Python completa passou com 76 testes, mas não executa JavaScript.
  E2E posterior em navegador e banco descartável percorreu as dez ondas da
  Fase 10 até o chefe, confirmou o modal e resgatou três baús. A progressão
  anterior foi pré-carregada e os ataques foram acelerados por harness; isso
  valida o fluxo da tela corrigida, não gameplay representativo. Em v0.133,
  três E2E Playwright adicionais executaram Flask/Socket.IO reais nos riscos
  Moderado, Alto e Extremo, cobrindo contagem, movimento, Ataque básico e dano
  inimigo na primeira onda; outro cobriu mochila cheia, venda e resgate. Em
  v0.134, E2E adicionais percorreram as dez ondas da Fase 10 em Moderado, Alto
  e Extremo, concluíram o chefe e abriram a tela pós-fase; houve dano inimigo
  durante as execuções de 66–80 s. O harness usou nível 400, atributos no teto
  e coordenadas de alvo, não controles humanos. A suíte JavaScript passou com
  10 testes; a suíte Python passou com 84 e `compileall` sem erros.
- **Estado:** corrigido; inicialização e fluxo integrado P-048 exercitados no
  navegador, inclusive a conclusão E2E automatizada nos outros riscos e o
  combate prolongado com harness. Movimento/esquiva/mira humana, avaliação
  manual de equilíbrio e aprovação dos valores candidatos permanecem fora
  dessa validação.

## Revisão periódica

Antes de encerrar uma etapa, rever bugs abertos, corrigidos pendentes e em
monitoramento que toquem os arquivos/sistemas alterados. Ao confirmar que um
problema voltou, reabrir o mesmo ID e registrar os novos passos observados em
vez de criar uma ocorrência duplicada.
