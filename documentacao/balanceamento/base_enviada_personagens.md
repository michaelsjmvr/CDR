# Base enviada — Balanceamento de personagens

**Estado:** referência recebida do responsável; proposta para avaliação.
Não tratar automaticamente cada número como regra implementada/aprovada.

Este arquivo preserva o conteúdo matemático do material enviado, organizado
com notas de compatibilização. A aplicação ao código depende da etapa de
balanceamento e confirmação dos valores finais.
**Nota sobre nomes:** os rótulos antigos usados na tabela são preservados por
serem parte da referência recebida. Os nomes visíveis atuais são Guerreiro,
Tecelão, Caçador e Lâmina Arcana; os IDs internos das quatro classes não mudam.
**Nota de estado atual:** as fórmulas abaixo continuam como referência recebida,
nunca como parâmetros automaticamente aprovados. O código ainda progride até
400 sem Reset, mas a direção decidida em v0.135 é um teto-alvo 170 e
rebalanceamento de XP, PL e combate; a mudança está pendente. Os quatro
atributos já participam das fórmulas provisórias, ainda sujeitas a calibração.
Consultar `decisoes_aprovadas.md` para a direção vigente.
**Atualizado em:** 15/11/2026 16:38:57 (UTC−03:00), v0.135.

## Classes e arquétipos mapeados

| Arquétipo da referência | Classe original do projeto | Função |
| --- | --- | --- |
| Guerreiro (BK) | Guardião do Umbral | Corpo a corpo, resistência e dano físico |
| Mago (SM) | Tecelão de Cinzas | Dano mágico em área, mana e escudo arcano |
| Elfo (ME) | Vigia do Ermo | Distância, esquiva e suporte |
| Gladiador Mágico (MG) | Lâmina Rúnica | Híbrido de força e magia |

A classe híbrida é indicada como desbloqueada no nível 220 na referência.
Essa exigência foi descartada: as quatro classes continuam disponíveis desde
a criação do personagem.

## Atributos iniciais e pontos por nível

| Classe | Força | Agilidade | Vitalidade | Energia | Vida base | Mana base | Pontos/nível |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Guardião do Umbral | 28 | 20 | 25 | 10 | 110 | 20 | 5 |
| Tecelão de Cinzas | 18 | 18 | 15 | 30 | 60 | 60 | 5 |
| Vigia do Ermo | 22 | 25 | 20 | 15 | 80 | 30 | 5 |
| Lâmina Rúnica | 26 | 26 | 26 | 26 | 110 | 60 | 7 |

A referência declara progressão acumulativa após Reset e limite de 32.767
pontos por atributo; ambos são apenas dados da fonte recebida. O projeto não
tem Reset e usa teto técnico provisório de 10.000. A proposta de 7 pontos por
nível para a Lâmina Rúnica foi descartada; todas as classes recebem 5 pontos
por nível ganho. Os motivos sobre elmo/evolução não existem como sistemas
implementados no projeto.

## Fórmulas propostas

As fórmulas abaixo são transcritas da referência. `Nível` representa o nível
atual do personagem; a unidade das taxas de ataque/acerto e o arredondamento
precisam ser definidos na implementação.

### Guardião do Umbral (Guerreiro)

- Dano físico mínimo: Força / 6.
- Dano físico máximo: Força / 4.
- Defesa base: Agilidade / 3.
- Velocidade de ataque: Agilidade / 15.
- Taxa de acerto: (Nível × 5) + (Agilidade × 1,5) + (Força / 4).
- Esquiva: Agilidade / 3.
- Vida máxima: 35 + ((Nível − 1) × 2) + (Vitalidade × 3).
- Mana máxima: 10 + ((Nível − 1) × 0,5) + Energia.
- Multiplicador de habilidade física: 200% + (Energia / 10)% do dano final.
- Trava proposta: limitar o multiplicador para evitar eliminações em um golpe.

### Tecelão de Cinzas (Mago)

- Dano físico mínimo/máximo: Força / 8 e Força / 4.
- Dano mágico mínimo/máximo: Energia / 9 e Energia / 4.
- Defesa base: Agilidade / 4.
- Velocidade de ataque: Agilidade / 10.
- Taxa de acerto: (Nível × 5) + (Agilidade × 1,5) + (Força / 4).
- Esquiva: Agilidade / 3.
- Vida máxima: 30 + (Nível − 1) + (Vitalidade × 2).
- Mana máxima: (Energia + Nível − 1) × 2.
- Escudo de mana: 10% + (Agilidade / 50)% + (Energia / 200)%; teto 60%.

### Vigia do Ermo (Elfo)

- Dano físico mínimo: (Agilidade / 8) + (Força / 14).
- Dano físico máximo: (Agilidade / 4) + (Força / 8).
- Defesa base: Agilidade / 10.
- Velocidade de ataque: Agilidade / 50.
- Taxa de acerto: (Nível × 5) + (Agilidade × 1,5) + (Força / 4).
- Esquiva: Agilidade / 4.
- Vida máxima: 40 + (Nível − 1) + (Vitalidade × 2).
- Mana máxima: 6 + ((Nível − 1) × 1,5) + (Energia × 1,5).
- Cura de suporte: (Energia / 5) + 5.
- Defesa extra: (Energia / 8) + 2.
- Ataque extra: (Energia / 7) + 3.

### Lâmina Rúnica (Gladiador Mágico)

- Dano físico mínimo: (Força / 6) + (Energia / 12).
- Dano físico máximo: (Força / 4) + (Energia / 8).
- Dano mágico mínimo/máximo: Energia / 9 e Energia / 4.
- Defesa base: Agilidade / 5.
- Velocidade de ataque: Agilidade / 15 físico; Agilidade / 20 mágico.
- Taxa de acerto: (Nível × 5) + (Agilidade × 1,5) + (Força / 4).
- Esquiva: Agilidade / 3.
- Vida máxima: 58 + (Nível − 1) + (Vitalidade × 2).
- Mana máxima: 8 + (Nível − 1) + (Energia × 2).

## Fórmulas gerais de combate propostas

- Dano líquido PvE: dano total do atacante − (defesa total do alvo / 2).
- Acerto: comparar taxa de acerto do atacante com esquiva do alvo; a
  probabilidade e a regra exata para igualdade ainda precisam ser definidas.
- Monstros: a referência propõe escalar nível, vida, dano, defesa e chances
  por faixa de Reset. Essa proposta é histórica e não se aplica ao jogo atual,
  que não tem Reset; a escala vigente usa fase/onda e para no nível 400.
- Limites: teto de 32.767 em atributo; escudo de mana limitado a 60%; dano,
  vida e interfaces devem suportar inteiros de 32/64 bits sem overflow.

## Questões de integração com as regras atuais

1. A referência original menciona 1 Ponto de Legado por Reset e recompensas por
   incursão. A regra vigente não concede pontos por Reset nem por fim de run:
   o Reset foi removido, e os Pontos de Legado seguem marcos de nível.
2. A progressão vigente é contínua até o nível 400, sem Reset. O nível inimigo
   usa `5 × fase + onda`, limitado a 400; cada fase tem orçamento fixo de EXP,
   distribuído pelos abates com pesos 1/3/5. O balanceamento e as recompensas
   pós-400 ainda precisam de validação/definição.
3. **Registro histórico superado:** a escala antiga de Vida 1.000, Mana 200,
   ataques fixos e inimigos com Vida 100/320/600 não descreve o combate atual.
4. As fórmulas da referência não especificam regras suficientes para taxa de
   acerto, esquiva, defesa, velocidade de ataque e arredondamento. Essa é uma
   limitação do material recebido, não uma afirmação de que o protótipo atual
   não tenha regras; consultar as decisões aprovadas para o estado vigente.
5. A Lâmina Rúnica permanece disponível desde o início; o requisito de
   desbloqueio no nível 220 foi descartado na decisão de produto.
6. As árvores de talentos e o reembolso já foram integrados ao projeto. A
   calibração de efeitos permanece pendente; os custos e as regras vigentes de
   redistribuição estão registrados em `decisoes_aprovadas.md`.

## Estado e próximo fluxo de trabalho no projeto

- Atributos-base candidatos, banco, distribuição manual, 5 pontos por nível e
  opção de distribuição automática VIP estão implementados. Força, Agilidade,
  Vitalidade e Energia já afetam as fórmulas provisórias de combate; a
  calibração integrada continua pendente.
- **Nota histórica superada:** uma decisão anterior propunha Reset para nível
  1 e inimigos escalados pelo número de Resets. A decisão vigente removeu o
  Reset; não aplicar essa regra nem a escala associada.
- Os valores-base de atributos deste arquivo ainda são candidatos; os pontos
  por nível finais são 5 para todas as classes, substituindo a tabela original
  de 7 pontos para a classe híbrida.
- Antes de promover as fórmulas recebidas, comparar o modelo de combate atual
  com equipamentos, habilidades, dano elemental, resistências/estados, roubo de
  Vida, regeneração e cura por eliminação; simular inimigos, economia e builds
  até o nível 400.
- Requisitos de nível/classe dos equipamentos, progressão de equipamento e
  restauração de Vida/Mana entre fases continuam a exigir definição. Não há
  novo ciclo de Reset.

Até essas decisões, este documento é uma base de trabalho, não um conjunto de
valores numéricos já aplicado ao combate.
