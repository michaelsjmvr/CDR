# Auditoria do balanceamento e primeira simulação

**Criado em:** 13/11/2026  
**Atualizado em:** 15/11/2026 21:54:32 (UTC−03:00), v0.139 (ponteiro do índice; sem alteração dos dados de balanceamento).
**Decisão v0.135 — 15/11/2026 (UTC−03:00):** o teto-alvo é 170, com rebalanceamento de XP, PL e combate
pendente. O código e os dados simulados ainda usam teto 400. Os resultados
abaixo são snapshots anteriores; não validam a projeção, recompensas ou
dificuldade da meta nova, e nenhum valor foi aprovado.
**Nota de escopo:** os resultados identificados por versão são snapshots. Na
v0.132, `scripts/simulate_live_balance.py` foi executado: o baseline sem
equipamentos, cartas ou talentos comprados mediu TTK de 3,5–5,2 s para comuns,
20,1–35,0 s para semichefes e 61,4–111,0 s para chefes nos checkpoints
1/100/220/400; as 12 builds completas ficaram em 64,2–99,5 s contra o chefe
teórico da fase 70. São resultados matemáticos, não validação em combate ativo,
e não aprovam nenhum parâmetro. O bloco P-048 v0.126 e sua contagem de 78 testes
são históricos. O estado técnico mais recente está no Documento Mestre v0.139
e no Roadmap; em v0.134 passaram 84 testes Python, `compileall` sem erros e
10 testes JavaScript. E2E completou a Fase 10 em três riscos com harness
acelerado. A simulação v0.134 reproduziu as mesmas faixas baseline de TTK e
projeções; isso não aprova valores.
**Baseline anterior:** as fórmulas de progressão e combate estão implementadas
no código atual, mas foram calibradas para o teto 400, direção agora superada.
A projeção anterior de nível 170/26 PL e o benchmark extrapolado da fase
69/70 não são metas do novo design. Os TTKs e as 12 builds descritos abaixo
continuam evidência matemática do snapshot anterior, sem validação do teto 170.
Recalcular orçamento de XP por fase, curva de PL, Vida/dano inimigo e TTK, e
validar com gameplay antes de aprovar valores.
**Escopo:** documentos em `balanceamento/`, pendências de progressão/combate
(P-029 a P-035, P-047/P-048) e fórmulas de atributos, XP, dificuldade e
recompensas existentes no código.

> **Nota histórica de versão:** tabelas que chamam a fase 69 de chefe ou usam
> a projeção antiga de 5.585 abates foram supersedidas. O modelo pré-v0.135
> projetava nível 400 na fase 69/6.502 abates e usava a fase 70 como benchmark
> teórico de chefe. Esses dados não estendem o conteúdo jogável nem definem a
> meta atual de nível 170.
> Os nomes de classe nas tabelas reproduzem os rótulos vigentes na data da
> simulação; os nomes visíveis atuais são Guerreiro, Tecelão, Caçador e Lâmina
> Arcana, com os mesmos IDs internos.

## Conclusão da auditoria

Ainda faltam implementação e validação para fechar o novo balanceamento. A
direção de teto-alvo 170 foi decidida; recalcular XP, Pontos de Legado e combate
é pendência. O código continua em 400 enquanto isso não for implementado. Os
atributos e fórmulas atuais seguem candidatos; equipamentos, cartas, habilidades
e builds completos ainda precisam ser avaliados em conjunto.

**Registro histórico da implementação — v0.109 (superado):** Reset e nível 1000
foram retirados. A primeira fórmula concedia 48 Pontos de Legado no nível 400;
ela foi substituída em v0.115 pela curva vigente, que concede 64. A primeira
curva de Vida/dano inimigo descrita nos registros desta versão também não deve
ser lida isoladamente como a especificação atual. Os parâmetros de cada etapa
foram candidatos de protótipo, não balanceamento concluído.

**Atualização de implementação — v0.115:** a curva de Legado passou a
`nível // 10 + nível // 50 + nível // 25`, totalizando 64 pontos no nível 400.
As 12 especializações custam 58 ou 64 pontos cada para concluir; o total
agregado é 714, mas cada personagem investe em um único caminho. Os testes de
progressão e combate e a simulação de balanceamento foram executados.

**Estado de validação da progressão/combate (v0.123):** a suíte passou com 71 testes.
Sem equipamento, cartas ou talentos comprados, o TTK simulado ficou em
3,5–5,2 s para comuns, 20,1–35,0 s para semichefes e 61,4–111,0 s para chefes
nos checkpoints 1/100/220/400. As 12 builds completas no nível 400 contra o
chefe teórico da fase 70 ficaram entre 64,2 e 99,5 s. Os resultados são
determinísticos e não representam uma partida ativa. A direção híbrida pós-400
(cosméticos/recordes e equipamentos com poder limitado) foi aprovada; o
sistema de itens e os limites de poder/recompensa ainda precisam ser definidos
antes de simular o endgame.

**Registro histórico P-048 (v0.126):** a implementação passou a exibir e contabilizar
Ouro inteiro em carteira por conta, mantendo as quantias inteiras candidatas;
os valores não têm equivalência nem conversão para dinheiro real. A suíte
completa passou com 78 testes; cinco testes originais cobrem autorização,
desbloqueio, crédito idempotente, staging/capacidade, contagem e conclusão,
com regressões adicionais para formatação inteira e migração do esquema antigo.
Um E2E em navegador com banco descartável percorreu as dez ondas da Fase 10,
por ataques Socket.IO até o chefe, e confirmou modal, crédito e resgate de três
baús. As Fases 1–9 foram pré-carregadas para liberar a fase; atributos e
coordenadas enviados pelo harness aceleraram o combate. Portanto, não valida
progressão natural, movimento, mira manual, IA, equilíbrio ou gameplay
representativo. Outras dificuldades e o cenário de inventário cheio ainda
precisam de E2E. Multiplicadores de Vida/dano, inimigos adicionais, moeda por
abate, bônus, pesos de raridade, valores de venda e inventário de 30 espaços
são candidatos do código, não resultados aprovados. Ouro é moeda virtual de
jogo, sem valor real, saque ou conversão; compras com dinheiro real devem
permanecer em fluxo separado. Calibrar em combate ativo antes de atualizar
decisões aprovadas.

Ainda faltam avaliar em conjunto equipamentos e requisitos por nível, builds
completas, poções com estoque, pets, montarias e escala de grupo. Talentos,
efeitos de cartas, dano elemental, estados e roubo de Vida já participam do
combate, mas seus valores ainda precisam de calibração. Não é correto declarar
todo o jogo balanceado nem copiar os números de MU Online.

O baseline sem equipamento para as quatro classes e os níveis 1/100/220/400 já
foi implementado e automatizado. A próxima rodada deve acrescentar equipamentos,
cartas, talentos e habilidades ao mesmo orçamento de poder e validar o ritmo em
movimento ativo; o cenário de horda parada é apenas uma prova de estresse.

## Registro histórico supersedido: matriz de árvores completas — v0.119

> Esta matriz usa o chefe da fase 69, que não é um chefe na cadência atual.
> Ela foi supersedida pelo benchmark teórico na fase 70 descrito no estado
> vigente acima; os resultados abaixo não são referência atual de balanceamento.

`python scripts/simulate_live_balance.py` agora também simula cada caminho com
todos os seus talentos comprados, no nível 400, contra o chefe da fase 69/onda
10 (nível inimigo 355), sem equipamento ou cartas. Os tempos supõem uma rotação
perfeita de Ataque básico e habilidade, sem movimento ou dano recebido; são
comparáveis ao alvo de TTK, não substituem uma partida real.

| Classe | Caminho | PL gastos / 64 | TTK (s) |
| --- | --- | ---: | ---: |
| Guardião do Umbral | Furioso | 58 / 64 | 65,6 |
| Guardião do Umbral | Guardião | 64 / 64 | 80,5 |
| Guardião do Umbral | Senhor da Guerra | 58 / 64 | 71,7 |
| Vigia do Ermo | Atirador de Elite | 58 / 64 | 85,1 |
| Vigia do Ermo | Domador de Feras | 58 / 64 | 91,4 |
| Vigia do Ermo | Arqueiro Arcano | 58 / 64 | 85,1 |
| Tecelão de Cinzas | Arquimago | 64 / 64 | 122,5 |
| Tecelão de Cinzas | Necromante | 64 / 64 | 119,0 |
| Tecelão de Cinzas | Sábio | 58 / 64 | 128,2 |
| Lâmina Rúnica | Lâmina Arcana | 58 / 64 | 57,3 |
| Lâmina Rúnica | Gladiador Etéreo | 58 / 64 | 64,7 |
| Lâmina Rúnica | Forjador de Almas | 58 / 64 | 68,2 |

Todos os caminhos cabem no orçamento de 64 PL do nível 400. Oito resultados
ficaram no alvo padrão de 60–100 s; os três caminhos do Tecelão atingiram
119,0–128,2 s, abaixo da exceção aprovada de 130 s contra o chefe de Fogo.
Lâmina Arcana ficou 2,7 s abaixo do limite inferior padrão. Nenhum parâmetro foi
alterado: falta validar builds e combate ativo em mais faixas antes de decidir
se esse desvio exige ajuste.

## Regras confirmadas que entram no modelo

- Quatro classes disponíveis desde a criação: Guardião do Umbral, Tecelão de
  Cinzas, Vigia do Ermo e Lâmina Rúnica.
- Cinco pontos por nível; 1.995 pontos ganhos entre nível 1 e nível 400.
- Não há Reset nem níveis acima de 400. Pontos de Legado seguem
  `nível // 10 + nível // 50 + nível // 25`; 64 são acumulados ao nível 400.
- Inimigos escalam com fase/onda até o nível 400; curva e ritmo aguardam teste.
- Alvos iniciais de calibração solo: comum em 3–6 s, semichefe em 20–35 s,
  chefe em 60–100 s; personagem inicial sobrevive a aproximadamente 6–10
  ataques comuns.
- VIP pode automatizar a distribuição de atributos como conveniência, sem
  receber uma build numericamente superior. Auto-ataque PvE VIP P-035 está
  suspenso; não implementar sem nova aprovação.

## Registros históricos de simulação e propostas

> As seções a seguir registram hipóteses e estados de versões anteriores; não
> são especificação do combate atual nem uma lista atual de tarefas. Em especial,
> o retrato inicial de Vida fixa 1.000, atributos sem efeito e apenas Corte
> Rúnico disponível foi superado pela implementação registrada em v0.120 e
> descrita no resumo vigente deste documento.

## Resultado da simulação das fórmulas recebidas — registro histórico

O script `scripts/simulate_balance_model.py` aplica às fórmulas enviadas as
prioridades de distribuição automática atualmente usadas no protótipo. Ele
não altera o jogo e não considera itens, talentos, cartas ou o combate ao vivo.

| Medida nos quatro arquétipos | Nível 1 | Nível 400 |
| --- | ---: | ---: |
| Vida máxima mínima–máxima | 60–110 | 1.107–2.702 |
| Mana máxima mínima–máxima | 20–60 | 419,5–2.452 |
| Dano básico candidato mínimo–máximo entre classes | 3,3–9,8 | 69,3–283,2 |

O híbrido tem faixas físicas e mágicas diferentes; a tabela agrega apenas os
extremos observados. Cada classe e cada tipo de dano aparecem detalhados pelo
simulador.

A projeção anterior chegava ao nível 400 na fase 63 após cerca de **1.637
eliminações**, sem equipamentos. Depois, o modelo estimou 69 fases/5.585
abates; ambos os cálculos foram superados pela projeção atual de 69 fases/6.502
abates. A Temporada 1 termina na fase 30 e projeta nível 170/26 Pontos de
Legado, ainda sem validação de ritmo em combate ativo.

### Primeira proposta numérica — baseline sem equipamento (histórica/superada)

Para começar a calibrar de fato, o mesmo simulador agora compara um primeiro
modelo simples com as metas de combate. São fórmulas de **teste**, ainda sem
efeitos de equipamento ou habilidades ativas. A base usa os atributos de
classe e os pesos VIP existentes:

- Dano básico candidato: Guardião `10 + 0,50 × Força + 0,20 × Agilidade`;
  Tecelão `20 + 0,35 × Energia + 0,20 × Agilidade`; Vigia `10 + 0,35 ×
  Agilidade + 0,20 × Força`; Lâmina `10 + 0,40 × Força + 0,40 × Energia +
  0,10 × Agilidade`. Os coeficientes do Tecelão, Vigia e Lâmina foram
  ajustados nesta rodada para reduzir a diferença entre distribuições e classes.
- Vida máxima: `100 + 1,5 × (nível − 1) + 2 × Vitalidade`.
- Mana máxima: `60 + (nível − 1) + 1,5 × Energia`.
- Redução de recarga por Agilidade: `0,04%` por ponto, limitada a `35%`.
- Recarga básica: `1,15 s × (1 − redução por Agilidade)`. O valor inicial foi
  ajustado na simulação comparativa para manter o ataque dentro da meta de
  3–6 s por inimigo comum também em uma build manual focada em Agilidade.
- Inimigo comum provisório: Vida `143 × 1,05 × [1 + 0,06 × (nível inimigo − 6)]`;
  dano recebido `12 + 0,65 × nível inimigo`. O nível usa o mapeamento atual
  (`5 × fase + onda`), que permanece sob revisão.

| Nível | TTK só com ataque básico (VIP e builds manuais) | Ataques comuns sobrevividos |
| ---: | ---: | ---: |
| 1 | 4,6–6,8 s | 8,2–9,6 |
| 100 | 4,3–6,3 s | 6,9–9,2 |
| 220 | 4,3–5,6 s | 6,3–8,8 |
| 400 | 4,0–5,4 s | 6,1–8,7 |

Esses primeiros passes ficam dentro das metas aprovadas para inimigos comuns e
golpes sobrevividos, mas não são balanceamento fechado. O simulador compara
também uma distribuição manual representativa: Guardião 60% Força/25%
Vitalidade/15% Agilidade; Tecelão 60% Energia/25% Vitalidade/15% Agilidade;
Vigia 55% Agilidade/25% Vitalidade/20% Força; Lâmina 35% Força/35% Energia/
20% Vitalidade/10% Agilidade. Essas divisões são cenários de análise, não uma
recomendação final. A tabela mostra as faixas de ataque básico sem habilidade;
as rotações ativas são comparadas separadamente a seguir.
### Primeira proposta de habilidades e chefes (histórica/superada)

Para representar as quatro classes, o simulador usa um ataque ativo de alvo
único por arquétipo. Os nomes são rótulos provisórios; não definem ainda
animação, elemento, área, estados ou versão final das habilidades.

| Classe | Habilidade candidata | Dano relativo ao ataque básico | Custo de Mana | Recarga-base |
| --- | --- | ---: | ---: | ---: |
| Guardião do Umbral | Impacto do Umbral | 1,25× | 18 | 8 s |
| Tecelão de Cinzas | Chama Crescente | 1,50× | 24 | 9 s |
| Vigia do Ermo | Disparo Perfurante | 1,25× | 18 | 7 s |
| Lâmina Rúnica | Ruptura Rúnica | 1,25× | 22 | 8 s |

Ataques básicos e habilidades têm recargas independentes, como os controles
atuais do jogo. A simulação começa com ambos disponíveis, aplica a mesma
redução provisória de recarga por Agilidade e não regenera Mana durante o
combate. Vida de semichefe e chefe usa multiplicadores de 6,5× e 18× sobre o
inimigo comum, escalados de 75% a 100% desse valor entre os níveis 1 e 400.
Essa curva de elite é um recurso de calibração, não uma regra aprovada.

| Alvo | Nível 1 | Nível 100 | Nível 220 | Nível 400 | Meta registrada |
| --- | ---: | ---: | ---: | ---: | ---: |
| Comum | 3,4–5,7 s | 3,2–5,4 s | 3,2–5,6 s | 3,0–5,5 s | 3–6 s |
| Semichefe | 19,4–30,7 s | 21,0–31,5 s | 22,4–34,5 s | 24,1–36,5 s | 20–35 s |
| Chefe | 62,8–96,8 s | 60,9–88,0 s | 65,0–98,5 s | 69,2–103,1 s | 60–100 s |

O desvio mais claro é o Tecelão VIP no nível 400: chega a 36,5 s no semichefe
e 103,1 s no chefe. O resultado de 19,4 s no semichefe do nível 1 pertence ao
Tecelão (VIP e build manual começam com os mesmos atributos), não ao Guardião.
Esses extremos precisam ser calibrados antes de conectar o modelo ao combate. A simulação não considera dano elemental,
resistência do chefe, estados, área de efeito, interrupção, movimentação,
grupo, regeneração ou poções; os alvos são de um inimigo parado e em combate
solo.

O script cobre semichefes e chefes como alvos de Vida fixa provisória, mas não
simula seus padrões de ataque, movimento ou resistências elementais. Também
seguem fora do modelo itens, grupo, poções, estados, área de efeito e
regeneração. **Retrato histórico superado:** naquela etapa, as habilidades
acima eram apenas parâmetros de simulação e Corte Rúnico era a única ativa no
jogo. Esse registro não descreve o catálogo de habilidades da v0.120.

## Problemas encontrados na primeira simulação (registro histórico)

1. **Retrato antigo superado:** naquela versão o jogo usava 1.000 de Vida,
   200 de Mana, ataque fixo 35, habilidade fixa 100 e inimigos com Vida
   100/320/600; atributos não afetavam esses cálculos. Isso não é o estado atual.
2. As fórmulas recebidas produzem faixas de Vida, Mana e dano muito diferentes
   entre classes. Isso pode expressar papéis, mas precisa ser comparado aos
   tempos de combate e ataques sobrevividos antes de ser adotado.
3. `Agilidade / 15`, `/10` ou `/50` foi chamada de velocidade de ataque na
   referência, mas a unidade não está definida. No código atual, a redução de
   recarga de 0,5% por Agilidade atinge o teto de 50% em 100 pontos; com os
   pesos VIP atuais, as quatro classes já chegam a esse teto até o nível 100.
   Esse crescimento precisa ser recalibrado antes de ligar Agilidade aos
   cooldowns reais.
4. **Retrato antigo superado:** naquela versão apenas Corte Rúnico existia
   como habilidade ativa; as habilidades e passivas das classes foram
   implementadas depois e seguem em calibração.
5. Vida/Mana e dano usam fórmulas candidatas ligadas aos atributos; a curva de
   inimigos por nível foi aplicada em v0.109 e ainda requer calibração manual.
6. O modelo não pode fechar ainda defesa, chance de acerto/esquiva, crítico,
   resistência elemental, estados, cura, roubo de Vida, Mana, consumíveis,
   equipamento ou escala para grupos de até três.

## Próxima sequência de trabalho da primeira simulação (registro histórico)

1. **Concluído como simulação:** recalibrar os casos de elite e comparar uma
   auto-distribuição VIP candidata com builds manuais representativas, sem
   alterar os pesos/fórmulas do jogo.
2. Definir para cada habilidade candidata alvo, área, elemento, efeito de
   estado, duração, chance, acúmulo e interação com movimento. Simular estados
   de chefe antes de implementar P-025.
3. Avaliar variações de builds e partidas em grupo sem transformar VIP em
   vantagem numérica; ajustar ameaça, dano e tempo de combate no modelo.
4. Conectar atributos derivados a todas as rotas Socket.IO e ao HUD, com o
   servidor como autoridade; incluir mudanças de nível sem valores
   antigos presos em constantes.
5. Calibrar a escala de inimigos e EXP por nível/fase/onda, depois solo/dupla/
   trio, e repetir os cenários de níveis 1/100/220/400.
6. Acrescentar habilidades de classe, equipamento, elementos, talentos, cartas,
   pets/montarias e poções ao orçamento de poder; recalibrar a cada camada.
7. Fechar economia, drops, aprimoramento e redistribuição quando houver dados de
   renda/gasto; validar o endgame após o nível 400 antes de chamar a etapa concluída.

**Estado na época das primeiras simulações:** os valores candidatos ainda não
estavam conectados ao combate; as medições revelaram incompatibilidades
antes da migração coordenada de combate, HUD e banco. O trabalho de balancear
de fato começou pelo baseline mensurável; as regras finais continuam abertas.

## Segundo passe: distribuição automática e durabilidade de elites

Foi feita uma segunda simulação separada do código ativo. O objetivo foi
aproximar a distribuição automática Premium/VIP de uma distribuição manual de
referência da classe, mantendo-a como conveniência sem vantagem numérica. Os pesos candidatos
reproduzem as divisões usadas na comparação manual: Guardião 60/25/15 (Força,
Vitalidade, Agilidade); Tecelão 60/25/15 (Energia, Vitalidade, Agilidade);
Vigia 55/25/20 (Agilidade, Vitalidade, Força); Lâmina 35/35/20/10 (Força,
Energia, Vitalidade, Agilidade). A automação candidata não investe em atributos
fora da distribuição de referência. Esses pesos ainda não foram aplicados a
`game_app/progression.py`; o alocador atual não aceita peso zero sem ajuste.

O multiplicador provisório de Vida do semichefe foi elevado de 6,5× para 6,7×
no simulador. Isso desloca o caso inicial do Tecelão de 19,4 s para 20,6 s e
mantém a distribuição candidata do nível 400 em 33,1 s, dentro da meta de 20–35 s.
O dano-base candidato do Vigia foi ajustado de `10 + 0,35 × Agilidade + 0,20 ×
Força` para `15 + 0,35 × Agilidade + 0,20 × Força`; o ataque básico do nível 1
passa de 6,8 s para 5,7 s, dentro da meta comum de 3–6 s.

| Faixa da distribuição automática candidata | Ataque básico vs. comum | Comum com habilidade | Semichefe com habilidade | Chefe com habilidade | Ataques comuns sobrevividos |
| --- | ---: | ---: | ---: | ---: | ---: |
| Níveis 1/100/220/400, quatro classes | 4,0–6,0 s | 3,0–4,6 s | 20,6–33,1 s | 60,9–91,4 s | 7,0–9,6 |

Nos checkpoints avaliados, a distribuição automática candidata coincide com a
distribuição manual de referência da mesma classe e ambas ficam nas metas solo
definidas. Isso compara só essas distribuições de referência: não prova que toda distribuição
manual será igual nem fecha o balanceamento. A simulação ainda exclui itens,
efeitos elementais, estados, área, grupo e regeneração. Os valores são
propostas, não parâmetros do jogo.

## Terceiro passe: perfis candidatos de habilidades e estados

Os perfis abaixo foram usados no terceiro passe do simulador. Todos os dados são
provisórios e permanecem fora do combate ativo. O dano contínuo considera os
tiques possíveis durante a duração; será menor se o alvo morrer antes.

| Classe | Habilidade | Alvo/área | Elemento | Estado proposto | Regra de simulação |
| --- | --- | --- | --- | --- | --- |
| Guardião do Umbral | Impacto do Umbral | Único, corpo a corpo | Físico | Quebra de escudo | 30% de chance; 4 s; reduz resistência em 15% |
| Tecelão de Cinzas | Chama Crescente | Círculo, raio 80; até 3 alvos | Fogo | Queimadura | Garantida; 4 s; 1,5% do dano da habilidade/s; não acumula |
| Vigia do Ermo | Disparo Perfurante | Linha, largura 30; até 3 alvos | Físico | Sangramento | 35% de chance; 4 s; 1,5% do dano da habilidade/s; não acumula |
| Lâmina Rúnica | Ruptura Rúnica | Único | Raio | Paralisia | 20% de chance; interrompe telegráfico por 1 s; chefe imune 6 s |

A queimadura representa até 6% de dano adicional por aplicação completa; o
sangramento representa 2,1% em valor esperado (35% × 6%). Quebra de escudo e
paralisia são utilidades, sem dano equivalente no modelo. Quebra de escudo
depende de definir uma camada de proteção, ainda ausente no protótipo; paralisia
requer autoridade do servidor sobre os ciclos e instantes de impacto. Estes
perfis não são decisão final nem estão implementados no jogo.

### Resultado da simulação de grupo e afinidades

Executado `python scripts/simulate_balance_model.py`. Para cada classe e nível
1/100/220/400, o modelo atacou três inimigos comuns em sequência; ataques em
área atingem até três alvos simultaneamente, com alinhamento ideal. Para o chefe,
calculou-se o tempo de eliminação contra as quatro afinidades, aplicando a
resistência elemental provisória de 30% quando a habilidade combina com a
afinidade. O ataque básico continua físico. A tabela resume a faixa entre os
quatro níveis avaliados:

| Classe | Grupo de 3 comuns (s) | Chefe nas quatro afinidades (s) |
| --- | ---: | ---: |
| Guardião do Umbral | 12,0–16,0 | 60,9–78,7 |
| Tecelão de Cinzas | 8,9–11,1 | 62,8–95,4 |
| Vigia do Ermo | 9,1–12,2 | 69,5–78,6 |
| Lâmina Rúnica | 13,4–14,1 | 64,9–84,7 |

As faixas mostram que a área favorece o Tecelão no grupo simulado; a habilidade
de alvo único do Guardião e da Lâmina Rúnica leva mais tempo para limpar três
inimigos. Contra chefes, a resistência correspondente aumenta o TTK do Tecelão
e da Lâmina Rúnica. Isso não determina que a diferença esteja balanceada: não
foram modelados deslocamento, erro de mira/posicionamento, composição de grupo,
cooperação, mitigação da quebra de escudo nem o valor tático de interromper um
telegráfico.

DoT foi calculado como dano fracionário esperado por chance de ativação, com
tiques por segundo; isso estima médias, não a aleatoriedade de uma partida real.
O escudo e a paralisia não modificam os TTKs acima, pois ainda faltam regras de
camada defensiva e um modelo de telegráficos autoritativo. A comparação entre
afinidades considera apenas a resistência elemental provisória do chefe, não
resistências de outros inimigos. Os resultados são hipóteses para calibrar e
continuam fora do combate ativo.

### Quarto passe: posicionamento e grupo cooperativo

O simulador agora separa o limite da habilidade da quantidade de inimigos que
de fato foram alcançados. Contra três inimigos comuns, ele calcula os cenários
de um, dois e três alvos atingidos; não há chance inventada de acerto. A tabela
resume as faixas dos níveis 1/100/220/400:

| Classe | 1 alvo alcançado (s) | 2 alvos alcançados (s) | 3 alvos alcançados (s) |
| --- | ---: | ---: | ---: |
| Guardião do Umbral | 12,0–16,0 | 12,0–16,0 | 12,0–16,0 |
| Tecelão de Cinzas | 11,9–16,6 | 10,3–13,3 | 8,9–11,1 |
| Vigia do Ermo | 12,1–15,9 | 9,7–13,7 | 9,1–12,2 |
| Lâmina Rúnica | 13,4–14,1 | 13,4–14,1 | 13,4–14,1 |

Isso torna explícito que o Tecelão e o Vigia recebem seu ganho de limpeza pelo
posicionamento do jogador, enquanto Guardião e Lâmina Rúnica mantêm o mesmo
ritmo por terem a habilidade candidata de alvo único. Não é uma penalidade
adicional nem um valor aplicado ao jogo: é a consequência do teto atual de
três alvos e será reavaliada quando os mapas e o comportamento de monstros
estiverem fechados.

Também foi acrescentado um baseline de dano de grupo contra a Vida atual de um
chefe solo, nas quatro afinidades. Dupla Guardião + Tecelão: 30,8–39,3 s;
trio Guardião + Tecelão + Vigia: 20,8–25,1 s; trio Guardião + Vigia + Lâmina:
21,3–24,1 s. O modelo inclui ataques básicos, habilidades, custo inicial de
Mana e DoT esperado. Ele não concede dano por quebra de escudo/paralisia e não
simula cura, mortes, equipamentos, cartas, movimentação ou escala do chefe por
grupo. Portanto esses tempos demonstram apenas o ponto de partida do dano
somado; não são metas de duração de chefe em cooperativo.

### Próximo passo de P-031

Definir escala de Vida/dano e regras de alvo dos inimigos para dupla e trio;
depois adicionar ao modelo equipamentos, regeneração/poções e recompensas
após o nível 400.
Quebra de escudo e paralisia continuam como efeitos utilitários até haver
combate autoritativo suficiente para medir sua contribuição sem convertê-los
artificialmente em dano. Só então revisar e aprovar parâmetros para
implementação de P-025 no servidor e HUD. P-036 segue aguardando validação
manual visual e de esquiva; seus valores permanecem provisórios.

### Quinto passe: escala candidata de chefe cooperativo

Para obter uma primeira referência, o simulador aplica apenas ao chefe estes
multiplicadores de Vida: solo 1,0×, dupla 1,6× e trio 2,2×. Dano por ataque,
recompensas, número de ataques e alvo não são escalados neste passe. São
parâmetros candidatos, não uma regra aprovada.

| Composição | Multiplicador de Vida | TTK nos níveis 1/100/220/400, nas quatro afinidades |
| --- | ---: | ---: |
| Guardião + Tecelão | 1,6× | 53,1–63,2 s |
| Guardião + Tecelão + Vigia | 2,2× | 49,8–55,3 s |
| Guardião + Vigia + Lâmina Rúnica | 2,2× | 47,6–54,2 s |

Sob essa hipótese, os grupos ficam próximos da meta provisória de chefe solo
(60–100 s), com trios um pouco mais rápidos por terem três fontes de dano. Isso
não valida justiça ou dificuldade cooperativa: Vida/dano dos monstros comuns,
ameaça e seleção de alvo, cura/suporte, mortes, buffs, itens e recompensas por
participante ainda não entram. Próximo passo: definir essas regras cooperativas
e testá-las; depois incluir equipamentos, recursos e endgame. A escala segue
desativada no jogo até validação manual e aprovação.

### Sexto passe: inimigo comum focado em cooperação

Testou-se Vida comum em 1,25× para dupla e 1,50× para trio, com todos focando
o mesmo inimigo e usando ataques/habilidades candidatas desde o início. Nos
checkpoints, a eliminação levou 1,0–1,1 s. Isso fica abaixo da meta de 3–6 s
por inimigo comum; portanto, não adotar essa multiplicação de Vida.

A direção mais promissora é manter a Vida individual dentro da meta e ajustar
a quantidade/organização dos monstros por onda para grupos, junto da distribuição
de ameaça e alvos. A simulação não cobre movimentação nem dano recebido. Nenhuma
escala comum foi aprovada ou ligada ao jogo.

### Sétimo passe: quantidade de inimigos e ataques simultâneos

O simulador foi corrigido para processar eventos simultâneos em lote, manter
Vida individual dos monstros e atingir alvos distintos com habilidades em área.
Na hipótese de 3/4/5 inimigos comuns para solo/dupla/trio, mantendo a Vida
individual, o tempo estimado de limpeza nos níveis 1/100/220/400 foi 12,0–16,0 s
solo, 7,0–8,0 s em dupla e 6,0–6,8 s em trio. Ainda não entram dano recebido,
movimentação ou distribuição de ameaça; portanto, a quantidade é proposta e
aguarda validação, sem aplicação ao jogo.

Foi adicionada uma estimativa de pressão: inimigos atacam a cada 2 s e alternam
alvos igualmente, sem esquiva, cura ou suporte. A dupla e o trio mantiveram Vida
positiva nos checkpoints simulados; o solo não sobreviveu à onda candidata de
3 inimigos sob essas hipóteses. Isso não fecha o balanceamento: frequência de
ataque e seleção de alvo são suposições simplificadas. Antes de aprovar 3/4/5,
calibrar ataque inimigo e validar esquiva, cura e movimentação em combate.

### Registro histórico supersedido (cadência e densidade): orçamento de EXP por fase e hordas progressivas

Implementada uma regra candidata de 3, 4, 5, 6, 7, 8, 9 e 10 inimigos comuns
nas ondas 1–8; onda 9 mantém um semichefe e onda 10 um chefe. O orçamento da
fase é fixado quando ela começa em seis vezes a EXP necessária para o próximo
nível naquele instante. O orçamento é dividido por peso entre todas as criaturas
da fase: comum vale 1, semichefe 3 e chefe 5. Portanto, o orçamento completo é
recebido apenas ao derrotar os monstros da fase; mais inimigos reduzem o valor
individual, sem aumentar o total. Derrotas/reinícios não recalculam o orçamento.

O Socket.IO concede EXP somente no abate; os caminhos antigos de avanço de onda
não pagam novamente. O cálculo da progressão chegou ao nível 400 em cerca de 69
fases e 5.585 abates, contra 63 fases/1.637 abates no modelo anterior. A fase
inicial concede 750 EXP no total: a primeira onda divide 37 EXP entre três
monstros, então não sobe o jogador de nível sozinha. São resultados do modelo,
com orçamento e pesos provisórios, que precisam de teste de ritmo no jogo.

O aumento de densidade ainda requer uma etapa de design: variar formação,
entrada e espaçamento das hordas, preservar leitura de telegráficos e evitar
que todos os inimigos cubram a tela. O total de inimigos não define sozinho o
visual nem o desafio.

### Oitavo passe: pressão com ataques reais do protótipo

A simulação usa os ataques atuais de `combat.py`: melee causa 25 a cada 3,8 s
(aviso 1,05 s) e distância causa 20 a cada 4,2 s (aviso 1,35 s). Com Vida
derivada dos atributos, alvos em rotação e cenários de 0%, 50% e 100% de acertos
recebidos, o Guardião solo no nível 1 morre sem esquiva e fica com ~10 Vida se
metade dos ataques for evitada. Dupla (quatro inimigos) e trio (cinco) sobrevivem
à hipótese sem esquiva. Como posição e impacto ainda são controlados pelo
cliente, validar colisão/esquiva e corrigir o risco do solo antes de aprovar
quantidades ou cooperação.

### Nono passe: horda progressiva e distribuição de surgimento

O simulador agora interrompe a pressão de cada inimigo quando ele é eliminado,
em vez de contar ataques até o fim da onda para criaturas já derrotadas. O
cenário de estresse usa a onda 8 (10 inimigos) e ataques/telegráficos atuais;
para o Guardião nível 1 estima 84 ataques potenciais e Vida negativa sem esquiva.
Esse é um limite superior: o modelo ainda não limita quantos inimigos chegam ao
jogador, não verifica alcance durante a onda e não modela o acerto dos
telegráficos. Não é uma previsão da dificuldade real nem base para alterar dano
ou quantidade sem primeiro modelar aproximação e posicionamento.

O código funcional distribui inimigos por coordenadas pseudoaleatórias estáveis
por personagem/fase/onda. Mantém 380 unidades do ponto de entrada do jogador e
92 entre inimigos; ao trocar de onda, usa a posição enviada no último golpe. A
validação manual desses limites ainda falta. Teletransporte, saída do chão,
queda do céu e efeitos de entrada continuam adiados.

O passe acima ainda não representa aproximação, alcance ou esquiva; o décimo
passe abaixo adiciona aproximação e alcance de forma simplificada.

### Décimo passe: aproximação e nível real por onda

O cálculo passou a usar o nível no começo de cada onda conforme a EXP fixa da
fase, em vez de manter o jogador artificialmente no nível 1/100/220/400 durante
todas as ondas. Também inclui as posições pseudoaleatórias usadas pelo código,
tempo aproximado para entrar no alcance, velocidade de perseguição e primeiro
aviso/recarga dos ataques atuais. A tabela registra ondas 1/4/8 para o Guardião;
Vida restante é uma hipótese de 50% de ataques acertando, com jogador parado.

| Checkpoint | Nível ao entrar na onda 8 | Duração estimada das ondas 1 / 4 / 8 | Vida restante na onda 8 |
| ---: | ---: | ---: | ---: |
| 1 | 4 | 23,4 / 47,7 / 86,4 s | -880 |
| 100 | 98 | 22,5 / 40,6 / 60,8 s | -272 |
| 220 | 222 | 21,5 / 38,7 / 59,3 s | 279 |
| 400 | 400 | 17,7 / 33,9 / 49,6 s | 1.136 |

O resultado sugere que ondas densas podem exigir esquiva quase perfeita no início
da progressão, enquanto o ritmo de abates só entra na faixa provisória de 30–60
segundos mais tarde. É uma hipótese de risco, não a experiência final: ficar
parado, acertar sempre o mesmo alvo e não modelar rotas/colisão muda bastante a
pressão real. Nenhum número de combate foi alterado. Próxima tarefa P-031:
simular ajustes candidatos de Vida e cadência/dano comum e comparar sobrevivência
e duração nos quatro checkpoints antes de decidir quais parâmetros entram no
protótipo.

### Décimo primeiro passe: ajuste candidato de inimigos comuns

Foi comparada, somente no simulador, uma redução de Vida dos comuns para 45% e
de dano dos ataques comuns para 25% dos parâmetros atuais. Sob a hipótese de
50% de ataques acertando, a onda 8 do Guardião muda assim:

| Checkpoint | Nível ao entrar na onda 8 | Duração atual → candidata | Vida restante candidata |
| ---: | ---: | ---: | ---: |
| 1 | 4 | 86,4 → 41,9 s | 54,5 |
| 100 | 98 | 60,8 → 32,0 s | 447,4 |
| 220 | 222 | 59,3 → 31,6 s | 952,1 |
| 400 | 400 | 49,6 → 29,5 s | 1.671,6 |

O cenário aproxima melhor a faixa de duração e remove a derrota prevista para a
onda 8 no início do ciclo, mas não é decisão aprovada: considera só o Guardião
com distribuição automática candidata, jogador parado e taxa fixa de acerto. O
dano de 25% pode ficar fraco em grupos ou contra builds defensivas; faltam as
quatro classes, distribuição manual, semichefe, chefe, equipamento, elementos
e cura antes de qualquer aplicação.

Uma primeira varredura do mesmo ajuste nas quatro classes encontrou, para a
onda 8, estes intervalos de duração e Vida restante com 50% de ataques
acertando:

| Checkpoint | Nível de entrada | Duração entre classes | Vida restante entre classes |
| ---: | ---: | ---: | ---: |
| 1 | 4 | 28,3–41,9 s | 54–80 |
| 100 | 98 | 27,6–32,2 s | 401–451 |
| 220 | 222 | 25,9–32,1 s | 844–958 |
| 400 | 400 | 18,7–30,6 s | 1.471–1.698 |

A sobrevivência melhorou no início do ciclo, mas a progressão enfraquece o
desafio no nível 400 para três das quatro classes, abaixo da faixa de 30–60 s.
Além disso, a varredura usa apenas uma posição aleatória fixa por checkpoint e
distribuição automática candidata. Próxima tarefa P-031: modelar uma escala
gradual de Vida por fase/nível que mantenha a janela de duração sem recriar a
pressão fatal do início; depois incluir builds manuais, outros pontos de mapa,
semichefe/chefe, equipamento, elementos, cura e endgame.

### Décimo segundo passe: simulação ligada ao combate de produção

Foi criado `scripts/simulate_live_balance.py`. A simulação usa a distribuição
automática real, os atributos derivados, a habilidade-base ativa, a recarga por
Agilidade, o cálculo compartilhado de dano, as resistências, a Vida dos
inimigos, a densidade e o dano dos ataques. `socket_events.py` também passou a
chamar o cálculo compartilhado de dano; os eventos continuam sorteando crítico
e surto normalmente. Não há equipamento, cartas ou talentos comprados, a
rotação é perfeita e a pressão da horda supõe o jogador parado.

Para fazer a sobrevivência inicial corresponder à meta de 6–10 golpes, a base
de Vida do personagem passou de 100 para 120. A curva de inimigos comum,
semichefe e chefe recebeu escala progressiva em `enemy_max_health`. Seja
`base = arredondar(143 × 1,05 × [1 + 0,06 × máximo(0, nível inimigo − 6)])`,
`progresso = limitar((nível inimigo − 6) / 394, 0, 1)` e
`ciclo = (nível inimigo − 1) / 399`:

- comum: `base × (1,45 + 0,65 × progresso)`;
- semichefe: `base × 6,5 × (0,75 + 0,25 × ciclo) ×
  mínimo(1,65; 1 + 0,9 × raiz(progresso))`;
- chefe: `base × 18 × (0,75 + 0,25 × ciclo) ×
  mínimo(1,7; 0,8 + 3,6 × progresso)`.

Todos os limites continuam no nível inimigo 400. A suíte agora verifica o TTK
de todas as classes nos checkpoints 1/100/220/400:

| Checkpoint | Comum | Semichefe | Chefe |
| ---: | ---: | ---: | ---: |
| 1 | 4,0–5,0 s | 22,1–31,4 s | 63,2–91,6 s |
| 100 | 3,5–4,6 s | 20,1–24,1 s | 65,0–90,9 s |
| 220 | 3,5–5,0 s | 22,4–28,2 s | 65,6–88,6 s |
| 400 | 4,0–5,2 s | 24,1–31,6 s | 71,3–130,0 s |

O caso de 130 s é o Tecelão contra o chefe de Fogo no nível 400. O chefe reduz
em 30% o dano do próprio elemento; o responsável escolheu manter essa
contrajogada e aceitar até 130 s nesse confronto. Contra o chefe de Gelo no
checkpoint de nível 400, o mesmo personagem leva 92,5 s.

A pressão da horda também é reproduzível: posições aleatórias são semeadas,
aproximação/aviso são estimados e os ataques cessam após a morte de cada
inimigo. Na onda 8, o tempo estimado entre classes ficou em 74,7–96,2 s no
checkpoint 1, 67,9–90,9 s no 100, 63,3–85,7 s no 220 e 69,0–87,5 s no 400.
Com 50% de acertos antes da esquiva, o jogador parado morre em todas as classes;
o maior limite de acertos que permite sobreviver fica entre 4,8% e 8,1%.
O responsável escolheu manter a horda como desafio de esquiva, sem diminuir
dano, frequência ou densidade. Este é um cenário de estresse, não uma previsão
do jogador em movimento. A duração ainda supera a janela provisória de 30–60 s;
movimento real, builds manuais, cooperação, equipamento e recursos permanecem
para validação.

A projeção atual de nível 400 na fase 69 após 6.502 eliminações extrapola a
campanha, que encerra na Fase 30. O comando
`python scripts/simulate_live_balance.py` também mede builds completas contra
o chefe teórico da fase 70, fora do conteúdo atual.
a regressão completa segue em `python -m unittest discover -s tests -v`.
