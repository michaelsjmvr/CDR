# Personagens e progressão

> Guia temático iniciado a partir do Documento Mestre v0.55 e atualizado com decisões posteriores. Consulte `Cronicas_do_Recomeco_Documento_Mestre_v0.139.md` para navegar entre assuntos.
>
> Atualizado em: 15/11/2026 21:54:32 (UTC−03:00).


## 6. Progressão durante a partida

### 6.1 Nível do personagem

- **Direção decidida, ainda não implementada:** alterar o teto-alvo para 170 e
  rebalancear XP, Pontos de Legado e combate para a campanha de 30 fases. O
  código continua com teto 400 até a execução dessa tarefa; as fórmulas e
  resultados descritos abaixo são o snapshot anterior, não valores finais para
  o alvo 170.
-   O personagem começa a partida no nível 1.
-   O limite atualmente implementado é o nível 400; a direção de produto
    superveniente é substituí-lo pelo teto-alvo 170. Não há Reset nem
    progressão para o nível 1000.
-   Monstros derrotados concedem experiência.
-   Ao subir de nível, o jogador recebe pontos para distribuir entre
    atributos.
-   Cada nível conquistado restaura completamente a Vida e a Mana máximas.
    A restauração e os novos máximos são enviados pelo Socket.IO sem recarga.

O combate com inimigos e a progressão por abates estão implementados. Os
parâmetros ativos em `game_app/progression.py` são candidatos de protótipo,
não valores finais: o próximo nível exige `100 + 25 × nível` de XP; ao entrar
na fase, o orçamento total corresponde a seis limiares de nível e é repartido
entre inimigos com pesos 1/3/5 para comum/semichefe/chefe. A XP é concedida
pelos abates, não novamente ao avançar de onda. O limite 400 zera o avanço
de nível, sem reiniciar o ciclo.

**Snapshot da curva anterior:** a Temporada 1 contém 30 fases, dez ondas por
fase e três atos. A onda 10 das fases 5/15/25 é de semichefe; a onda 10 das
fases 10/20/30 é de chefe de ato. Concluir a Fase 30 persiste
`campaign_complete` e mantém fase/onda em 30/10, sem criar a Fase 31. A curva
anterior projetava nível 170 e 26 Pontos de Legado ao fim da campanha; essa
saída não foi aprovada como balanceamento do novo teto e será recalculada. O
teto 400 é apenas o estado atual do código até a mudança planejada. As nove
áreas temáticas reutilizam uma arena lógica única; não representam nove
geometrias próprias. A narrativa detalhada está limitada às Fases 1–10; os
temas visuais dos Atos 2 e 3 são provisórios.

Ainda existe um fluxo/botão de teste que pode simular a conclusão de uma onda
para desenvolvimento. Ele não significa que inimigos ou combate estejam
ausentes e não substitui a progressão normal por abates. A curva e o ritmo
continuam sujeitos à calibração P-031/P-043/P-047, principalmente em combate
ativo, builds completas e cooperação.

### 6.2 Atributos

Os quatro atributos planejados são:

  -----------------------------------------------------------------------
  Atributo                            Influência pretendida
  ----------------------------------- -----------------------------------
  Força                               Dano e eficiência de ataques
                                      físicos

  Agilidade                           Velocidade de ataque, defesa ou
                                      mobilidade, conforme a classe

  Vitalidade                          Vida e capacidade de sobrevivência

  Energia                             Poder mágico, energia ou eficiência
                                      de habilidades
  -----------------------------------------------------------------------

Os quatro atributos já têm efeitos funcionais no combate. Seus coeficientes,
limites e impacto por classe são candidatos de protótipo e permanecem sujeitos
à calibração indicada abaixo.

A tela de atributos informa, em tempo real enquanto a quantidade é digitada,
o valor estimado após o investimento. Ela também avisa quando a quantidade
excede os pontos livres ou o teto técnico. A confirmação da distribuição é
salva por Socket.IO, sem recarregar a página, e os valores derivados de combate
são atualizados junto com os atributos. A notificação de sucesso some após
cinco segundos. O atalho fica nos Serviços da Sala de Espera.

### Base enviada para o balanceamento dos personagens

O responsável forneceu `DOCUMENTO MESTRE DE BALANCEAMENTO E SISTEMAS` como
referência para a próxima rodada de balanceamento. As tabelas de atributos
iniciais, pontos por nível e fórmulas por arquétipo devem ser avaliadas e
adaptadas às classes originais do projeto. Até aprovação explícita, esses
números são uma **proposta de balanceamento**, não valores já aplicados ao
jogo.

O arquivo de referência está preservado em
`documentacao/balanceamento/base_enviada_personagens.md`. Ele contém os
valores e fórmulas integrais enviados pelo responsável, além de uma análise
dos pontos que precisam ser compatibilizados com as regras existentes.
O norte de trabalho adaptado ao protótipo está em
`documentacao/balanceamento/norte_de_balanceamento.md`; seus números são
propostas para simulação, não parâmetros ativos.

**Compatibilizações necessárias para o balanceamento:**

-   A progressão não usa Reset. O código avança até 400, mas a direção decidida
    é teto-alvo 170; recalibrar o ciclo de XP/PL/combate antes de declarar
    progresso ou recompensas finais.
-   Pontos de Legado são concedidos em marcos de nível; não são concedidos por
    Reset nem por encerrar uma run.
-   As fórmulas de atributos, dano e Vida já estão ligadas ao combate. A tarefa
    pendente é calibrar em conjunto personagens, inimigos, talentos, cartas e
    futuros equipamentos, sem misturar parâmetros de versões antigas.
-   A Temporada 1 termina na fase 30. O teto 170 é a nova direção de progressão,
    ainda não implementada; conteúdo e recompensas após a campanha precisam ser
    revistos em função dela. A projeção antiga de nível 400 na fase 69 não
    significa que essas fases estejam jogáveis nem define o novo ritmo.
-   O teto provisório de 10.000 exige validação no servidor para qualquer distribuição
    ou bônus, e as fórmulas de ataque devem limitar dano e usar inteiros
    seguros.

**Etapa pendente de balanceamento:** implementar o teto-alvo 170 e recalcular
orçamento/curva de XP, Pontos de Legado, escalas de Vida/dano e combate.
Depois, testar classes, atributos e caminhos completos em gameplay. A árvore
e a distribuição atuais permanecem implementadas sob o modelo anterior; não
aprovam a nova progressão.

**Direção anterior, superada quanto ao teto:** consultar
`documentacao/balanceamento/decisoes_aprovadas.md`. O personagem progride
continuamente até 400 no código atual, sem Reset. A fórmula anterior de PL
concede 64 pontos no nível 400 e o combate escala até esse nível; esses dados
serão recalculados para o alvo 170 e não são uma aprovação de valores novos.

**Primeira etapa implementada:** personagens novos recebem os quatro valores
iniciais candidatos da classe; contas existentes recebem migração compatível.
Cada nível ganho concede 5 pontos. A rota autenticada `/jogo/atributos` valida
saldo e teto provisório de 10.000 por atributo. A distribuição automática é
optativa, exclusiva Premium/VIP e aplica pesos por classe. Ao ativá-la, os
pontos livres acumulados também são distribuídos de acordo com o arquétipo;
ganhos futuros seguem a mesma prioridade. Desativar interrompe a automação
futura e não desfaz os pontos já gastos. A distribuição manual continua
disponível. Não há Reset nem perda de atributos/pontos no nível máximo.
O menu atualiza pontos por Socket.IO. A fórmula ativa de XP exigida é
`100 + 25 × nível`; cada fase tem orçamento fixo de seis limiares de nível,
repartido entre abates com pesos 1/3/5 para comum/semichefe/chefe. A projeção
matemática do modelo atual chega ao nível 400 na fase 69, com cerca de 6.502
abates, se a progressão for extrapolada além da Temporada 1. Isso não significa
que as fases posteriores à 30 estejam jogáveis nem é uma meta de ritmo
validada. O modelo anterior estimava 5.585 abates. Os quatro atributos já afetam
as fórmulas provisórias de combate: Força, Agilidade e Energia escalam o dano
conforme a classe; Vitalidade concede 2 de Vida máxima por ponto; Energia
concede 1,5 de Mana máxima; Agilidade reduz recargas em 0,5% por ponto (limite
50%), aumenta movimento em 0,1% por ponto (limite 25%) e também concede
0,01 ponto percentual de chance crítica e +0,01 ponto percentual de esquiva
por ponto. As chances totais, somadas a talentos, passivas e cartas, têm
limites de 50% para crítico e 35% para esquiva. O dano é arredondado para
valores inteiros durante o golpe. A página mostra também a estimativa decimal
pré-arredondamento para deixar visíveis incrementos menores que um ponto de dano.
Ao investir em Vitalidade/Energia, o aumento do máximo também é somado aos
recursos atuais, sem ultrapassar o novo máximo. Os coeficientes ainda são
candidatos e precisam de balanceamento. A tela de Atributos mostra os valores
derivados ativos para facilitar a leitura dos efeitos. Personagens novos
iniciam com Vida/Mana atuais calculadas para a classe; personagens antigos com
recursos acima dos máximos derivados são limitados ao entrar no jogo.

**Tela v0.101:** o desktop usa duas colunas: distribuição de atributos e
efeitos de combate. O cabeçalho identifica a classe. O cartão em destaque
continua mostrando pontos livres; a linha menor mostra a EXP que falta para o
próximo nível e os 5 pontos que serão recebidos ao subir. No nível 400 informa
que não há novos pontos por nível. O resumo inclui críticos, cura no crítico,
esquiva, alcance, dano mitigado e recargas. Roubo de Vida, dano elemental ou
refletido e dano de projétil do jogador aparecem como não implementados quando
não há fórmula ativa. A automação VIP pode ser ligada e desligada por Socket.IO
sem recarregar a tela.

Pesos provisórios da automação VIP: Guerreiro — Força 40%, Vitalidade 30%,
Agilidade 20%, Energia 10%; Tecelão — Energia 40%, Vitalidade 25%,
Agilidade 25%, Força 10%; Caçador — Agilidade 40%, Força 30%, Vitalidade
20%, Energia 10%; Lâmina Arcana — Força 30%, Energia 30%, Agilidade 25%,
Vitalidade 15%. O algoritmo distribui ponto a ponto considerando os pontos já
investidos e os limites de cada atributo, sem prometer uma divisão fixa por
lote pequeno.

**Fórmulas candidatas atualmente ligadas ao combate:** Guerreiro: dano base
`10 + 0,5 × Força + 0,2 × Agilidade`; Tecelão: `20 + 0,35 × Energia
+ 0,2 × Agilidade + 0,1 × Força`; Caçador: `15 + 0,35 × Agilidade +
0,2 × Força`; Lâmina Arcana: `10 + 0,4 × Força + 0,4 × Energia + 0,1 ×
Agilidade`. Habilidade causa `1,5 × dano base`. Vida máxima é `120 + 1,5 ×
(nível − 1) + 2 × Vitalidade`; Mana máxima é `60 + (nível − 1) + 1,5 ×
Energia`. O dano inteiro exibido é arredondado, por isso ganhos pequenos podem
não alterar o número a cada ponto.

**Fatores que devem entrar no balanceamento conjunto:** dano elemental causado,
resistências dos inimigos, efeitos elementais de estado, roubo de Vida,
regeneração passiva e recuperação ao eliminar monstros. Roubo de Vida não será
tratado como sinônimo de recuperação por eliminação. Esses efeitos também
podem vir de atributos, equipamentos, habilidades ou companheiros e precisam
ser simulados junto de dano, defesa e cura. Ver
`documentacao/balanceamento/base_enviada_itens_mu_online.md`.

#### Snapshot anterior: dificuldade e progressão até o nível 400

No código atual, o limite permanece 400 e não há Reset. A decisão v0.135
estabelece 170 como teto-alvo; as escalas abaixo são o snapshot anterior e
serão recalculadas antes de definir a progressão final. O nível inimigo atual é
`5 × fase + onda`, limitado entre 1 e 400. Os parâmetros de Vida e dano ativos no protótipo
correspondem a `enemy_max_health` e `scale_enemy_attack_damage`; são candidatos
de balanceamento, não valores finais. Para o nível inimigo `L`, define-se
`base = arredondar(143 × 1,05 × [1 + 0,06 × máximo(0, L − 6)])`,
`progresso = limitar((L − 6) / 394, 0, 1)` e
`ciclo = (L − 1) / 399`. A Vida máxima é:

- comum: `arredondar(base × [1,45 + 0,65 × progresso])`;
- semichefe (onda 10 das fases 5/15/25): `arredondar(base × 6,5 × (0,75 + 0,25 × ciclo) ×
  mínimo(1,65; 1 + 0,9 × raiz(progresso)))`;
- chefe (onda 10 das fases 10/20/30): `arredondar(base × 18 × (0,75 + 0,25 × ciclo) ×
  mínimo(1,7; 0,8 + 3,6 × progresso))`.

Nas demais fases, a onda 10 usa a escala comum. As fórmulas são aplicadas de
acordo com o tipo de encontro programado, não apenas pelo número da onda.

O dano de cada ataque inimigo parte do dano-base definido para o ataque e
recebe `0,65 × máximo(0, L − 6)`, arredondado para inteiro e com mínimo de 1.
Como `L` para em 400, essas escalas também param nesse nível. A suíte e
`python scripts/simulate_live_balance.py` comparam as fórmulas reais às metas,
usando atributos automáticos e habilidades-base.

Na simulação atual, sem equipamento, cartas ou talentos comprados, o TTK de
comuns ficou entre 3,5–5,2 s, semichefes entre 20,1–35,0 s e chefes entre
61,4–111,0 s nos checkpoints 1/100/220/400. O benchmark das 12 builds completas
no chefe teórico da fase 70 ficou entre 64,2–99,5 s. São resultados
determinísticos, não validação em combate ativo. A resistência elemental de
30% permanece uma contrajogada aprovada; o antigo caso de 130 s do Tecelão
contra o chefe de Fogo pertence a uma simulação anterior e não é o resultado
atual. No início, as quatro classes sobrevivem a 6,0–6,9 golpes comuns.

A medição de horda é um estresse determinístico com o personagem parado, não
uma previsão de movimento: na onda 8, 50% de acertos antes da esquiva ainda
derruba as quatro classes nos quatro checkpoints. O cenário exige evitar mais
de 90% dos ataques; essa pressão foi mantida intencionalmente como desafio de
esquiva. Movimento real, grupos, equipamento, recursos e endgame continuam
pendentes de calibração (P-031/P-043/P-047).

### 6.3 Melhorias temporárias

As melhorias temporárias da partida serão representadas por cartas. Uma
escolha inicial permite montar a coleção; durante a partida, a progressão
normal das cartas vem da coleta de orbes de EXP espalhados pelo cenário.
Ao completar a barra, o jogador recebe uma oferta de **3 cartas** e escolhe
uma para adicionar ou, se a coleção estiver cheia, substituir uma ativa.
Cartas não têm níveis individuais.

**Regras definidas:**

-   A coleção temporária poderá manter até **6 cartas ativas** em contas
    padrão e **8 cartas ativas** em contas Premium/VIP.
-   Cada monstro derrotado deixa um orbe de EXP exatamente na posição onde
    morreu. Ao coletá-lo, a barra da coleção avança para a próxima escolha.
    Cada orbe concede 25 EXP para contas comuns e 40 EXP para Premium/VIP.
    O limiar é dinâmico: `100 + 25 × quantidade de cartas ativas` (por exemplo,
    100 EXP com coleção vazia e 300 EXP com oito cartas). Os valores são
    provisórios para balanceamento.
-   A escolha inicial de cartas e cada barra completada apresentam 3 opções;
    o jogador escolhe 1 para ativar ou substituir uma carta.
-   Ao iniciar uma nova coleção vazia, uma escolha inicial fica registrada
    como pendente e acessível pelo botão/Tab, mesmo antes de recolher o primeiro
    orbe.
-   As opções iniciais e as liberadas durante a partida são botões de seleção
    ligados ao mesmo evento Socket.IO. A confirmação atualiza a coleção em tempo
    real; se o servidor recusar a ação ou a conexão cair, o botão volta a ficar
    disponível e a interface informa o problema.
-   Quando uma escolha é liberada, as cartas começam ocultas e o botão **Tab**
    recebe o destaque “Nova carta”. O botão ou a tecla **Tab** abre e recolhe a
    seleção; o destaque aparece quando há escolha pendente e o painel está
    oculto, para que o jogador escolha quando parar para ler. Mesmo com as
    cartas visíveis,
    o jogador pode andar com WASD/setas e usar Avanço; os
    ataques ficam suspensos enquanto o painel está aberto. Tab é consumido pelo
    jogo e não avança o foco do navegador. O jogador pode continuar recolhendo
    orbes enquanto uma escolha está pendente; EXP e novas escolhas ficam
    acumuladas, sem exigir que interrompa o combate para selecionar a carta.
-   Não há nível individual nas cartas. A EXP pertence à progressão de
    aquisição da coleção temporária.
-   As 3 opções da mesma oferta são cartas distintas; uma carta já ativa
    não pode ser adicionada de novo à coleção.
-   Cartas não escolhidas e cartas removidas por substituição voltam a
    ficar elegíveis e podem aparecer em ofertas futuras, desde que não
    estejam ativas na coleção.
-   Quando a coleção estiver cheia, após escolher uma das 3 opções, o
    jogador poderá escolher uma carta ativa para substituir. A troca é
    opcional: se não quiser substituir, mantém a coleção atual e a carta
    nova não é ativada.
-   A coleta continua acumulando EXP mesmo com todos os espaços ocupados.
    A barra libera novas ofertas; escolher uma carta permite substituir uma
    ativa ou manter a coleção. O limiar aumenta com a quantidade de cartas
    ativas, conforme `card_xp_needed`.
-   O conjunto inicial terá pelo menos **30 cartas diferentes**, com
    atributos e habilidades distintos.
-   As cartas exibem raridade pela escala e paleta de 6 níveis da Seção
    8.2: Comum, Incomum/Mágico, Raro, Excelente, Épico/Ancestral e
    Lendário/Mítico.
-   Cartas ativas são melhorias temporárias da partida; são removidas ao
    concluir a fase ou morrer, conforme as regras das Seções 6.3 e 7.
-   Ao encerrar a partida, toda a coleção temporária é removida.

**Pesos iniciais de sorteio por raridade (soma: 100%):**

  Raridade                  Peso
  ------------------------- -----
  Comum                      50%
  Incomum / Mágico            25%
  Raro                        14%
  Excelente                    7%
  Épico / Ancestral             3%
  Lendário / Mítico             1%

O catálogo contém 36 cartas em `game_app/cards.py`. As passivas estão ligadas
ao combate no servidor e são aplicadas somente enquanto a carta está ativa:
dano geral, de habilidade, projétil e elemental, dano contra inimigos comuns e
chefes, redução de dano, esquiva e resistência a projéteis, Vida/Mana máximas,
movimento, alcance e recargas, críticos, cura crítica e de habilidades,
sequências de ataques, golpes especiais, recuperação de Mana por abate e cura
ao concluir ondas. As descrições exibidas na interface correspondem aos efeitos
implementados. A recomendação considera a classe, a especialização, a passiva
ativa e a habilidade assinatura já liberada, além da situação da partida e da
raridade. Valores e limites ainda são provisórios; P-022 aguarda calibração e
validação manual.

**Recomendação e prazo das cartas:** cada oferta de três cartas recebe uma
recomendação determinística baseada na classe, na especialização e, quando
liberada, na habilidade assinatura, além dos efeitos, da raridade, da Vida
atual e da proximidade das ondas 9 e 10. Afinidades de projétil, elemento, cura
de habilidade e recuperação de Mana recebem peso adicional quando combinam com
a habilidade ou passiva ativa. A utilidade para a classe e o conjunto é o fator
principal; a raridade influencia comparações próximas, sem fazer uma carta
rara superar automaticamente uma passiva claramente mais útil. A recomendada
recebe destaque; contas comuns continuam escolhendo manualmente qualquer uma
das três sem cronômetro. Para Premium/VIP, se o jogador não
escolher antes do prazo de **10 segundos**, o servidor ativa a recomendada.
Cada escolha pendente recebe seu próprio prazo persistido; atualizar a página
não reinicia o timer. Ofertas antigas são migradas para a nova duração.

Cada orbe rende 25 EXP para contas comuns e 40 EXP para Premium/VIP (+60% sobre
a conta comum; antes eram 30 EXP). Com oito cartas ativas, o próximo limiar é
300 EXP: o VIP precisa de cerca de oito orbes, contra dez no valor anterior de
30. O limiar continua aumentando conforme há mais cartas ativas. O novo bônus
VIP é provisório e foi elevado para abrir mais oportunidades de escolha e
substituição; validar manualmente o ritmo em uma partida completa antes de
recalibrar.

**Coleção cheia:** em contas comuns, a carta escolhida abre uma segunda decisão:
selecionar manualmente qual carta ativa sai ou manter a coleção. No Premium/VIP,
a carta escolhida ou recomendada é comparada às ativas por uma pontuação que
considera encaixe da classe, situação da run e raridade. Sai a carta ativa de
menor utilidade estimada; se a nova carta ajudar menos do que todas as ativas,
a coleção é mantida. Em empate, sai primeiro a carta ativa mais antiga. O
servidor valida a regra; pesos e resultados aguardam validação manual.

O botão flutuante **Ativar Premium (VIP) / Desativar Premium (VIP)** é uma
ferramenta de teste local da conta atual. A alteração é persistida no servidor
e a página recarrega para atualizar limites e recursos. Pode ser desligada com
`CRONICAS_ENABLE_PREMIUM_TEST_TOGGLE=0` e deve ser removida antes do lançamento.

Os orbes usam a posição final do inimigo derrotado enviada no ataque e gravada
junto ao inimigo e ao orbe. O evento Socket.IO transmite essa mesma posição para
que o cliente desenhe o drop no ponto da morte. Ao subir de nível, o servidor
recalcula os máximos e restaura completamente Vida e Mana na mesma atualização
em tempo real.

Ao morrer, a fase atual é mantida e a onda volta a 1. Vida e Mana são restauradas,
e a coleção temporária é zerada: cartas ativas, EXP da coleção, escolhas pendentes,
ofertas e orbes. O evento Socket.IO atualiza o HUD sem recarregar a página; ao
reiniciar a fase, uma nova coleção pode ser montada.

**Apresentação visual do orbe:** núcleo branco/dourado bem definido e
claramente visível, envolto por uma aura luminosa intensa com difusão suave
e pequenos brilhos. A luz pulsa lentamente, aumentando e diminuindo com
transição suave, sem cintilação brusca.

**P-022:** efeitos conectados ao combate e 36 cartas catalogadas. Testes
automatizados cobrem as novas sinergias de projétil, elemento, cura e Mana.
Balancear magnitudes e validar o conjunto em uma partida continuam pendentes.

### 6.4 Árvore de Talentos

Cada classe tem uma árvore própria, com talentos e efeitos distintos em cada
um de seus **três caminhos de evolução**. Não há trilhas extras, origens
alternativas nem outras classes avançadas. Talentos menores, especiais,
aprimoramentos laterais e principais são nós internos ao ramo escolhido; não
representam opções adicionais de evolução.

**Evolução no nível 100:** ao atingir o nível 100 pela primeira vez, aparece
um botão destacado na Árvore de Talentos. Ao clicar, abre uma caixa com somente
as três evoluções daquela classe. O personagem escolhe uma; o ramo escolhido
fica ativo e os outros dois permanecem bloqueados:

| Classe base | Únicos três caminhos disponíveis |
| --- | --- |
| Guerreiro / Guardião | Berserker (Bárbaro); Guardião; Senhor da Guerra (Warlord). |
| Arqueiro | Atirador de Elite (Sharpshooter); Domador de Feras (Beast Master); Arqueiro Arcano (Arcane Archer). |
| Mago | Arquimago (Archmage); Necromante; Sábio (Sage). |
| Gladiador Mágico | Lâmina Arcana (Spellblade); Gladiador Etéreo; Forjador de Almas. |

**Passivas, atributos e habilidades funcionais (v0.111):** a passiva entra em
efeito assim que o jogador escolhe a evolução, sem custo adicional. Cada ramo
concede +11 no atributo principal e +4 no secundário ao comprar todos os nós de
atributo. Os talentos próprios de cada especialização também aprimoram seus
atributos, passiva e habilidades em combate. A habilidade assinatura é comprada
no talento principal por 4 PL e substitui a habilidade-base da classe; até essa
compra, a habilidade-base continua equipada.

| Evolução | Bônus do ramo | Passiva ativa ao escolher | Habilidade no talento principal |
| --- | --- | --- | --- |
| Berserker | +11 Força, +4 Agilidade | +8% dano | Talho Frenético: 135% do dano de habilidade; 32 Mana; recarga-base 7,5s |
| Guardião | +11 Vitalidade, +4 Força | +8% Vida máxima e +4% redução de dano | Impacto do Bastião: 120%; 24 Mana; 7s |
| Senhor da Guerra | +11 Energia, +4 Vitalidade | recargas 5% menores; abates restauram 3% da Mana máxima | Investida de Comando: 120%; 26 Mana; 7s; abate devolve 15% do custo |
| Atirador de Elite | +11 Agilidade, +4 Força | +6 pontos percentuais de crítico e +8% alcance | Disparo Perfurante: 140%; 28 Mana; 8s |
| Domador de Feras | +11 Vitalidade, +4 Agilidade | +3% redução de dano; abates restauram 6% da Mana máxima | Investida Selvagem: 125%; 22 Mana; 6,5s |
| Arqueiro Arcano | +11 Energia, +4 Agilidade | +8% dano de habilidade e +3 pontos percentuais de crítico | Flecha Elemental: 125%; 28 Mana; 7,5s |
| Arquimago | +11 Energia, +4 Vitalidade | +10% dano de habilidade e +8% Mana máxima | Cataclismo das Cinzas: 145%; 38 Mana; 8,5s |
| Necromante | +11 Energia, +4 Agilidade | +5% dano de habilidade; abates restauram 7% da Mana máxima | Dreno de Almas: 105%; recupera 20% do dano causado como Vida; 26 Mana; 6,5s |
| Sábio | +11 Vitalidade, +4 Energia | +3% redução de dano e +5% de cura ao avançar de onda | Pulso Restaurador: 100%; cura 5% da Vida máxima ao acertar; 30 Mana; 7s |
| Lâmina Arcana | +11 Força, +4 Energia | +5% dano em ataques básicos e habilidades | Lâmina Elemental: 130%; 28 Mana; 6,5s |
| Gladiador Etéreo | +11 Agilidade, +4 Vitalidade | +7 pontos percentuais de esquiva e +5% velocidade | Fenda Etérea: 120%; 25 Mana; 6s |
| Forjador de Almas | +11 Energia, +4 Força | +8 pontos percentuais de chance de surto e +15% dano do surto | Lâminas Espectrais: 130%; 30 Mana; 7s |

As habilidades-base são Golpe de Escudo (Guerreiro), Tiro Preciso (Caçador),
Projétil de Cinzas (Tecelão) e Corte Rúnico (Lâmina Arcana). Os valores acima são
parâmetros iniciais de balanceamento. No protótipo, todas as habilidades ativas
atingem um único alvo; invocações de pets, dano em área, teleporte e bônus para
aliados não estão implementados. O antigo espaço lateral de melhoria agora é
um talento de combate próprio e funcional em cada especialização.

O catálogo inclui 15 habilidades supremas distribuídas pelas 12 especializações.
Cada habilidade suprema tem um talento de desbloqueio (4 PL) e um talento próprio
de maestria (+15% de dano, 2 PL). As quatro habilidades-base, as 12 assinaturas
e as 15 supremas também têm talentos próprios de maestria. Uma partida permite
equipar até três habilidades desbloqueadas e, entre elas, no máximo uma suprema.
O Ataque básico permanece fixo na tecla 1; as três habilidades equipadas usam
as teclas 2, 3 e 4.

Entre os efeitos supremos, **Erga-se** transforma o inimigo que derrotar em um
soldado das sombras: até três aliados podem ajudar nos três ataques seguintes
cada, com duração máxima de 15 segundos e bônus de dano de 35% por soldado. O
**Poço de Inércia** atrai e imobiliza os inimigos próximos por 1,5 segundo antes
de encerrar o efeito. O limite de uma habilidade suprema equipada continua
valendo para ambos.

Com os novos nós, cada especialização custa **58 ou 64 PL**: 42 PL em atributos,
2 PL em aprimoramento de combate, 4 PL no talento principal, 4 PL em maestrias
da habilidade-base e da assinatura, e 6 PL por habilidade suprema (4 para
desbloquear e 2 para aprimorar). Nove caminhos com uma suprema custam 58 PL;
três caminhos com duas supremas custam 64 PL. A soma dos 12 caminhos é **714 PL**,
mas cada personagem escolhe e desenvolve somente um caminho.

A fórmula atual do código é `pontos = nível // 10 + nível // 50 + nível // 25`.
Ela concede 16 PL no nível 100 e 64 PL no nível 400 no modelo anterior. Será
recalculada para a meta 170; não há curva nova nem total de PL aprovado. A
migração retroativa atual é idempotente e preserva saldos existentes maiores
que o novo mínimo.

**Crítico e esquiva pela Agilidade (v0.112):** cada ponto de Agilidade concede
0,01 ponto percentual de chance crítica e 0,01 ponto percentual de esquiva.
Assim, 100 pontos de Agilidade concedem +1% de crítico e +1% de esquiva. Esses
bônus se somam aos modificadores dos talentos, passivas e cartas antes dos
limites de 50% e 35%. O crítico já multiplica o dano por 1,5; uma esquiva
bem-sucedida anula o dano daquele ataque. As chances são exibidas no resumo de
combate e atualizadas após investir atributos. Talentos e passivas que já
concediam essas chances continuam funcionando e acumulam com a Agilidade.

As 12 especializações mantêm árvores únicas e efeitos conectados ao combate.
Cada habilidade suprema tem desbloqueio e maestria próprios; os novos nós elevam
o custo total para 58 ou 64 PL por caminho (714 PL somando as 12 opções). A
curva de Legado foi ajustada para conceder 64 pontos no nível 400, o suficiente
para concluir qualquer caminho sem exigir Reset nem obrigar a compra de todos
os talentos para equipar uma habilidade desbloqueada.

A escolha inicial é permanente para contas comuns. Enquanto o Premium/VIP
estiver ativo, o jogador pode trocar de caminho a qualquer momento, mesmo
em qualquer nível. A troca remove os nós comprados no ramo atual,
devolve seus Pontos de Legado e subtrai os atributos concedidos; depois permite
ativar um dos outros dois caminhos. Ao terminar o Premium/VIP, o caminho atual
permanece, mas não pode mais ser trocado até reativar o benefício. O servidor
confere a permissão VIP na hora da troca.

Ao abrir a árvore pela primeira vez após a atualização v0.111, talentos v0.104
comprados são removidos e seus custos e atributos são devolvidos uma única vez,
para que o jogador invista no novo ramo sem perder saldo. Investimentos
v0.102/v0.103 continuam registrados como legado e seus custos permanecem
contabilizados; não podem ser adquiridos novamente. Os testes cobrem os 12
conjuntos de passiva/habilidade, a unicidade e os efeitos dos nós, os custos,
exibição da comparação, a migração v0.104 e danos elemental/de projétil.
Os valores de poder seguem candidatos de balanceamento, não calibração final.

### 6.5 Densidade das hordas e desafio por fase

As ondas comuns 1–9 começam com 3 a 10 inimigos. A cada quatro fases, recebem
mais um inimigo por onda comum, até um máximo de quatro adicionais. A onda 10
tem semichefe nas fases 5/15/25, chefe de ato nas fases 10/20/30 e encontro
comum nas demais fases. Vida e dano não usam percentuais separados por
fase/onda: são calculados pela escala de nível
inimigo descrita na Seção 6.1, com limite no nível 400.

O orçamento total de EXP continua fixado ao entrar na fase e é repartido entre
os inimigos conforme as quantidades atuais e os pesos de comum/semichefe/chefe
1/3/5. Aumentar o número de monstros não aumenta a EXP total da fase; cada
inimigo comum recebe uma parcela menor. Quantidade, crescimento e ritmo da EXP
são valores provisórios e aguardam validação manual.

------------------------------------------------------------------------

## 7. Marcos de nível e Pontos de Legado

O personagem evolui continuamente do nível 1 ao 400. Não existe Reset: ao
alcançar o teto, o jogador mantém nível, atributos, pontos livres, talentos e
progresso da partida. O nível 400 não zera a EXP para reiniciar o ciclo.

**Recompensas aprovadas e implementadas:**

-   1 Ponto de Legado a cada 10 níveis alcançados, mais 1 a cada 50 níveis e
    mais 1 a cada 25 níveis: `nível // 10 + nível // 50 + nível // 25`.
-   No nível 400, o personagem recebeu 64 pontos. Os pontos gastos em talentos
    continuam contabilizados como saldo total adquirido.
-   Ao alcançar um marco de 50 níveis, a interface informa o marco junto com
    a recompensa de Legado. O nível 100 também libera a escolha de evolução.
-   Personagens existentes recebem saldo mínimo retroativo para os marcos do
    nível atual, somado aos Resets registrados no campo legado. A migração
    usa `MAX` e pode ser executada novamente sem duplicar pontos.

O campo `characters.resets` permanece apenas para compatibilidade dos bancos
existentes e para reconstruir pontos já concedidos em ciclos antigos; não
representa uma mecânica ativa nem aparece na interface. Pontos existentes,
talentos comprados e atributos são preservados.

### 7.1 Fim de fase, morte e recompensas

Morrer não encerra automaticamente a partida.

**Regra de morte:** ao chegar a zero de Vida, o jogador recebe o aviso de
morte e a sala pausa. O personagem retorna à onda 1 da fase atual com Vida
e Mana completas; o jogador escolhe reiniciar a fase ou ir à Sala de Espera. A
morte não encerra automaticamente a run. Cartas ativas, EXP de cartas, escolhas
pendentes, ofertas e orbes temporários são apagados. O cliente recebe a limpeza
por Socket.IO. Nenhum Ponto de Legado é concedido por morrer ou encerrar uma
partida; os marcos dependem exclusivamente do nível alcançado.

**Início de fase:** ao derrotar o chefe e começar a fase seguinte, Vida e
Mana também são restauradas por completo. Avançar entre ondas comuns não
restaura esses recursos.

**Fim de fase e cartas:** após o chefe da onda 10, a sala pausa e oferece
as opções de ir à Sala de Espera ou preparar a próxima fase. As cartas ativas, a
EXP, as ofertas e os orbes antigos da coleção são removidos nessa transição;
somente o orbe do chefe que acabou de morrer permanece no local do abate e pode
ser recolhido durante a preparação da nova fase. A próxima fase começa sem
cartas ativas e permite formar uma nova coleção.

**Recargas e Agilidade:** as recargas-base do protótipo, antes dos modificadores,
são 1,15 segundo para Ataque básico, 5 segundos para Golpe de Escudo
(Guerreiro) e Projétil de Cinzas (Tecelão), 4,5 segundos para Tiro Preciso
(Caçador), 6 segundos para Corte Rúnico (Lâmina Arcana) e 3 segundos para
Avanço. Cada ponto de Agilidade reduz 0,5% das recargas, até o limite de 50% de
redução como valor provisório de protótipo. O cálculo já considera
Agilidade persistida e talentos de Agilidade; a distribuição normal de
pontos de atributo ainda depende do sistema de atributos, e a taxa deverá
ser balanceada.

Ao iniciar uma missão pela Sala de Espera, a contagem regressiva de 5 segundos
congela movimento, ataques e IA dos monstros; o tempo oficial da run começa
quando a contagem termina. Esta regra é distinta da preparação de 30 segundos
que já ocorre após avançar para uma nova fase. Durante a preparação de fase,
não há ataques dos monstros. O jogador pode recolher orbes e
usar a experiência acumulada para escolher/substituir cartas nesse intervalo;
o servidor não bloqueia a coleta nem a escolha durante a preparação. Os
Talentos já disponíveis também podem ser abertos. Quando Inventário, Baú,
distribuição de atributos e configuração de habilidades forem implementados,
devem ficar acessíveis durante a preparação, sem pausar ou reiniciar o
cronômetro persistido.

O fluxo de missão também registra tempo de conclusão, dificuldade, saldo
virtual e baús em staging. Esses dados não alteram a progressão de XP ou os
Pontos de Legado atuais: o orçamento total de XP por fase permanece fixo e é
repartido entre as quantidades de inimigos da dificuldade selecionada. A
dificuldade e os valores de recompensa estão em protótipo e aguardam
calibração/aprovação (P-048).

-   Os Pontos de Legado são usados na Árvore de Talentos para aprimorar
    atributos ou comprar vantagens permanentes.

Exemplos de melhorias: - Desbloqueio de classes; - Melhorias na Árvore
de Talentos; - Espaços adicionais de inventário e baú dentro dos limites
gratuitos; - Melhorias de progressão e conveniência; - Aumento de chance
de encontrar determinados itens, caso o balanceamento permita.

**P-047:** a suíte em `tests/` verifica marcos de Legado, progressão de XP,
curva de inimigos e migração de personagens existentes. Ao mudar essas regras,
atualize e execute os testes. Calibração de ritmo e recompensas de endgame
continuam pendentes; novos cenários mensuráveis devem ser adicionados quando
esses sistemas forem definidos.

------------------------------------------------------------------------
