# Direção aprovada — progressão e balanceamento

**Estado:** direção de design atualizada em 15/11/2026. O teto-alvo decidido é
170, com rebalanceamento de XP, Pontos de Legado e combate ainda pendente.
Nenhuma fórmula ou valor novo foi aprovado; o código continua temporariamente
com teto 400.
**Atualizado em:** 15/11/2026 16:38:57 (UTC−03:00), v0.135.

## Direção vigente — teto-alvo 170

- Alterar o teto-alvo do personagem para 170 e rebalancear a progressão de XP,
  a concessão de Pontos de Legado e o combate para a campanha de 30 fases.
- Esta é uma direção decidida, mas ainda não implementada. Até a alteração do
  código, `MAX_LEVEL` permanece em 400.
- Recalcular projeção de nível/XP por fase e PL, escalas de Vida/dano dos
  inimigos, TTK e sobrevivência. Os resultados da curva anterior, inclusive
  nível 170/26 PL ao fim da Fase 30 e simulações até 400, não aprovam a nova
  calibração.
- A direção anterior de endgame pós-400 fica sob revisão, pois depende do teto
  que foi substituído.

## Snapshot anterior — progressão até 400 (direção superada)

As regras e valores abaixo registram a implementação/direção anterior à decisão
v0.135. Permanecem úteis para descrever o código atual, mas não são a meta de
balanceamento do teto 170.

### Progressão anterior

- A Temporada 1 tem 30 fases, organizadas em três atos de dez, com dez ondas
  por fase. Semichefes aparecem na onda 10 das fases 5/15/25; chefes de ato,
  nas fases 10/20/30. A Fase 30 encerra a temporada, sem fase 31.
- O jogo usa nove temas visuais para agrupar as fases da Temporada 1, mas
  mantém uma arena lógica única. Os temas visuais dos Atos 2 e 3 são
  provisórios; sua lore não está aprovada. A história detalhada ainda cobre
  apenas as Fases 1–10.
- No baseline anterior, a simulação de XP projetava nível 170 e 26 Pontos de
  Legado ao fim da Fase 30. Essa projeção não é uma meta de ritmo validada nem
  o resultado final da nova curva.
- No baseline anterior, o personagem progredia continuamente do nível 1 ao
  máximo **400**, sem Reset e sem nível 1000. Naquela decisão, o teto 400 era
  futuro; foi superado pela direção v0.135 de teto-alvo 170, ainda sem alteração
  do código.
  A campanha termina na Fase 30 e fases posteriores não estão implementadas.
- Após a Fase 30, temporadas futuras ou endgame ainda exigem definição de
  conteúdo, progressão e recompensas; não estender automaticamente a cadência
  atual.
- Direção híbrida de endgame aprovada em v0.120, sob revisão após a mudança do
  teto: marcos pós-400 concederiam
  títulos/cosméticos e recordes, além de equipamentos com poder limitado. O
  sistema de equipamentos ainda não existe; slots, atributos, teto de poder,
  cadência dos marcos e recompensas específicas continuam pendentes. Não criar
  moeda nova sem decisão explícita.
- Não existe botão, endpoint ou recompensa de Reset. Nível, EXP, atributos e
  talentos não são apagados para continuar a progressão.
- A fórmula aprovada em v0.115 é `nível // 10 + nível // 50 + nível // 25`.
  Ela concede **64 Pontos de Legado** no nível 400, o bastante para concluir
  qualquer caminho de talentos (58 ou 64 pontos). Nenhum ponto é concedido por
  morte ou fim de partida.
- Personagens já existentes recebem retroativamente o saldo mínimo dos marcos
  alcançados, somado aos Resets registrados no campo legado. A migração é
  idempotente e nunca reduz saldo nem remove talentos comprados.
- O campo `characters.resets` fica somente para compatibilidade dos bancos e
  recuperação dos pontos históricos. Não é exibido nem usado como mecânica.
- A dificuldade de inimigos aumenta com o nível inimigo até o nível 400; as
  fórmulas atuais estão implementadas, mas são parâmetros candidatos e precisam
  de validação por faixa. Após o teto, os tipos de recompensa híbrida estão
  aprovados; faltam regras numéricas e implementação.

## Atributos e identidade das classes

- Quatro atributos: Força (dano físico), Agilidade (ataque, mobilidade e defesa),
  Vitalidade (Vida) e Energia (Mana, magia e habilidades). Cada ponto de
  Agilidade concede +0,01 ponto percentual de chance crítica e +0,01 ponto
  percentual de esquiva, além dos efeitos de combate já existentes.
- Valores-base candidatos do material recebido já estão no protótipo e entram
  nos cálculos provisórios. Eles ainda não são valores finais aprovados; sua
  calibração depende de testes de combate e validação integrada.
- Todas as classes recebem **5 pontos por nível ganho**, inclusive a classe
  híbrida. A proposta de 7 pontos para o Gladiador Mágico é descartada porque
  a justificativa de equipamento/evolução não existe no jogo e criaria vantagem
  permanente sem contrapartida.
- A distribuição automática opcional de pontos é um benefício de conveniência
  Premium/VIP; a distribuição manual permanece acessível. Os pesos atuais são
  protótipos e devem ser verificados para que o VIP não tenha uma vantagem de
  poder sobre uma build manual bem montada.
- A Lâmina Arcana permanece selecionável desde o começo (ID interno
  `rune_blade`), conforme o criador atual. O desbloqueio no nível 220 da
  referência é descartado.
- Nível 1 começa sem pontos livres; cada subida de nível concede 5. Entre os
  níveis 1 e 400 são ganhos 1.995 pontos (399 subidas).
- Teto provisório de 10.000 por atributo, validado pelo servidor. É menor que
  32.767; como não há Reset, esse teto não pressupõe ciclos de progressão
  adicionais nem representa uma meta de build. Será revisto na calibração de
  combate.

## Combate e simplicidade para o jogador

- A interface exibe os pontos livres e a estimativa dos efeitos antes de
  confirmar cada investimento. Os textos devem explicar o ganho em valores
  finais compreensíveis.
- O balanceamento deve considerar conjuntamente dano elemental causado,
  resistências e efeitos elementais, roubo de Vida, regeneração passiva e cura
  por eliminação. As mecânicas são diferentes; fórmulas e valores permanecem
  pendentes.
- O protótipo já conecta atributos a fórmulas provisórias de Vida e dano do
  personagem e dos inimigos; a Vida máxima do personagem usa base 120. Não
  tratar a antiga escala de Vida 1.000/dano fixo como atual nem copiar
  diretamente as fórmulas recebidas. A tarefa vigente é calibrar em conjunto
  os cálculos implementados, não migrá-los.
- Metas de calibração solo: monstro comum 3–6 s, semichefe 20–35 s e chefe
  60–100 s; personagem inicial aguenta aproximadamente 6–10 ataques comuns.
  São alvos de teste, não garantias de balanceamento.
- A horda permanece um desafio centrado em esquiva: não reduzir quantidade,
  dano ou frequência dos ataques comuns para acomodar a simulação de jogador
  parado. O cenário com 50% de acertos é uma prova de estresse, não uma previsão
  de movimento ativo.
- Manter a resistência elemental de 30% dos chefes como contrajogada. A antiga
  medição de 130 s do Tecelão contra o chefe de Fogo pertence a uma simulação
  anterior; a simulação atual registra 61,4–111,0 s para chefes nos
  checkpoints 1/100/220/400 e 64,2–99,5 s para as 12 builds completas contra o
  chefe teórico da fase 70. O alvo padrão de chefe continua 60–100 s; esses
  modelos ainda exigem calibração em combate ativo.
- Chance crítica e esquiva são percentuais aditivos com limites de 50% e 35%,
  respectivamente. Cada ponto de Agilidade concede +0,01 ponto percentual de
  cada chance; talentos, passivas e cartas
  acumulam com esse valor. O crítico causa 1,5× o dano normal e uma esquiva
  bem-sucedida anula o dano do ataque. Dano líquido mantém piso e limites para
  impedir dano zero ou redução infinita.
- Progressão de inimigos e recompensas será testada por faixas de nível e fase;
  também deve cobrir quantidade/composição do grupo (solo a 3 jogadores),
  equipamentos e efeitos elementais. Chefes e resistências serão calibrados com
  atributos, dano elemental, cura e roubo de Vida no mesmo modelo.
- O protótipo já calcula o nível inimigo por `5 × fase + onda`, limitado a 400,
  e fixa no início da fase um orçamento de seis vezes a EXP necessária para o
  próximo nível (`100 + 25 × nível`). O total é distribuído pelos abates com
  pesos 1/3/5 para comum/semichefe/chefe. A tabela antiga de 1 nível por fase
  não é a regra atual. Esses parâmetros estão implementados como candidatos;
  falta calibrar o ritmo e validá-lo em combate ativo antes de tratá-los como
  balanceamento final.

## Árvore de Talentos e redistribuição

- Árvore continua exclusiva por classe e compra com Pontos de Legado.
- Cada uma das 12 especializações recebe talentos, descrições e modificadores
  próprios, conectados aos atributos, à passiva e às habilidades ativas.
- Um caminho completo custa 58 ou 64 Pontos de Legado: 42 em atributos, 2 em
  aprimoramento de combate, 4 no talento principal, 4 nas maestrias da habilidade
  base e da assinatura, e 6 por habilidade suprema (4 para desbloquear e 2 para
  maestria). Nove caminhos custam 58 PL e três custam 64 PL; cada personagem
  pode desenvolver apenas o caminho escolhido.
- O custo dos três caminhos por classe é: Guerreiro 180 PL, Caçador 174 PL,
  Tecelão 186 PL e Lâmina Arcana 174 PL; total das 12
  opções: 714 PL. Esses totais são comparativos, não um custo por personagem.
- A fórmula atual concede 64 pontos até o nível 400 e cobre qualquer caminho
  individual. Não há custo atual de 48 PL por caminho.
- A Agilidade também aumenta crítico e esquiva sem criar nós ou custos novos:
  o limite de 64 PL continua suficiente para concluir o caminho escolhido.
- Na primeira abertura da árvore nova, os talentos v0.104 comprados são
  devolvidos uma única vez, incluindo seus pontos e atributos. Talentos
  v0.102/v0.103 continuam registrados como legado.
- Talentos poderão ter ranks e limites visíveis, definidos junto com os atributos
  após as simulações. Não inventar ranks/ganhos antes dessa calibração.
- Redistribuição será gratuita para Premium/VIP. Conta comum paga Ouro; preço
  será centralizado como parâmetro e calibrado quando a economia de Ouro/drop/venda
  estiver implementada, evitando um preço arbitrário sem referência de renda.

## Ordem de trabalho para fechar o balanceamento

1. Confirmar o modelo completo de poder: atributos, habilidades, equipamentos,
   aprimoramentos, dano elemental, resistências/estados, cura/roubo de Vida,
   progressão, economia e grupo cooperativo.
2. Definir a ordem de cálculo e limites para danos fixos/percentuais, crítico,
   defesa, absorção, esquiva, cura e recuperação por eliminação.
3. Integrar os efeitos dos atributos e equipamentos em uma fórmula coerente;
   registrar parâmetros centrais e apresentar no HUD valores compreensíveis.
4. Calibrar inimigos, XP e drops por nível, fase, onda e tamanho do
   grupo. Incluir os alvos de duração e sobrevivência como critérios de teste.
5. Simular builds das quatro classes em nível 1, 50, 100, 220 e 400,
   com conjuntos de equipamento e combinações ofensivas/defensivas.
6. Revisar talentos, cartas, pets e montarias contra o mesmo orçamento de poder.
7. Calibrar ouro, aprimoramento, consumo de poções e custo de redistribuição
   com renda/gasto observados nas simulações.

Os atributos-base e a distribuição de 5 pontos por nível já estão prototipados.
O Reset foi removido e os Pontos de Legado agora são ganhos pelos marcos de
nível. O orçamento de XP por fase e a relação fase/onda/nível inimigo já estão
implementados como parâmetros candidatos; dificuldade, ritmo de progressão e
requisitos do endgame ainda precisam de validação manual. A projeção de fases
não é uma meta final.

Se um teste falhar, ajustar parâmetros no módulo central e repetir a faixa
afetada. Não fazer correções pontuais no HUD ou em inimigos para esconder uma
fórmula desbalanceada.

## Missões e recompensas — P-048 (estado, não aprovação)

O fluxo de quatro dificuldades, Ouro virtual inteiro creditado na conta,
raridades de baú
e staging está implementado como protótipo. Os multiplicadores, densidade,
valores por abate, bônus de fase/chefe, probabilidades de baú/venda e limite
de 30 espaços não foram aprovados como regras de balanceamento. Ouro não
representa dinheiro real e não deve ser convertido nem usado em pagamentos.
Antes de aprovar, simular a renda e o tempo de
progressão por dificuldade, testar sobrevivência/TTK em combate ativo e
verificar que os prêmios não distorçam a futura economia de itens. Os valores
em execução e os critérios pendentes constam em P-048, no Roadmap e em
`03_itens_e_economia.md`. O E2E em navegador da Fase 10 confirmou o percurso
técnico até o resgate; progresso pré-carregado e harness acelerado impedem
interpretá-lo como calibração ou aprovação dos valores candidatos.
