# Pendências e decisões

> Guia temático iniciado a partir do Documento Mestre v0.55 e atualizado com decisões posteriores. Consulte `Cronicas_do_Recomeco_Documento_Mestre_v0.139.md` para navegar entre assuntos.
>
> Atualizado em: 15/11/2026 21:54:32 (UTC−03:00).


## 19. Pendências e decisões em aberto

Esta seção é a lista principal de perguntas ainda não resolvidas. Ao
decidir um item, atualizar a seção correspondente e registrar a decisão
no histórico.

  -----------------------------------------------------------------------
  ID                Tema              O que falta       Situação
                                      decidir           
  ----------------- ----------------- ----------------- -----------------
  P-001             Classes           Quais serão as    Concluído
                                      classes oficiais  
                                      iniciais e seus   
                                      nomes próprios?   

  P-002             Reset             Retirar Reset   Decisão substituída;
                                      e adotar        mecânica removida,
                                      progressão      não há nível 1000
                                      contínua

  P-003             Fim de partida    Definir regras     Direção híbrida aprovada;
                                      e implementar     detalhes de equipamentos,
                                      prêmios pós-400   limites e marcos pendentes;
                                                       sem código implementado

  P-004             Ondas/campanha    Qual a cadência   Concluído
                                      da Temporada 1?    (30 fases,
                                                        10 ondas/fase;
                                                        semichefes 5/15/25,
                                                        chefes 10/20/30)

  P-005             Multiplayer       Qual o tamanho e  Parcial
                                      composição do     (solo padrão;
                                      grupo?            até 3, quaisquer
                                                        classes; rede
                                                        pendente)

  P-006             PvP               O modo 1x1 fará   Pendente
                                      parte do          
                                      lançamento ou     
                                      ficará para uma   
                                      atualização?      

  P-007             Arte              Qual será o       Pendente
                                      padrão final dos  
                                      sprites,          
                                      personagens,      
                                      monstros e        
                                      cenários? A arte   
                                      da Fase 1 foi       
                                      integrada, mas      
                                      ainda não é arte    
                                      aprovada.           

  P-008             Produção visual   Quais recursos    Parcial
                                      serão gerados por 
                                      IA, desenhados ou 
                                      construídos por   
                                      código? Uso/edição
                                      por IA documentado
                                      para o mapa da
                                      Fase 1; política
                                      geral pendente.

  P-009             Banco             Confirmar SQLite  Pendente
                                      no protótipo e    
                                      PostgreSQL em     
                                      produção, ou      
                                      escolher outra    
                                      estratégia.       

  P-010             Loja              Definir o que a   Pendente
                                      loja de partida   
                                      vende e qual      
                                      moeda utiliza.    

  P-011             Premium           Aprovar ou        Parcial
                                      descartar         
                                      assinatura VIP e  
                                      seus benefícios.  

  P-012             Monetização       Definir se haverá Pendente
                                      compras com       
                                      dinheiro real e   
                                      quais itens       
                                      poderão ser       
                                      vendidos.         

  P-013             Joias             Definir nomes     Pendente
                                      originais,        
                                      raridades, usos e 
                                      taxas de drop.    

  P-014             Forja             Definir receitas, Pendente
                                      chances de        
                                      sucesso e         
                                      consequências de  
                                      falha.            

  P-015             Asas              Definir           Pendente
                                      categorias,       
                                      requisitos, bônus 
                                      e evolução.       

  P-016             Inventário        Confirmar limites Pendente
                                      finais de mochila 
                                      e baú, inclusive  
                                      expansões.        

  P-017             Mercado           Definir taxas,    Pendente
                                      limites, itens    
                                      negociáveis e     
                                      regras de         
                                      segurança.        

  P-018             Habilidades       Concluir e       Parcial:
                                      balancear o      habilidades-base, 12
                                      catálogo por     assinaturas e 15 supremas
                                      classe.          integradas; equilíbrio e
                                                       validação final pendentes

  P-019             Morte             Definir se a      Concluído
                                      morte encerra     (pausar, voltar
                                      imediatamente a   onda 1 ou sala de espera)
                                      partida ou        
                                      permite alguma    
                                      forma de          
                                      recuperação.      

  P-020             Plataforma        Definir se o      Pendente
                                      lançamento será   
                                      apenas desktop ou 
                                      também adaptado a 
                                      dispositivos      
                                      móveis.           

  P-021             Personagens       Definir regras    Parcialmente
                                      finais de nome,   definido;
                                      classe e estado   restam detalhes
                                      persistido.       

  P-022             Cartas            Balancear e     Parcialmente
                                      validar as      catálogo com 36 cartas,
                                      passivas       novas sinergias e testes;
                                      no combate      calibração pendente

  P-023             Talentos          Balancear       Árvores, loadout e efeitos
                                      magnitudes      cobertos por testes nas
                                                       quatro classes; E2E em
                                                       banco descartável validou
                                                       os fluxos nas quatro.
                                                       Calibração em combate e
                                                       Encaixes dependem de itens.

  P-024             Pets e           Definir tipos,  Pendente
                    montarias        obtenção, usos,
                                     habilidades e
                                     efeitos de jogo

  P-025             Chefes e         Definir/implementar Depende da simulação
                    estados          elementos,
                                     resistências,
                                     fraquezas,
                                     quebra de escudo,
                                     sangramento,
                                     paralisia e
                                     queimadura       P-031 para definir
                                                      gatilhos/efeitos

  P-026             Hub de fim       Completar hub    Parcial
                    de capítulo      com Inventário,  (tela-base da Sala de Espera feita;
                                     Baú, Estatísticas serviços faltam)
                                     e Status

  P-027             Movimento e IA   Validar rotas   Parcial: colisão ambiental
                    dos monstros     e contorno     da Fase 1 implementada;
                                                     testes anteriores cobrem
                                                     somente a versão antiga.
                                                     Editor
                                                     e integração visual v0.139
                                                     não validados; outras fases
                                                     não testadas.
                                                     Movimento autoritativo e
                                                     sincronização multiplayer
                                                     pendentes

  P-028             Sala de Espera social     Implementar     Pendente
                    e serviços       presença de     (tela-base feita;
                                     amigos, grupo,   recursos online
                                     convites e       faltam)
                                     acesso aos
                                     serviços

  P-029             Atributos        Calibrar as     Quatro atributos e efeitos
                    do personagem    magnitudes de   de combate implementados e
                                     Força, Agilidade, cobertos por testes;
                                     Vitalidade e     falta balancear magnitudes
                                     Energia         e validar builds em combate

  P-030             Equipamentos     Adaptar efeitos Referência recebida;
                    e opções          de armas,       números e regras
                                      armaduras, asas, aguardam simulação
                                      acessórios,
                                      elementos e
                                      roubo de Vida

  P-031             Modelo de        Fechar fórmulas Em andamento:
                    combate           integradas,                         baseline v0.123;
                                      grupo e níveis  TTK comum 3,5–5,2 s,
                                                      semichefe 20,1–35,0 s,
                                                      chefe 61,4–111,0 s;
                                                      suíte Python v0.133:
                                                      84 testes (não recalcula
                                                      todo P-031); movimento
                                                      ativo, builds, horda,
                                                      equipamentos, cooperação
                                                      e endgame pendentes
  P-032             Poções e          Definir estoque, Pendente de
                    auto-poção VIP    obtenção, uso e integração
                                      balanceamento na economia
  P-033             Câmera e          Revisar projeção  Base 2.5D/zoom v0.105
                    profundidade      final após P-031 implementada; movimento e
                                                       zoom manualmente validados;
                                                       acabamento final pendente
  P-034             Coleta de itens   Simular alcance, Pendente de
                    por pet/VIP        efeito no drop  balanceamento;
                                      e modo coop      valores sugeridos
                                                      ainda não adotados
  P-035             Auto-ataque PvE   Suspenso pela    Ataques exigem comando
                    Premium/VIP       decisão v0.107  explícito; reabrir só com
                                                       nova aprovação
  P-036             Movimento do      Observar o chefe  Validado manualmente:
                    chefe             durante o ciclo   ataques, avisos e reposicionamento
  P-037             Alcance e cartas  Automatizar timer, Prazo VIP e substituição
                                      recomendação e    automática em 8/8 observados;
                                      troca VIP         manter coleção se inferior
                                                       e automação E2E pendentes
  P-040             HUD de combate   —                  Concluído: posição da
                    compacto                            contagem na barra superior
                                                       conferida visualmente em
                                                       desktop
  P-041             Atributos         Automatizar tela   alocação manual e recarga
                    em tempo real                       validação visual concluída;
                                                       Socket.IO cobre atributos,
                                                       mensagens, automação VIP e
                                                       persistência
  P-042             Evoluções de       Testar fluxos       conteúdo e efeitos
                    classe              completos           automatizados; compra,
                                                          bloqueio, troca VIP e
                                                          persistência E2E nas
                                                          quatro classes em banco
                                                          descartável; balanceamento
                                                          e integração de Encaixes
                                                          com itens pendentes
  P-043             Hordas e           Medir combate     Simulação determinística
                    desafio            em simulação      executada e testes aprovados;
                                                       horda parada é prova de
                                                       estresse letal; movimento
                                                       ativo/cooperação pendentes
  P-044             Registro de bugs   Criar regressões   Documento criado; cada correção
                    e regressões       para correções     deve ter teste automatizado
  P-045             Controles, HUD     Testes de          Persistência automatizada;
                    de alvo e câmera   integração         movimento e limites do zoom
                                                         verificados no navegador;
                                                         fallback de Mana e Avanço
                                                         validados; mira por mouse,
                                                         Numpad e pitch pendentes
  P-046             Cartas com         Criar testes de    Troca e manutenção em 8/8,
                    coleção cheia      integração         persistência e detalhes
                                                         validados no navegador e cobertos
                                                         por testes de integração
  P-047             Teto 170 e        Rebalancear XP,    Direção registrada v0.135;
                    balanceamento     PL e combate       código ainda usa teto 400;
                                                        projeções/TTKs anteriores
                                                        são snapshot, não validam a
                                                        meta nova; fórmulas, testes
                                                        e gameplay representativo
                                                        pendentes
  P-048             Missões, risco,    Validar outros     Backend/UI implementados;
                    recompensas e      cenários e         E2E navegador da Fase 10
                    espólios             calibrar/aprovar    até resgate, com progresso
                                         candidatos          pré-carregado e harness;
                                                         quatro riscos, recompensas,
                                                         raridades e HTML do lobby
                                                         cobertos por testes;
                                                         Python v0.134: 84 testes;
                                                         JS: 10 testes, incluindo
                                                         E2E da Fase 10 em três
                                                         riscos e inventário cheio;
                                                         teste humano e decisão
                                                         dos candidatos pendentes
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 20. Decisões consolidadas

### Cobertura automatizada e simulação — estado documental v0.134

- P-022: calibrar os valores das cartas e validar o equilíbrio em partida.
  Testes automatizados cobrem bônus de projétil/elemento, cura de habilidade e
  recomendação compatível com a especialização, habilidade assinatura e passiva.
- P-037: prazo VIP de 10 segundos e escolha automática numa coleção 8/8 foram
  observados manualmente; automatizar o ciclo e validar que uma oferta inferior
  à carta ativa menos útil mantém a coleção.
- P-037: testar 25 EXP por orbe em conta comum e o novo valor provisório de
  40 EXP por orbe no Premium/VIP, incluindo se surgem ofertas suficientes antes
  do fim da partida.
- P-040: posição da contagem de monstros na barra superior, junto de fase e
  onda, conferida visualmente em desktop; nenhuma validação pendente registrada.
- P-041: efeitos de Agilidade, limites e aplicação em combate têm testes;
  testes Socket.IO cobrem alocação dos quatro atributos, resumo de combate,
  distribuição automática VIP para as quatro classes, ativação/desativação,
  mensagens e persistência. E2E v0.119 confirmou visualmente as notificações
  manual, automática e de desativação.
- P-042: conteúdo, custos, prévia das classes, Keystone e efeitos têm testes;
  compra, bloqueio, recusa de troca sem o benefício especial, troca VIP com
  reembolso de talentos/atributos e persistência após nova consulta estão
  automatizados para as quatro classes. E2E v0.120 validou escolha, compra,
  bloqueio visual, persistência após recarga e troca VIP nas quatro classes em
  banco descartável. Balancear magnitudes em jogo e integrar Encaixes com itens.
- P-044: adicionar testes de regressão para bugs corrigidos e ampliar a suíte
  quando o registro indicar uma área ainda sem cobertura.
- P-043: simulação determinística e testes executados em 15/11/2026; medem
  densidade, TTK e pressão de sobrevivência com as fórmulas de produção.
  Avançar para movimento real e cooperação. O cenário parado de 50% de acertos
  permanece uma prova de estresse letal.
- P-045: persistência de esquema, espaços e botões foi verificada no navegador
  e ganhou teste de integração. E2E v0.120 confirmou fallback para Ataque básico
  com Mana zerada, dano no alvo e Avanço através do cerco. Faltam mira por mouse,
  Numpad e validação visual do pitch em resoluções variadas.
- P-046: E2E v0.119 substituiu uma carta e manteve a coleção em 8/8; os dois
  resultados persistiram após recarga. Testes de integração cobrem substituição
  e descarte da oferta sem alterar as cartas ativas. O prazo VIP e a decisão
  automática inferior permanecem em P-037.
- P-047: a validação de progressão/combate v0.123 passou com 71 testes e verifica
  progressão de XP, níveis 10/50/100/400,
  fase/abates necessários para o nível 400, orçamento de XP por fase, TTK,
  sobrevivência inicial, curva inimiga e migração idempotente. Atualizar os
  testes sempre que essas fórmulas ou parâmetros mudarem. Recompensas de endgame
  ainda exigem definição. A matriz atualizada percorre as 12 árvores completas
  no nível 400 contra o chefe teórico da fase 70; o TTK ficou entre 64,2 e
  99,5 s sem itens/cartas. Esse benchmark é uma extrapolação, não uma fase
  implementada nem validação em combate ativo.
  A suíte v0.124 passou com 76 testes após adicionar P-048; os resultados
  específicos de balanceamento P-047 não foram recalculados nesta rodada.
  Crítico/esquiva por Agilidade e sua aplicação em combate têm testes; os
  percentuais continuam candidatos até validação integrada de equilíbrio.
- P-048: os testes existentes cobrem desbloqueio em cascata, crédito
  idempotente, staging/capacidade, autorização de rotas, congelamento na
  contagem e conclusão pela última onda. A v0.128 acrescenta verificações
  determinísticas para Vida e dano em encontros comuns, semichefes e chefes,
  quantidade de inimigos, Ouro, chances e pesos de raridade nos quatro riscos.
  Um teste de rota confirma que o lobby renderiza os quatro perfis e os
  identifica como candidatos. A suíte completa v0.131 passou com 84 testes;
  `compileall` concluiu sem erros em v0.133. E2E em navegador com banco
  descartável percorreu as dez ondas da Fase 10 por ataques Socket.IO até o
  chefe de ato; modal, recompensa e resgate de três baús foram confirmados.
  As Fases 1–9 foram pré-carregadas e atributos/coordenadas do harness
  aceleraram o combate; não foi gameplay representativo. Em v0.133, Playwright
  também executou o aplicativo Flask/Socket.IO real com sessão e banco
  temporários nos riscos Moderado, Alto e Extremo: contagem, movimento por
  teclado, Ataque básico e dano inimigo na Vida. O teste de inventário abriu os
  espólios em 30/30, vendeu item antigo, resgatou o baú e confirmou a capacidade
  final. O acesso aos riscos foi liberado semeando o progresso anterior; naquele
  snapshot, cada combate novo percorreu somente a primeira onda. A limitação de
  fase completa foi superada pelos E2E v0.134 descritos abaixo; ainda não há
  validação de mira manual, equilíbrio ou
  avaliação visual manual. Cadência, dificuldade, economia, raridades e
  capacidade continuam candidatas, sem aprovação final.
  Em v0.134, três novos E2E completaram a Fase 10 em Moderado, Alto e Extremo,
  do início ao chefe e à tela pós-fase, com eventos Socket.IO reais. Duraram
  cerca de 66–80 s por cenário e registraram dano inimigo. O fixture preparou
  os desbloqueios e usou nível 400, atributos no teto de 10.000 e coordenadas
  de alvo do harness; não demonstra progressão natural, movimento/mira humana
  ou equilíbrio real. A suíte JS passou com 10 testes, Python com 84 e
  `compileall` sem erros. A simulação de balanceamento foi reexecutada, mas
  continua sendo evidência matemática. Avaliação manual de desafio/recompensa
  e aprovação dos valores candidatos seguem pendentes.
  Em v0.130, `npm run test:js` passou com três verificações: sintaxe dos
  scripts first-party e dois fluxos executados em Chromium com Playwright.
  Eles usam HTML mínimo de teste, não carregam templates Flask, backend,
  Socket.IO ou sessão autenticada e não são E2E completo da missão nem
  confirmação visual manual.
  A v0.131 também serializa inícios de missão por conta: não há segunda run
  ativa em outro personagem e espólios pendentes pausam as ações das runs
  existentes. Dois testes de regressão cobrem esses casos. A calibração dos
  multiplicadores, Ouro, raridades e capacidade de 30 espaços permanece
  pendente; nenhum valor foi promovido ou aprovado. Baús continuam registros
  de protótipo, não equipamentos reais.
  Testes de rota v0.128 confirmam os perfis candidatos dos quatro riscos, a
  seleção agrupada por Ato 1/2/3 e que o
  resumo de Ouro/ocupação aparece em `/inventario`, não na Sala de Espera;
  não houve E2E visual autenticado nesta rodada.
  Ouro é moeda virtual inteira por conta, sem saque, conversão ou vínculo com
  pagamentos reais; a calibração e aprovação das quantias candidatas seguem pendentes.

### Resultado histórico da validação automatizada — v0.119 (15/11/2026)

- `python -m unittest discover -s tests -v`: **63 testes aprovados**.
- Os testes de talento validam compra, bloqueio de ramo, troca VIP com
  reembolso e persistência para as quatro classes, além da recusa de troca sem
  o benefício especial.
- Os testes Socket.IO validam os quatro atributos e seus efeitos no resumo de
  combate, mensagens e emissões `attributes:updated`; distribuição automática
  VIP para as quatro classes, ativação/desativação, persistência e recusa sem
  VIP também foram cobertas.
- E2E no navegador confirmou avisos de atributos, persistência de controles,
  movimento, limites de zoom, substituição de carta VIP 8/8 e manutenção das
  oito cartas após recarga. O navegador também exibiu descrições das ofertas.
- `python scripts/simulate_live_balance.py`: concluído; inclui baseline e
  matriz dos 12 caminhos completos de talentos no nível 400.
- TTK registrado naquela versão: comuns **3,5–5,2 s**; semichefes
  **20,1–31,6 s**; chefes **63,2–130 s** nos marcos 1/100/220/400. Esses
  valores foram supersedidos pela simulação atual v0.123; conservar aqui como
  registro histórico, não como baseline vigente.
- Horda parada com 50% de acertos antes da esquiva: derrota das quatro classes.
  Resultado previsto como estresse; não substitui teste de movimento ativo.
- Estes resultados validam código e modelo determinístico, não a experiência
  subjetiva em partida, cooperação, builds equipadas ou os fluxos web pendentes.

### Resultado histórico da validação — v0.120 (15/11/2026 08:54:49 UTC−03:00)

- `python -m unittest discover -s tests -v`: **65 testes aprovados**.
- Teste de regressão reproduziu o bloqueio por ataque inimigo expirado antes
  da correção; após a limpeza do estado expirado antes da checagem de bloqueio,
  ataques subsequentes são aceitos. Cliente também tem timeout e limpeza de
  estado na desconexão.
- E2E isolado de talentos no Guardião: escolha do ramo, compra de talento,
  bloqueio visual de outro ramo, persistência após recarga e troca VIP com
  reembolso de 2 Pontos de Legado.
- Complemento E2E em navegador, com conta e banco descartáveis: escolha,
  compra, bloqueio de ramo, troca VIP com reembolso e persistência após recarga
  também foram confirmados no Tecelão, Caçador e Lâmina Arcana.
- E2E isolado de combate: com Mana zerada, o comando acionou Ataque básico e
  causou dano; Avanço atravessou o cerco. O teste não substitui avaliação longa
  de sobrevivência em combate ativo.
- Interface conferida em desktop e celular: pontos livres na coluna esquerda,
  sem barra inferior e com coordenadas X/Y ainda visíveis no canto inferior.

### Decisões de balanceamento registradas na v0.120 — histórico

- Manter a horda como desafio de esquiva. Não reduzir a densidade, o dano nem a
  frequência dos ataques comuns para acomodar o cenário de jogador parado.
  Na simulação estacionária, 50% de acertos antes da esquiva é letal; o modelo
  exige evitar mais de 90% dos ataques e não representa movimento ativo.
- Manter a resistência elemental de 30% do chefe. Na simulação v0.120, foi
  aceita uma exceção de até 130 s para o Tecelão contra o chefe de Fogo; essa
  medição foi supersedida pela matriz atual, que apresenta os novos
  benchmarks, sem alterar a aprovação da resistência elemental.

O responsável informou como OK os demais itens da validação manual de P-037 e
P-036, além da HUD anterior em telas grandes e pequenas. O foco visual imediato
é desktop; adaptação de controles para tablets e celulares fica para uma etapa
posterior. Não substituir regressões automatizadas por pedidos de validação
manual; ampliar `tests/` quando um comportamento ainda não tiver cobertura.

### Direção híbrida pós-400 — P-003 (histórica, sob revisão)

O modelo híbrido de marcos pós-400 (títulos, cosméticos, recordes e equipamentos
com poder limitado) foi aprovado anteriormente, quando o teto de design era
400. A decisão v0.135 substituiu essa direção por teto-alvo 170 e rebalanceamento
da progressão; o destino do endgame e das recompensas após o nível 170 precisa
ser revisto depois da recalibração. A implementação atual ainda usa teto 400.
O sistema de equipamentos/inventário final não existe; o staging P-048 é um
protótipo. Não introduzir moeda nova sem decisão explícita; Ouro permanece
virtual e separado de pagamentos reais.

Esta lista resume o que já foi informado e incorporado ao documento:

-   Nome do jogo: **Crônicas do Recomeço**.
-   Mistura de RPG clássico inspirado em MU Online com estrutura
    roguelike.
-   Ambientação medieval dark fantasy, sombria e original.
-   Câmera isométrica ou superior em estilo ARPG.
-   Partidas organizadas em salas e ondas.
-   **Registro histórico superado:** progressão infinita, semichefe na onda 9
    e chefe em toda onda 10. A Temporada 1 atual tem 30 fases, dez ondas por
    fase; a onda 10 tem semichefe em 5/15/25, chefe de ato em 10/20/30 e
    encontro comum nas demais. A Fase 30 encerra a campanha.
-   Ao iniciar uma fase após derrotar o chefe, o personagem recebe 30
    segundos de preparação antes de a horda começar. Vida e Mana são
    restauradas nesse momento; ondas comuns não restauram esses recursos.
-   A coleção de cartas é temporária por fase; as cartas ativas são removidas
    ao derrotar o chefe e começa uma nova coleção na fase seguinte.
-   A morte pausa o jogo; o jogador pode reiniciar a fase ou ir à Sala de Espera.
-   Após selecionar personagem, o botão Jogar abre a sala de espera. A capacidade
    desejada do grupo é de três jogadores (jogador e dois amigos).
-   Recargas-base do protótipo: ataque básico 1,15 s; habilidades-base de
   Guerreiro/Tecelão 5 s, Caçador 4,5 s e Lâmina Arcana 6 s; Avanço 3 s.
   Agilidade reduz provisoriamente 0,5% por ponto, com redução
    máxima de 50%; valores aguardam balanceamento.
-   Ao concluir um capítulo (a cada 10 fases), a partida pausa e abre uma
    área para Inventário, Baú, Estatísticas e Status do Personagem (P-026).
-   O HUD mostra monstros restantes. Chefes deverão exibir elemento,
    resistências e estados (escudo quebrado, sangramento, paralisia,
    queimadura); regras e parâmetros continuam em P-025.
-   Ondas com duração aproximada de 30 a 60 segundos.
-   Escalonamento de monstros por onda e nível do jogador.
-   Eventos especiais e chefes em intervalos de ondas.
-   Progressão de nível planejada de 1 a 400.
-   Atributos: Força, Agilidade, Vitalidade e Energia.
-   Árvore de Talentos própria para cada classe, com trilhas ramificadas,
    atributos e vantagens adequadas ao arquétipo. Os Pontos de Legado
    compram nós; efeitos/custos seguem em protótipo até balanceamento.
-   Classes iniciais visíveis: Guerreiro, Tecelão (mago), Caçador (arqueiro)
    e Lâmina Arcana (híbrida). Os IDs internos permanecem estáveis.
-   Personagens são criados e selecionados após o login; os limites são 4
    por conta padrão e 6 por conta Premium/VIP.
-   Deletar personagem remove seus dados vinculados após confirmação; o
    Baú da Conta é removido junto ao último personagem da conta.
-   Nível máximo 400 sem Reset; nível, EXP, atributos e talentos não são
    reiniciados para ganhar recompensas.
-   Pontos de Legado pela fórmula `nível // 10 + nível // 50 + nível // 25`,
    totalizando 64 no nível 400; migração retroativa idempotente.
-   Melhorias temporárias são cartas: uma oferta inicial permite começar a
    coleção; durante a partida, orbes coletáveis de EXP enchem uma barra e
    liberam uma escolha entre 3 cartas para adicionar ou substituir. Não há
    nível individual das cartas. Coleção ativa de 6 cartas padrão ou 8
    Premium/VIP; pelo menos 30 cartas distintas com efeitos e raridade
    visível. A coleção é removida no fim da partida e usa pesos iniciais de
    raridade 50/25/14/7/3/1% do Comum ao Lendário. Cartas não ativas podem
    voltar a aparecer em ondas futuras.
-   Referência de itens MU Online foi recebida e adaptada como base de análise,
    sem adotar seus valores. Ver `balanceamento/base_enviada_itens_mu_online.md`.
-   O modelo de balanceamento deverá considerar dano elemental causado e roubo
    de Vida, além de resistências, regeneração passiva e cura ao eliminar.
    Fórmulas e limites ainda não foram definidos.
-   Não há Pontos de Legado por morte ou fim de partida; após o nível 400,
    recompensas de endgame ainda precisam ser definidas em P-003/P-047.
-   Combate manual em todos os modos; proposta de auto-ataque PvE P-035
    suspensa pela decisão v0.107 e fora da implementação atual.
-   Sistema oficial de **6 níveis de raridade e cores de borda** para
    todos os itens (Comum, Incomum, Raro, Excelente, Épico, Lendário).
-   Separação visual entre borda externa (raridade) e brilho interno
    (aprimoramento).
-   Joias, aprimoramento de equipamentos e efeitos visuais por nível.
-   Asas criáveis pela Forja do Caos.
-   Pets como companheiros visuais e montarias para deslocamento; detalhes
    de obtenção, mecânicas e efeitos ainda pendentes.
-   Itens persistentes após morte, guardados no inventário ou baú.
-   Inventário com 8 colunas como referência.
-   Mochila inicial com 16 espaços e baú inicial com 24 espaços.
-   Expansão gratuita por Árvore de Talentos e expansões premium
    propostas.
-   Sala de Espera com salas abertas ou privadas para amigos.
-   Cooperação em salas planejada.
-   Trade e mercado entre jogadores propostos.
-   PvP 1x1 mencionado, ainda sem regras definidas.
-   Direção visual com preto abissal, ardósia, aço, bronze e brilhos de
    raridade.
-   HTML5, JavaScript, Tailwind CSS, Python, Flask e Socket.IO sobre
    WebSocket como tecnologias planejadas.
-   SQLite para protótipo e PostgreSQL como recomendação para produção.
-   Servidor como autoridade para validar ações, inventário e economia.

------------------------------------------------------------------------
