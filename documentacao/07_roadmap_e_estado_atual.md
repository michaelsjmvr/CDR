# Roadmap e estado atual

> Guia temático iniciado a partir do Documento Mestre v0.55 e atualizado com decisões posteriores. Consulte `Cronicas_do_Recomeco_Documento_Mestre_v0.139.md` para navegar entre assuntos.
>
> Atualizado em: 15/11/2026 21:54:32 (UTC−03:00).


## 18. Escopo por etapas

As etapas abaixo são uma organização inicial sugerida, não um cronograma
aprovado.

### Legenda das tarefas

-   `[x]` Concluído e validado.
-   `[~]` Implementado ou em andamento, mas ainda não validado/concluído.
-   `[ ]` Ainda não iniciado ou aguardando decisão.

## Estado atual após v0.139 — campanha, progressão, missões e mapa

O código de campanha e combate permanece conforme as validações anteriores;
v0.134 amplia a automação E2E. Nesta versão, a arte de referência e os
colisores aproximados da Fase 1 foram integrados ao Canvas e à prévia. A prévia
local agora permite editar colisores e limites de movimento/spawn e persistir
a configuração JSON, utilizada pelo cliente e pelo servidor. O mundo continua
em 2.400 × 1.800; apenas a Fase 1 usa os limites personalizados. O salvamento
é local e protegido por CSRF.

**Decisão v0.135:** o teto-alvo passa a ser 170, com rebalanceamento de XP,
Pontos de Legado e combate para a campanha de 30 fases. É uma direção decidida,
mas ainda não implementada: o código continua com teto 400 e nenhuma fórmula
ou recompensa nova foi aprovada. A projeção antiga de nível 170/26 PL e as
simulações até 400 não são calibração para essa meta.

- Implementadas 30 fases, dez ondas por fase, nove temas visuais e a
  cadência de semichefes nas fases 5/15/25 e chefes de ato nas fases 10/20/30.
  A conclusão da Fase 30 é persistida e não avança para a 31; personagens já
  salvos além da 30 são marcados como concluídos sem perda de progresso.
- O mapeamento usa uma arena lógica única. Os temas dos Atos 2 e 3 são
  provisórios e não equivalem a mapas com geometria, hazards ou lore próprios.
  O guia narrativo cobre as Fases 1–10; as Fases 11–30 ainda precisam de roteiro.
- A simulação anterior projetava nível 170 e 26 Pontos de Legado ao fim da
  Fase 30; esse resultado será recalculado para a nova meta. A extrapolação
  anterior ao nível 400 na fase 69/6.502 abates e o chefe teórico da fase 70
  são históricos, não metas vigentes.
- O modo solo é funcional; cooperativo de até três jogadores e combinações
  livres de classes são direção aprovada, não funcionalidade implementada.
- A validação automatizada inclui testes de estrutura da temporada, encontros,
  orçamento de XP e encerramento/migração da Fase 30. O smoke test em navegador
  conferiu a tela de conclusão após recarga em banco descartável; o fluxo
  integral de combate da Fase 30 ainda não teve E2E visual. Em v0.134, Python
  passou com 84 testes, `compileall` passou e `npm run test:js` passou com 10
  testes. Três E2E completaram a Fase 10 em Moderado/Alto/Extremo e duraram
  aproximadamente 66–80 s cada. A simulação calculou TTK e cenários de horda,
  mas não substitui avaliação humana.
- O fluxo de missões P-048 está implementado: bloqueios de dificuldade/fase e
  de run concorrente por conta no servidor, contagem regressiva de 5 segundos,
  crédito de Ouro inteiro por conta,
  staging de baús e resolução de inventário. Na validação original v0.124, a
  suíte passou com 76 testes, incluindo cinco casos focados. Um E2E em navegador com banco
  descartável percorreu as dez ondas da Fase 10, por ataques Socket.IO, até o
  chefe de ato, modal, recompensa e resgate de três baús. O E2E precedeu a
  troca do rótulo monetário por Ouro e não validou essa apresentação. O progresso das
  Fases 1–9 foi pré-carregado para liberar a Fase 10; atributos elevados e
  coordenadas fornecidas pelo harness aceleraram os combates. Portanto, o
  fluxo servidor/interface foi exercitado, mas não movimento, mira manual, IA
  ou equilíbrio em gameplay representativo. Testes determinísticos agora
  cobrem as quatro escalas em encontros comuns, semichefes e chefes, densidade,
  Ouro, chances/pesos de raridade e HTML renderizado dos perfis no lobby.
  A suíte Node v0.130 verificava sintaxe e dois fluxos isolados em HTML mínimo;
  em v0.133 passou a executar E2E contra Flask/Socket.IO reais com banco e
  sessão descartáveis, cobrindo movimento por teclado, Ataque básico, dano
  inimigo na primeira onda e inventário cheio com venda/resgate. Em v0.134, três
  E2E adicionais percorreram a Fase 10 até o chefe nos riscos Moderado, Alto e
  Extremo. O progresso anterior foi semeado; o fixture usou nível 400,
  atributos no teto de 10.000 e coordenadas fornecidas pelo harness. Ataques e
  transições usaram eventos reais do servidor, e houve dano recebido durante
  cada execução. São evidências de fluxo completo/prolongado, não de progressão
  natural nem de movimento, esquiva, mira humana ou sensação representativa.
  Uma run ativa por conta é permitida; staging pendente bloqueia novos inícios
  e pausa ações de combate em outras sessões/personagens até a resolução.
  Dois testes cobrem esses bloqueios, inclusive a pausa de uma run ativa quando
  há espólio pendente em outro personagem.
  E2E de fase completa nos outros riscos está automatizado. Continua pendente a
  avaliação manual de gameplay e a decisão explícita sobre os parâmetros.
  Multiplicadores, recompensas, raridades, vendas e capacidade de 30 espaços
  seguem candidatos, sem aprovação.
- O seletor de fases agora agrupa as fases por ato sem mudar as regras de
  desbloqueio. O saldo compartilhado de Ouro e a ocupação da mochila são
  apresentados na página Inventário, não soltos na Sala de Espera; a verificação
  automatizada de rota cobre os dois pontos.
-   **Mapa da Fase 1:** a arte atual de 1.200 × 896 px e os efeitos do HTML
  atualizado foram conectados ao Canvas da missão; somente a Fase 1 recebe essas
  mudanças. A prévia `/mapas/terminal-vilar-fase1` usa a mesma imagem e
  configuração. O mapa JSON mantém 23 retângulos editáveis, 16 polígonos sólidos,
  quatro paredes lineares e espessura de 13 unidades; `map_geometry.py` valida
  essas formas para colisões e spawns do servidor. O editor local permite
  adicionar, mover, redimensionar, rotacionar e remover retângulos, além de
  alterar limites de movimento e spawn; polígonos e paredes não são editáveis
  pelo painel. O mundo permanece fixo em 2.400 × 1.800. A pedido do responsável,
  nenhum teste, checagem de sintaxe, build ou inspeção no navegador foi executado
  na v0.139. A validação anterior corresponde à imagem e à geometria anteriores,
  não cobre esta integração. Não foram testadas outras fases. A arte continua sem
  medição de semelhança percentual e sem aprovação visual.

### Linha de prioridade recomendada para a próxima rodada

Esta ordem prioriza validar o núcleo já implementado antes de ampliar o
orçamento de poder. Não altera decisões de produto nem transforma os parâmetros
provisórios em valores finais.

1. **Completar a validação de missões (P-048):** os quatro perfis têm testes
   determinísticos; a Fase 10 foi completada em E2E nos riscos Moderado, Alto e
   Extremo, com harness acelerado. Ainda é necessário jogar manualmente para
   avaliar sensação, movimento e esquiva e decidir se os valores candidatos
   devem ser ajustados ou aprovados.
2. **Fechar regressões e E2E do núcleo atual (P-044/P-045/P-037):**
   retestar os BUGs em monitoramento; validar mira por mouse, Numpad e pitch em
   várias resoluções; automatizar o ciclo de cartas e a decisão de manter a
   coleção quando a nova recomendação for inferior. O E2E de talentos P-042 já
   foi concluído nas quatro classes em banco descartável. Repetir BUG-015 no
   save real continua dependendo de a correção chegar a esse ambiente.
3. **Validar o combate-base em jogo (P-031/P-043/P-047):** testar as quatro
   classes em movimento, esquiva, ondas e builds com os talentos/cartas atuais.
   Registrar TTK, sobrevivência e dificuldades observadas antes de ajustar
   parâmetros; dar atenção ao desvio da Lâmina Arcana e aos limites do Tecelão.
4. **Construir as dependências que alteram o poder e a cooperação:** ampliar o
   inventário de staging para itens/equipamentos persistentes, consumíveis e
   economia aprovada; completar a infraestrutura de grupo de até três,
   sincronização e movimento autoritativo.
   Integrar estados de chefe e demais efeitos planejados antes da calibração
   final.
5. **Planejar a narrativa restante da Temporada 1:** começar pelas Fases
   11–20 e concluir o planejamento das Fases 21–30, alinhando história,
   encontros e recompensas às regras de XP/nível; propostas narrativas não são
   conteúdo implementado.
6. **Fazer a calibração integrada:** medir builds completas em solo, dupla e
   trio, com equipamentos, cartas, talentos, habilidades e consumíveis. Ajustar
   progressão/EXP e dificuldade somente com esses resultados; definir os
   números e a implementação das recompensas pós-400.
7. **Fechar produção e apresentação:** concluir arte/polimento visual,
   segurança, desempenho, hospedagem e demais decisões de lançamento depois que
   os fluxos e regras principais estiverem estabilizados.

### Etapa 1 --- Definição do projeto

-   [x] Definir o nome provisório/oficial do projeto: Crônicas do
    Recomeço.
-   [x] Consolidar a proposta de mistura entre RPG clássico e roguelike.
-   [x] Definir a direção de arte dark fantasy.
-   [x] Definir sistema de raridades e cores de borda dos itens.
-   [x] Definir a estrutura básica de salas e ondas.
-   [x] Registrar progressão contínua até o nível 400, sem Reset ou nível 1000.
-   [x] Registrar a direção tecnológica HTML5 + JavaScript + Flask +
    WebSocket.
-   [x] Definir as quatro classes iniciais e seus nomes próprios (P-001).
-   [~] Conceder Pontos de Legado por marcos de nível; fórmulas e TTK testados,
    validar o ritmo em combate ativo e definir recompensas de endgame (P-047).
-   [ ] Definir economia e monetização.
-   [ ] Definir escopo do multiplayer e PvP.
-   [ ] Definir catálogo inicial de itens/joias e ampliar o catálogo de
    habilidades além das habilidades-base e 12 assinaturas já implementadas.

### Etapa 2 --- Projeto técnico

**Estado:** em andamento. O cadastro e login iniciais foram prototipados;
modelo de dados completo, autenticação para produção, permissões e
hospedagem permanecem pendentes.

-   [ ] Definir arquitetura do cliente e do servidor.
-   [ ] Definir banco de dados e modelo de entidades.
-   [x] Criar e validar cadastro, login, logout e bloqueio de `/jogo` sem
    sessão; funcionamento confirmado pelo responsável.
-   [ ] Definir autenticação e contas para a versão final.
-   [~] Finalizar modelo e regras de personagens da conta (P-021).
-   [ ] Definir protocolo de comunicação em tempo real.
-   [~] Integrar Socket.IO no protótipo para eventos de jogo; autenticação
    dos eventos existe, enquanto sincronização multiusuário e controles
    contra abuso continuam pendentes. SQLite usa WAL e espera por gravações
    concorrentes por até 15 segundos.
-   [ ] Definir estrutura de salas e sincronização.
-   [ ] Definir estratégia de segurança e auditoria.

### Etapa 3 --- Protótipo jogável

**Estado:** em andamento. A sala, seleção/troca, combate manual e os fluxos
de morte, capítulo e ondas foram implementados e validados pelo responsável.
Inimigos e Vida/Mana persistem no protótipo; perseguição e posicionamento são
simulados no cliente. O dano inimigo agora vem de ataques telegráficos,
resolvidos e persistidos pelo servidor via Socket.IO. Sincronização de movimento
em multiplayer ainda falta. Canvas 2D e retratos são provisórios. Os quatro
atributos persistem e já alteram dano, Vida, Mana, recarga e movimento; as
quatro classes têm habilidade-base e as 12 evoluções têm passiva e habilidade
assinatura funcionais. O catálogo mais amplo e o balanceamento permanecem em
aberto.

**Registro de validação v0.120 — histórico; resultados de TTK supersedidos
pela simulação v0.123 abaixo:**

As validações manuais anteriores informadas como OK permanecem concluídas. A
árvore mantém três evoluções por classe; no nível 100, o jogador escolhe uma e
somente o ramo ativo aceita compras. Os 12 caminhos têm talentos e efeitos
próprios; 15 habilidades supremas têm nós individuais de desbloqueio e maestria,
e todas as habilidades-base, assinaturas e supremas podem ser aprimoradas.
Caminhos custam 58 ou 64 PL (714 somados), e a fórmula concede 64 PL no nível
400. O loadout aceita três habilidades desbloqueadas e no máximo uma suprema.
`python -m unittest discover -s tests -v` passou com 65 testes. O resultado de
TTK v0.120 contra a fase 69 foi supersedido: no calendário atual, a fase 69 não
é chefe. O benchmark teórico na fase 70 ficou em 64,2–99,5 s contra o chefe
(12 builds completas, sem equipamentos ou cartas), dentro do alvo matemático
de 60–100 s. Isso não valida a experiência em combate ativo nem adiciona fases
além da 30. A simulação
mediu TTK de 3,5–5,2 s para comuns, 20,1–31,6 s para semichefes e 63,2–130 s
para chefes nos marcos 1/100/220/400. A horda estacionária é letal para todas
as classes, conforme previsto para a prova de estresse, e não mede movimento
ativo. Em v0.117, foram validados manualmente no navegador compra de talento,
bloqueio de ramo e troca VIP com reembolso; alocação de atributo em tempo real
e após recarga; controles persistidos, movimento e zoom; troca de carta com
coleção VIP cheia e escolha automática pelo prazo. Em v0.118, testes de
integração cobrem compra, bloqueio, troca VIP e persistência para as quatro
classes; os quatro atributos via Socket.IO; distribuição automática VIP por
classe, ativação/desativação, persistência e mensagens/eventos de atualização.
A E2E v0.119 confirmou avisos visíveis para alocação manual e distribuição
automática, persistência de controles, movimento/zoom, substituição e
manutenção de coleção VIP 8/8 após recarga. Em v0.120, o E2E isolado validou a árvore do Guardião e, em rodada
complementar com banco descartável, os mesmos fluxos nas outras três classes:
escolha, compra, bloqueio visual de outro ramo, persistência após recarga e
troca VIP com reembolso. Ataque básico como fallback por falta de Mana e Avanço
para atravessar o cerco também foram exercitados. Ainda
faltam mira por mouse, Numpad, validação do pitch em resoluções variadas e
validação subjetiva do balanceamento em combate ativo. Encaixes aguardam o
sistema de itens. O registro
vivo de bugs/regressões está em
`10_registro_de_bugs_e_regressoes.md`; toda correção deve adicionar ou atualizar
testes em `tests/`.

Também foram validados outros fluxos do jogo: ao subir de nível, Vida e Mana
são restauradas por completo e o evento atualiza o HUD por Socket.IO; o orbe
usa a posição final do inimigo derrotado; as 30 passivas estão ligadas a
fórmulas/eventos de combate; morrer limpa cartas,
EXP/ofertas pendentes e orbes e retorna à onda 1 da fase; com a coleção cheia,
a barra de EXP continua progredindo e permite substituir uma carta ou manter
a coleção. Ao derrotar o chefe final, a coleção antiga é limpa e o orbe dele
permanece para coleta durante a preparação da próxima fase.

**P-037 — painel do alvo, alcance e cartas:** a oferta VIP foi observada com prazo de 10 segundos; a escolha automática ativou a recomendação numa coleção 8/8, mantendo oito cartas. Recomendação por classe/especialização/raridade e substituição persistente também têm cobertura funcional. Ainda falta validar em jogo a decisão de manter a coleção quando a nova carta é inferior à menos útil e automatizar o ciclo completo.

**P-036 — movimento do chefe:** ciclos, avisos, projéteis, esquiva, ataques e reposicionamento do chefe foram validados manualmente pelo responsável.

**HUD v0.100:** retrato, nível/limite, EXP, Vida/Mana e a contagem de monstros foram validados pelo responsável. A posição atual da contagem na barra superior, junto de fase e onda, também foi conferida visualmente. A prioridade imediata é desktop; controles adaptados para tablets e celulares ficam para depois.

**P-041 — tela de atributos em tempo real:** além da alocação manual e do dano já validados, a E2E v0.119 exibiu “1 ponto adicionado em Força”, a notificação de distribuição automática com os três pontos restantes e a mensagem de desativação. Os testes Socket.IO cobrem os quatro atributos, efeitos no resumo de combate, distribuição VIP nas quatro classes, mensagens, eventos e persistência. Validação visual concluída.

**P-042 — exatamente três evoluções por classe:** a E2E v0.120 validou no
Guardião e, nesta rodada, nas outras três classes, em banco descartável, escolha
de evolução, compra de talento, bloqueio visual do ramo incompatível,
persistência após recarga e troca VIP com reembolso de 2 PL. Testes de integração
cobrem compra, bloqueio, recusa sem VIP, troca VIP e persistência para as quatro
classes. O E2E das quatro classes está concluído; magnitudes ainda exigem
balanceamento em jogo e Encaixes aguardam itens.

**P-044 — revisão de bugs e regressões:** antes de encerrar uma correção, rever os registros abertos e em monitoramento no `10_registro_de_bugs_e_regressoes.md`; adicionar/atualizar testes automatizados para o mesmo ID e relacionar sistemas afetados para procurar regressões.

**P-045 — controles, combate, alvo e câmera v0.110:** Opções, os esquemas
Teclado + Mouse/Apenas Teclado, mapeamento fixo de teclas, vínculo da habilidade
atual da classe e fallback para Ataque básico estão implementados. A habilidade
assinatura da evolução substitui a habilidade-base no mesmo espaço após a compra
do Keystone. A câmera 2.5D tem pitch visual de 58°, zoom suave e limites. Mira
assistida não ataca; todos os ataques precisam de comando do jogador. E2E v0.119
validou persistência das opções e movimento/zoom; E2E isolado v0.120 confirmou
fallback para Ataque básico com Mana zerada, dano de 28 no alvo, movimento por
tecla e Avanço através dos inimigos. A regressão de telegráficos expirados foi
coberta por teste; também foram implementados timeout do cliente e limpeza ao
desconectar. Um teste de integração verifica persistência do esquema e dos
espaços. Ainda falta
validar mira pelo mouse, Numpad, pitch em resoluções variadas e os cenários
abaixo:

1. Teclado + Mouse: olhar acompanha cursor e painel superior acompanha monstro
   sob cursor; mouse esquerdo/direito executa a ação do espaço configurado.
2. Em Apenas Teclado, mova/olhe para um inimigo sem apertar ataque; confirme
   que selecionar o alvo assistido não causa dano. Depois ataque por comando.
3. Tecla 1 sempre executa o Ataque básico. Teclas 2, 3 e 4 executam as magias
   equipadas nos espaços 1, 2 e 3. Repita com a fileira superior e o Numpad,
   nos dois esquemas; confirme que espaços vazios não atacam.
4. Em Teclado + Mouse, configure os botões esquerdo/direito para magias
   diferentes, segure cada botão e confira ação e recarga; confirme que cliques
   não atacam no modo Apenas Teclado.
5. Tentar a habilidade equipada da classe sem Mana e em recarga; confirmar
   Ataque básico como fallback, consumo/recarga corretos e nenhum dano se o
   básico estiver em recarga ou fora do alcance. Repetir nas quatro classes.
6. Conferir que o novo ângulo oblíquo permite ler topo da cabeça, ombros,
   equipamentos e piso; o enquadramento central acompanha o jogador.
7. Girar o scroll nos dois sentidos, confirmar transição suave, limites e
   enquadramento sem áreas fora do mapa em desktop largo e resolução menor.
8. Com zoom e projeção alterados, validar mira, círculo, hitbox, alcance por
   contato, seleção pelo cursor e painel superior sem deslocamento visual.

P-035, proposta anterior de auto-ataque VIP, fica suspensa pela regra atual de
que todo ataque exige comando do jogador. No P-033, o ângulo de protótipo foi
definido em 58°; sprites com volume, perspectiva final, ordenação e acabamento
de profundidade continuam para revisão integrada à arte após o balanceamento.
Novos poderes distintos para preencher a barra de habilidades permanecem em
P-018/P-031.

**P-046 — coleção cheia e substituição manual de cartas v0.108:** ao clicar uma
das três ofertas com todos os espaços preenchidos, o seletor abre no mesmo
clique, sem Tab ou atraso; o servidor persiste a carta escolhida e só então
habilita a confirmação. Cada carta ativa mostra nome, raridade e efeito atual.
O jogador escolhe uma carta ativa para substituir e confirma. O botão abaixo
das três ofertas mantém a coleção e descarta a oferta atual. O servidor mantém
a escolha manual também para VIP; a automação VIP por prazo só atua se o
jogador ainda não iniciou uma escolha manual. Opções já exibidas não voltam no
restante da mesma onda, mas podem voltar em ondas futuras se não estiverem
ativas. Em v0.119, a E2E exercitou substituição e manutenção manual de uma
coleção VIP 8/8; ambas mantiveram oito cartas e persistiram após recarga.
Testes Socket.IO cobrem também os dois resultados. A escolha automática por
prazo e a regra de manter a coleção quando a recomendação é inferior continuam
no P-037.

1. Preencha todos os espaços (6 conta comum/8 VIP), abra uma oferta e clique
   uma única vez em uma opção; confirme que o seletor de troca abre
   imediatamente sem Tab nem segundo clique.
2. Confira nome, raridade e efeito atual de cada carta ativa; clique em uma
   carta ativa, confira o destaque visual e confirme a troca;
   valide que a nova carta entra no lugar selecionado.
3. Em outra oferta cheia, use abaixo das três cartas **Manter cartas ativas**;
   confirme que os ativos permanecem e as três opções não voltam a aparecer na
   mesma onda; podem voltar em onda futura se continuarem inativas.
4. Automatize o mesmo fluxo como Premium/VIP; sem clique numa oferta, teste
   separadamente a escolha automática VIP.
5. Se houver mais de uma escolha pendente, confirme que a próxima oferta chega
   após substituir ou descartar a atual.

**P-043 — densidade e desafio:** ondas comuns aumentam em um inimigo a cada quatro fases, até quatro adicionais. O código atual escala Vida/dano até o nível 400; a regra e a dificuldade precisam ser rebalanceadas para o teto-alvo 170. A simulação determinística existente usa fórmulas anteriores e não valida essa nova meta. O E2E v0.120 confirmou movimento e saída de um cerco com Avanço, mas ainda falta medir sobrevivência em combate representativo e cooperação. A prova de estresse estacionária de 50% de acertos é intencionalmente letal, conforme decisão do responsável.

**P-003 — fim de jogo:** a direção anterior de teto 400 e endgame pós-400 foi superada pelo teto-alvo 170 decidido em v0.135. A implementação e o rebalanceamento estão pendentes. A campanha termina na Fase 30; definir a progressão/recompensas de fim de campanha após recalibrar XP, PL e combate. A antiga direção híbrida pós-400 não deve ser tratada como vigente até ser revista. O saldo de Ouro de P-048 é virtual, pertence à conta e não se relaciona a pagamentos reais.

**Correção do bloqueio durante cartas e no intervalo entre fases:** a pausa do mundo agora depende somente das telas de morte ou decisão de fim de fase; abrir a seleção de cartas nunca pausa o mundo. Movimento por WASD/setas e Avanço permanece liberado enquanto os inimigos continuam atacando. Ao concluir o chefe, o cliente fecha ofertas antigas e limpa teclas/botões mantidos antes da pausa. O responsável confirmou manualmente a movimentação com cartas abertas e a saída da pausa por **Preparar próxima fase** ou **Sala de Espera**.

**Controle temporário de Premium/VIP:** botão flutuante no jogo altera o estado Premium da conta autenticada, com gravação validada no servidor via Socket.IO. A opção de teste fica ligada por padrão no protótipo e pode ser desligada com `CRONICAS_ENABLE_PREMIUM_TEST_TOGGLE=0`. Remover antes do lançamento.

-   [x] Criar sala de teste e implementar movimentação/câmera;
    funcionamento confirmado pelo responsável.
-   [ ] Implementar um personagem e uma classe inicial.
-   [x] Validar a tela de seleção e a troca de personagem no navegador.
-   [~] Validar criação, limite de slots, exclusão e Baú da Conta em
    diferentes situações.
-   [x] Inimigos persistidos por onda, colisão local e perseguição. P-036 adiciona tipos corpo a corpo/à distância, telegráficos no chão, projéteis com sombra e ciclos especiais de semichefe/chefe via Socket.IO; esses comportamentos e o reposicionamento do chefe foram validados manualmente.
-   [x] Preparação de 30 segundos após cada mudança de fase; o servidor persiste o horário final e impede ataques durante a preparação. Validado manualmente pelo responsável.
-   [x] Contador de monstros acompanha derrotas e transição de onda em tempo real; a posição v0.100 na barra superior também foi validada visualmente.
-   [x] P-037: contato do alcance e carta de alcance, escolha comum sem cronômetro e escolhas VIP com prazo sequencial foram confirmados pelo responsável.
-   [~] P-037: timer VIP de 10 segundos, recomendação e substituição pela carta
    menos útil já têm cobertura funcional; validar manter a coleção quando a
    nova carta é inferior e automatizar o ciclo integral.
-   [~] P-037: validar em combate o ritmo dos valores implementados de 25 EXP
    por orbe comum e 40 EXP VIP.
-   [x] P-036: chefe se movimenta/reposiciona enquanto ataca; telegráficos e ciclos permanecem legíveis, conforme validação manual.
-   [x] HUD anterior: retrato, nível/limite, EXP atual/próximo nível, Vida/Mana e contagem em tempo real foram validados em tamanhos de tela variados.
-   [x] P-040: posição da contagem de monstros na barra superior ao lado de fase/onda conferida visualmente em desktop.
-   [x] P-041 v0.119: Socket.IO cobre atributos e automação VIP; notificações manuais, automáticas e de desativação foram vistas na E2E de navegador.
-   [~] P-042 v0.120: E2E de escolha, compra, bloqueio, troca VIP e persistência confirmado nas quatro classes em banco descartável; integração cobre as quatro classes; balancear magnitudes em jogo e integrar Encaixes com itens.
-   [~] P-044 v0.104: revisar ocorrências em aberto/monitoramento no `10_registro_de_bugs_e_regressoes.md` e atualizar o estado após validação manual.
-   [~] P-045 v0.120: ataque básico por falta de Mana e Avanço de fuga validados no navegador; faltam mira por mouse, Numpad e pitch em diferentes resoluções.
-   [x] P-046 v0.119: substituição e manutenção VIP 8/8, detalhes e persistência após recarga verificadas no navegador e cobertas por integração; a escolha automática inferior permanece em P-037.
-   [~] P-043 v0.116: simulação determinística e testes aprovados; validar movimento ativo e cooperação.
-   [ ] P-047 v0.135: implementar teto-alvo 170 e recalibrar XP, Pontos de Legado, Vida/dano dos inimigos e combate para a campanha de 30 fases. Código ainda usa teto 400; projeção 170/26 PL e TTKs anteriores são snapshot, não validam a meta. Fórmulas, testes de progressão/PL/combate e gameplay representativo pendentes.
-   [~] P-048 (código de gameplay v0.131): bloqueios de dificuldade/fase, run única por conta, pausa por staging, contagem inicial, Ouro, raridades e resolução estão implementados. Em v0.134, a suíte JS passou com 10 testes e completou a Fase 10 em E2E nos riscos Moderado/Alto/Extremo, com harness acelerado. O combate automatizado durou 66–80 s por cenário e confirmou dano inimigo. Python: 84 testes; `compileall` passou; simulação baseline executada. Validação manual e decisão sobre parâmetros candidatos continuam pendentes.
-   [x] Movimento com cartas abertas, transição de fim de fase e limpeza das entradas; validados manualmente pelo responsável.
-   [x] Alternância Premium/VIP no botão de teste; ativação, desativação e recarga da página validadas. Remover ferramenta antes da versão final.
-   [x] Ao derrotar o último inimigo, a onda avança pelo Socket.IO sem recarregar a página; destaque central, chefe individual na onda final e apresentação por capítulo/onda foram validados pelo responsável.
-   [x] Definir 10 ondas por fase e encontros da Temporada 1: onda 10 das
    fases 5/15/25 tem semichefe; onda 10 das fases 10/20/30 tem chefe de ato;
    as demais ondas 10 são comuns. A Fase 30 encerra a campanha. P-004 está
    concluído quanto à estrutura; balanceamento permanece.
-   [~] EXP usa orçamento fixo por fase e pesos 1/3/5 por abate comum/
    semichefe/chefe; pontos por nível e distribuição automática VIP estão
    implementados. Simulações/testes cobrem os parâmetros candidatos; validar
    o ritmo em combate ativo.
-   [~] Cartas temporárias com escolha inicial, orbes coletáveis
    de EXP, barra de progresso e oferta de 3 cartas ao completá-la; coleção
    ativa (6 padrão / 8 Premium/VIP); contas comuns decidem a substituição e
    Premium/VIP substitui pela menor utilidade estimada para a classe e
    especialização, considerando habilidade assinatura, passiva, efeitos,
    situação e raridade, com estado
    atualizado por Socket.IO sem recarregar a sala. E2E v0.119 verificou a
    coleção VIP cheia, substituição/manutenção e persistência; automatizar o
    ciclo integral e calibrar efeitos. As 36
    passivas já estão conectadas às fórmulas/eventos de combate; ver P-022.
    As cartas iniciam ocultas quando liberadas, e o botão Tab destaca “Nova
    carta”; botão e tecla alternam a seleção. Andar e usar Avanço continuam
    possíveis com o painel aberto; ataques ficam suspensos enquanto ele está
    visível. Orbes continuam sendo coletados com escolhas pendentes; EXP e
    escolhas extras entram na fila. ACK do Socket.IO atualiza a barra e a
    coleção sem depender da difusão em sala; coletas são serializadas e podem
    repetir após bloqueio momentâneo do banco. Uma sugestão por classe/situação
    é destacada; após 10 s o servidor escolhe a sugerida com prazo persistido.
    Quando a coleção está cheia, a sugestão não substitui carta ativa sem ação
    do jogador. A escolha automática quando a recomendação é inferior continua
    pendente em P-037.
-   [~] Socket.IO para coleta de orbes, escolhas de cartas e avanço de ondas
    implementado. E2E v0.119 cobriu coleção cheia, substituição/manutenção e
    persistência; falta automatizar o ciclo integral e a decisão de manter a
    coleção quando a nova carta é inferior (P-037).
-   [~] Combate manual: todo ataque exige comando; a tecla 1 usa o básico e 2–4 usam magias 1–3. No modo Teclado + Mouse, os botões esquerdo/direito podem ser vinculados às magias; valores de dano/EXP são provisórios.
-   [x] Baseline anterior: progressão implementada até 400 sem Reset; 5 pontos
    de atributo por nível e fórmula de PL antiga. A direção do teto foi
    substituída em v0.135; o rebalanceamento correspondente está pendente em
    P-047.
    A migração retroativa é idempotente; simulações e testes cobrem o ritmo
    candidato, mas falta validação em combate ativo (P-047).
    Distribuição automática por classe é opcional e exclusiva VIP.
-   [x] A tela protegida de atributos está acessível em Serviços na Sala de Espera;
    permite consultar Força, Agilidade, Vitalidade e Energia, investir pontos
    disponíveis e, para Premium/VIP, configurar a distribuição automática.
    Exibe estimativa prévia e valores derivados de dano, Vida/Mana máximas,
    recargas e movimento. Os quatro atributos afetam o combate com fórmulas
    candidatas; a calibração final segue pendente. Novos personagens iniciam
    com recursos calculados para a classe, e excessos de personagens antigos
    são limitados ao máximo ao entrar no jogo. O serviço mostra indicador com
    pontos livres; Talentos também sinaliza Pontos de Legado disponíveis.
-   [~] Recargas iniciais: ataque básico 1,15 s; habilidades-base de Guerreiro
    e Tecelão 5 s, Caçador 4,5 s e Lâmina Arcana 6 s; Avanço 3 s.
    Agilidade reduz 0,5% por ponto, até 50%, e aumenta movimento 0,1% por ponto,
    até 25%. Os valores persistidos são usados pelo servidor; integração
    Socket.IO e notificações foram testadas, enquanto o balanceamento dos
    coeficientes continua pendente.
-   [~] Morte pausa a sala e oferece reiniciar a fase ou ir à Sala de Espera; chefe
    da onda 10 abre escolha entre sala de espera e próxima fase. Cartas são removidas
    ao concluir fase.
-   [~] Criar tela inicial de sala de espera após selecionar personagem;
    layout responsivo com três cartões de grupo, retrato Canvas provisório,
    chat visual, progresso/serviços e início da partida. Busca e seletor de
    amigos estão esboçados, mas não conectados a perfis. Amizades persistentes,
    convites, salas de grupo e chat Socket.IO ainda não existem. Talentos está
    ativo; Inventário, Baú, Máquina do Caos e trade continuam indisponíveis.
-   [~] P-025 em andamento: chefes exibem afinidade elemental e resistência provisórias; o Corte Rúnico recebe redução de dano contra chefes Umbral. Estados de escudo quebrado, sangramento, paralisia e queimadura ainda não foram implementados.
-   [—] Auto-ataque PvE Premium/VIP (P-035) suspenso pela decisão v0.107:
    ataques exigem comando explícito; retomar somente com nova aprovação.

### Etapa 4 --- Progressão e conteúdo

-   [x] Implementar progressão contínua ao nível 400, sem Reset, com Pontos de
    Legado por marcos de nível.
-   [~] Árvore de Talentos implementada: quatro árvores próprias, 12 caminhos,
    compra/efeitos e custos de 58–64 PL. A suíte e a E2E de navegador em banco
    descartável cobrem as quatro classes; faltam balancear magnitudes e integrar
    Encaixes com itens.
-   [~] Inventário mínimo de conta/staging para baús implementado em P-048;
    implementar equipamentos, mochila final e Baú da Conta.
-   [ ] Implementar baú persistente.
-   [ ] Implementar joias e aprimoramentos.
-   [ ] Implementar Forja do Caos e asas.
-   [ ] Definir e implementar pets e montarias; regras de obtenção e efeitos
    ainda precisam ser decididos.
-   [ ] Definir drops de equipamentos/materiais/Ouro e coleta com alcance-base,
    coleta automática por pet e ampliação VIP após fechar a simulação P-034.
-   [ ] Criar eventos e chefes.
-   [ ] Criar hub de fim de capítulo (a cada 10 fases) com Baú da Conta,
    Estatísticas e Status do Personagem (P-026); o resultado e staging de
    missão P-048 não substituem esse hub.

### Etapa 5 --- Recursos online

-   [~] Sala de Espera individual e seleção de missões implementadas; conexões
    sociais, presença, convites e salas multiplayer ainda pendentes.
-   [ ] Criar lista de amigos.
-   [ ] Criar salas abertas e privadas.
-   [ ] Implementar partidas cooperativas.
-   [ ] Implementar trade.
-   [ ] Implementar mercado.
-   [ ] Avaliar e implementar PvP, se aprovado.

### Etapa 6 --- Polimento e lançamento

-   [~] Base de câmera 2.5D, inclinação visual e zoom suave implementados por
    solicitação antecipada; movimento e zoom foram observados em v0.117. Após concluir
    100% do balanceamento (P-031), revisar ângulo, profundidade, arte e leitura
    de personagens/equipamentos, pets, montarias, asas e mapa (P-033).
-   [ ] Produzir arte, animações e efeitos originais.
-   [ ] Produzir áudio original ou licenciado.
-   [ ] Ajustar interface e acessibilidade.
-   [ ] Testar balanceamento.
-   [ ] Testar segurança e concorrência.
-   [ ] Testar desempenho em navegadores.
-   [ ] Preparar hospedagem, backups e monitoramento.
-   [ ] Preparar documentação para jogadores.

### 18.1 Painel de andamento e ponto de retomada

Este painel é o resumo operacional atual do projeto. A lista detalhada de
decisões em aberto continua na Seção 19.

**Estado atual (15/11/2026, v0.134; gameplay validado até v0.131):** o protótipo tem seleção de personagens,
partida individual, combate com inimigos, progressão por abates, cartas e
atualizações de combate/atributos via Socket.IO. O limite 400 e a curva de
Pontos de Legado estão implementados: 64 PL no nível 400. As 12 árvores são
únicas; cada caminho custa 58 ou 64 PL (714 somados entre as opções), com 15
habilidades supremas e maestrias próprias. A suíte Python v0.131 passou com
84 testes; os 82 testes da v0.128 são um resultado histórico. E2E v0.120 validou escolha, compra, bloqueio, persistência e troca VIP
nas quatro classes, em banco descartável; magnitudes e cooperação não foram
validadas por esse teste. O fallback de Ataque básico sem Mana e o Avanço para
atravessar o cerco também foram exercitados. Mira por mouse, Numpad, pitch em
diferentes resoluções, avaliação humana de combate, cooperação e balanceamento
completo permanecem pendentes. A direção híbrida pós-400 foi aprovada, mas os
detalhes e a base de equipamentos ainda não estão implementados. Consulte a Seção 19 e o documento
de Pendências.

P-048 também implementa dificuldades, seleção autorizada de fase, contagem
inicial de 5 segundos, crédito de Ouro inteiro para a conta e resolução
obrigatória dos baús. Python v0.134: 84 testes aprovados; `compileall` passou.
`npm run test:js`: 10 testes aprovados. E2E autenticado completou a Fase 10 em
Moderado/Alto/Extremo até o chefe e a tela pós-fase; usou progresso pré-semeado,
nível 400, atributos no teto e coordenadas de alvo do harness. Cada execução
também recebeu dano inimigo, mas não representa movimento/mira do jogador.
Continuam pendentes o teste manual de sensação de jogo e a aprovação dos
parâmetros. O E2E de inventário cheio com venda e resgate também passou.

**Implementado e validado pelo responsável:**

-   Cadastro, login, logout e proteção de `/jogo` sem sessão.
-   Sala visual provisória com movimentação por teclado e câmera de
    acompanhamento.
-   Tela de seleção e retorno à seleção pelo botão **Trocar Personagem**.
-   Movimentação, mira e dash foram confirmados manualmente em versões
    anteriores. Em v0.107, a mira não ataca: tecla 1 usa o básico; 2–4 usam
    magias, e os botões esquerdo/direito recebem magias configuráveis.
-   Introdução única de capítulo na faixa narrativa, transições de fase/onda,
    onda de chefe e restauração de Vida/Mana após morte foram confirmadas
    pelo responsável.

**Referência de progressão após v0.123:** a XP necessária por nível usa
`100 + 25 × nível`; cada fase distribui um orçamento de seis limiares por abate
com pesos 1/3/5. A projeção de nível 400 na fase 69 e 6.502 abates extrapola
além da campanha e não descreve conteúdo jogável atual. A antiga estimativa de
5.585 abates e a matriz que chamava a fase 69 de chefe são superadas. Vida e
dano dos inimigos escalam até o nível inimigo 400; builds com itens/cartas,
combate ativo e ritmo real ainda precisam de validação.

**Decisão aprovada e implementada:** P-002 foi substituída. Não há Reset nem
nível 1000; o nível máximo permanece 400. O jogador recebe Pontos de Legado
pela fórmula `nível // 10 + nível // 50 + nível // 25`, totalizando 64 no
nível 400.
Consulte `02_progressao_e_personagens.md` e
`balanceamento/decisoes_aprovadas.md`.

**Escopo necessário antes de fechar o balanceamento:** incluir dano elemental
causado e roubo de Vida junto de resistências, estados elementais, regeneração
passiva, cura por eliminação, equipamentos e atributos. São sistemas distintos;
as fórmulas e os limites continuam pendentes. Ver
`balanceamento/base_enviada_itens_mu_online.md`.

**Implementado no código:**

-   Armazenamento local de contas em SQLite e hash de senha.
-   Cadastro/seleção de personagens, limite de slots, escolha para jogar e
    confirmação de exclusão.
-   Tela de seleção em três zonas, cenário noturno, sprite SVG provisório
    com idle, dados em painel translúcido, slots laterais e destaque Bronze
    conforme a paleta. O botão **Voltar** encerra a sessão e volta à tela de
    acesso, pois ainda não existe menu principal.
-   Link **Trocar Personagem** no topo da sala; retorna à seleção sem fazer
    logout. O fluxo foi validado pelo responsável; para trocar, selecionar
    outro personagem e clicar em **Jogar**.
-   Progressão contínua até o nível 400, sem rota de Reset. Pontos de Legado
    são concedidos por marcos em combate; o banco migra saldos existentes de
    forma idempotente, preservando pontos e talentos já adquiridos.
-   Progressão de protótipo com XP, nível até 400, 10 ondas por fase,
    encontro especial na onda 10 conforme a fase: semichefe em 5/15/25,
    chefe em 10/20/30 e comum nas demais. O avanço real ocorre ao derrotar
    a horda; um botão de teste ainda simula a conclusão para desenvolvimento.
-   Catálogo de 36 cartas, sorteio ponderado, ofertas sem duplicatas,
    coleção ativa de 6/8 cartas e troca opcional quando cheia. As cartas cobrem
    projéteis, dano elemental, cura de habilidades e Mana por abate; a
    recomendação considera a especialização, a passiva e a habilidade assinatura
    liberada. As descrições correspondem aos efeitos; magnitudes aguardam
    balanceamento.
    Morte também limpa cartas, EXP/ofertas pendentes e orbes. A descrição de cada carta ativa aparece ao
    passar o mouse ou focá-la por teclado. Cada monstro derrotado deixa um
    orbe na posição da morte; recolhê-lo enche a barra de EXP (25 por orbe;
    100 para uma oferta de três cartas, valores provisórios). Cartas não têm
    níveis.
    A substituição e a manutenção manual de coleção VIP 8/8 foram verificadas
    no navegador; P-037 ainda pede validar a escolha automática quando a nova
    carta é inferior e o ritmo de EXP/ofertas.
-   Eventos de jogo em Socket.IO no modo threading; coleta de orbes, barra
    de EXP, ofertas/escolhas de cartas e conclusão simulada de ondas atualizam
    a sala sem recarregar. A biblioteca JavaScript do Socket.IO está servida
    em arquivo local. A E2E v0.119 exibiu as notificações de atributos; P-037
    e P-040 mantêm validações visuais específicas de ofertas e da contagem.
-   Conexões SQLite usam WAL e `busy_timeout` de 15 segundos. Eventos de
    escrita retornam erro controlado caso ainda não consigam iniciar a
    transação; ataques não são enviados em paralelo pelo cliente.
-   Mira pelo mouse no combate: o personagem gira para o cursor e ataques
    acionados pelo jogador selecionam inimigos alinhados à direção apontada;
    WASD/setas mantêm a movimentação. Mapeamento anterior de botões/atalhos foi
    substituído em v0.107 pela regra de tecla 1 básico, teclas 2–4 magias e
    botões esquerdo/direito configuráveis para magia no modo Teclado + Mouse.
-   Dash no Espaço avança na direção atual da mira, respeita os limites do
    cenário e a colisão com inimigos, e exibe recarga no HUD. Duração,
    velocidade e recarga são valores provisórios; funcionamento validado
    pelo responsável.
-   Ao morrer, o servidor restaura Vida e Mana completas e retorna o
    personagem à onda 1 da fase atual; a sala pausa com escolha entre
    reiniciar fase e ir à Sala de Espera. O fluxo foi testado pelo responsável.
-   Após a seleção do personagem, o botão Jogar abre a sala de espera individual.
    Após o chefe da onda 10, a sala oferece sala de espera ou preparação da próxima
    fase; cartas temporárias e orbes são limpos nessa transição.
-   Ao iniciar uma fase nova após derrotar o chefe, o servidor restaura
    Vida e Mana completas. Ondas comuns não recuperam esses recursos; o HUD
    atualiza por Socket.IO.
-   Transições de onda destacam a onda/chefe no centro da tela. Chefes têm
    apresentação e vida maiores, aparecem individualmente na onda final e
    mantêm nome/nível ao carregar a sala. A introdução do capítulo aparece
    uma vez na área narrativa superior; depois, o destaque mostra fase/onda.
    Transições validadas pelo responsável.
-   IA inicial de monstros: corpo a corpo persegue e prepara golpe em área;
    inimigo à distância mantém espaço e dispara projétil. Semichefe alterna
    Ruptura do Arauto/Estilhaços da Cripta; chefe alterna Chuva do Umbral/Fenda
    do Umbral. Avisos mostram a zona e a contagem antes do impacto; projéteis
    desenham sombra no chão. Socket.IO valida aviso/impacto e persiste o dano.
    Movimento e posição do jogador ainda são simulados pelo cliente. Ciclos,
    avisos, esquiva, dano e reposicionamento do chefe foram validados; a
    sincronização de movimento de jogadores em multiplayer continua pendente.
-   Árvore de Talentos exclusiva para cada uma das quatro classes, com
    trilhas ramificadas, custos, pré-requisitos e compras persistidas por
    personagem. Caminhos custam 58 ou 64 PL; a progressão concede 64 no nível
    400. Loadout, efeitos e fluxos de compra/bloqueio/troca VIP têm testes para
    as quatro classes; E2E de navegador em banco descartável confirmou os
    fluxos nas quatro. Falta validar magnitudes em combate real.
-   Registro do Baú da Conta compartilhado; removido ao deletar o último
    personagem. O protótipo ainda não armazena itens no baú.
-   Estrutura de arquivos separada entre autenticação, banco, segurança,
    rotas, templates, CSS e JavaScript.

**Documentação atualizada:**

-   Documento mestre mantido como referência central, com histórico e
    painel de andamento.
-   README atualizado com a estrutura e os comandos para iniciar.

**Decisão aprovada:** consultar `documentacao/balanceamento/decisoes_aprovadas.md`.
Nível máximo 400 sem Reset; 5 pontos de atributo por nível; 1 Ponto de Legado
a cada 10 níveis e 1 ponto adicional a cada 50. Atributos-base continuam
candidatos à calibração.

**Implementado nesta etapa:** atributos-base por classe no banco, migração de
personagens existentes, 5 pontos por nível ganho, tela protegida de distribuição
em `/jogo/atributos`, teto provisório 10.000 e saldo validados no servidor.
Pontos de Legado são ganhos pelos marcos de nível. EXP escala pelo nível do
inimigo com bônus de 3x/5x para semichefe/chefe. O modo VIP opcional distribui
automaticamente por pesos de classe. Implementação aguarda validação manual.

**Auto-poções Premium/VIP:** controles de Vida e Mana com preferências
persistentes por personagem; o servidor verifica a conta e aplica as
recuperações em tempo real, com recargas separadas. Funcionalidade provisória,
sem consumo de estoque; depende da futura definição dos consumíveis e do
balanceamento em P-032.

**Ponto de retomada P-031:** a Vida do personagem passou de base 100 para 120,
e a Vida de comuns, sem chefes e chefes recebeu curvas progressivas em
`enemy_max_health`. A nova simulação
`python scripts/simulate_live_balance.py` chama as fórmulas reais de dano,
recarga, atributos, Vida e resistência elemental. Na execução atual, sem
equipamento, cartas ou talentos comprados, o TTK ficou em 3,5–5,2 s para
comuns, 20,1–35,0 s para semichefes e 61,4–111,0 s para chefes nos checkpoints
1/100/220/400. O benchmark das 12 builds completas no chefe teórico da fase 70
ficou em 64,2–99,5 s. A antiga medição de 130 s do Tecelão contra o chefe de
Fogo está superada; a resistência elemental de 30% continua aprovada.

A mesma simulação estima as ondas 8 em 63–96 s. Com o personagem parado e 50%
de acertos antes da esquiva, a Vida restante fica negativa em todas as classes;
seria preciso evitar aproximadamente 92–95% dos ataques. O responsável escolheu
manter esse desafio centrado em esquiva, sem reduzir densidade, dano ou
frequência. A estimativa não inclui evasão por movimento, alcance real dinâmico,
equipamento, cartas nem cooperação; não é uma previsão da experiência ativa.
Próximo passo P-031: comparar movimento real e builds manuais, então validar
tempo e sobrevivência em combate. Efeitos utilitários, cooperação e a
implementação das recompensas híbridas de endgame continuam pendentes. O
relatório está em
`balanceamento/auditoria_e_primeira_simulacao.md`.

**P-043:** a simulação de hordas agora é determinística e cobre as quatro
classes nos checkpoints; a suíte verifica sua repetibilidade, densidade,
pressão, acertos e esquiva. O cenário parado é explicitamente de estresse, não
substitui testes de movimento ou cooperação.

**P-047:** a suíte valida TTK comum/semichefe/chefe, sobrevivência inicial,
limite de nível dos inimigos, distribuição integral de EXP por fase e a chegada
ao nível 400 na fase 69 após 6.502 abates, em extrapolação matemática além da
campanha. Isso não define conteúdo jogável após a Fase 30; recompensas e ritmo
futuros ainda precisam de definição. A cifra de 5.585 abates foi superada.

**EXP/hordas implementadas para avaliação:** ondas comuns crescem de 3 a 10
inimigos (ondas 1–8). A cadência vigente reserva a onda 10 das fases 5/15/25
para semichefes e 10/20/30 para chefes; as outras ondas são comuns. Cada fase
fixa um orçamento de seis limiares de nível com base no nível de entrada;
pesos 1/3/5 distribuem o total entre comuns/semichefe/chefe. EXP só é paga por
abate, sem bônus repetido ao avançar. A projeção teórica de nível 400 em
~69 fases/6.502 abates extrapola a Temporada 1 e não é conteúdo disponível.

**Surgimento aleatório implementado:** posições pseudoaleatórias distribuídas
pelo mapa, com 380 unidades de afastamento do jogador e 92 entre inimigos. A
simulação semeia essas posições e estima aproximação e avisos. O cenário
estacionário com 50% de acertos é um limite de estresse, não previsão de
movimento: a próxima etapa P-031 é validar deslocamento, alcance e evasão reais.

**Direção visual futura:** teletransporte, saída do chão ou queda do céu,
animações e efeitos visuais seguem para polimento posterior.

**Correção de inicialização da sala:** `/jogo` seleciona `phase_xp_budget`
junto aos dados do personagem e `enemy_index` na consulta de inimigos ativos;
ambos são necessários para calcular a EXP e verificar/reparar posições. A falta
desses campos na projeção SQLite causava `IndexError: No item with that key`.

**Atualização de fórmula (v0.120):** inimigos comuns, semichefes e chefes usam
`enemy_max_health`, ligada a fase/onda e nível; inimigos persistidos mantêm a
proporção de Vida ao migrarem para o novo máximo. A função e os cenários
determinísticos estão cobertos por testes e simulações; a validação pendente é
medir dano recebido, sobrevivência, telegráficos e esquiva em combate ativo,
incluindo builds e grupos.

**Ainda pendente:** movimentação autoritativa no servidor e sincronização
multiplayer; calibração das passivas das cartas, atributos, talentos, ondas e
inimigos; estados de chefe e interação com equipamentos; detalhes e
implementação do endgame híbrido; economia, multiplayer/PvP, inventário/itens,
catálogo futuro de habilidades, autenticação/arquitetura de produção e
validações de desempenho/segurança. O reembolso de talentos v0.104 e os fluxos
de troca VIP já têm implementação/testes; não confundir isso com o balanceamento
de P-042: os fluxos E2E de P-023/P-042 foram concluídos nas quatro classes em
banco descartável; calibração das magnitudes e integração dos Encaixes com
itens continuam pendentes.

------------------------------------------------------------------------
