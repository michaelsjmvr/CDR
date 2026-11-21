# Conceito e jogabilidade

> Guia temático iniciado a partir do Documento Mestre v0.55 e atualizado com decisões posteriores. Consulte `Cronicas_do_Recomeco_Documento_Mestre_v0.139.md` para navegar entre assuntos.
>
> Atualizado em: 15/11/2026 21:54:32 (UTC−03:00).


## 2. Visão geral e identidade do jogo

**Crônicas do Recomeço** será um jogo de fantasia medieval sombria que
combina progressão de RPG online clássico, inspiração em jogos de ação
com ondas de inimigos e estrutura de salas/partidas com características
de roguelike.

A proposta é unir a sensação de evolução de personagem, equipamentos,
aprimoramentos, joias, asas, classes e economia de um RPG online
clássico com partidas de combate intensas, salas desafiadoras, eventos
aleatórios e progressão crescente.

O jogo deverá ter identidade própria. A referência a MU Online é
conceitual: nostalgia de RPG medieval online, equipamentos visualmente
evoluídos, joias, asas, forja, monstros e progressão. Os nomes,
habilidades, criaturas, mapas, interfaces, ícones, efeitos e recursos
finais deverão ser originais ou devidamente licenciados.

### 2.1 Pilares do projeto

1.  **Progressão constante:** o jogador deve sentir que está ficando
    mais forte, tanto durante uma partida quanto entre partidas.
2.  **Progressão contínua:** a direção atual é um teto-alvo de 170, com XP,
    Pontos de Legado e combate reequilibrados para a campanha; a mudança ainda
    está pendente. O código permanece temporariamente em 400, sem Reset.
3.  **Combate acessível e intenso:** o jogador comanda cada ataque; mira
    assistida identifica alvos, mas nunca dispara por conta própria.
4.  **Salas e ondas:** a experiência principal acontece em salas com
    ondas crescentes, eventos e chefes.
5.  **Equipamentos persistentes:** itens conquistados não desaparecem
    simplesmente porque o personagem morreu ou encerrou uma partida.
6.  **Cooperação e comunidade:** sala de espera, amigos, grupos, trocas e mercado
    entre jogadores.
7.  **Atmosfera dark fantasy:** cenários obscuros, medievais e góticos,
    contrastando com efeitos luminosos de equipamentos raros.
8.  **Originalidade:** aproveitar referências de gênero sem reproduzir
    conteúdo protegido de outros jogos.

------------------------------------------------------------------------

## 3. Gênero, câmera e experiência de jogo

  -----------------------------------------------------------------------
  Elemento                            Diretriz atual
  ----------------------------------- -----------------------------------
  Gênero                              Ação, RPG e roguelike

  Ambientação                         Fantasia medieval sombria

  Estrutura                           Salas, ondas, eventos e chefes

  Câmera                              Projeção 2.5D suave e zoom limitado
                                      implementados no protótipo (P-033)

  Combate                             Manual; ataques exigem comando

  Progressão                          Nível, atributos, equipamentos,
                                      Marcos de nível e meta-progressão

  Plataforma                          Navegador, com tecnologia HTML5

  Multiplayer                         Sala de Espera, salas cooperativas e
                                      recursos sociais planejados
  -----------------------------------------------------------------------

### 3.1 Modos de controle e combate

Os dois esquemas de controle mantêm combate manual: mirar ou ter um alvo
assistido nunca inicia um ataque. Ataques básicos e magias só acontecem após
uma tecla ou botão configurado pelo jogador. A antiga proposta de auto-ataque
Premium/VIP P-035 fica suspensa e não deve ser implementada sem nova decisão.

Em **Apenas Teclado**, a direção do movimento orienta o personagem e a mira
assistida pode destacar o inimigo próximo à frente no HUD; isso não dispara
ataques. Em **Teclado + Mouse**, o cursor orienta o personagem e o HUD destaca
o inimigo sob ele. O combate deve manter ritmo ágil com grupos de inimigos,
habilidades de área, movimentação e oportunidades de esquiva.

### 3.2 Habilidades

Haverá habilidades de ataque, área, controle e suporte, com nomes e
efeitos próprios. Habilidades clássicas de RPG online podem servir como
referência funcional, mas não deverão ser copiadas literalmente.

**Estado de P-018:** o catálogo-base já tem uma habilidade de classe para cada
uma das quatro classes, 12 habilidades assinaturas e 15 supremas; passivas,
maestrias e efeitos correspondentes estão integrados à Árvore de Talentos e ao
combate. Permanecem pendentes a calibração de custos, recargas e magnitudes,
animações/arte finais e a decisão sobre ampliar o catálogo. Não tratar a lista
inicial como balanceamento final.

### 3.3 Auto-poções Premium/VIP no protótipo

Os controles opcionais de Auto Vida e Auto Mana ficam na barra de combate e
podem ser ligados separadamente por contas Premium/VIP. Q e E alternam cada
opção. O servidor é a autoridade: Vida é restaurada quando cai a 50% ou menos
(recupera 30%, com recarga de 8 s); Mana é restaurada quando cai a 30% ou
menos (recupera 40%, com recarga de 12 s). As preferências são salvas por
personagem e as alterações de recurso são transmitidas por Socket.IO.

Esses números são provisórios. O protótipo ainda não tem estoque nem obtenção
de poções e, por isso, a automação não consome itens. P-032 acompanha a
integração futura com inventário, drops, loja e o orçamento de sobrevivência.

### 3.4 Controles do protótipo v0.108

WASD ou setas movem o personagem. Em **Teclado + Mouse**, ele olha para o
cursor e o painel superior mostra o monstro sob ele. Em **Apenas Teclado**,
olha para a direção do último movimento e o painel mostra o alvo assistido à
frente; nenhum dos dois modos ataca sem comando.

As teclas 1–4 da fileira superior e do Numpad têm mapeamento fixo: **1** sempre
executa Ataque básico; **2, 3 e 4** usam, respectivamente, as magias equipadas
nos espaços de magia 1, 2 e 3. A tela **Opções** permite equipar ou esvaziar
cada espaço de magia. Em Teclado + Mouse, os botões esquerdo e direito podem
ser vinculados a qualquer um desses espaços de magia (2–4). As preferências
são salvas por conta e sincronizadas por Socket.IO.

Se uma magia acionada por tecla ou mouse estiver em recarga ou sem Mana, o
Ataque básico é executado como fallback; o servidor valida alcance, alvo,
Mana, dano e recarga. Se o básico também não puder ser usado, a tentativa não
causa dano.

O fallback vale para a habilidade acionada que estiver equipada para a classe
e especialização atuais. Corte Rúnico é a habilidade-base da Lâmina Arcana,
não o nome genérico de todas as habilidades; se o Ataque básico também estiver
em recarga ou fora de alcance, nenhum dano é aplicado. Custos e magnitudes
continuam sujeitos ao balanceamento integrado P-031.

------------------------------------------------------------------------

## 4. Classes de personagem

O elenco inicial usa quatro arquétipos tradicionais de fantasia, com
nomes próprios para manter a identidade do projeto. As quatro classes,
seus atributos funcionais, habilidades-base, passivas, assinaturas e
especializações iniciais estão implementados. Atributos/equipamentos ainda
precisam de calibração conjunta; compatibilidade final de equipamentos, arte
dos retratos e eventuais classes desbloqueáveis continuam pendentes.

**Classes iniciais definidas:**

-   **Guerreiro** — arquétipo de combate corpo a corpo e resistência.
-   **Tecelão** — arquétipo de magia e controle.
-   **Caçador** — arquétipo de combate à distância.
-   **Lâmina Arcana** — arquétipo híbrido de combate físico e magia.

Os nomes visíveis atuais foram definidos para a campanha; os IDs internos das
classes permanecem estáveis para preservar personagens e compatibilidade. A
inspiração é o gênero e a estrutura de classes de RPGs clássicos; os nomes e
conteúdos permanecem próprios do projeto.

**Pendente em P-021:** definir eventuais classes desbloqueáveis, se será
possível trocar a classe de um personagem já criado, compatibilidade final
de equipamentos e detalhes de nomes/moderação. As três evoluções por classe
já estão implementadas; em P-018 continuam pendentes a calibração das
habilidades existentes e a decisão sobre ampliar o catálogo.

### 4.1 Seleção e criação de personagens

O responsável definiu que, após o login, o jogador veja a tela de seleção
de personagens. Nela, poderá criar um personagem com um nome disponível,
selecionar um personagem existente e usar o botão **Jogar** para iniciar
a partida. Também haverá uma ação **Deletar** para excluir um personagem.

Cada cartão de personagem deverá mostrar:

-   Retrato do personagem;
-   Nome;
-   Classe;
-   Nível;
-   Progresso de nível e Pontos de Legado.

A criação deverá associar o personagem a uma das classes iniciais da
Seção 4. O **Baú da Conta** continuará compartilhado por todos os
personagens da conta, conforme definido na Seção 10.2.

**Regras definidas pelo responsável:**

-   Limite padrão de 4 personagens por conta.
-   Limite de 6 personagens para uma conta Premium/VIP (nome usado na
    Seção 12).
-   Ao deletar, pedir confirmação e informar que os itens e demais dados
    vinculados àquele personagem serão perdidos, incluindo equipamento,
    inventário e progresso do personagem. O saldo de Ouro é compartilhado
    pela conta e não é perdido ao excluir um personagem.
-   A regra de exclusão vale mesmo quando a conta tem mais de um
    personagem; os itens vinculados ao personagem deletado são perdidos.
-   O Baú da Conta permanece enquanto houver pelo menos um personagem
    ativo. Ao deletar o último personagem, o baú e seu conteúdo também são
    perdidos, depois da confirmação explícita.

**Implementação inicial:** nomes globalmente únicos, com 3 a 20
caracteres; letras, números, espaços, hífen e sublinhado são permitidos.
Essa validação é provisória. A política final de nomes e moderação ainda
não está definida.

No protótipo, personagens começam no nível 1. O legado de Reset permanece
apenas como dado histórico compatível no banco; não é uma mecânica nem é
exibido ao jogador.
Os retratos atuais são provisórios e não são a arte final.

**Pendente em P-021:** regra de alteração de classe, arte dos retratos e tratamento
de contas com 6 personagens quando o Premium/VIP expirar. As regras de
tamanho/formato e moderação dos nomes também faltam.

------------------------------------------------------------------------

## 5. Estrutura das partidas: salas e ondas

A experiência de combate será organizada em salas. O jogador entra em
uma sala e enfrenta ondas progressivas de monstros.

### 5.1 Duração e composição das ondas

-   Cada onda deverá durar aproximadamente **30 a 60 segundos**.
-   A quantidade e a força dos inimigos aumentarão progressivamente.
-   Ao terminar uma onda, poderá ocorrer uma pausa para escolher
    melhorias temporárias, consultar uma loja rápida ou organizar a
    estratégia.
-   A progressão deverá manter o desafio mesmo quando o jogador
    encontrar bons equipamentos ou receber drops favoráveis.

### 5.2 Fases e chefes

**Temporada 1:** são 30 fases, organizadas em três atos de dez, com **10 ondas
por fase**. As ondas 1–9 são comuns; na onda 10 há semichefe nas fases 5, 15 e
25, chefe de ato nas fases 10, 20 e 30, e encontro comum nas demais fases. Ao
concluir a onda 10, o jogo pausa e oferece a escolha entre a Sala de Espera e a
preparação da fase seguinte, exceto na Fase 30, que encerra a temporada sem
avançar para a 31. Temporadas futuras e progressão após a Fase 30 ainda não
estão definidas.

**Entrada e conclusão de missão — protótipo v0.124:** a Sala de Espera oferece
quatro dificuldades em cascata e seleção de fase. O servidor valida o acesso:
a fase seguinte exige a conclusão da anterior na mesma dificuldade; a próxima
dificuldade exige 100% das fases da anterior. Ao iniciar uma missão, há uma
contagem regressiva visual de cinco segundos (`5, 4, 3, 2, 1, VAI!`), durante
a qual movimento, ataques e IA dos monstros ficam congelados. O cronômetro da
run começa após a contagem. Ao concluir a fase, a interface abre a tela
obrigatória de resultado/espólios; o resumo aparece em modal nativo e os baús
ficam em staging até o jogador resgatar ou descartar. Valores de dificuldade e
recompensa permanecem candidatos, não regras aprovadas (P-048). Um E2E em
navegador isolado percorreu as dez ondas da Fase 10 até o chefe e o resgate,
com progresso anterior pré-carregado e harness de combate acelerado; não
representa gameplay nem valida equilíbrio. Baú de
Recompensa de missão/chefe é espólio; Baú da Conta é armazenamento compartilhado
planejado, não o destino automático dos espólios.

### 5.3 Escalonamento de dificuldade

A dificuldade dos monstros deverá considerar dois fatores:

1.  Número da onda alcançada.
2.  Nível e poder atual do personagem.

O objetivo é evitar que a partida fique fácil demais apenas porque o
jogador teve sorte com equipamentos ou evoluiu rapidamente.

**Estado atual:** a estrutura da Temporada 1, as fórmulas de progressão de XP,
o orçamento e a distribuição de XP por fase, a densidade de inimigos e as
escalas de Vida/dano inimigo estão
implementadas como parâmetros de protótipo. Elas não são ainda o balanceamento
final. P-031/P-043/P-047 continuam exigindo calibração em combate ativo, várias
faixas e builds; equipamentos, composição de grupo e recompensas pós-400
também precisam ser integrados. O número e a posição dos chefes por fase foram
definidos.

### 5.4 Eventos especiais e chefes

A cada 5 ou 10 ondas, poderá surgir um evento especial ou um chefe.
Exemplos de inspiração:

-   Invasão de criaturas raras;
-   Sobrevivência contra ondas intensas;
-   Sala de desafio com limite de tempo;
-   Chefe com padrões de ataque próprios;
-   Evento com recompensa diferenciada.

Eventos inspirados em arenas de sobrevivência e invasões de monstros
deverão receber nomes, cenários, regras e recompensas originais.

**Pendente:** decidir se os eventos ocorrerão em salas separadas, em uma
área especial da sala atual ou por meio de uma transição.

### Protótipo P-036: leitura e ciclo dos ataques dos monstros

Os monstros comuns têm dois papéis: o Lacaio das Cinzas ataca de perto; a
Sentinela Rachada mantém distância e lança projéteis. Antes do impacto, o chão
mostra a área de perigo e o tempo restante. Os projéteis têm sombra visível no
chão para ajudar a ler a trajetória e o ponto de queda.

O semichefe alterna Ruptura do Arauto e Estilhaços da Cripta. O chefe alterna
Chuva do Umbral e Fenda do Umbral, com áreas marcadas que mudam entre círculo e
faixa de impacto. Os padrões repetem em ciclo para o jogador aprender o tempo e
encontrar a janela de esquiva. A advertência, o impacto e o dano são
transmitidos em tempo real por Socket.IO; o servidor valida inimigo ativo,
janela do impacto e posição informada na resolução. A movimentação ainda é
simulada no cliente neste protótipo. O chefe também se reposiciona e circula o
jogador durante o combate em vez de ficar parado dentro do alcance de ataque.

Valores atuais do protótipo: Golpe de Cinzas causa 25 de dano, marca raio 58
por 1,05 s e recarrega em 3,8 s; Projétil Sombrio causa 20, marca raio 42 por
1,35 s e recarrega em 4,2 s. A Ruptura do Arauto causa 42 em raio 100 após
1,65 s; Estilhaços da Cripta causam 30 em três áreas de raio 48 após 1,45 s.
Ambos recarregam em 7 s. Chuva do Umbral marca três círculos de raio 62 e causa
48 após 2,05 s; Fenda do Umbral marca quatro pontos alinhados, raio 46, e causa
42 após 1,85 s. Os dois ataques do chefe recarregam em 8,5 s.

Danos, raios, recargas e tempos de aviso são valores de protótipo, não o
balanceamento final. O movimento do chefe foi exercitado manualmente e o
movimento/zoom da câmera foi coberto na E2E v0.119. Isso não encerra a validação
visual dos telegráficos nem da esquiva em combate ativo; pitch em várias
resoluções e mira por mouse continuam pendentes.

### Protótipo P-025: afinidade dos chefes

O chefe recebe uma afinidade provisória em ciclo por fase: Fogo, Gelo, Raio
e Umbral. O protótipo atribui 30% de resistência ao elemento correspondente.
O perfil é calculado no servidor e enviado ao cliente; o elemento e a
resistência aparecem no painel superior do monstro mirado, não sobre o sprite.
O Corte Rúnico é tratado como
Umbral e causa dano reduzido quando enfrenta um chefe Umbral. O movimento do
chefe foi exercitado manualmente; isso não valida os valores experimentais de
afinidade/resistência, que seguem sem balanceamento e aprovação.

**Ainda não implementado em P-025:** escudo quebrado, sangramento, paralisia,
queimadura e atualização dinâmica desses estados. A aplicação está condicionada
à definição dos gatilhos, durações, resistências e limites em P-031; não atribuir
esses efeitos às habilidades atuais por suposição.

### Protótipo P-037: leitura do monstro mirado

Ao apontar o mouse para um inimigo, a interface mostra no alto, ao centro, um
painel com retrato procedural em Canvas, nome, nível, Vida e barra de Vida,
elemento, resistência e ponto fraco. A seleção prioriza o inimigo sob o cursor
e, quando não há um diretamente sob ele, o inimigo mais próximo alinhado à mira.
Os monstros no cenário exibem somente nome e barra de Vida.

Os dados respeitam o que o protótipo conhece: chefes mostram a afinidade e a
resistência provisória já existente; monstros sem perfil elemental mostram
“Neutro” e nenhuma resistência especial registrada. O ponto fraco aparece como
“Ainda não identificado” até que P-025/P-031 definam fraquezas e seus efeitos.
O painel é informativo e não muda fórmulas de dano. Vida e alvo acompanham as
atualizações de combate já transmitidas pelo Socket.IO.

O protótipo desenha dois círculos suaves correspondentes ao alcance real:
dourado para o ataque básico e azul para a habilidade-base ou assinatura
atualmente equipada. Os raios variam por
classe: Guerreiro 125/170, Tecelão 190/255, Caçador 225/305 e Lâmina Arcana
155/210 unidades. Cartas que alteram alcance multiplicam o raio e a distância
aceita pelo servidor na mesma proporção. Basta o contorno do monstro encostar
no círculo para o ataque alcançar: o cálculo soma o raio de colisão do alvo ao
alcance do personagem. Um alvo que não encosta no círculo fica fora do alcance.
O acerto por contato e a leitura dos círculos foram validados manualmente nas
quatro classes, inclusive com carta de alcance. Os raios continuam candidatos
de balanceamento; a mira por mouse e o pitch em diferentes resoluções ainda
precisam de validação.

------------------------------------------------------------------------
A arena jogável atual é um protótipo retangular de 2.400 × 1.800 unidades de
mundo, com origem no canto superior esquerdo e jogador iniciando no centro
(1.200, 900). Os inimigos usam posições pseudoaleatórias determinísticas,
mantendo 380 unidades de distância mínima do jogador e 92 entre si; a área de
surgimento vai de X=180 a 2.220 e Y=180 a 1.620. Na próxima onda, a posição do
jogador enviada pelo cliente vira o centro da área segura. Esses valores são os
do código, não uma escala de arte aprovada, e ainda precisam de validação em
combate ativo. Nas arenas genéricas, paredes e pilares continuam cenográficos,
sem colisão física. A Fase 1 é exceção: ônibus, colunas e bancos do Terminal de
Vilar bloqueiam movimento; a geometria aproximada e seus limites estão em
[Arquitetura e integridade](./06_arquitetura_e_integridade.md).
Veja [Arquitetura e integridade](./06_arquitetura_e_integridade.md) para a
geometria completa, projeção, limites, adornos e raios.

