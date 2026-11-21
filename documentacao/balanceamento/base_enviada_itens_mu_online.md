# Referência enviada — itens e opções inspirados em MU Online

**Origem:** texto enviado pelo responsável em 13/11/2026, baseado em MU
Online 97d+99i e versões expandidas.

**Uso neste projeto:** material comparativo para futura modelagem de armas,
armaduras, acessórios, asas, pets, montarias e aprimoramentos. As regras e
valores abaixo registram a referência recebida; não são estatísticas aprovadas
para Crônicas do Recomeço e não devem ser copiados diretamente.
**Nota de estado atual:** o código ainda progride até o nível 400 sem Reset,
mas a direção decidida em v0.135 é teto-alvo 170 com rebalanceamento de XP,
Pontos de Legado e combate, ainda pendente. As opções de equipamento abaixo
permanecem apenas como referência, sem implicar que o sistema de equipamentos
já esteja implementado.
**Atualizado em:** 15/11/2026 16:38:57 (UTC−03:00).

## 1. Conteúdo da referência recebida

### 1.1 Armas

Referência de tipos: espadas, machados, cajados, arcos e bestas.

- A arma soma dano direto ao cálculo-base do personagem.
- Aprimoramento de +0 a +11 na versão 97d ou até +15 em versões expandidas.
  Cada nível acrescenta cerca de 3–4 pontos aos danos mínimo e máximo; acima
  de +9, os bônus crescem progressivamente para +5, +6 e valores seguintes.
- Cajados podem conceder aumento percentual de dano mágico (referência: +20%
  a +85%), aplicado ao dano mágico baseado em Energia.
- Adicional de Vida citado: +4 a +16 de dano físico ou mágico.
- Opção Sorte: +5% de chance crítica, com dano no máximo da faixa da arma, e
  +25% de chance de sucesso em aprimoramento.
- Opções excelentes ofensivas citadas: 10% de chance de dano excelente
  (110% do dano máximo e parte da defesa ignorada); dano adicional baseado no
  nível do personagem dividido por 20; +2% de dano; +7 de velocidade de ataque;
  recuperar Vida Máxima/8 ou Mana Máxima/8 por monstro eliminado. Essa é
  recuperação por eliminação, não roubo de Vida por dano causado.

### 1.2 Armaduras e escudos

Referência de peças: elmo, peito, calça, luvas, botas e escudos.

- Aprimoramento +0 a +11/+15 acrescenta defesa por peça: cerca de +3 por nível,
  aumentando para +4 a +6 após +9.
- Conjunto completo: referência de 5 peças, ou 4 para Gladiador Mágico,
  concede +10% de chance de esquiva.
- Se todas as peças do conjunto estiverem em +10 ou mais, a referência concede
  +5% de defesa total por nível acima de +9, até +30% em +15.
- Adicional de Vida citado: +4 a +16 de defesa por peça; no escudo, alternativa
  de +5 a +20 na taxa de bloqueio.
- Opções excelentes defensivas citadas: +4% de Vida Máxima, +4% de Mana
  Máxima, redução de dano recebido de 4%, reflexão de dano de 5%, +10% de
  chance de defesa/esquiva e +40% de Ouro derrubado por monstro.
- A referência soma essas opções entre várias peças, escudo e anéis, chegando
  a valores altos de redução, reflexão, esquiva, Vida e bônus de Ouro.

### 1.3 Asas

A referência trata asas como itens que aumentam dano e absorvem dano recebido.

| Categoria da referência | Classes | Defesa base +0 | Aumento de dano base a +11 | Absorção base a +11 |
| --- | --- | ---: | ---: | ---: |
| Nível 1 (Satan, Angel, Fairy) | Todas | 10–20 | 12% → 23% | 12% → 23% |
| Nível 2 (Dragon, Soul, Spirit, Darkness) | Evoluídas e MG | 25–45 | 32% → 43% | 25% → 36% |

Opções especiais de nível 2 citadas: +115 Vida, +115 Mana, 3% de chance de
ignorar defesa ou +5 de velocidade de ataque. Também são citados adicionais
de Vida para dano e recuperação automática de Vida.

### 1.4 Pets e montarias

A referência descreve um único espaço de companheiro, exigindo escolha entre
ataque, defesa ou mobilidade:

| Exemplo citado | Papel e efeito na referência |
| --- | --- |
| Diabrete (Imp) | +30% de dano físico e mágico; consome Vida do pet por ataque. |
| Anjo Guardião | Absorve 20% do dano e concede +50 de Vida Máxima. |
| Unicórnio (Uniria) | Aumenta movimento e impede recuo por golpes críticos. |
| Dinorant | Aumenta movimento, concede +15% de dano e absorve 10% de dano; opções citadas incluem +5% absorção ou +5 velocidade de ataque. |

O espaço único e os efeitos são exemplos da referência, não regras aprovadas
para o sistema de pets/montarias do nosso jogo.

### 1.5 Anéis e pendentes

- Dois anéis defensivos e um pendente ofensivo.
- Aprimoramento do acessório aumenta resistência elemental específica
  (Fogo, Gelo, Veneno, Raio, Terra, Vento ou Água) e reduz chance/efeito de
  estados negativos.
- Adicional de Vida citado: 1% a 4% de regeneração automática por segundo em
  cada acessório; a referência calcula até 12% no total.
- Opções excelentes dos anéis repetem as opções defensivas das armaduras.
- Opções excelentes dos pendentes repetem as opções ofensivas das armas.

## 2. O que isso muda na análise do nosso balanceamento

O material destaca que o personagem não é definido apenas por nível e
atributos. Arma, armadura completa, escudo, asas, acessórios, opções do item,
aprimoramento e companheiro podem alterar simultaneamente dano, sobrevivência,
recargas, resistência elemental e renda de Ouro. O responsável acrescentou dois
fatores que também precisam entrar no modelo: **dano elemental causado** e
**roubo de Vida**. Esses sistemas precisam ser considerados antes de fechar as
fórmulas finais do personagem e dos monstros.

### 2.1 Fatores adicionais aprovados para análise

Estes fatores foram solicitados pelo responsável como parte da futura etapa de
balanceamento. Sua existência deve ser considerada no modelo; as fontes,
fórmulas, tipos, valores e limites continuam sem definição.

- **Dano elemental causado:** dano de Fogo, Gelo, Raio ou outros elementos
  poderá vir de atributos, arma, opção, carta, pet ou habilidade. Deve ser
  separado da parcela física/mágica para que só a parte elemental seja
  comparada com a resistência correspondente, uma única vez e de forma visível
  ao jogador. A lista final de elementos e se cada dano é fixo, percentual ou
  convertido ainda estão abertos.
- **Roubo de Vida:** recuperação vinculada ao dano efetivamente causado. É
  diferente de regeneração passiva e de recuperar Vida ao eliminar um monstro.
  Definir a base de cálculo (dano antes/depois das resistências, dano real à
  Vida ou outro valor), limites por golpe/segundo, interação com dano em área,
  chefes, escudos, dano contínuo e Vida já cheia.
- **Resistência e estados elementais:** decidir a ordem entre dano elemental,
  resistência, absorção e efeitos como queimadura, congelamento ou choque. Um
  estado não deve receber múltiplas aplicações de resistência nem permitir
  controle ou dano contínuo ilimitado.

Riscos principais ao adaptar a referência:

1. Somar muitas opções percentuais de redução de dano, absorção, esquiva,
   Vida, dano e velocidade pode tornar o personagem quase invulnerável ou
   multiplicar dano/recuperação sem limite útil.
2. Repetir as mesmas opções em armadura, anéis, pendente e asas permite
   empilhamento muito maior do que o jogador percebe pela interface.
3. Valores fixos de MU Online não correspondem à escala atual do protótipo
   (Vida 1.000, dano fixo e inimigos provisórios).
4. Chance crítica, dano excelente, ignorar defesa, reflexão, regeneração por
   segundo, recuperação por morte, dano elemental e roubo de Vida precisam ter
   definições sem sobreposição e limites explícitos.
5. Opções de Ouro aumentam a economia e, por consequência, o poder de comprar,
   aprimorar ou redistribuir; precisam ser calibradas junto de drops e preços.

## 3. Diretrizes de adaptação para Crônicas do Recomeço

- Usar o material como catálogo de categorias e relações entre equipamentos,
  não como tabela numérica pronta.
- Separar bônus fixos de bônus percentuais e declarar se percentuais somam ou
  multiplicam; usar tetos ou retornos decrescentes para defesa, esquiva,
  velocidade, absorção, dano elemental e recuperação.
- Calcular o dano e a defesa efetivos a partir do personagem e do equipamento
  equipado, sem misturar escalas antigas e novas.
- Considerar bônus de conjunto e escolhas ofensivas/defensivas como decisões
  legíveis para o jogador, com tooltip mostrando o efeito final.
- Tratar asas como equipamento de alto impacto e testar dano e defesa juntos.
- Avaliar pets e montarias como sistemas separados: pet pode oferecer
  companhia/efeito de combate; montaria pode enfatizar deslocamento. A quantidade
  de slots e a possibilidade de acumular bônus continuam em aberto.
- Definir resistência elemental e efeitos de estado em conjunto com os chefes,
  para que resistir a um elemento não anule completamente um encontro.
- Balancear dano elemental causado junto da resistência correspondente e
  definir uma regra explícita de roubo de Vida, separada de regeneração e
  recuperação por eliminação.
- Balancear bônus de Ouro com a economia, drops, preços e eventual custo de
  redistribuição de talentos.

### 3.1 Modelo de papéis recomendado para o nosso jogo

Esta tradução preserva as escolhas interessantes da referência sem copiar sua
quantidade de multiplicadores. É uma recomendação para a futura modelagem; não
fecha números nem substitui a simulação do P-031.

- **Arma:** principal fonte de dano direto e identidade de combate da classe.
  Cajados favorecem magia; arcos/bestas favorecem alcance; armas corpo a corpo
  favorecem dano próximo. Velocidade e crítico devem entrar no orçamento da
  arma, sem somar bônus repetidos ilimitadamente.
- **Armadura e escudo:** defesa e sobrevivência previsíveis. Cada peça deve ter
  função simples; conjunto completo pode oferecer um bônus pequeno de estilo,
  evitando acrescentar ao mesmo tempo grandes percentuais de Vida, defesa,
  esquiva e absorção.
- **Asas:** item de progressão marcante com um benefício ofensivo e um defensivo
  moderados. Dano e absorção precisam ocupar o mesmo orçamento de poder; asas
  não devem virar multiplicador obrigatório para todas as builds.
- **Acessórios:** escolhas legíveis para resistência elemental, recurso,
  recuperação ou utilidade. Cada acessório deve cobrir uma necessidade
  diferente, sem replicar em vários espaços a mesma redução/cura percentual.
- **Pet:** companhia com uma função de combate escolhida — ofensiva, defensiva
  ou suporte — e contribuição limitada. **Montaria:** prioridade em mobilidade
  e deslocamento; qualquer bônus de combate deve ser pequeno. Separar esses
  papéis evita que equipar ambos some dois pacotes completos de poder.
- **Elementos:** dano elemental e resistência precisam aparecer como partes
  explícitas do cálculo. A mesma parcela passa por sua resistência uma vez;
  estados negativos têm duração, chance e limite próprios.
- **Roubo de Vida e poções:** são fontes distintas. Roubo depende do dano real
  causado; poção é uma recuperação pontual sujeita a recarga e obtenção. As
  três fontes (poções, roubo e regeneração) devem compartilhar o orçamento de
  sobrevivência, especialmente contra chefes.
- **Aprimoramento e raridade:** devem aumentar escolhas e especialização, não
  apenas empilhar porcentagens universais. O jogador precisa conseguir
  comparar o efeito final sem fazer contas externas.

O jogo tem ondas curtas e grupos de até três jogadores, diferente dos spots e
do ritmo de MU Online. Por isso, a progressão de equipamento deve ser medida
por tempo para derrotar inimigos, golpes sobrevividos e contribuição em grupo;
percentuais e bônus de Ouro da referência são apenas ideias funcionais.

## 4. Decisões que continuam pendentes

- Atributos e fórmulas numéricas de cada tipo de equipamento.
- Faixa de aprimoramento, bônus por nível e riscos/custos da Forja do Caos.
- Quantidade de opções por raridade e frequência de combinações.
- Regras de empilhamento, tetos e retornos decrescentes para bônus percentuais.
- Bônus de conjuntos, escudos, asas, acessórios, pets e montarias.
- Fontes/tipos e cálculo do dano elemental; interação com resistências e
  estados de combate.
- Base, limites e alvos válidos do roubo de Vida; interação com dano em área,
  chefes, dano contínuo, escudos e outras curas.
- **Nota superada:** uma proposta anterior previa equipamentos persistentes e
  inimigos escalados pelo número de Resets. Não há Reset na direção vigente;
  o balanceamento de equipamentos deve considerar a progressão contínua até o
  nível 400 e as recompensas pós-400, ainda pendentes.
- Como obter, guardar, repor e usar poções; no protótipo, auto-poções VIP têm
  recargas e restauração provisórias, mas ainda não consomem itens do inventário.

**Próximo uso:** ao iniciar a etapa de itens/equipamentos, consultar este
arquivo junto de `03_itens_e_economia.md`, `decisoes_aprovadas.md` e do modelo
de atributos. Não implementar os valores da referência sem simulação e
aprovação específica.
