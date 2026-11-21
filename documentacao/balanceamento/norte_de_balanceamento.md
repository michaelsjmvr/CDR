# Norte de balanceamento — guia de trabalho adaptado

**Estado:** guia de trabalho que consolida regras aprovadas, propostas e lacunas.
Os valores candidatos não substituem os parâmetros ativos até serem simulados
e validados. Para decisões aprovadas, consultar `decisoes_aprovadas.md`. A
auditoria e a primeira simulação executável estão em
`auditoria_e_primeira_simulacao.md`; os resultados não alteraram o combate.
**Nota de estado v0.139 — 15/11/2026 21:54:32 (UTC−03:00):** a integração da
arte/efeitos do Terminal de Vilar não altera progressão ou balanceamento. A
meta segue teto 170 em planejamento, com o código ainda no nível 400. Nenhum
valor novo foi aprovado.

**Nota de estado v0.138 — 15/11/2026 19:00:22 (UTC−03:00), histórica:** a
implementação do editor local da Fase 1 não alterou progressão ou
balanceamento; nenhum valor foi aprovado.

**Nota de estado v0.137 — 15/11/2026 18:28:51 (UTC−03:00), histórica:** a direção é
teto-alvo 170, com XP, PL e combate a rebalancear; a execução permanece
pendente e o código ainda usa 400. Nenhum valor novo foi aprovado. Este guia
preserva o retrato de balanceamento v0.126; seus limites, TTKs e fórmulas até
400 são snapshot anterior, não calibração do alvo 170. E2E v0.134 validou o
fluxo com atributos no teto e coordenadas do harness, não equilíbrio. A
simulação existente é baseline matemática anterior e não aprova nem valida o
alvo novo. O Documento Mestre v0.137 também registra a arte e colisões
aproximadas da Fase 1; isso não altera nem valida parâmetros de balanceamento.

**Nota de estado histórica v0.134 — 15/11/2026 16:20:21 (UTC−03:00):** este guia preserva
o retrato de balanceamento v0.126; o histórico de P-048 ali descrito não é o
status técnico vigente. A implementação recebeu em v0.131 o bloqueio de runs
concorrentes por conta, sem alterar os valores de balanceamento. Consulte o
Documento Mestre v0.139 para o estado atual. E2E v0.134 completou a Fase 10
nos riscos Moderado, Alto e Extremo, mas usou atributos no teto e coordenadas
do harness; não calibra sensação de jogo. A simulação baseline foi reexecutada
e mantém os TTKs nos alvos históricos, mas não cobre a sensação dos perfis de
risco. Os candidatos seguem sem calibração/aprovação.
**Retrato de balanceamento v0.126 (documentação; implementação inicial P-048 v0.124):** a
Temporada 1 tem 30 fases, três atos, dez ondas por fase e nove temas visuais
sobre uma arena lógica única. A Fase 30 encerra a campanha. A simulação projeta
nível 170 e 26 Pontos de Legado ao final da Fase 30; ritmo e dificuldade ainda
precisam de validação em combate ativo. O teto futuro de nível 400 permanece
aprovado, sem Reset. A EXP usa orçamento fixo por fase, calculado na entrada e
distribuído entre abates com pesos 1/3/5. O auto-ataque Premium/VIP P-035 está
suspenso. A projeção matemática vigente chega ao nível 400 na fase 69 com
6.502 abates se o modelo for extrapolado; o jogo encerra na fase 30. A
estimativa anterior de 5.585 abates está superada. Notas anteriores sobre
Reset, fórmula de EXP por inimigo ou automação são históricas e estão
superadas; não são decisões nem recomendações ativas.
O sistema P-048 adicionou quatro dificuldades encadeadas, Ouro inteiro na
carteira da conta, recompensas por fase e Baús de Recompensa em staging. Um E2E em navegador
percorreu a Fase 10 até o chefe e o resgate, mas usou fases anteriores
pré-carregadas, atributos de teste e ataques acelerados por harness; não
calibra o combate. Seus multiplicadores e valores continuam candidatos, sem
aprovação. Ouro é apenas uma unidade virtual de protótipo; dinheiro real exige
um fluxo separado.
**Atualizado em:** 15/11/2026 21:54:32 (UTC−03:00), v0.139.

## Princípios para manter o curso

1. Manter quatro atributos com nomes simples: Força (dano físico), Agilidade
   (cadência/esquiva), Vitalidade (Vida) e Energia (Mana e magia).
2. Mostrar sempre valores atuais, valor após investir e pontos restantes.
3. Evitar fórmulas invisíveis no jogador: tooltip deve explicar o ganho em
   linguagem direta; o servidor continua sendo a autoridade dos cálculos.
4. As fórmulas provisórias de combate já estão implementadas. Não tratar a
   antiga escala de Vida 1.000 e dano fixo como atual; calibrar os valores
   existentes em conjunto, sem voltar a propor uma migração já concluída.
5. Toda regra numérica nasce como parâmetro central, recebe cenário de teste
   por classe e só então é promovida a regra aprovada.

## Base candidata para a primeira simulação

Usar como pontos de partida as linhas raciais/classes fornecidas pelo
responsável, mapeadas para os nomes originais do projeto:

| Classe do jogo | Força | Agilidade | Vitalidade | Energia | Pontos por nível |
| --- | ---: | ---: | ---: | ---: | ---: |
| Guerreiro | 28 | 20 | 25 | 10 | 5 |
| Tecelão | 18 | 18 | 15 | 30 | 5 |
| Caçador | 22 | 25 | 20 | 15 | 5 |
| Lâmina Arcana | 26 | 26 | 26 | 26 | 5 |

Snapshot de regras anterior à decisão v0.135: personagem começa no nível 1 sem
pontos livres e recebe 5 pontos por nível; a curva de PL entrega 64 pontos no
nível 400 e inimigos escalam até esse nível. O código ainda mantém esses valores,
mas XP, PL e combate precisam ser recalculados para o teto-alvo 170. O teto
técnico provisório de 10.000 por atributo também pertence à implementação atual.

### Distribuição automática VIP (protótipo)

A opção VIP é optativa e distribui apenas pontos novos; a alocação manual
continua disponível. Os pesos atualmente usados pelo protótipo são prioridades
de distribuição, não proporções finais aprovadas:

| Classe | Força | Agilidade | Vitalidade | Energia |
| --- | ---: | ---: | ---: | ---: |
| Guerreiro | 40% | 20% | 30% | 10% |
| Tecelão | 10% | 25% | 25% | 40% |
| Caçador | 30% | 40% | 20% | 10% |
| Lâmina Arcana | 30% | 25% | 15% | 30% |

Na calibração, verificar se essas recomendações são viáveis com cada conjunto
de equipamento e se não tornam o benefício VIP mais poderoso que uma build
manual bem distribuída. A distribuição automática deve continuar sendo uma
facilidade de uso, não uma vantagem exclusiva de combate.

O bônus de 7 pontos para a classe híbrida e seu desbloqueio no nível 220 eram
hipóteses da referência e foram descartados. A regra aprovada concede 5 pontos
por nível a todas as classes, e a Lâmina Arcana permanece disponível desde o
início.

## Escala do combate e calibração

### Equipamentos e efeitos persistentes

Foi recebida uma nova base comparativa de MU Online sobre armas, armaduras,
escudos, asas, acessórios, pets e montarias; consultar
`base_enviada_itens_mu_online.md`. Ela mostra que o orçamento de poder também
precisa contabilizar bônus fixos, percentuais, conjunto, aprimoramento,
resistências e recuperação. O responsável acrescentou dano elemental causado
e roubo de Vida como fatores obrigatórios. Separar roubo de Vida de regeneração
passiva e recuperação por eliminação; cada um tem fontes e ritmos diferentes.
Não importar os números da referência diretamente.

Como atributos e itens persistem sem Reset, a calibração deve considerar seu
impacto durante toda a progressão 1–400 e no endgame. A escala atual usa nível
de inimigo por fase/onda; a experiência e as recompensas após o teto ainda
precisam de um modelo testável.
Empilhamento de redução/absorção de dano, esquiva, velocidade, dano e bônus de
Ouro precisa ter limites ou retornos decrescentes explícitos. Dano elemental
deve passar pela resistência do elemento correspondente uma única vez. Roubo
de Vida precisa de base de cálculo e limite claros, sobretudo para dano em área,
golpes rápidos, dano contínuo e chefes; somado a regeneração, cura por morte,
poções e absorção não pode sustentar o personagem indefinidamente sob pressão.

**Lista obrigatória do modelo conjunto:** atributos e nível; dano físico e
mágico; arma e aprimoramento; dano elemental e resistências; crítico e
penetração; armadura, escudo, esquiva, redução/absorção e conjunto; Vida/Mana e
regeneração; roubo de Vida; recuperação por eliminação; habilidades, velocidade
e recargas; asas, acessórios, pets/montarias; cartas temporárias; poções,
drops e bônus de Ouro; nível do jogador, fase, onda e número/composição de
jogadores (solo até grupo de 3).

### Lacunas identificadas antes de fechar as fórmulas

- **Ordem de resolução:** definir em que ordem se aplicam dano base, bônus de
  atributo/equipamento, crítico, dano elemental, resistência, defesa, absorção,
  dano real à Vida, roubo de Vida e recuperação. Sem uma ordem única há risco de
  aplicar multiplicadores ou resistências mais de uma vez.
- **Teto de nível:** decidir as recompensas de endgame após o nível 400 sem
  conceder níveis ou pontos de atributo além do teto.
- **Requisitos dos itens:** definir exigência de nível/classe/atributo e se um
  item permanece equipado e ativo imediatamente após voltar ao nível 1.
- **Sustento de Mana:** a referência inclui recuperação de Mana ao eliminar,
  mas não define roubo/regeneração de Mana por acerto. Decidir se o jogo terá
  essas fontes e impedir que elas removam toda a decisão de custo/cooldown.
- **Poções:** incluir quantidade, recarga, cura por uso e contribuição da
  auto-poção para sobrevivência, junto de regeneração e roubo de Vida.
- **Grupo cooperativo:** testar solo, dupla e trio. Ajustar Vida/dano e controle
  dos inimigos por grupo e composição de classes; cura, bônus e itens de um
  jogador não podem tornar os demais irrelevantes.
- **Limites de atributos:** verificar quando o teto técnico 10.000 ocorre,
  como pontos excedentes são tratados e se a distribuição VIP respeita esse
  limite ao longo dos níveis.
- **Endgame no nível 400:** definir recompensas de fase e objetivos de longo
  prazo quando o personagem continua jogando no teto, sem novo ciclo de nível.
- **Economia completa:** incorporar chance de drop, venda de itens, custos e
  falhas de aprimoramento, ouro extra de equipamentos e preço de redistribuição.

As fórmulas recebidas podem orientar proporções entre classes, mas não usar
literalmente os resultados enquanto os valores atuais estiverem em escala
diferente. Primeira calibração deve definir uma referência comum por nível:

- tempo-alvo para derrotar monstro comum: 3–6 s no começo de uma fase;
- semichefe: 20–35 s;
- chefe: 60–100 s solo;
- personagem aguenta 6–10 golpes comuns sem cura no início da faixa;
- Mana permite 6–10 usos da habilidade principal antes de depender de
  recuperação; cooldown e custo aparecem juntos no HUD.

Esses tempos são metas de teste, não valores já implementados. Ajustar vida,
dano e defesa dos monstros contra personagem de mesmo nível; aumentar uma
variável de cada vez. A fórmula de dano líquido da referência precisa de piso
de 1 e limite de redução para impedir dano nulo/infinito. Precisão e esquiva
devem virar uma chance percentual limitada, não comparação binária de valores.

## Cadência vigente de encontros — Temporada 1

Cada fase tem dez ondas. As ondas 1–9 são de inimigos comuns. A classificação
da onda 10 segue a fase: semichefe nas fases 5, 15 e 25; chefe de ato nas fases
10, 20 e 30; comum nas demais. O nível inimigo segue `5 × fase + onda`, com
limite 400, e o orçamento de EXP da fase segue a regra descrita no início
deste documento. A campanha termina na fase 30; fases posteriores não são
conteúdo atual.

**Registro supersedido:** tabelas antigas deste documento projetavam um
semichefe na onda 9 e chefe em toda onda 10, em faixas que chegavam à fase 400.
Elas pertencem ao modelo pré-campanha e não devem ser usadas como calendário
atual. A projeção de nível 400 na fase 69/6.502 abates é uma extrapolação
matemática, não conteúdo jogável da Temporada 1.

## Ordem de implementação para evitar regressões

1. **Concluído:** registrar atributos-base, pontos livres e limites no banco;
   migrar existentes sem apagar Agilidade que já venha de Talentos.
2. **Concluído:** entregar tela/rota de distribuição protegida por login e
   CSRF, com validação transacional, ponto disponível e teto provisório 10.000.
3. **Concluído:** conceder Pontos de Legado pela fórmula aprovada
   `nível // 10 + nível // 50 + nível // 25`; conceder 64 pontos no nível 400
   e migrar personagens existentes sem reduzir saldos.
4. Calibrar os cálculos de Vida/Mana/dano já ligados aos atributos e integrar
   ao orçamento de poder dano elemental, resistências/estados, roubo de Vida,
   regeneração e cura por eliminação.
5. Calibrar no jogo o orçamento de EXP já implementado: `6 × EXP necessária
   para o próximo nível` no início da fase, com EXP por abate distribuída pelos
   pesos 1/3/5 para comum/semichefe/chefe. A EXP necessária segue
   `100 + 25 × nível`. A projeção de 69 fases/6.502 abates extrapola a
   Temporada 1 e não é conteúdo disponível. Validar o ritmo/dificuldade até a Fase 30 e,
   separadamente, definir conteúdo para progressão futura.
   **Registro superado:** uma proposta anterior usava `20 + 6 × nível do
   inimigo` (semichefe 3x, chefe 5x) e estimava 63 fases/1.637 abates; não usar
   essa proposta como recomendação ativa.
6. Calibrar as árvores de talentos já implementadas: limites por nó, custos,
   efeitos, pré-requisitos e redistribuição (VIP grátis; comum paga Ouro).
7. Validar cada classe em níveis 1, 50, 100, 220 e 400 em combate ativo.

## Decisões e definições que permanecem abertas

- Validar em jogo os valores-base candidatos por classe e a alocação até o nível
  400.
- Validar a fórmula de escala dos inimigos e EXP por nível, fase e onda.
- Fechar dano físico/mágico/elemental, crítico, penetração, resistências e
  estados; declarar a ordem de cálculo e os limites para cada bônus.
- Definir Vida/Mana derivadas, mitigação, esquiva, bloqueio, absorção, cura,
  roubo de Vida, regeneração e recuperação por eliminação.
- Balancear armas, aprimoramentos, sets, asas, acessórios, pets/montarias,
  cartas, habilidades e talentos como um orçamento de poder conjunto.
- Definir nível/classe mínimo de equipamento e o comportamento no nível 400.
- Verificar se a distribuição automática VIP gera resultados competitivos,
  mas não superiores, às opções de distribuição manual de cada classe.
- Definir ordem única de cálculo de dano/cura e requisitos de uso de equipamento.
- Calibrar solo/dupla/trio, poções, Mana em combate e recompensas após nível 400.
- Integrar poções ao inventário e à economia; a auto-poção VIP funcional atual
  é um protótipo sem estoque de consumíveis e seus valores/recargas não são
  números finais de balanceamento.
- P-034: a coleta futura parte de 24 unidades sem pet, 72 com pet e 108 com
  Premium/VIP e pet (3x, depois mais 50%). Medir em coordenadas do mundo, do
  personagem ao drop; validar em ondas e coop. Não implementado; o protótipo
  atual só coleta orbes de cartas.
- P-035: auto-ataque PvE Premium/VIP suspenso; ataques exigem comando do
  jogador. Não implementar nem tratar como pendência aberta sem nova aprovação.
- Fechar ritmo de XP, duração de ondas/fases, drops e economia de Ouro por
  faixas de nível/fase.
- P-048: calibrar TTK, sobrevivência, duração e renda por dificuldade; verificar
  cadência, raridades e valores dos Baús de Recompensa. O E2E da Fase 10
  confirma o fluxo técnico, não a experiência ou o equilíbrio. Os parâmetros
  atuais são candidatos; Ouro não tem valor real nem conversão.
- Definir preço em Ouro da redistribuição comum após conhecer renda média.

**Estado atual da simulação (P-031):** uma primeira rotação de habilidade por
classe foi comparada em níveis 1/100/220/400 contra comuns, semichefes e chefes,
para builds com distribuição automática VIP e builds manuais representativas.
O TTK de comuns
ficou dentro de 3,0–5,7 s. Há desvios pequenos em semichefes/chefes: Guardião
manual no nível 1 e Tecelão VIP no nível 400. Nomes, fórmulas e durabilidade
continuam candidatos. Os resultados completos e as limitações estão em
`auditoria_e_primeira_simulacao.md`.

**Próximo passo de balanceamento:** ajustar esses desvios, definir alvo/área/
elemento/estados das habilidades e simular as composições cooperativas. Depois,
integrar atributos, combate e HUD juntos; os demais sistemas abertos acima
seguem dentro do orçamento de poder antes do fechamento final.
