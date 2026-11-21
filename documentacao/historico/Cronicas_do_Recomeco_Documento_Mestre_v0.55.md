# Crônicas do Recomeço

## Documento Mestre do Projeto

> **ARQUIVO HISTÓRICO — NÃO É A ESPECIFICAÇÃO VIGENTE.** Esta é a fonte
> integral v0.55 preservada para consulta histórica. O índice mestre ativo é
> `../Cronicas_do_Recomeco_Documento_Mestre_v0.139.md`. Regras antigas deste
> arquivo podem estar superadas.
>
> Aviso histórico acrescentado em: 15/11/2026 15:32:56 (UTC−03:00).
> Ponteiro para o índice ativo atualizado em: 15/11/2026 21:54:32 (UTC−03:00).

> **Finalidade:** este documento é a fonte central de verdade do
> projeto. Ele reúne decisões, sistemas planejados, regras, pendências e
> histórico de alterações para que qualquer pessoa ou IA consiga retomar
> o desenvolvimento sem redescobrir decisões já tomadas.
>
> **Regra de trabalho:** atualizar este arquivo antes de considerar uma
> decisão como parte oficial do projeto. Não iniciar implementação de
> sistemas ainda não aprovados. Quando uma informação estiver
> indefinida, mantê-la em **Pendências e decisões em aberto**, sem
> inventar uma resposta.

------------------------------------------------------------------------

## 1. Controle do documento

  Campo                   Informação
  ----------------------- ---------------------------------------------------------------
  Projeto                 Crônicas do Recomeço
  Tipo                    Jogo de ação com elementos de roguelike e RPG online clássico
  Documento               Documento Mestre
  Versão atual            0.55
  Última atualização      13/11/2026
  Estado geral            Protótipo inicial em andamento
  Implementação           Autorizada pelo responsável para iniciar o protótipo em 12/11/2026
  Plataforma pretendida   Navegador / HTML5
  Idioma inicial          Português (Brasil) --- provisório

### 1.1 Como a IA deve utilizar este documento

Ao trabalhar neste projeto, a IA deverá:

1.  Ler este documento antes de propor alterações ou implementar
    funcionalidades.
2.  Tratar as decisões marcadas como **Definido** como regras atuais do
    projeto.
3.  Não reapresentar perguntas que já estejam respondidas aqui.
4.  Não transformar sugestões em decisões sem confirmação do responsável
    pelo projeto.
5.  Manter as seções de pendências atualizadas e apontar conflitos entre
    novas ideias e regras existentes.
6.  Ao alterar uma regra, atualizar a seção correspondente e registrar
    no **Histórico de versões** o que mudou e por quê.
7.  Evitar repetir explicações já documentadas. Nas próximas conversas,
    priorizar apenas as informações novas, as decisões necessárias e as
    alterações realizadas.
8.  Não iniciar a implementação enquanto não houver autorização
    explícita.
9.  Preservar a identidade própria do jogo. Referências a outros jogos
    servem apenas como inspiração de gênero e experiência, não como
    autorização para copiar nomes, personagens, mapas, artes, sons,
    textos ou elementos protegidos.
10. Usar o painel de andamento da Seção 18.1 como registro contínuo do que
    foi concluído, está em andamento, falta fazer e de onde retomar.
11. A cada atualização, incrementar a versão e renomear o arquivo para
    `Cronicas_do_Recomeco_Documento_Mestre_vX.YY.md`, mantendo o nome do
    arquivo sincronizado com a versão da Seção 1 e do histórico. Atualizar
    também as referências ao arquivo, como no README.

### 1.2 Legenda de situação

-   **Definido:** decisão já informada e aceita como parte do projeto.
-   **Proposto:** ideia registrada, mas que ainda pode ser alterada.
-   **Pendente:** falta uma decisão ou informação.
-   **A fazer:** trabalho necessário para uma etapa futura.
-   **Concluído:** tarefa efetivamente realizada e validada.

------------------------------------------------------------------------

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
2.  **Recomeço estratégico:** o Reset é uma escolha que troca o nível
    atual por poder adicional e a possibilidade de avançar mais.
3.  **Combate acessível e intenso:** opção de jogar manualmente ou
    desbloquear o combate automático.
4.  **Salas e ondas:** a experiência principal acontece em salas com
    ondas crescentes, eventos e chefes.
5.  **Equipamentos persistentes:** itens conquistados não desaparecem
    simplesmente porque o personagem morreu ou executou um Reset.
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

  Câmera                              Isométrica ou perspectiva superior
                                      em estilo ARPG

  Combate                             Manual e automático desbloqueável

  Progressão                          Nível, atributos, equipamentos,
                                      Reset e meta-progressão

  Plataforma                          Navegador, com tecnologia HTML5

  Multiplayer                         Sala de Espera, salas cooperativas e
                                      recursos sociais planejados
  -----------------------------------------------------------------------

### 3.1 Modos de combate

O jogador poderá escolher entre duas formas de jogar:

-   **Manual:** o jogador controla diretamente o personagem,
    movimentação, ataques e esquivas.
-   **Automático:** o personagem realiza ataques automaticamente,
    conforme as regras e habilidades disponíveis.

**Regra definida:** o modo automático deverá ser desbloqueado pela
Árvore de Talentos. Não estará disponível desde o início para todos os
jogadores.

O combate deve manter ritmo ágil, com grupos de inimigos, habilidades de
área, movimentação e oportunidades de esquiva. O modo manual deve
permitir participação ativa; o automático deve funcionar como uma opção
de progressão, sem eliminar a necessidade de construir o personagem
adequadamente.

### 3.2 Habilidades

Haverá habilidades de ataque, área, controle e suporte, com nomes e
efeitos próprios. Habilidades clássicas de RPG online podem servir como
referência funcional, mas não deverão ser copiadas literalmente.

**Pendente em P-018:** fechar o catálogo de habilidades de combate por
classe, com custos, recargas, efeitos e animações. A Árvore de Talentos e
suas trilhas passivas são tratadas separadamente na Seção 6.4.

------------------------------------------------------------------------

## 4. Classes de personagem

O elenco inicial usa quatro arquétipos tradicionais de fantasia, com
nomes próprios para manter a identidade do projeto. Atributos,
equipamentos compatíveis e habilidades de cada classe ainda serão
definidos.

**Classes iniciais definidas:**

-   **Guardião do Umbral** — arquétipo de guerreiro, combate corpo a corpo.
-   **Tecelão de Cinzas** — arquétipo de mago, magia e controle.
-   **Vigia do Ermo** — arquétipo de arqueiro, combate à distância.
-   **Lâmina Rúnica** — arquétipo de gladiador mágico, mistura de combate
    físico e magia.

Os nomes e arquétipos iniciais foram definidos pelo responsável em
13/11/2026. A inspiração é o gênero e a estrutura de classes de RPGs
clássicos; os nomes e conteúdos permanecem próprios do projeto.

**Pendente:** definir classes desbloqueáveis, evoluções/especializações,
se será possível trocar a classe de um personagem já criado, e as
diferenças de atributos, equipamentos e habilidades. O catálogo de
habilidades continua na pendência P-018.

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
-   Quantidade de Resets.

A criação deverá associar o personagem a uma das classes iniciais da
Seção 4. O **Baú da Conta** continuará compartilhado por todos os
personagens da conta, conforme definido na Seção 10.2.

**Regras definidas pelo responsável:**

-   Limite padrão de 4 personagens por conta.
-   Limite de 6 personagens para uma conta Premium/VIP (nome usado na
    Seção 12).
-   Ao deletar, pedir confirmação e informar que os itens e demais dados
    vinculados àquele personagem serão perdidos, incluindo equipamento,
    inventário, Ouro e progresso do personagem.
-   A regra de exclusão vale mesmo quando a conta tem mais de um
    personagem; os itens vinculados ao personagem deletado são perdidos.
-   O Baú da Conta permanece enquanto houver pelo menos um personagem
    ativo. Ao deletar o último personagem, o baú e seu conteúdo também são
    perdidos, depois da confirmação explícita.

**Implementação inicial:** nomes globalmente únicos, com 3 a 20
caracteres; letras, números, espaços, hífen e sublinhado são permitidos.
Essa validação é provisória. A política final de nomes e moderação ainda
não está definida.

No protótipo, personagens começam no nível 1 com 0 Resets; esses campos
são exibidos no cartão, mas ainda não acompanham progressão de partida.
Os retratos atuais são provisórios e não são a arte final.

**Pendente em P-021:** regra de alteração de classe, origem/persistência
do nível e dos Resets mostrados no cartão, arte dos retratos e tratamento
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

A progressão de fases é infinita. Cada fase tem **10 ondas**: a onda 9
apresenta um semichefe e a onda 10, o chefe da fase. Ao derrotar o chefe,
o jogo pausa e pergunta se o jogador quer ir à Sala de Espera ou preparar a próxima
fase. A regra substitui o valor provisório anterior de cinco ondas.

### 5.3 Escalonamento de dificuldade

A dificuldade dos monstros deverá considerar dois fatores:

1.  Número da onda alcançada.
2.  Nível e poder atual do personagem.

O objetivo é evitar que a partida fique fácil demais apenas porque o
jogador teve sorte com equipamentos ou evoluiu rapidamente.

**Pendente:** definir fórmulas de vida, dano, defesa, quantidade de
inimigos, experiência e recompensas. O escalonamento deverá ser testado
para evitar crescimento exagerado ou dificuldade impossível. O número e
a posição dos chefes por fase foram definidos.

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

------------------------------------------------------------------------

## 6. Progressão durante a partida

### 6.1 Nível do personagem

-   O personagem começa a partida no nível 1.
-   O limite planejado é o nível 400.
-   Monstros derrotados concedem experiência.
-   Ao subir de nível, o jogador recebe pontos para distribuir entre
    atributos.

O limite 400 é uma referência inicial e poderá ser ajustado após testes
de balanceamento.

No protótipo, experiência por conclusão de onda e experiência necessária
por nível usam fórmulas provisórias em `game_app/progression.py`. Até a
implementação de inimigos, o botão **Concluir onda (teste)** simula a
conclusão e concede a experiência de teste; ele não representa combate
nem recompensa final.

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

Os efeitos exatos deverão variar conforme a classe e serão definidos no
balanceamento.

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
    No protótipo, cada orbe concede
    25 EXP e são necessários 100 EXP para liberar uma oferta de 3 cartas.
    Esses valores são provisórios para balanceamento.
-   A escolha inicial de cartas e cada barra completada apresentam 3 opções;
    o jogador escolhe 1 para ativar ou substituir uma carta.
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
-   O conjunto inicial terá pelo menos **30 cartas diferentes**, com
    atributos e habilidades distintos.
-   As cartas exibem raridade pela escala e paleta de 6 níveis da Seção
    8.2: Comum, Incomum/Mágico, Raro, Excelente, Épico/Ancestral e
    Lendário/Mítico.
-   Cartas ativas são melhorias temporárias da partida; ao fazer Reset,
    todas são removidas, conforme a Seção 7.1.
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

O protótipo contém 30 definições em `game_app/cards.py`. Orbes luminosos
aparecem na posição de cada monstro derrotado; ao encostar neles, o jogador
coleta EXP. A barra de EXP aparece no painel de cartas
ativas. Ao completar a barra, abre-se a oferta de três cartas. Na interface,
ao passar o mouse ou focar uma carta ativa, sua descrição informa o que ela
faz. Os efeitos são apresentados, mas ainda não alteram atributos ou
habilidades durante combate; sua integração e balanceamento permanecem
pendentes.

**Apresentação visual do orbe:** núcleo branco/dourado bem definido e
claramente visível, envolto por uma aura luminosa intensa com difusão suave
e pequenos brilhos. A luz pulsa lentamente, aumentando e diminuindo com
transição suave, sem cintilação brusca.

**Pendente em P-022:** aplicar os efeitos das cartas às regras de combate
e balanceá-los. As 30 definições iniciais e a política de sorteio estão
no protótipo.

### 6.4 Árvore de Talentos

Cada personagem possui uma Árvore de Talentos própria e determinada por
sua classe. A apresentação usa um tabuleiro escuro de nós ramificados,
trilhas e pré-requisitos como referência de navegação ARPG, mantendo
nomes, organização e efeitos originais de Crônicas do Recomeço.

**Estrutura do protótipo:** três trilhas por classe, com nós em camadas
conectadas por pré-requisitos. Os nós podem aprimorar Força, Agilidade,
Vitalidade ou Energia, ou oferecer vantagens defensivas e passivas
adequadas ao arquétipo da classe. Os custos iniciais de protótipo são 1,
2 ou 3 Pontos de Legado por nó; custos e efeitos precisam de
balanceamento. Compras são registradas por personagem.

**Estado:** quatro árvores originais estão prototipadas em
`game_app/talents.py`. O saldo compra nós na rota protegida
`/talentos/comprar`; a tela mostra conexões, pré-requisitos e pontos
disponíveis. Os efeitos dos nós ainda são majoritariamente descrições;
talentos de Agilidade já atualizam esse atributo, que reduz as recargas.
Os demais atributos e efeitos continuam sem aplicação mecânica.

**Pendente em P-023:** integrar e balancear efeitos, definir regras de
reembolso/redistribuição e validar os custos. Pontos de Legado só poderão
ser obtidos quando P-003 definir a recompensa de fim de partida; o
protótipo não concede pontos de teste.

------------------------------------------------------------------------

## 7. Sistema de Reset

O Reset é uma das mecânicas centrais de Crônicas do Recomeço.

### 7.1 Reset voluntário durante a partida

Ao atingir o nível 400, o jogador poderá escolher a opção **Resetar**.

**Regras definidas:**

-   Ao atingir o nível 400, o jogador pode escolher fazer Reset.
-   O personagem retorna ao nível 1 e sua experiência volta ao início
    desse nível.
-   A fase atual é mantida; a onda volta à primeira onda daquela fase.
-   As melhorias temporárias da partida são perdidas.
-   Ouro, equipamentos e demais itens persistentes do personagem são
    mantidos, conforme a Seção 10.1.
-   Cada Reset concede 1 Ponto de Legado para a Árvore de Talentos. A
    concessão está implementada no fluxo de Reset.

O Reset é voluntário e permite seguir a progressão infinita dentro da
fase atual, reiniciando a evolução do nível e a sequência de ondas da
fase. A implementação depende da base de experiência, fases e ondas.

### 7.2 Encerramento da partida e Pontos de Legado

Quando o jogador encerrar a partida, o progresso obtido será contabilizado
para a meta-progressão. Morrer não encerra automaticamente a partida.

**Regra de morte:** ao chegar a zero de Vida, o jogador recebe o aviso de
morte e a sala pausa. O personagem retorna à onda 1 da fase atual com Vida
e Mana completas; o jogador escolhe reiniciar a fase ou ir à Sala de Espera. A
morte não encerra automaticamente a run. A recompensa final continua em
aberto em P-003.

**Início de fase:** ao derrotar o chefe e começar a fase seguinte, Vida e
Mana também são restauradas por completo. Avançar entre ondas comuns não
restaura esses recursos.

**Fim de fase e cartas:** após o chefe da onda 10, a sala pausa e oferece
as opções de ir à Sala de Espera ou preparar a próxima fase. As cartas ativas, a
EXP e as ofertas temporárias da coleção são removidas nessa transição; a
próxima fase começa sem cartas ativas e permite formar uma nova coleção.

**Recargas e Agilidade:** os valores iniciais de protótipo são 1 segundo
para ataque básico, 6 segundos para Corte Rúnico e 3 segundos para Avanço.
Cada ponto de Agilidade reduz 0,5% das recargas, até o limite de 50% de
redução como valor provisório de protótipo. O cálculo já considera
Agilidade persistida e talentos de Agilidade; a distribuição normal de
pontos de atributo ainda depende do sistema de atributos, e a taxa deverá
ser balanceada.

Após entrar em uma fase nova, há 30 segundos de preparação antes de a
horda começar a perseguir/atacar. O tempo é persistido no servidor; durante
a preparação não há ataques dos monstros. O jogador pode recolher orbes e
usar a experiência acumulada para escolher/substituir cartas nesse intervalo;
o servidor não bloqueia a coleta nem a escolha durante a preparação. Os
Talentos já disponíveis também podem ser abertos. Quando Inventário, Baú,
distribuição de atributos e configuração de habilidades forem implementados,
devem ficar acessíveis durante a preparação, sem pausar ou reiniciar o
cronômetro persistido.

-   Os Resets realizados durante a partida contribuem para a quantidade
    de **Pontos de Legado** concedida ao encerrar a partida.
-   Os Pontos de Legado são usados na Árvore de Talentos para aprimorar
    atributos ou comprar vantagens permanentes.

Exemplos de melhorias: - Desbloqueio de classes; - Melhorias na Árvore
de Talentos; - Espaços adicionais de inventário e baú dentro dos limites
gratuitos; - Melhorias de progressão e conveniência; - Aumento de chance
de encontrar determinados itens, caso o balanceamento permita.

**Pendente em P-003:** definir a fórmula e o momento de concessão dos
Pontos de Legado adicionais ao ponto concedido por Reset, limites, bônus
por desempenho e eventual penalidade por encerramento voluntário. A morte
e o Ouro persistente também devem ser considerados nas regras de fim de
partida sem contrariar a Seção 10.1.

------------------------------------------------------------------------

## 8. Itens, equipamentos, raridades e aprimoramentos

### 8.1 Equipamentos

O jogo terá equipamentos persistentes, incluindo:

-   Elmo;
-   Armadura;
-   Luvas;
-   Calças;
-   Botas;
-   Arma da mão direita;
-   Escudo ou arma secundária na mão esquerda;
-   Asas;
-   Colar (Pendente);
-   Dois anéis.

A compatibilidade dos equipamentos dependerá da classe e das regras de
cada item.

### 8.2 Níveis de Raridade e Cores de Borda (Definido)

Todos os itens do jogo (armaduras, espadas/armas, asas, anéis, colares/pendentes, joias e consumíveis) seguem uma escala visual padronizada de **6 níveis de raridade**.

Para manter a leitura clara e separar **Raridade** de **Aprimoramento**, a **borda do slot** identifica exclusivamente a raridade do item:

  -----------------------------------------------------------------------
  Nível de Raridade       Cor da Borda (Hex)     Efeito Visual no Slot
  ----------------------- ---------------------- ------------------------
  **Comum**               Cinza-Aço (`#475569`)  Borda simples e fosca,
                                                 sem brilho.

  **Incomum / Mágico**    Verde-Esmeralda        Borda fina com leve
                          (`#10B981`)            reflexo esverdeado.

  **Raro**                Azul-Safira            Borda com brilho
                          (`#38BDF8`)            azul-arcano suave.

  **Excelente**           Dourado / Âmbar        Borda metálica dourada
                          (`#F59E0B`)            com pulso luminoso.

  **Épico / Ancestral**   Roxo-Ametista          Borda rúnica violeta com
                          (`#A855F7`)            aura sutil.

  **Lendário / Mítico**   Vermelho-Carmesim      Borda intensa com
                          (`#F43F5E`)            partículas de brasa.
  -----------------------------------------------------------------------

### 8.3 Aprimoramento de equipamentos

Equipamentos poderão receber níveis de aprimoramento. A referência
inicial é uma escala que inclui +0 até +11 ou superior.

Enquanto a **borda do slot** indica a raridade (Seção 8.2), o **nível de aprimoramento** é identificado pela tag numérica (ex: `+9`) e pelo **brilho interno / aura sobre o ícone do item**, além de mudanças visuais no personagem:

  -----------------------------------------------------------------------
  Nível                               Aparência planejada
  ----------------------------------- -----------------------------------
  +0 a +6                             Aparência metálica normal, sem
                                      brilho interno intenso

  +7 a +9                             Brilho interno dourado/âmbar

  +10 a +11 ou superior               Aura interna intensa (azul arcano
                                      ou carmesim)
  -----------------------------------------------------------------------

Os efeitos de aprimoramento deverão manter legibilidade e não
prejudicar a visualização da cor da borda de raridade.

### 8.4 Joias

Joias serão itens importantes de aprimoramento e economia. Os nomes
provisórios citados são equivalentes conceituais a joias clássicas de
bênção, alma e caos.

Para preservar a identidade própria do projeto, os nomes finais deverão
ser originais.

Conceito definido: - Joias podem ser obtidas como drops de monstros e
chefes. - Poderão ser usadas em aprimoramentos e receitas. - O drop
deverá ter destaque visual e sonoro. - O jogador poderá armazená-las
permanentemente.

**Pendente:** definir nomes oficiais, raridades, usos, taxas de drop,
limites de pilha e regras de falha de aprimoramento.

------------------------------------------------------------------------

## 9. Asas e Forja do Caos

### 9.1 Asas

As asas serão equipamentos especiais e elementos importantes de
progressão visual.

Conceito definido: - Poderão ser obtidas por criação na forja ou por
outros meios que venham a ser aprovados. - Poderão representar marcos de
evolução. - Poderão oferecer bônus e, eventualmente, alterar mobilidade
ou estilo de ataque. - O visual deverá comunicar raridade e evolução do
personagem.

**Pendente:** definir categorias, requisitos, atributos, habilidades,
progressão e se todas as classes poderão usar todos os modelos.

### 9.2 Forja do Caos

A **Forja do Caos** será acessível por um botão ou menu na interface,
sem exigir que o jogador procure um NPC no cenário.

Conceito inicial: - A forja usa Ouro, uma Pedra do Caos e itens-base. -
Poderá criar asas e outros itens especiais. - Receitas e requisitos
serão exibidos na interface. - A criação poderá ter chance de sucesso ou
falha. - O jogador deverá visualizar os materiais exigidos e as chances
antes de confirmar.

**Pendente:** definir taxas de sucesso, consequências de falha, proteção
contra perda de itens, custos, receitas e se a forja poderá ser usada
durante o combate ou apenas na Sala de Espera/pausas.

### 9.3 Pets e montarias

O jogo também contará com **pets** e **montarias**. Os pets acompanharão
visualmente o personagem; as montarias servirão para deslocamento e
apresentação do personagem. Tipos, obtenção, velocidade, habilidades,
limites de uso, possibilidade de combate e efeitos de atributos ainda
serão definidos antes da implementação desses sistemas.

------------------------------------------------------------------------

## 10. Persistência de itens, inventário e baú

### 10.1 Regra de persistência

**Decisão definida:** equipamentos, asas, Ouro e joias não deverão
desaparecer simplesmente por causa de um Reset ou da morte do
personagem.

Os itens conquistados serão mantidos no inventário ou no Baú da Conta,
conforme as regras de armazenamento.

A perda ou destruição de itens só poderá ocorrer por uma mecânica
explícita, informada ao jogador e aprovada no projeto.

### 10.2 Inventário e equipamentos

A interface terá duas áreas principais:

-   **Painel do personagem:** equipamentos equipados e mochila.
-   **Painel do Baú da Conta:** armazenamento compartilhado entre
    personagens da mesma conta.

O Baú da Conta permanece enquanto existir pelo menos um personagem ativo
na conta. Se o último personagem for deletado, o baú e o conteúdo nele
armazenado também são deletados após confirmação explícita.

No protótipo atual, existe apenas o registro do baú por conta; interface,
slots e armazenamento de itens do baú ainda não foram implementados.

A mochila terá uma grade modular com 8 colunas como referência inicial.

Slots de equipamento: - Elmo; - Armadura; - Luvas; - Calças; - Botas; -
Mão direita; - Mão esquerda; - Asas; - Colar; - Anel 1; - Anel 2.

### 10.3 Capacidade inicial

  Área              Capacidade inicial planejada
  --------------- ------------------------------
  Mochila                   2 linhas, 16 espaços
  Baú principal             3 linhas, 24 espaços

Os espaços bloqueados deverão permanecer visíveis, com aparência
escurecida e indicação de cadeado ou corrente.

### 10.4 Expansão de espaço

A expansão poderá ocorrer por dois caminhos:

1.  **Progressão gratuita:** nós da Árvore de Talentos comprados com
    Pontos de Legado desbloqueiam novas linhas, até o limite gratuito
    planejado.
2.  **Loja Premium:** possibilidade de adquirir expansões adicionais,
    como abas extras de baú ou capacidade além do limite gratuito.

O limite gratuito de referência para a mochila é de até 6 linhas. O
limite final do baú ainda precisa ser definido.

### 10.5 Interações

A interface deverá oferecer: - Arrastar e soltar itens entre mochila,
baú e equipamentos; - Tooltips com nome, nível, raridade, atributos e
descrição; - Indicação visual de slots compatíveis; - Bloqueio visual de
espaços indisponíveis; - Comparação entre item selecionado e item
equipado; - Exibição do saldo de Ouro; - Depósito e saque de Ouro entre
personagem e baú, conforme regras de segurança.

### 10.6 Validação

Toda movimentação deverá ser validada pelo servidor. O cliente não
poderá decidir sozinho se um item existe, se pertence à conta ou se um
slot está desbloqueado.

A validação deverá conferir: - Propriedade do item; - Localização
atual; - Espaço de destino; - Compatibilidade com o equipamento; -
Capacidade desbloqueada; - Quantidade disponível; - Regras de bloqueio e
transação.

------------------------------------------------------------------------

## 11. Economia do jogo

### 11.1 Moedas e recursos

O projeto já menciona os seguintes recursos:

-   **Ouro:** moeda obtida durante as partidas e usada em sistemas
    internos, como a Forja do Caos. Pertence ao personagem e não pode
    ser perdido por Reset, morte ou encerramento de partida; poderá ser
    gasto pelo jogador conforme as regras dos sistemas.
-   **Pontos de Legado:** moeda de meta-progressão obtida ao encerrar
    partidas.
-   **Gemas Premium:** moeda associada à loja paga, ainda sujeita à
    decisão final sobre monetização.
-   **Joias e materiais:** recursos de aprimoramento e fabricação, não
    necessariamente moedas de uso geral.

**Pendente:** fechar a lista oficial de moedas, fontes, usos, limites e
regras de transferência.

### 11.2 Loja durante a partida

Foi proposta uma loja rápida entre ondas, com melhorias e itens
temporários ou consumíveis.

**Pendente:** definir se a loja usa Ouro, se vende itens permanentes,
consumíveis ou apenas melhorias da partida.

### 11.3 Loja Premium

Foi proposta uma loja acessível pelo menu principal ou por um ícone na
interface. A ideia inicial inclui: - Asas prontas; - Pacotes de joias; -
Skins; - Expansões de inventário e baú; - Itens de conveniência; - Gemas
Premium como moeda.

Esta proposta ainda precisa de avaliação de equilíbrio, modelo de
negócio, regras da plataforma e proteção contra vantagens injustas.

**Pendente:** decidir se haverá compras com dinheiro real, quais itens
poderão ser vendidos e se a loja será apenas cosmética/conveniência ou
também afetará poder e progressão.

------------------------------------------------------------------------

## 12. Conta Premium / VIP

Foi proposta uma assinatura ou status Premium que concede benefícios
enquanto estiver ativo.

Benefícios cogitados: - Maior chance de drop de itens raros e
excelentes; - Multiplicador de ganho de Ouro; - Maior chance de drop de
joias; - Acesso remoto ao Baú; - Espaços extras de armazenamento.

**Benefício de cartas definido para contas com status Premium/VIP ativo:**
até 8 cartas temporárias ativas na partida, em comparação às 6 de uma
conta padrão. Isso não aprova, por si só, assinatura paga, preço ou os
demais benefícios Premium/VIP.

**Situação:** proposta, ainda não aprovada como regra final.

**Benefício de capacidade definido para personagens:** contas padrão
podem ter até 4 personagens; contas Premium/VIP podem ter até 6. A
definição dos limites não aprova, por si só, a assinatura, o preço nem os
demais benefícios Premium/VIP.

**Pontos que precisam ser definidos:** - Preço, duração e renovação; -
Benefícios exatos; - Se os bônus afetam partidas cooperativas de forma
justa; - Se vantagens de drop serão aplicadas individualmente ou ao
grupo; - Como evitar que a assinatura crie desequilíbrio competitivo; -
Regras de cancelamento, expiração e reembolso, quando aplicáveis.

------------------------------------------------------------------------

## 13. Multiplayer, sala de espera e recursos sociais

### 13.1 Sala de Espera

Os jogadores terão uma sala de espera para se encontrar e organizar partidas.

Depois de selecionar um personagem e clicar em **Jogar**, o fluxo passa
primeiro pela sala de espera. O caminho público é `/sala-de-espera`, e a
página usa rolagem vertical para se adaptar a diferentes alturas de tela.
O layout atualizado organiza a tela em duas colunas: à esquerda ficam os
três cartões do grupo e o painel de Chat da Sala; à direita ficam os serviços
e a lista de amigos.
O espaço do personagem local mostra nível, classe e uma ilustração Canvas
provisória colorida conforme a classe. Os dois cartões restantes indicam
vagas para amigos. O serviço Árvore de Talentos está ativo; Inventário,
Baú, Máquina do Caos e Troca aparecem como indisponíveis/planejados.

Na barra superior fica a busca de perfis, fina e discreta, junto à identidade
do jogo e ao atalho para trocar personagem. A lista de amigos fica na coluna
direita, abaixo dos serviços. O cartão de grupo mostra as informações do
personagem e o botão **Começar!**, contido e alinhado ao canto inferior, sem
painel separado de personagem que repita esses dados. Cada vaga vazia abre um
seletor da lista de amigos; a página exibe o total de amigos e uma lista com
até cinco linhas visíveis, rolável se for maior.
O aviso de intervalo após concluir uma fase fica ao lado do botão Começar,
na mesma linha quando houver espaço, para preservar altura para o Chat da Sala.

**Estado atual do protótipo:** busca de perfis, amizades persistentes,
convites, grupos e chat em tempo real ainda não existem. Busca e botões de
convite aparecem desabilitados; contagem inicia em zero e não há amigos
falsos no protótipo. Clicar numa vaga abre o seletor com o estado vazio. A
área de chat é somente visual e permanece desabilitada até a infraestrutura
de salas e associação de jogadores. Não transmitir mensagens em sala global.

Na sala de espera deverão ficar disponíveis Inventário, Baú, Máquina do Caos para
criação de itens, Talentos, troca direta (*trade*) e gerenciamento de
amigos. Os serviços ainda não implementados aparecem identificados como
indisponíveis no protótipo.

O jogador poderá: - Criar uma sala aberta para qualquer pessoa entrar; -
Criar uma sala privada/trancada; - Permitir entrada apenas de amigos
adicionados à lista de amigos.

### 13.2 Salas cooperativas

**Direção definida:** jogadores poderão jogar juntos em salas de ondas.
O sala de espera será o ponto de encontro e organização.

**Pendente:** definir tamanho máximo do grupo, convite, expulsão, líder
da sala, reconexão, entrada durante uma partida e regras de dificuldade
para grupos.

### 13.3 Lista de amigos

O projeto prevê uma lista de amigos para permitir salas privadas e
facilitar a formação de grupos.

**Pendente:** definir solicitações, bloqueios, presença online, convites
e notificações.

### 13.4 Troca direta e mercado entre jogadores

Foi proposta uma economia entre jogadores com: - Janela de troca direta
(*trade*); - Anúncios de equipamentos e joias no mercado; - Compra de
itens por Ouro ou recursos permitidos; - Persistência dos itens após a
troca.

A troca deverá ser validada no servidor e realizada como uma operação
segura, impedindo duplicação, perda indevida ou alteração de itens
durante a confirmação.

**Pendente:** definir taxas de mercado, limites, itens negociáveis,
bloqueios de troca, histórico e prevenção contra fraude.

### 13.5 PvP

Foi mencionado o modo jogador contra jogador (1x1), mas não foram
definidas regras.

**Pendente:** decidir se o PvP fará parte do lançamento, se será
ranqueado ou casual, quais atributos e equipamentos serão permitidos e
se haverá arenas próprias.

------------------------------------------------------------------------

## 14. Direção de arte e identidade visual

### 14.1 Atmosfera

A direção visual será **Dark Fantasy medieval**, sombria, madura e
estilizada.

Referências de atmosfera: - Cenários obscuros e góticos; - Ruínas,
fortalezas, masmorras, florestas sombrias e regiões amaldiçoadas; -
Ferro escuro, obsidiana e bronze envelhecido; - Contraste entre
ambientes escuros e efeitos luminosos de equipamentos raros; - Monstros
com silhuetas bem definidas e leitura clara durante o combate.

Evitar: - Visual infantil ou excessivamente cartunesco; - Excesso de
brilho que prejudique a leitura; - Cópia de mapas, monstros, personagens
ou interfaces de outros jogos; - Uso de nomes e artes protegidos sem
autorização.

### 14.2 Paleta de cores da interface e raridades (Definido)

  Uso                                 Cor
  ----------------------------------- -----------
  Fundo principal                     `#090A0F`
  Painéis                             `#12151E`
  Bordas metálicas base               `#2A303C`
  Ouro velho / bronze                 `#B48A3E`
  Títulos dourados                    `#E2C07D`
  Borda Raridade: Comum               `#475569`
  Borda Raridade: Incomum / Mágico    `#10B981`
  Borda Raridade: Raro                `#38BDF8`
  Borda Raridade: Excelente           `#F59E0B`
  Borda Raridade: Épico / Ancestral   `#A855F7`
  Borda Raridade: Lendário / Mítico   `#F43F5E`

### 14.3 Tipografia

Sugestões iniciais: - **Títulos:** Cinzel ou outra fonte serifada de
fantasia medieval. - **Textos e números:** Inter, Rajdhani ou outra
fonte sem serifa de leitura rápida.

As fontes deverão ter licença compatível com o projeto.

### 14.4 Produção de gráficos

A intenção é produzir gráficos e elementos visuais com apoio de IA e
também considerar recursos criados por código.

Possibilidades: - Sprites e ilustrações originais; - Elementos vetoriais
e SVG; - Efeitos procedurais em Canvas/WebGL; - Partículas e animações
feitas por código; - Cenários em camadas para efeitos de
profundidade/parallax.

**Pendente:** definir o padrão de arte dos personagens, monstros, mapas,
animações, efeitos e ícones. Também será necessário definir quais
elementos serão gerados por IA, desenhados manualmente ou construídos
por código.

------------------------------------------------------------------------

## 15. Interface e experiência do usuário (UI/UX)

### 15.1 Padrão geral

A interface deverá usar tema escuro, painéis de aparência metálica,
bordas discretas e detalhes em bronze/dourado.

Janelas principais: - Inventário; - Baú; - Forja do Caos; - Loja; -
Trade; - Árvore de Talentos; - Perfil/personagem; - Configurações.

**Árvore de Talentos:** abrir a árvore exclusiva da classe do personagem
em foco, com três trilhas ramificadas, nós conectados e saldo de Pontos de
Legado. A tela do protótipo está descrita na Seção 6.4.

**Tela inicial definida:** após autenticar, exibir a seleção de
personagens antes de entrar na sala. A composição tem três zonas sobre
um cenário noturno: prévia grande e central do personagem selecionado
com animação idle provisória; caixa escura semitransparente com nome,
classe, nível e Resets; painel vertical à direita com slots, seleção,
criação e ações inferiores. O slot ativo usa borda Bronze `#B48A3E`,
segundo a paleta da Seção 14.2. Um slot livre oferece **Criar Novo
Personagem**. **Jogar** fica junto à prévia; **Deletar** e **Voltar** ficam
no canto inferior direito. A prévia SVG é apenas um placeholder visual,
não a arte final. O fluxo está descrito na Seção 4.1; arte final e demais
detalhes continuam pendentes em P-021.

Na sala de jogo, o topo também oferece **Trocar Personagem**, que retorna
à seleção da conta sem encerrar a sessão. O jogador pode escolher outro
personagem e entrar novamente com **Jogar**.

As janelas deverão sobrepor a área de jogo quando fizer sentido, sem
retirar o jogador da sala. Ações que possam interromper o combate ou
causar perda de recursos deverão ter confirmação adequada.

### 15.2 Slots e tooltips

-   Slots vazios deverão manter aparência organizada.
-   Slots bloqueados deverão mostrar cadeado ou corrente.
-   A **borda externa do slot** exibe a cor oficial da raridade do item
    (conforme tabela da Seção 8.2), enquanto o **brilho interno**
    representa o nível de aprimoramento (Seção 8.3).
-   Ao passar o mouse sobre um item, será exibido um tooltip com suas
    informações.
-   O tooltip deverá usar a cor da raridade do item em seu cabeçalho e
    borda.
-   Quando possível, deverá comparar o item com o equipamento atualmente
    utilizado.

### 15.3 Feedback de interação

Diretrizes propostas: - Hover com destaque sutil; - Slots compatíveis
destacados durante o arraste; - Slots incompatíveis ou bloqueados com
indicação visual distinta; - Animações curtas e discretas; - Sons de
interface para abrir/fechar janelas, movimentar itens e transferir
moedas.

Os sons deverão ser originais ou licenciados. O uso de efeitos sonoros
deverá respeitar as configurações de volume do jogador.

### 15.4 HUD de combate

A proposta inicial para o HUD inferior inclui: - Indicador de Vida em
vermelho carmesim; - Indicador de Mana/Energia em azul safira; - Barra
de experiência dourada; - Atalhos de poções; - Atalhos de habilidades; -
Informações essenciais da onda e do personagem.

A disposição final deverá ser testada em diferentes resoluções e
tamanhos de tela.

**Direção e controles do protótipo:** WASD ou setas direcionais controlam
a movimentação. O personagem acompanha a posição do mouse para mirar, e
ataques/habilidades atingem inimigos alinhados à direção apontada dentro
do alcance do protótipo. Botão esquerdo executa o ataque básico; botão
direito usa a habilidade Corte Rúnico. Impacto do Umbral foi removido do
combate do protótipo. Espaço executa um avanço rápido na direção da mira,
com colisão preservada e recarga visual no HUD. Velocidade, duração e
recarga do dash são valores iniciais de protótipo. A mira não altera a
movimentação normal.

**Apresentação de capítulos e ondas:** a introdução de cada capítulo usa
a faixa narrativa superior do cenário uma única vez por personagem e
capítulo no navegador. Depois da introdução, transições exibem somente
fase/onda ou chefe; o início de um capítulo novo mostra a introdução nessa
faixa e, em seguida, a fase/onda.

**Controles contínuos:** não permitir seleção de texto dentro da sala. Ao
segurar o botão esquerdo/direito, repetir ataque/habilidade respeitando a
recarga; Espaço repetirá o dash enquanto continuar pressionado e a recarga
permitir. O ataque básico também possui recarga curta.

**Informações de combate:** exibir a quantidade de monstros restantes e
atualizá-la a cada derrota. O painel do chefe deverá apresentar tipo,
elemento, resistências e estados de combate: escudo quebrado, sangramento,
paralisia e queimadura. Regras e valores de elementos/resistências ainda
serão definidos em P-025.

**Sala de Espera e configuração:** a tela individual já existe e contém
espaços visuais para dois amigos. Inventário, Baú,
Máquina do Caos, grupo em tempo real, convites, lista de amigos e troca
continuam pendentes em P-028/P-005/P-016/P-014/P-017. Esses sistemas de
configuração deverão poder ser usados na Sala de Espera e na preparação de fase
assim que forem implementados.

**IA e contato dos monstros:** cada monstro ativo tem sua própria recarga de
dano por contato, validada pelo servidor para o ID do inimigo e a onda atual.
Monstros que encontram um aliado no caminho tentam rotas laterais e contornam
o bloqueio para chegar ao jogador; não devem formar uma fila imóvel enquanto
houver espaço para se aproximarem e atacarem.

------------------------------------------------------------------------

## 16. Arquitetura e tecnologias

### 16.1 Plataforma

**Direção definida:** jogo executado no navegador, utilizando
tecnologias HTML5.

A interface e o cliente de jogo deverão funcionar em navegadores
modernos. O uso de Canvas ou WebGL será avaliado para renderização
2D/isométrica.

### 16.2 Tecnologias planejadas

  -----------------------------------------------------------------------
  Camada                              Tecnologia / direção
  ----------------------------------- -----------------------------------
  Estrutura web                       HTML5

  Estilização                         Tailwind CSS

  Lógica do cliente                   JavaScript

  Renderização do jogo                Canvas ou WebGL --- a definir

  Backend                             Python

  Framework web                       Flask

  Comunicação em tempo real           Socket.IO sobre WebSocket

  Banco de dados                      SQLite no protótipo; PostgreSQL
                                      como opção para produção
  -----------------------------------------------------------------------

### 16.3 Banco de dados

Recomendação técnica inicial: - **SQLite:** adequado para prototipagem
local e desenvolvimento inicial com poucos usuários. - **PostgreSQL:**
recomendado como banco principal quando o projeto evoluir para múltiplos
usuários, transações, inventário persistente, mercado e partidas
simultâneas.

MongoDB não é a primeira opção recomendada neste momento, porque boa
parte das informações do jogo possui relações claras --- contas,
personagens, itens, inventários, transações, salas e histórico --- que
se beneficiam de integridade relacional.

**Uso no protótipo:** o primeiro cadastro local utiliza SQLite para
armazenar nomes de usuário e hashes de senha. Isso é uma escolha
provisória de implementação e não encerra a pendência P-009 nem define o
banco de produção.

A escolha final deverá considerar hospedagem, custo, escalabilidade e
testes reais.

### 16.4 Comunicação em tempo real

Socket.IO sobre WebSocket será utilizado para recursos que exigem
atualização em tempo real, como: presença e sala de espera, entrada e saída de
jogadores, estado de salas cooperativas, eventos e ondas, ações dos
jogadores, progresso das cartas e notificações. A biblioteca cliente será
servida localmente pelo projeto para não depender de CDN durante a
execução.

O servidor deverá ser a autoridade sobre ações importantes do jogo. O
cliente envia intenções; o servidor valida e atualiza o estado oficial.

### 16.5 Segurança e integridade

Princípios obrigatórios de arquitetura: - Não confiar em valores de
dano, Ouro, experiência ou drops enviados pelo cliente; - Validar
movimentação e propriedade de itens no servidor; - Proteger sessões e
senhas com práticas adequadas; - Validar entradas e limitar
requisições; - Registrar operações importantes de economia e
inventário; - Evitar duplicação de itens e transações concorrentes; -
Implementar controles contra abuso de WebSocket; - Manter backups do
banco de dados; - Separar ambiente de desenvolvimento e produção.

**Pendente:** elaborar modelo de dados, autenticação para produção, permissões,
estrutura de salas, estratégia de hospedagem e plano de testes de carga.

**Protótipo de autenticação:** cadastro e login básicos foram
implementados no servidor Flask, com senhas armazenadas em hash, sessão
assinada e proteção CSRF nos formulários. A solução ainda precisa de
revisão para uso online e não define requisitos finais de contas,
recuperação de senha, limitação de tentativas ou permissões.

------------------------------------------------------------------------

## 17. Regras de integridade da economia e dos itens

Como o jogo prevê inventário persistente, trocas e mercado, a
integridade dos dados será essencial.

Regras de projeto: 1. Um item deverá ter identificação única. 2. Toda
movimentação deverá ser registrada e validada no servidor. 3. Uma troca
só será concluída quando os participantes confirmarem os termos finais.
4. O servidor deverá impedir que o mesmo item seja utilizado em duas
operações simultâneas. 5. Alterações de saldo deverão ser transacionais.
6. Ações administrativas e correções deverão gerar registros de
auditoria. 7. Recompensas de partidas deverão ser calculadas e
concedidas pelo servidor. 8. O histórico deverá permitir investigar
operações suspeitas.

------------------------------------------------------------------------

## 18. Escopo por etapas

As etapas abaixo são uma organização inicial sugerida, não um cronograma
aprovado.

### Legenda das tarefas

-   `[x]` Concluído e validado.
-   `[~]` Implementado ou em andamento, mas ainda não validado/concluído.
-   `[ ]` Ainda não iniciado ou aguardando decisão.

### Etapa 1 --- Definição do projeto

-   [x] Definir o nome provisório/oficial do projeto: Crônicas do
    Recomeço.
-   [x] Consolidar a proposta de mistura entre RPG clássico e roguelike.
-   [x] Definir a direção de arte dark fantasy.
-   [x] Definir sistema de raridades e cores de borda dos itens.
-   [x] Definir a estrutura básica de salas e ondas.
-   [x] Registrar o conceito de Reset e Pontos de Legado.
-   [x] Registrar a direção tecnológica HTML5 + JavaScript + Flask +
    WebSocket.
-   [x] Definir as quatro classes iniciais e seus nomes próprios (P-001).
-   [x] Definir as regras centrais do Reset (P-002); fórmula dos Pontos
    de Legado continua em P-003.
-   [ ] Definir economia e monetização.
-   [ ] Definir escopo do multiplayer e PvP.
-   [ ] Definir catálogo inicial de itens, joias e habilidades.

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
Inimigos e Vida/Mana persistem no protótipo; a primeira IA de perseguição e
ataque por contato foi implementada no cliente, com dano validado e aplicado
no servidor via Socket.IO. Sincronização de movimento em multiplayer ainda
falta. Canvas 2D e retratos são provisórios; classes ainda não têm atributos
completos nem habilidades próprias no combate. Agilidade já está persistida
e afeta recargas quando obtida por talentos.

-   [x] Criar sala de teste e implementar movimentação/câmera;
    funcionamento confirmado pelo responsável.
-   [ ] Implementar um personagem e uma classe inicial.
-   [x] Validar a tela de seleção e a troca de personagem no navegador.
-   [~] Validar criação, limite de slots, exclusão e Baú da Conta em
    diferentes situações.
-   [~] Inimigos persistidos por onda, colisão local, perseguição ao personagem e ataque por contato; movimento da IA aguarda validação e balanceamento.
-   [~] Preparação de 30 segundos após cada mudança de fase; o servidor persiste o horário final e impede ataques durante a preparação. Aguarda validação manual.
-   [~] HUD mostra monstros restantes e atualiza após derrotas; aguarda validação manual.
-   [x] Ao derrotar o último inimigo, a onda avança pelo Socket.IO sem recarregar a página; destaque central, chefe individual na onda final e apresentação por capítulo/onda foram validados pelo responsável.
-   [x] Definir e configurar 10 ondas por fase; onda 9 tem semichefe e onda
    10 tem chefe. P-004 concluído quanto à estrutura; balanceamento permanece.
-   [~] Implementar experiência e nível com fórmula provisória por onda;
    experiência real por inimigo e pontos de atributo continuam pendentes.
-   [~] Implementar cartas temporárias com escolha inicial, orbes coletáveis
    de EXP, barra de progresso e oferta de 3 cartas ao completá-la; coleção
    ativa (6 padrão / 8 Premium/VIP) e substituição opcional, com estado
    atualizado por Socket.IO sem recarregar a sala. Código feito, aguardando
    validação manual da coleta e do ciclo completo. Efeitos ainda não são
    aplicados em combate.
-   [~] Usar Socket.IO para coleta de orbes, escolhas de cartas e avanço
    simulado de ondas; falta validar no navegador.
-   [~] Combate manual: ataque básico no botão esquerdo e Corte Rúnico no botão direito; valores de dano/EXP são provisórios.
-   [~] Cooldowns iniciais: ataque básico 1 s, Corte Rúnico 6 s e Avanço 3 s;
    Agilidade reduz 0,5% por ponto, até 50%. Agilidade persistida afeta talentos
    e os cooldowns são validados no servidor; aguarda validação manual.
-   [~] Morte pausa a sala e oferece reiniciar a fase ou ir à Sala de Espera; chefe
    da onda 10 abre escolha entre sala de espera e próxima fase. Cartas são removidas
    ao concluir fase.
-   [~] Criar tela inicial de sala de espera após selecionar personagem;
    layout responsivo com três cartões de grupo, retrato Canvas provisório,
    chat visual, progresso/serviços e início da partida. Busca e seletor de
    amigos estão esboçados, mas não conectados a perfis. Amizades persistentes,
    convites, salas de grupo e chat Socket.IO ainda não existem. Talentos está
    ativo; Inventário, Baú, Máquina do Caos e trade continuam indisponíveis.
-   [ ] Mostrar elemento/resistências do chefe e efeitos de escudo quebrado, sangramento, paralisia e queimadura (P-025).
-   [ ] Prototipar o combate automático como habilidade desbloqueável.

### Etapa 4 --- Progressão e conteúdo

-   [~] Implementar Reset: confirmação e regra de servidor preparadas;
    pode ser alcançado pela progressão simulada; aguarda inimigos e combate
    real para validar o fluxo de gameplay completo.
-   [x] Conceder 1 Ponto de Legado por Reset.
-   [~] Criar Árvore de Talentos original para as quatro classes; interface
    e compra por personagem implementadas, efeitos e pontos aguardam os
    sistemas de progressão/fim de partida.
-   [ ] Implementar equipamentos e inventário.
-   [ ] Implementar baú persistente.
-   [ ] Implementar joias e aprimoramentos.
-   [ ] Implementar Forja do Caos e asas.
-   [ ] Definir e implementar pets e montarias; regras de obtenção e efeitos
    ainda precisam ser decididos.
-   [ ] Criar eventos e chefes.
-   [ ] Criar pausa de fim de capítulo (a cada 10 fases) e área de preparação com Inventário, Baú, Estatísticas e Status do Personagem (P-026).

### Etapa 5 --- Recursos online

-   [ ] Criar sala de espera.
-   [ ] Criar lista de amigos.
-   [ ] Criar salas abertas e privadas.
-   [ ] Implementar partidas cooperativas.
-   [ ] Implementar trade.
-   [ ] Implementar mercado.
-   [ ] Avaliar e implementar PvP, se aprovado.

### Etapa 6 --- Polimento e lançamento

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

**Estado atual:** cadastro, login, logout, bloqueio de `/jogo` sem sessão,
movimentação por WASD/setas, mira pelo mouse, tela de seleção, botão **Trocar Personagem**, exibição e
troca/manutenção das cartas ativas e subida de nível foram testados e
aprovados pelo responsável em 13/11/2026. As regras centrais do Reset
(P-002) estão definidas. A progressão e as cartas podem ser percorridas no
modo de simulação. A Árvore de Talentos por classe foi prototipada;
combate manual básico foi validado; Pontos de Legado concedidos ainda faltam. O responsável confirmou ataque, EXP por monstro, orbes e barra dinâmica por cartas ativas. O novo
ciclo de orbes de EXP e escolha de cartas foi implementado e aguarda teste
manual do responsável. Socket.IO foi integrado à coleta, às cartas e à
simulação de ondas, também aguardando validação manual.

**Implementado e validado pelo responsável:**

-   Cadastro, login, logout e proteção de `/jogo` sem sessão.
-   Sala visual provisória com movimentação por teclado e câmera de
    acompanhamento.
-   Tela de seleção e retorno à seleção pelo botão **Trocar Personagem**.
-   Mira pelo mouse, botões esquerdo/direito para ataque básico/habilidade
    e dash no Espaço foram testados e confirmados pelo responsável nesta
    sessão.
-   Introdução única de capítulo na faixa narrativa, transições de fase/onda,
    onda de chefe e restauração de Vida/Mana após morte foram confirmadas
    pelo responsável.

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
-   Preparação do Reset: campos de experiência, fase, onda, Ouro e Pontos
    de Legado no modelo do personagem; rota protegida e confirmação
    disponíveis apenas a partir do nível 400. A confirmação aplica nível 1,
    experiência 0, primeira onda da fase atual e incrementa Resets;
    melhorias temporárias são removidas, enquanto fase, Ouro e itens ficam.
    A simulação de ondas consegue evoluir até 400; nível por combate real,
    carta efetiva e concessão de Pontos de Legado ainda não existem.
-   Progressão de protótipo com XP, nível até 400, 10 ondas por fase,
    semichefe na onda 9 e chefe na 10. O avanço real ocorre ao derrotar
    a horda; um botão de teste ainda simula a conclusão para desenvolvimento.
-   Catálogo de 30 cartas, sorteio ponderado, ofertas sem duplicatas,
    coleção ativa de 6/8 cartas e troca opcional quando cheia. O Reset
    limpa cartas ativas; seus efeitos ainda são descritivos, sem aplicação
    aos atributos do jogo. A descrição de cada carta ativa aparece ao
    passar o mouse ou focá-la por teclado. Cada monstro derrotado deixa um
    orbe na posição da morte; recolhê-lo enche a barra de EXP (25 por orbe;
    100 para uma oferta de três cartas, valores provisórios). Cartas não têm
    níveis.
    O fluxo está implementado e aguarda validação manual.
-   Eventos de jogo em Socket.IO no modo threading; coleta de orbes, barra
    de EXP, ofertas/escolhas de cartas e conclusão simulada de ondas atualizam
    a sala sem recarregar. A biblioteca JavaScript do Socket.IO está servida
    em arquivo local. Falta validação manual no navegador.
-   Conexões SQLite usam WAL e `busy_timeout` de 15 segundos. Eventos de
    escrita retornam erro controlado caso ainda não consigam iniciar a
    transação; ataques não são enviados em paralelo pelo cliente.
-   Mira pelo mouse no combate: o personagem gira para o cursor e ataques
    selecionam inimigos alinhados à direção apontada; WASD/setas mantêm a
    movimentação. Botão esquerdo ataca e botão direito usa Corte Rúnico;
    Impacto do Umbral removido. Controles validados pelo responsável.
-   Dash no Espaço avança na direção atual da mira, respeita os limites do
    cenário e a colisão com inimigos, e exibe recarga no HUD. Duração,
    velocidade e recarga são valores provisórios; funcionamento validado
    pelo responsável.
-   Ao morrer, o servidor restaura Vida e Mana completas e retorna o
    personagem à onda 1 da fase atual; a sala pausa com escolha entre
    reiniciar fase e ir à Sala de Espera. Interface implementada, aguarda validação.
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
-   IA inicial de monstros: perseguem o personagem, evitam se sobrepor uns
    aos outros e atacam por contato. O servidor aplica recarga individual
    por inimigo, persiste a Vida/Mana e transmite o dano por
    Socket.IO. Movimento da IA fica local no protótipo até o multiplayer;
    aguarda validação manual.
-   Árvore de Talentos exclusiva para cada uma das quatro classes, com
    trilhas ramificadas, nós conectados, custos, pré-requisitos e compras
    salvas por personagem. Como P-003 ainda não define a concessão de
    Pontos de Legado, o saldo atual pode ser zero; não foram criados pontos
    artificiais. Efeitos ainda não se aplicam ao gameplay.
-   Registro do Baú da Conta compartilhado; removido ao deletar o último
    personagem. O protótipo ainda não armazena itens no baú.
-   Estrutura de arquivos separada entre autenticação, banco, segurança,
    rotas, templates, CSS e JavaScript.

**Documentação atualizada:**

-   Documento mestre mantido como referência central, com histórico e
    painel de andamento.
-   README atualizado com a estrutura e os comandos para iniciar.

**Próxima etapa:** validar no navegador os novos fluxos da sala de espera, morte,
pausa após o chefe, limpeza das cartas e ondas 9/10. Em seguida, completar
os serviços da Sala de Espera (P-028/P-026) e validar cooldowns com Agilidade (P-029).

**Ainda não iniciado:** autoridade do servidor sobre movimentação/combate;
aplicação dos efeitos das cartas; balanceamento de atributos, talentos e
limites por nível da árvore (adiados para serem feitos em conjunto);
regras adicionais de fim da partida (P-003); reembolso da árvore (P-023);
balanceamento de ondas e inimigos; economia,
multiplayer/PvP, catálogo final de habilidades/itens e arquitetura final.

------------------------------------------------------------------------

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

  P-002             Reset             Definir o que é  Concluído
                                      mantido e o que   (regras centrais)
                                      reinicia no Reset 
                                      voluntário?        

  P-003             Fim de partida    Como a morte      Pendente
                                      encerra a run e   
                                      calcula Pontos de 
                                      Legado?           

  P-004             Ondas             A cada quantas    Concluído
                                      ondas haverá      (estrutura)
                                      eventos e chefes? 

  P-005             Multiplayer       Quantos jogadores Parcial
                                      poderão entrar em (grupo de 3
                                      uma sala          definido; rede
                                      cooperativa?      pendente)

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
                                      cenários?         

  P-008             Produção visual   Quais recursos    Pendente
                                      serão gerados por 
                                      IA, desenhados ou 
                                      construídos por   
                                      código?           

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

  P-018             Habilidades       Criar catálogo    Pendente
                                      original de       
                                      habilidades por   
                                      classe.           

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

  P-022             Cartas            Aplicar efeitos  Parcialmente
                                      e balancear     catálogo/sorteio
                                      na progressão   implementados

  P-023             Talentos          Integrar e      Parcialmente
                                      balancear       prototipados;
                                      efeitos e       efeitos/reembolso
                                      definir         pendentes
                                      reembolso       

  P-024             Pets e           Definir tipos,  Pendente
                    montarias        obtenção, usos,
                                     habilidades e
                                     efeitos de jogo

  P-025             Chefes e         Definir/implementar Pendente
                    estados          elementos,
                                     resistências,
                                     quebra de escudo,
                                     sangramento,
                                     paralisia e
                                     queimadura

  P-026             Hub de fim       Completar hub    Parcial
                    de capítulo      com Inventário,  (tela-base da Sala de Espera feita;
                                     Baú, Estatísticas serviços faltam)
                                     e Status

  P-027             IA e contato     Validar rotas   Em validação
                    dos monstros     ao redor de     após correção
                                     aliados e       de contato e
                                     cadência por    contorno
                                     inimigo

  P-028             Sala de Espera social     Implementar     Pendente
                    e serviços       presença de     (tela-base feita;
                                     amigos, grupo,   recursos online
                                     convites e       faltam)
                                     acesso aos
                                     serviços

  P-029             Atributos        Definir pontos  Pendente
                    do personagem    por nível e     (Agilidade já
                                     alocação de      reduz recargas)
                                     Agilidade
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 20. Decisões consolidadas

Esta lista resume o que já foi informado e incorporado ao documento:

-   Nome do jogo: **Crônicas do Recomeço**.
-   Mistura de RPG clássico inspirado em MU Online com estrutura
    roguelike.
-   Ambientação medieval dark fantasy, sombria e original.
-   Câmera isométrica ou superior em estilo ARPG.
-   Partidas organizadas em salas e ondas.
-   Progressão infinita em fases de 10 ondas; onda 9 é semichefe, onda 10
    é chefe. Após o chefe, o jogador escolhe entre sala de espera e próxima fase.
-   Ao iniciar uma fase após derrotar o chefe, o personagem recebe 30
    segundos de preparação antes de a horda começar. Vida e Mana são
    restauradas nesse momento; ondas comuns não restauram esses recursos.
-   A coleção de cartas é temporária por fase; as cartas ativas são removidas
    ao derrotar o chefe e começa uma nova coleção na fase seguinte.
-   A morte pausa o jogo; o jogador pode reiniciar a fase ou ir à Sala de Espera.
-   Após selecionar personagem, o botão Jogar abre a sala de espera. A capacidade
    desejada do grupo é de três jogadores (jogador e dois amigos).
-   Cooldowns iniciais de protótipo: ataque básico 1 s, Corte Rúnico 6 s e
    Avanço 3 s. Agilidade reduz provisoriamente 0,5% por ponto, com redução
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
-   Classes iniciais: Guardião do Umbral (guerreiro), Tecelão de Cinzas
    (mago), Vigia do Ermo (arqueiro) e Lâmina Rúnica (gladiador mágico).
-   Personagens são criados e selecionados após o login; os limites são 4
    por conta padrão e 6 por conta Premium/VIP.
-   Deletar personagem remove seus dados vinculados após confirmação; o
    Baú da Conta é removido junto ao último personagem da conta.
-   Reset voluntário ao atingir o nível 400.
-   No Reset, nível/experiência voltam ao início, fase é mantida, onda
    retorna ao início da fase e melhorias temporárias são perdidas.
-   Melhorias temporárias são cartas: uma oferta inicial permite começar a
    coleção; durante a partida, orbes coletáveis de EXP enchem uma barra e
    liberam uma escolha entre 3 cartas para adicionar ou substituir. Não há
    nível individual das cartas. Coleção ativa de 6 cartas padrão ou 8
    Premium/VIP; pelo menos 30 cartas distintas com efeitos e raridade
    visível. A coleção é removida no fim da partida e usa pesos iniciais de
    raridade 50/25/14/7/3/1% do Comum ao Lendário. Cartas não ativas podem
    voltar a aparecer em ondas futuras.
-   Ouro e itens persistentes do personagem permanecem no Reset.
-   Resets contribuem para Pontos de Legado usados na Árvore de Talentos;
    fórmula e quantidade continuam pendentes em P-003.
-   Combate manual e automático, com automático desbloqueado pela Árvore
    de Talentos.
-   Sistema oficial de **6 níveis de raridade e cores de borda** para
    todos os itens (Comum, Incomum, Raro, Excelente, Épico, Lendário).
-   Separação visual entre borda externa (raridade) e brilho interno
    (aprimoramento).
-   Joias, aprimoramento de equipamentos e efeitos visuais por nível.
-   Asas criáveis pela Forja do Caos.
-   Pets como companheiros visuais e montarias para deslocamento; detalhes
    de obtenção, mecânicas e efeitos ainda pendentes.
-   Itens persistentes após Reset e morte, guardados no inventário ou
    baú.
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

## 21. Histórico de versões
### v0.27 --- 13/11/2026

**Tipo:** correção da validação incompatível com o ímã dos orbes.

**O que mudou:** - Removida a comparação entre a posição local do orbe atraído e a posição original salva no banco. A coleta continua limitada a orbes não coletados pertencentes ao personagem ativo.

**Por que mudou:** - O ímã move o orbe apenas no cliente; o servidor comparava com a posição original persistida, causando a mensagem mesmo após a atração.

**Impacto no projeto:** - Corrige o falso erro. A validação de distância real depende de movimentação autoritativa no servidor, ainda não implementada no protótipo.

**Seções atualizadas:** - Seções 1, 18.1 e 21.

**Pendências criadas ou resolvidas:** - Causa corrigida; validação manual pendente. A tentativa da v0.26 foi registrada como falha para não ser repetida.

### v0.26 --- 13/11/2026

**Tipo:** correção da coleta dos orbes e ajuste da atração magnética.

**O que mudou:** - A validação de proximidade usa agora a posição do orbe
após o ímã atraí-lo, eliminando a discrepância com a posição do personagem
em movimento. - A velocidade de atração aumenta conforme o orbe se aproxima.

**Por que mudou:** - O responsável relatou que correr enquanto o orbe era
atraído causava uma mensagem de distância incorreta ao coletá-lo e pediu
absorção mais rápida.

**Impacto no projeto:** - Coleta e atração continuam via Socket.IO; requer
validação manual no navegador.

**Seções atualizadas:** - Seções 1, 18.1 e 21.

**Pendências criadas ou resolvidas:** - A validação manual desta correção
permanece pendente.

### v0.25 --- 13/11/2026

**Tipo:** atualização em tempo real do protótipo e inclusão de pets e
montarias no escopo planejado.

**O que mudou:** - Adicionado Socket.IO ao servidor e ao cliente local. -
Coleta de orbes, atualização da EXP, escolhas/substituições de cartas e
conclusão simulada de ondas passam a atualizar a sala sem recarregá-la. -
Orbes recebem atração suave quando o personagem se aproxima. - Registrados
pets como companheiros e montarias como recurso de deslocamento, com regras
específicas ainda pendentes.

**Por que mudou:** - O responsável pediu comunicação em tempo real para
evitar recarregar a página ao coletar orbes, solicitou uma atração leve e
incluiu pets e montarias no escopo do jogo.

**Impacto no projeto:** - `python app.py` passa a iniciar por Socket.IO;
dependência Flask-SocketIO e cliente JavaScript compatível são adicionados.
Eventos ainda precisam de validação manual no navegador. Pets e montarias
estão planejados, sem implementação de gameplay.

**Seções atualizadas:** - Seções 1, 9.3, 16, 18, 18.1, 20 e 21.

**Pendências criadas ou resolvidas:** - A validação de Socket.IO e atração
de orbes permanece aberta. Criada P-024 para definir tipos, obtenção,
habilidades e efeitos de pets e montarias.

### v0.24 --- 13/11/2026

**Tipo:** mudança no ritmo de aquisição de cartas temporárias e início da
coleta de orbes de EXP.

**O que mudou:** - Substituída a oferta automática de cartas a cada onda por
orbes coletáveis que enchem a barra de EXP da coleção. - Ao completar 100
EXP, o jogador recebe uma oferta de 3 cartas para adicionar ou substituir;
cada orbe concede 25 EXP no protótipo. - Confirmado que cartas não terão
níveis individuais. - Implementada persistência de EXP, escolhas pendentes,
orbes por personagem e desenho/coleta de orbes no cenário.

**Por que mudou:** - O responsável pediu que as cartas não precisassem ser
adicionadas ou trocadas ao final de toda onda e definiu que EXP coletável
deve liberar a escolha.

**Impacto no projeto:** - Valores de EXP e posicionamento dos orbes são
provisórios. O fluxo aguarda validação manual; cartas ainda não aplicam
efeitos ao combate.

**Seções atualizadas:** - Seções 1, 6.3, 18, 18.1, 20 e 21.

**Pendências criadas ou resolvidas:** - P-022 continua parcialmente
pendente para validação manual, aplicação dos efeitos e balanceamento.

### v0.23 --- 13/11/2026

**Tipo:** descrição das cartas ativas e registro de validação da
progressão.

**O que mudou:** - Adicionada descrição acessível ao passar o mouse ou
focar uma carta ativa; ela explica seu efeito. - Registrado que o
responsável testou e validou a exibição/manutenção/troca das cartas e a
subida de nível.

**Por que mudou:** - O responsável solicitou a explicação do efeito ao
inspecionar uma carta e informou que validou o fluxo de cartas e nível.

**Impacto no projeto:** - A descrição usa o texto do catálogo. Os efeitos
continuam sem aplicação mecânica até a implementação de atributos e
combate.

**Seções atualizadas:** - Seções 1, 6.3, 18.1 e 21.

**Pendências criadas ou resolvidas:** - Fluxo de cartas e subida de nível
marcados como validados pelo responsável. A interação de tooltip foi
implementada e aguarda validação manual.

### v0.22 --- 13/11/2026

**Tipo:** protótipo de Árvore de Talentos por classe.

**O que mudou:** - Criadas quatro árvores originais, uma para cada classe,
cada qual com três trilhas ramificadas e nós com pré-requisitos. - A nova
tela mostra saldo de Pontos de Legado, custos, efeitos, conexões e estado
de cada nó. - Compras são protegidas por sessão/CSRF, validadas no
servidor e persistidas no personagem. - Adicionado acesso à árvore pelo
topo da sala.

**Por que mudou:** - O responsável pediu uma árvore com navegação visual
de ARPG, inspirada na legibilidade de Diablo IV, mas usando classes,
atributos e vantagens próprias do projeto.

**Impacto no projeto:** - A árvore muda conforme a classe vinculada ao
personagem. Os custos de 1/2/3 Pontos de Legado e os efeitos são valores
iniciais de protótipo; efeitos ainda não modificam atributos ou combate.
Como a recompensa de fim de partida (P-003) não está definida, contas
atuais podem não ter pontos para comprar nós. Nenhum saldo artificial foi
adicionado.

**Seções atualizadas:** - Seções 1, 3.2, 6.4, 15.1, 18, 19, 20 e 21.

**Pendências criadas ou resolvidas:** - Criada P-023 para integração e
balanceamento dos efeitos e definição de redistribuição/reembolso. A
interface e persistência por personagem estão prototipadas.

### v0.21 --- 13/11/2026

**Tipo:** primeira simulação de progressão, ondas e cartas.

**O que mudou:** - Criados módulos separados para catálogo/sorteio de
cartas e progressão provisória. - A conta recebe 3 ofertas de cartas por
onda, pode ativar uma, manter até 6 (padrão) ou 8 (Premium/VIP), e pode
substituir uma carta ativa ou recusar a troca. - O catálogo inicial tem
30 cartas com raridade e descrições de efeitos. - A conclusão simulada
de onda concede experiência e avança até a quinta onda, tratada como
chefe de teste; concluir essa onda inicia a próxima fase.

**Por que mudou:** - Iniciar a próxima etapa definida no painel e tornar
testáveis a progressão, a coleção e as regras de Reset já decididas.

**Impacto no projeto:** - Fórmulas de experiência e 5 ondas por fase são
valores provisórios. Não há inimigos nem combate real; o botão de concluir
onda simula o resultado. Os efeitos das cartas ainda são descritivos e
não mudam atributos ou habilidades. O Reset pode ser alcançado na
simulação, mas precisa de validação manual.

**Seções atualizadas:** - Seções 1, 5, 6.1, 6.3, 18, 19, 20 e 21.

**Pendências criadas ou resolvidas:** - Implementada primeira versão de
progressão e ofertas; P-004 permanece aberto sobre o número final de
ondas. P-022 tem catálogo prototipado e aguarda integração/balanceamento
dos efeitos. Combate e XP real por inimigo continuam pendentes.

### v0.20 --- 13/11/2026

**Tipo:** retorno de cartas não ativas ao sorteio.

**O que mudou:** - Cartas não escolhidas e cartas removidas por
substituição podem aparecer em ondas futuras, desde que não estejam
ativas na coleção. - Mantida a regra contra duplicatas na oferta atual e
na coleção ativa.

**Por que mudou:** - O responsável definiu a política de retorno das
cartas ao sorteio.

**Impacto no projeto:** - O conjunto pode continuar oferecendo escolhas
ao longo da progressão infinita sem permitir cópias simultâneas da mesma
carta na coleção.

**Seções atualizadas:** - Seções 1, 6.3, 19 e 21.

**Pendências criadas ou resolvidas:** - Resolvida a política de retorno
ao sorteio em P-022. Falta criar o catálogo inicial de pelo menos 30
cartas com seus efeitos e raridades.

### v0.19 --- 13/11/2026

**Tipo:** regras de raridade, unicidade e duração da coleção temporária.

**O que mudou:** - Definidos pesos iniciais: Comum 50%, Incomum/Mágico
25%, Raro 14%, Excelente 7%, Épico/Ancestral 3% e Lendário/Mítico 1%.
- A coleção de cartas é removida ao encerrar a partida. - As 3 cartas
oferecidas na mesma onda são distintas e não se pode ativar uma segunda
cópia de uma carta que já esteja ativa.

**Por que mudou:** - O responsável delegou o balanceamento inicial dos
pesos e definiu que a coleção é temporária e não deve ter cartas iguais.

**Impacto no projeto:** - A regra de retorno ao sorteio ainda aguardava a
decisão do responsável, registrada depois em v0.20. O conjunto inicial
de pelo menos 30 cartas ainda precisa ser criado.

**Seções atualizadas:** - Seções 1, 6.3, 18, 19, 20 e 21.

**Pendências criadas ou resolvidas:** - Pesos de raridade e limpeza ao fim
da partida definidos. P-022 continua parcial para retorno ao sorteio e
catálogo de cartas.

### v0.18 --- 13/11/2026

**Tipo:** regra de substituição de cartas ativas.

**O que mudou:** - Quando a coleção está cheia, o jogador escolhe uma
carta das 3 ofertas e depois pode escolher uma carta ativa para
substituir. - A substituição é opcional; se recusá-la, a coleção
permanece igual e a nova carta não é ativada.

**Por que mudou:** - O responsável definiu como tratar a escolha de cartas
quando todos os espaços ativos estão ocupados.

**Impacto no projeto:** - O limite de coleção não é ultrapassado e o
jogador mantém controle sobre suas cartas ativas. A interface ainda será
implementada com o sistema de cartas.

**Seções atualizadas:** - Seções 1, 6.3, 19 e 21.

**Pendências criadas ou resolvidas:** - P-022 parcialmente resolvida;
comportamento de coleção cheia definido. Sorteio e persistência no fim da
partida continuam pendentes.

### v0.17 --- 13/11/2026

**Tipo:** definição das cartas temporárias da partida.

**O que mudou:** - Registrado que cada onda oferece 3 cartas sorteadas e
o jogador ativa 1 na coleção temporária. - A coleção comporta 6 cartas
ativas em contas padrão e 8 em Premium/VIP. - A biblioteca inicial terá
no mínimo 30 cartas distintas, com efeitos em atributos/habilidades e
raridade visível pela escala de 6 níveis existente.

**Por que mudou:** - O responsável definiu a escolha de melhorias por
cartas, limites ativos, tamanho mínimo da biblioteca e exibição de
raridade.

**Impacto no projeto:** - O sistema ainda não foi implementado. A regra
de Reset já remove as melhorias temporárias; a implementação futura deve
limpar também a coleção ativa. Probabilidades de raridade, repetições,
escolhas com coleção cheia e comportamento ao fim da partida continuam
em aberto.

**Seções atualizadas:** - Seções 1, 6.3, 12, 18, 19, 20 e 21.

**Pendências criadas ou resolvidas:** - Criada P-022, parcialmente
definida. Conteúdo do conjunto inicial (30 cartas) está especificado;
detalhes do sorteio e do limite ativo permanecem pendentes.

### v0.16 --- 13/11/2026

**Tipo:** preparação técnica do Reset.

**O que mudou:** - O modelo SQLite foi preparado para experiência,
fase/onda, Ouro, Pontos de Legado e melhorias temporárias. - Adicionada a
confirmação do Reset, disponível apenas a partir do nível 400; a rota
revalida o nível no servidor e transaciona a alteração. - O Reset mantém
a fase e o Ouro, volta à primeira onda da fase, retorna ao nível 1 com
experiência zero, incrementa o contador de Resets e remove melhorias
temporárias.

**Por que mudou:** - Aplicar as regras definidas pelo responsável e
preparar a integração com o sistema de progressão.

**Impacto no projeto:** - O protótipo atual não tem ganho de experiência,
combate, ondas ou chefes; portanto, ainda não é possível chegar ao nível
400 nem validar manualmente o Reset completo. A concessão de Pontos de
Legado permanece aguardando P-003.

**Seções atualizadas:** - Seções 1, 18.1 e 21.

**Pendências criadas ou resolvidas:** - Implementação do Reset iniciada
(parcial). A progressão e validação manual continuam pendentes.

### v0.15 --- 13/11/2026

**Tipo:** definição das regras centrais do Reset e da progressão por
fases.

**O que mudou:** - Definido que a progressão de fases é infinita e que
cada fase termina em chefe; derrotá-lo avança à fase seguinte. - No
Reset, o personagem volta ao nível 1 com experiência reiniciada, mantém
a fase atual e retorna à primeira onda dela; melhorias temporárias são
perdidas. - Ouro, equipamentos e demais itens persistentes permanecem
com o personagem. - Os Resets contribuem para Pontos de Legado usados na
Árvore de Talentos para atributos e vantagens permanentes.

**Por que mudou:** - O responsável definiu o comportamento do Reset, a
persistência do Ouro e o uso dos Pontos de Legado.

**Impacto no projeto:** - P-002 foi resolvida no nível de regras. A
implementação depende da base de experiência, níveis, fases, ondas e
chefes. Quantidade de ondas por fase permanece em P-004; fórmula e
quantidade dos Pontos de Legado permanecem em P-003.

**Seções atualizadas:** - Seções 1, 5, 7, 11, 18, 19, 20 e 21.

**Pendências criadas ou resolvidas:** - P-002 concluída. P-003 e P-004
continuam pendentes.

### v0.14 --- 13/11/2026

**Tipo:** validação do fluxo de troca de personagem e avanço do ponto de
retomada.

**O que mudou:** - Registrado que o responsável validou a tela de seleção
e o botão **Trocar Personagem**. - Atualizado o painel para iniciar a
definição das regras do Reset (P-002), preservando o que já está decidido
sobre persistência de itens.

**Por que mudou:** - O responsável confirmou o funcionamento e autorizou
seguir para a próxima etapa.

**Impacto no projeto:** - A próxima implementação de gameplay depende de
fechar as regras ainda pendentes do Reset.

**Seções atualizadas:** - Seções 1, 18.1 e 21.

**Pendências criadas ou resolvidas:** - Fluxo de troca validado. P-002
permanece pendente até a definição do comportamento de partida e do
benefício permanente.

### v0.13 --- 13/11/2026

**Tipo:** retorno à seleção de personagens a partir da sala.

**O que mudou:** - Adicionado o botão **Trocar Personagem** ao topo da
sala, com estilo alinhado à paleta. - O botão abre a seleção da conta sem
encerrar a sessão; outro personagem pode ser selecionado e iniciado pelo
botão **Jogar**.

**Por que mudou:** - O responsável solicitou uma forma de trocar de
personagem depois de entrar no jogo.

**Impacto no projeto:** - A rota existente de seleção mantém a sessão e
continua protegida pela autenticação. O responsável validou manualmente o
fluxo com troca de personagem.

**Seções atualizadas:** - Seções 1, 15.1, 18.1 e 21.

**Pendências criadas ou resolvidas:** - Implementado e validado pelo
responsável.

### v0.12 --- 13/11/2026

**Tipo:** atualização da interface de seleção de personagens.

**O que mudou:** - A tela foi reorganizada em três zonas sobre cenário
noturno. - A área central mostra uma prévia SVG grande com animação idle,
caixa translúcida com os dados do personagem e botão **Jogar**. - O painel
à direita lista slots verticais, destaca o ativo com Bronze `#B48A3E`,
exibe nível/classe/Resets, apresenta a criação em slot livre e posiciona
**Deletar** e **Voltar** na parte inferior. - O layout também se adapta a
telas estreitas.

**Por que mudou:** - Implementar a composição visual solicitada pelo
responsável, respeitando a paleta já aprovada no documento.

**Impacto no projeto:** - A seleção continua a usar o fluxo e os dados já
implementados. A prévia é provisória e aguarda avaliação visual no
navegador; não substitui a arte final das classes. **Voltar** encerra a
sessão e retorna à tela de acesso enquanto não há menu principal.

**Seções atualizadas:** - Seções 15.1, 18.1 e 21.

**Pendências criadas ou resolvidas:** - Layout visual implementado, falta
validação manual. P-021 permanece parcialmente pendente para arte final,
regras de nome e progressão.

### v0.11 --- 13/11/2026

**Tipo:** implementação do fluxo de personagens.

**O que mudou:** - Criadas rotas e armazenamento de personagens por conta.
- Após login, o jogador passa à tela de personagens; pode criar com nome
globalmente disponível, escolher uma das quatro classes, selecionar,
jogar e deletar. - Cartões exibem retrato provisório, nome, classe, nível
e quantidade de Resets. - Aplicados limites de 4 personagens padrão e 6
Premium/VIP. - Adicionada confirmação de exclusão com aviso diferente
quando se trata do último personagem. - Criado registro de Baú da Conta
que permanece com personagens ativos e é removido junto ao último.

**Por que mudou:** - Implementar o fluxo definido pelo responsável e
refletir as regras de limite e exclusão no protótipo.

**Impacto no projeto:** - O novo fluxo está implementado, mas aguarda
validação manual do responsável. - Os nomes são globalmente únicos como
premissa inicial; regras finais de nomes, arte de retrato e persistência
de nível/Resets permanecem pendentes.

**Seções atualizadas:** - Seções 1 (Controle do documento), 4.1
(Personagens), 10.2 (Baú), 12 (Premium/VIP), 15.1 (UI/UX), 18 (Etapas e
painel), 19 (Pendências), 20 (Decisões consolidadas) e 21 (Histórico).

**Pendências criadas ou resolvidas:** - P-021 parcialmente resolvida;
modelo e fluxo básico implementados. - Aguardando validação manual antes
de marcar a tarefa como concluída.

### v0.10 --- 13/11/2026

**Tipo:** definição de regras de personagens e autorização do próximo
fluxo de implementação.

**O que mudou:** - Definido limite de 4 personagens por conta padrão e 6
por conta Premium/VIP. - Definido o aviso e a perda de dados vinculados
ao deletar qualquer personagem. - Definido que o Baú da Conta permanece
com pelo menos um personagem ativo e é perdido ao deletar o último.
- Registrado que após login o jogador seleciona/cria personagem e usa
**Jogar** para entrar na sala. - Atualizada a próxima tarefa para
implementação do modelo e tela de personagens.

**Por que mudou:** - Incorporar as regras informadas pelo responsável e
deixar o fluxo pronto para implementação sem perder as decisões sobre
persistência da conta e do baú.

**Impacto no projeto:** - O cadastro/login passa a encaminhar para a tela
de personagens. - A conta permanece separada dos personagens; deletar o
último personagem remove o baú e os dados associados, após confirmação.
- O nome globalmente único é uma regra provisória do protótipo.

**Seções atualizadas:** - Seções 1 (Controle do documento), 4.1
(Personagens), 10.2 (Baú), 12 (Premium/VIP), 15.1 (UI/UX), 18 (Etapas e
painel), 19 (Pendências), 20 (Decisões consolidadas) e 21 (Histórico).

**Pendências criadas ou resolvidas:** - P-021 parcialmente resolvida;
limite e regra de exclusão definidos. - Permanecem pendentes nomes,
persistência de nível/Resets, arte dos retratos, troca de classe e
expiração Premium/VIP.

### v0.9 --- 13/11/2026

**Tipo:** registro de proposta de seleção e gestão de personagens.

**O que mudou:** - Registrada a proposta de mostrar a seleção de
personagens após o login. - Incluídos os fluxos de criar, selecionar,
jogar e deletar, e os dados do cartão: retrato, nome, classe, nível e
quantidade de Resets. - Reconfirmado que o Baú da Conta é compartilhado
entre personagens. - Criada a pendência P-021 para limites, nomes,
exclusão e persistência.

**Por que mudou:** - Registrar a ideia do responsável e separar os
detalhes que precisam ser definidos antes de implementar um fluxo que
cria e exclui dados persistentes.

**Impacto no projeto:** - A tela proposta passa a ser o próximo item de
planejamento. - A exclusão deve respeitar a regra existente de persistência
de equipamentos, Ouro e joias. - Nenhum código de personagens foi
implementado nesta atualização.

**Seções atualizadas:** - Seções 1 (Controle do documento), 4.1
(Seleção e criação), 15.1 (UI/UX), 18 (Etapas e painel), 19 (Pendências)
e 21 (Histórico de versões).

**Pendências criadas ou resolvidas:** - P-021 criada. - P-001 continua
resolvida; P-002 permanece pendente para a etapa seguinte.

### v0.8 --- 13/11/2026

**Tipo:** validação de funcionalidades e definição das classes iniciais.

**O que mudou:** - Registrado que o responsável testou e aprovou cadastro,
login, logout, bloqueio de `/jogo` sem sessão e movimentação. - Definidas
quatro classes iniciais: Guardião do Umbral, Tecelão de Cinzas, Vigia do
Ermo e Lâmina Rúnica, baseadas nos arquétipos solicitados pelo
responsável. - Atualizado o painel para indicar P-002 (Reset) como próxima
decisão.

**Por que mudou:** - Incorporar o resultado dos testes do responsável e
registrar os arquétipos e nomes das classes autorizados por ele.

**Impacto no projeto:** - P-001 foi concluída. - A implementação de
classes no jogo permanece pendente; atributos e habilidades continuam
sem definição.

**Seções atualizadas:** - Seções 1 (Controle do documento), 4 (Classes),
18 (Escopo e painel), 19 (Pendências), 20 (Decisões consolidadas) e 21
(Histórico de versões).

**Pendências criadas ou resolvidas:** - P-001 resolvida. - P-002 passa a
ser a próxima decisão de projeto.

### v0.7 --- 13/11/2026

**Tipo:** validação de protótipo e preparação da próxima decisão.

**O que mudou:** - Registrado que o responsável testou e aprovou o fluxo
de cadastro, login e movimentação. - Marcadas essas entregas como
concluídas no roteiro. - Mantidos logout e proteção de `/jogo` sem sessão
como implementados, mas ainda sem confirmação. - Adicionada à Seção 4
uma proposta de quatro classes iniciais, claramente identificada como
não aprovada. - Atualizado o ponto de retomada para a decisão P-001.

**Por que mudou:** - Refletir o teste feito pelo responsável e preparar
uma proposta concreta para a primeira pendência de definição do jogo,
sem transformar a proposta em decisão oficial.

**Impacto no projeto:** - A próxima decisão é aprovar ou revisar os nomes
e arquétipos propostos para as classes. - Nenhuma classe deve ser
implementada antes dessa aprovação.

**Seções atualizadas:** - Seções 1 (Controle do documento), 4 (Classes),
18 (Escopo e painel), 19 (Pendências) e 21 (Histórico de versões).

**Pendências criadas ou resolvidas:** - P-001 recebeu uma proposta e
aguarda decisão do responsável. - Nenhuma pendência foi encerrada.

### v0.6 --- 13/11/2026

**Tipo:** expansão do acompanhamento e do processo de continuidade.

**O que mudou:** - Criado o painel de andamento da Seção 18.1 com itens
implementados, em andamento, não validados e próximos passos. - Adicionada
uma legenda uniforme para os estados das tarefas. - Registrado que a
correção e reorganização recentes ainda precisam ser iniciadas e
validadas. - Definido que cada sessão de trabalho deve deixar atualizado
o ponto de retomada.

**Por que mudou:** - Manter uma visão clara do que já foi feito, do que
falta, do que está em curso e da próxima ação, permitindo retomar o
projeto sem reconstruir o contexto pelas conversas.

**Impacto no projeto:** - O painel da Seção 18.1 passa a ser o resumo
operacional prioritário; a Seção 19 continua sendo a lista oficial de
decisões pendentes.

**Seções atualizadas:** - Seções 1.1 (Uso do documento), 18 (Escopo por
etapas), 18.1 (Painel de andamento), 21 (Histórico de versões) e 23
(Instrução permanente).

**Pendências criadas ou resolvidas:** - Nenhuma decisão P-001 a P-020 foi
fechada. - Foi explicitado o próximo passo de validação manual no painel.

### v0.5 --- 12/11/2026

**Tipo:** correção e organização da estrutura do projeto.

**O que mudou:** - Corrigido o erro de indentação que impedia o servidor
Flask de iniciar. - Separado o código em módulos para autenticação,
banco de dados, segurança e rotas do jogo. - Movidos templates e arquivos
estáticos para pastas próprias. - Atualizado o README com a estrutura e
as instruções de execução.

**Por que mudou:** - Corrigir o erro reportado e facilitar manutenção,
localização de funcionalidades e futuras atualizações.

**Impacto no projeto:** - O ponto de entrada permanece `app.py`; as
funcionalidades agora vivem em `game_app/`. - O banco e a chave de sessão
locais são criados em `game_app/instance/`.

**Seções atualizadas:** - Seções 1 (Controle do documento) e 21
(Histórico de versões).

**Pendências criadas ou resolvidas:** - Nenhuma pendência de gameplay ou
arquitetura para produção foi fechada.

### v0.4 --- 12/11/2026

**Tipo:** expansão do protótipo e início da autenticação.

**O que mudou:** - Criada uma página inicial com formulários de login e
cadastro. - Adicionado servidor Flask com rotas de autenticação e acesso
à sala protegido por sessão. - Criado armazenamento local SQLite para
usuários; senhas são armazenadas usando hash. - Adicionadas validação
básica, tokens CSRF, opção de sair e arquivos de execução/dependências.

**Por que mudou:** - O responsável definiu que o usuário deve entrar ou
criar uma conta antes de acessar o jogo.

**Impacto no projeto:** - A sala de movimentação agora é servida em
`/jogo` somente após autenticação. - SQLite é usado apenas como escolha
provisória deste protótipo. - A implementação não resolve ainda
recuperação de senha, proteção contra tentativas automatizadas,
permissões ou requisitos de produção.

**Seções atualizadas:** - Seções 1 (Controle do documento), 16.3
(Banco de dados), 16.5 (Segurança e integridade), 18 (Escopo por etapas)
e 21 (Histórico de versões).

**Pendências criadas ou resolvidas:** - P-009 permanece pendente; a
autenticação e o modelo final de contas também continuam pendentes para
produção.

### v0.3 --- 12/11/2026

**Tipo:** autorização de implementação e início de protótipo.

**O que mudou:** - O responsável autorizou explicitamente o início do
desenvolvimento nesta conversa. - Criado um protótipo de navegador com
uma sala visual de teste, movimentação por teclado e câmera que acompanha
o personagem. - Canvas 2D foi usado como escolha técnica provisória do
protótipo.

**Por que mudou:** - Iniciar a etapa prática do projeto com o primeiro
item previsto no escopo do protótipo, preservando como pendentes as
decisões de gameplay que ainda não foram aprovadas.

**Impacto no projeto:** - A Etapa 3 está em andamento. - A escolha entre
Canvas e WebGL para o jogo continua pendente; a implementação atual não
fecha essa decisão. - Não foram definidos classe, combate, inimigos,
ondas ou balanceamento.

**Seções atualizadas:** - Seção 1 (Controle do documento), Seção 18
(Escopo por etapas) e Seção 21 (Histórico de versões).

**Pendências criadas ou resolvidas:** - Nenhuma pendência P-001 a P-020
foi fechada.

### v0.2 --- 12/11/2026

**Tipo:** nova decisão e expansão de UI/UX.

**O que mudou:** - Adicionada a tabela oficial de **6 níveis de raridade e cores de borda** (Comum, Incomum/Mágico, Raro, Excelente, Épico/Ancestral e Lendário/Mítico) aplicável a todos os itens (armaduras, armas, asas, anéis, colares/pendentes, joias e consumíveis). - Definida a separação visual entre a **borda externa do slot** (indica raridade) e o **brilho interno / aura sobre o ícone** (indica nível de aprimoramento `+0` a `+11+`). - Atualizada a paleta de cores na Seção 14.2 e as regras de slots/tooltips na Seção 15.2.

**Por que mudou:** - Evitar ambiguidade visual entre a raridade base de um item e seu nível de aprimoramento, garantindo leitura rápida no inventário, baú e drops no chão.

**Impacto no projeto:** - Padroniza o design de interface (Tailwind CSS) de todos os slots de equipamentos, mochila, baú, loja, forja e janela de trade.

**Seções atualizadas:** - Seção 1 (Controle do documento), Seção 8 (Itens, equipamentos, raridades e aprimoramentos), Seção 14.2 (Paleta de cores), Seção 15.2 (Slots e tooltips), Seção 18 (Etapa 1) e Seção 20 (Decisões consolidadas).

**Pendências criadas ou resolvidas:** - Nenhuma pendência da tabela P-001 a P-020 foi fechada; nova diretriz visual incorporada como **Definido**.

### v0.1 --- 12/11/2026

**Tipo:** consolidação inicial do planejamento.

**O que foi feito:** - Reunidas as ideias enviadas em uma estrutura
única. - Removidas repetições sobre Reset, ondas, itens persistentes,
inventário, direção de arte e tecnologias. - Separadas decisões já
informadas de propostas e assuntos ainda pendentes. - Organizados os
sistemas em seções para facilitar futuras atualizações. - Criada uma
lista de pendências identificadas. - Criado um roteiro inicial de etapas
do projeto.

**Por que foi feito:** - Evitar que informações importantes fiquem
espalhadas em conversas. - Reduzir contradições e repetição de
contexto. - Permitir que futuras conversas consultem este documento como
referência central. - Evitar que uma IA trate ideias ainda não aprovadas
como funcionalidades confirmadas.

**O que não foi feito:** - Nenhum código foi implementado. - Nenhum
banco de dados foi criado. - Nenhuma arte ou sprite foi produzido. -
Nenhuma decisão pendente foi tomada em nome do responsável pelo projeto.

------------------------------------------------------------------------

## 22. Modelo para próximas atualizações

Sempre que uma nova decisão for tomada, registrar neste formato:

### vX.Y --- DD/MM/AAAA

**Tipo:** nova decisão / correção / expansão / remoção.

**O que mudou:** - Descrever objetivamente a alteração.

**Por que mudou:** - Registrar o motivo da decisão.

**Impacto no projeto:** - Informar quais sistemas, regras ou etapas
foram afetados.

**Seções atualizadas:** - Listar as seções alteradas.

**Pendências criadas ou resolvidas:** - Informar os IDs correspondentes.

------------------------------------------------------------------------

## 23. Instrução permanente para futuras sessões

Antes de continuar o projeto, consultar a versão mais recente deste
Documento Mestre.

Ao final de cada sessão de trabalho, atualizar a Seção 18.1 para registrar
o que foi concluído, o que continua em andamento, o que falta, se a
implementação foi validada e qual é a próxima ação concreta. Só marcar
uma tarefa como `[x]` quando estiver concluída e validada; usar `[~]`
para código implementado ou trabalho em andamento que ainda precise de
validação ou conclusão. Manter o histórico de versões atualizado quando
o estado do projeto ou uma decisão mudar.

Ao receber uma nova ideia: 1. Verificar se ela já existe no documento.
2. Se já existir, complementar ou corrigir sem duplicar. 3. Se for nova,
identificar a seção correta. 4. Se houver conflito, explicar o conflito
e pedir decisão antes de substituir uma regra definida. 5. Atualizar a
seção correspondente. 6. Atualizar o histórico de versões e a lista de
pendências, quando aplicável. 7. Entregar a versão completa e atualizada
do arquivo `.md` quando for solicitada uma atualização do documento.

**Este documento representa o estado atual do planejamento, não uma
autorização automática para iniciar a implementação.**



### v0.28 --- 13/11/2026

Iniciado o combate básico: inimigos persistidos por personagem/onda, colisão local para impedir atravessá-los, ataque por Espaço e concessão provisória de 35 EXP por derrota. Vida 100 e dano 35 são parâmetros de teste. Convivência/colisão entre jogadores permanece sem implementação porque o protótipo ainda não possui salas de partida/multiplayer (Etapa 5). A primeira parte aguarda validação manual.



### v0.29 --- 13/11/2026

Avanço automático de onda após derrotar o último inimigo via Socket.IO; inimigos seguintes são carregados sem recarregar a página. Removido o botão de conclusão manual. A transição aguarda validação do responsável. Valores de combate e XP continuam provisórios. Colisão entre jogadores permanece futura, condicionada ao multiplayer.\r\n


### v0.30 --- 13/11/2026

Corrigida a inicialização de inimigos: a sala verifica inimigos vivos, não apenas registros existentes, e restaura o grupo da onda atual se todos estiverem derrotados mas a onda não tiver avançado. Assim, reiniciar o servidor não deixa uma onda vazia. Compilação Python aprovada; validar no navegador.



### v0.31 --- 13/11/2026

A coleta Socket.IO de orbes agora é idempotente: requisições simultâneas para um orbe já coletado retornam sucesso silencioso, evitando aviso vermelho em abas/eventos concorrentes. Compilação Python aprovada; aguarda validação manual.



### v0.32 --- 13/11/2026

HUD provisória de Vida/Mana e barra de duas habilidades do guerreiro adicionadas. Ataque básico e habilidades usam Socket.IO; servidor valida mana e cooldown. Dano causado aparece sobre inimigos e contato com inimigos reduz Vida e mostra dano recebido. Valores de combate são provisórios e aguarda validação manual.



### v0.33 --- 13/11/2026

Corrigida a HUD de Vida/Mana: as larguras das barras agora são renderizadas a partir dos valores persistidos do personagem, em vez de iniciar visualmente em 100%. A persistência no servidor já existia; após recarga, a apresentação estava incorreta. Compilação Python e templates verificados.



### v0.34 --- 13/11/2026

Regras registradas: Vida zerada retorna o personagem à onda 1 mantendo a fase; monstro deve mostrar nome e nível; mudança de onda/fase recebe destaque central; capítulos narrativos a cada 10 fases, com história específica por classe; missões, conquistas e bestiário de eliminações; autopotion de Vida/Mana posicionadas nas laterais da barra de combate. Histórias, missões, conquistas e bestiário ficam planejados para implementação futura. Autopotões estão representadas visualmente como controles de protótipo.


### v0.35 --- 13/11/2026

**Tipo:** controle de direção por mouse no combate.

**O que mudou:** o personagem agora gira para acompanhar o cursor; ataques
e habilidades selecionam um inimigo próximo alinhado à mira. WASD e setas
continuam movimentando o personagem. Os textos de controle foram
atualizados.

**Por que mudou:** o responsável definiu que o personagem deve olhar para
onde o jogador aponta e usar habilidades nessa direção.

**Impacto no projeto:** implementado no cliente do protótipo. O ataque
continua emitido ao servidor por Socket.IO; alcance e seleção direcional
são parâmetros provisórios do cliente.

**Seções atualizadas:** Seções 1, 15.4, 18.1 e 21.

**Pendências:** validar visualmente a direção e a seleção dos ataques no
navegador.


### v0.36 --- 13/11/2026

**Tipo:** atualização dos controles do combate.

**O que mudou:** botão esquerdo do mouse executa o ataque básico; botão
direito usa Corte Rúnico. Impacto do Umbral, a terceira ação de combate
da barra, foi removido. Movimento continua em WASD/setas e o mouse mantém
a mira.

**Por que mudou:** o responsável definiu os botões do mouse como controles
de ataque e pediu a remoção da terceira habilidade.

**Impacto no projeto:** controles aplicados na sala de combate; poções
continuam representadas na interface. Aguarda validação manual.

**Seções atualizadas:** Seções 1, 15.4, 18.1 e 21.

**Pendências:** validar os dois botões do mouse e confirmar a remoção da
terceira ação no navegador.


### v0.37 --- 13/11/2026

**Tipo:** avanço rápido direcional (dash).

**O que mudou:** Espaço inicia um dash na direção da mira, com duração
inicial de 0,2 s, velocidade de 720 unidades/s e recarga de 1,2 s. O dash
para ao colidir com um inimigo, mantém os limites do cenário e mostra a
recarga no HUD. Os controles da tela foram atualizados.

**Por que mudou:** o responsável pediu que Espaço avance na direção para
onde o mouse estiver apontando.

**Impacto no projeto:** movimento do dash é local no cliente, seguindo o
modelo provisório da movimentação atual. Os parâmetros são ajustáveis e
aguardam validação manual.

**Seções atualizadas:** Seções 1, 15.4, 18.1 e 21.

**Pendências:** validar direção, bloqueio por colisão e sensação do dash no
navegador; ajustar duração/velocidade/recarga após o teste.


### v0.38 --- 13/11/2026

**Tipo:** transições de ondas e apresentação de chefes.

**O que mudou:** ao carregar a onda final, o servidor prepara um chefe
individual com vida/recompensa próprias; a mesma regra vale ao abrir a sala
diretamente nessa onda. O cliente destaca a nova onda ou chefe no centro,
atualiza a apresentação do chefe e mantém nome/nível dos inimigos após as
transições Socket.IO. Mudanças de fase exibem o início da nova fase; a cada
10 fases, um destaque genérico de capítulo aparece, sem história específica
implementada ainda.

**Por que mudou:** o Documento Mestre já previa destaque ao iniciar ondas,
chefes na última onda e capítulos a cada 10 fases. Este é o próximo ponto
de implementação após a validação dos controles de combate.

**Impacto no projeto:** transições continuam em tempo real via Socket.IO.
IA de perseguição e ataque dos monstros ainda está pendente. A validação
manual deste fluxo permanece aberta.

**Seções atualizadas:** Seções 1, 18, 18.1 e 21.

**Pendências:** validar a transição e a onda de chefe no navegador; depois
implementar IA dos inimigos.


### v0.39 --- 13/11/2026

**Tipo:** exibição única da introdução de capítulo.

**O que mudou:** introduções de capítulo agora aparecem na faixa narrativa
superior da sala somente uma vez por personagem/capítulo, com o registro
guardado no navegador. A faixa desaparece após a apresentação. As transições
de onda deixam de repetir o capítulo e mostram fase/onda ou chefe no destaque
central; quando começa um novo capítulo, sua introdução aparece primeiro e
depois surge a fase/onda.

**Por que mudou:** o responsável relatou que o capítulo estava reaparecendo
durante as ondas e pediu que fosse mostrado apenas uma vez na área indicada
na imagem.

**Impacto no projeto:** o registro de exibição é local ao navegador; histórias
específicas por classe ainda serão produzidas em etapa futura.

**Seções atualizadas:** Seções 1, 15.4, 18.1 e 21.

**Pendências:** validar visualmente o ciclo capítulo → fase/onda e as
transições de chefe.


### v0.40 --- 13/11/2026

**Tipo:** recuperação de Vida e Mana ao morrer.

**O que mudou:** a morte restaura Vida e Mana aos valores máximos, persiste
ambos no banco e envia os valores no evento Socket.IO. O cliente atualiza
as duas barras imediatamente ao receber a morte; a fase é mantida e a onda
volta para 1.

**Por que mudou:** o responsável definiu que Vida e Mana devem voltar
completas quando o personagem morrer.

**Impacto no projeto:** restauração fica no servidor e sobrevive a recargas
da página. A regra de encerramento definitivo e recompensa da partida segue
pendente em P-003/P-019.

**Seções atualizadas:** Seções 1, 7.2, 18.1 e 21.

**Pendências:** validar manualmente as barras de Vida/Mana e a persistência
após a morte.


### v0.41 --- 13/11/2026

**Tipo:** primeira IA de perseguição e ataque dos monstros.

**O que mudou:** inimigos vivos perseguem o personagem no cenário, mantêm
colisão com o personagem e entre si, e causam dano ao alcançar distância de
contato. O cliente regula as solicitações e o servidor também aplica uma
recarga por personagem, verifica que há inimigos ativos, persiste Vida/Mana
e transmite o resultado via Socket.IO. Fluxos de capítulo/onda/chefe e morte
foram marcados como validados após confirmação do responsável.

**Por que mudou:** após confirmar a etapa anterior, o responsável pediu
para avançar ao próximo item pendente do Documento Mestre: IA dos monstros.

**Impacto no projeto:** a movimentação dos inimigos é local no cliente neste
protótipo individual; a aplicação de dano e os atributos de Vida/Mana são
servidor/sessão persistidos. Sincronização de movimento entre jogadores
depende da futura implementação de salas multiplayer.

**Seções atualizadas:** Seções 1, 18, 18.1 e 21.

**Pendências:** validar perseguição, colisão, frequência/dano de contato e
persistência após a morte; balancear os parâmetros antes de ampliar a IA.


### v0.42 --- 13/11/2026

**Tipo:** recuperação de Vida/Mana ao iniciar uma fase.

**O que mudou:** derrotar o chefe e avançar para uma fase nova restaura
Vida e Mana máximas no banco e atualiza ambas as barras em tempo real. O
avanço entre ondas normais mantém os valores atuais. O fluxo simulado de
conclusão de onda segue a mesma regra.

**Por que mudou:** o responsável pediu que recursos sejam restaurados ao
iniciar uma fase, mas somente ao iniciar fase ou após morrer.

**Impacto no projeto:** a restauração ocorre no servidor tanto no combate
real quanto no fluxo simulado; a recuperação por morte permanece igual.

**Seções atualizadas:** Seções 1, 7.2, 18.1 e 21.

**Pendências:** validar fase nova com Vida/Mana reduzidas e confirmar que
uma onda comum não restaura os valores.


### v0.43 --- 13/11/2026

**Tipo:** controles contínuos, preparação de fase e informações de combate.

**O que mudou:** a sala impede seleção/arraste de texto; manter os botões
do mouse repete ataques dentro das recargas e manter Espaço repete o dash
quando disponível. Ataque básico ganhou recarga curta de 0,45 s, aplicada
no cliente e servidor. O HUD mostra a contagem de monstros restantes. Ao
começar fase nova após chefe, inicia uma preparação de 30 segundos,
persistida no banco, durante a qual os monstros não se movem nem podem
causar dano.

**Por que mudou:** o responsável pediu correções de interação, ataques
contínuos e tempo para preparar a próxima fase, além da contagem de inimigos.

**Impacto no projeto:** movimentos/contagem atualizam no cliente; servidor
valida recarga de ataques, bloqueia dano durante a preparação e persiste o
fim do intervalo. O painel avançado do chefe e o hub de capítulo não estão
implementados, pois dependem de regras/conteúdo e dos sistemas de
Inventário/Baú.

**Seções atualizadas:** Seções 1, 7.2, 15.4, 18, 18.1, 19, 20 e 21.

**Pendências:** validar controles segurados, cooldown básico, contador e
preparação. P-025 registra painel/estados do chefe; P-026 registra pausa e
hub ao fim de capítulo.


### v0.44 --- 13/11/2026

**Tipo:** contenção de gravações concorrentes do SQLite.

**O que mudou:** SQLite agora usa journal WAL e `busy_timeout` de 15 s.
Os eventos Socket.IO que iniciam transações usam um helper que converte uma
contenção persistente em retorno controlado ao cliente. O cliente permite
apenas um ataque em andamento por vez para evitar rajadas sobrepostas ao
segurar o mouse.

**Por que mudou:** foi relatado `sqlite3.OperationalError: database is
locked` no início de `attack_enemy`, durante gravações em paralelo no modo
threading do Socket.IO. O padrão anterior deixava o timeout no valor padrão
e não tratava a falha de início de transação.

**Impacto no projeto:** transações continuam protegidas por `BEGIN IMMEDIATE`;
WAL e espera de bloqueio reduzem conflitos entre leitores/escritores. Se a
contenção superar 15 s, o evento responde com erro em vez de propagar
traceback. Gravações de múltiplos processos continuam limitadas pelo SQLite.

**Seções atualizadas:** Seções 1, 16, 18, 18.1 e 21.

**Pendências:** validar ataques segurados e coleta simultânea de orbes no
navegador; observar se o erro reaparece sob uso contínuo.


### v0.45 --- 13/11/2026

**Tipo:** preparação de fase, coleta de cartas e IA dos monstros.

**O que mudou:** orbes agora podem ser coletados durante os 30 segundos de
preparação, e cartas liberadas pela experiência podem ser escolhidas ali.
O painel de preparação oferece acesso direto à árvore de Talentos. O dano
por contato passou a usar recarga individual por monstro, com validação do
ID do inimigo no servidor. A IA agora busca ângulos alternativos e tenta
contornar aliados que bloqueiam sua aproximação.

**Por que mudou:** a preparação bloqueava também a coleta de orbes, deixando
cartas disponíveis somente depois do cronômetro. Além disso, uma única
recarga global limitava o ataque de toda a horda; os inimigos também paravam
ao colidir entre si e acumulavam-se em fila.

**Impacto no projeto:** cartas e talentos podem ser preparados sem atualizar
a página. Cada contato é conferido contra um inimigo vivo da fase/onda atual.
Inventário, Baú, atributos e configuração de habilidades ainda não existem;
quando implementados, estarão disponíveis na preparação conforme P-026.

**Seções atualizadas:** Seções 7.2, 15.4, 18, 18.1, 19 e 21.

**Pendências:** validar manualmente coleta e escolha de carta durante a
preparação, além de observar se vários inimigos conseguem contornar aliados
e causar dano sem ficarem agrupados. P-027 registra a validação da IA.


### v0.46 --- 13/11/2026

**Tipo:** cooldowns por Agilidade, sala de espera, morte, transição de fase e estrutura
de ondas.

**O que mudou:** ataque básico (1 s), Corte Rúnico (6 s) e Avanço (3 s)
começam com recargas mais longas e Agilidade reduz o tempo. A seleção de
personagem agora leva à Sala de Espera-base. A morte pausa a sala e oferece reiniciar
a fase ou ir à Sala de Espera. Após a onda 10, o jogador escolhe entre sala de espera e
próxima fase; a coleção temporária é apagada. Cada fase passa a ter 10 ondas,
com semichefe na 9 e chefe na 10.

**Por que mudou:** o responsável pediu recargas iniciais mais deliberadas,
decisão de recuperação após morte, uma sala de espera antes do combate e
uma estrutura de fase mais longa com dois encontros especiais.

**Impacto no projeto:** cooldowns são validados no servidor para ataques e
Avanço. A tela-base da Sala de Espera mostra o personagem, três espaços de grupo e
atalho para Talentos; convites, amigos, cooperação, Inventário, Baú, Máquina
do Caos e trade continuam pendentes. A distribuição comum de pontos em
Agilidade também continua pendente; talentos de Agilidade já modificam as
recargas.

**Seções atualizadas:** Seções 1, 5, 7.2, 13, 15.4, 18, 18.1, 19, 20 e 21.

**Pendências:** validar manualmente os fluxos de morte, sala de espera, chefe, ondas 9
e 10, limpeza das cartas e efeito de Agilidade. P-028 reúne os recursos
sociais e serviços ainda não implementados.


### v0.47 --- 13/11/2026

**Tipo:** correção de transição de ondas e padronização de idioma.

**O que mudou:** ao criar a próxima onda, registros antigos de inimigos
agora são atualizados e reativados com vida cheia antes de o servidor
notificar o cliente. O nome da área foi padronizado como “Sala de Espera”
nos textos visíveis do jogo.

**Por que mudou:** algumas ondas existentes no banco continuavam marcadas
como derrotadas quando eram alcançadas novamente. O cliente recebia a
contagem da nova onda, mas seus monstros só voltavam após recarregar a sala.
Também foi pedido que toda a interface do jogo permaneça em português.

**Impacto no projeto:** a transição Socket.IO atualiza a posição, vida,
vida máxima, estado ativo e recompensa dos inimigos reaproveitados; a
quantidade enviada corresponde à horda reativada. Nomes internos de funções
e arquivos podem permanecer em inglês como identificadores do código.

**Seções atualizadas:** Seções 1, 18, 18.1 e 21.

**Pendências:** validar manualmente várias transições de ondas sem atualizar
a página e confirmar a tradução da interface no navegador.


### v0.48 --- 13/11/2026

**Tipo:** rolagem da Sala de Espera e localização da rota.

**O que mudou:** a página permite rolagem vertical no documento inteiro,
incluindo a raiz HTML, para alcançar o conteúdo abaixo da área visível. A
rota pública passou de `/lobby` para `/sala-de-espera`, e o envio de início
de partida passou para `/sala-de-espera/iniciar`.

**Por que mudou:** as regras globais mantinham a rolagem da página bloqueada
mesmo quando o conteúdo excedia a altura da tela. Também foi solicitado que
a URL visível da sala de espera estivesse em português.

**Impacto no projeto:** links gerados por `url_for` acompanham as rotas
atualizadas; os nomes Python internos permanecem estáveis.

**Seções atualizadas:** Seções 1, 13 e 21.

**Pendências:** conferir a rolagem e a URL em resoluções menores no navegador.


### v0.49 --- 13/11/2026

**Tipo:** posição e apresentação visual dos orbes de EXP de cartas.

**O que mudou:** orbes de EXP agora aparecem na posição em que o monstro
morre, usando a posição atual enviada pelo cliente no golpe final e salva
no estado do inimigo/orbe. Removidos os orbes artificiais em coordenadas
fixas que eram gerados ao concluir ondas de teste, e limpos os registros
antigos desses drops simulados. O desenho agora tem uma aura mais intensa e
difusa, brilhos ao redor e núcleo branco/dourado maior, com pulsação suave.

**Por que mudou:** o responsável pediu que o drop acompanhasse a morte real
do monstro e que a luz fosse intensa, respirasse suavemente e deixasse o
núcleo claramente visível.

**Impacto no projeto:** o cliente envia a posição atual do inimigo no ataque;
quando derrotado, o servidor persiste essa posição e transmite o orbe via
Socket.IO. A pulsação é desenhada no Canvas sem recarregar a página.

**Seções atualizadas:** Seções 1, 6.3, 18, 18.1 e 21.

**Pendências:** validar no navegador a posição de drops em monstros que se
movem e a legibilidade do núcleo/brilho em diferentes fundos do cenário.


### v0.50 --- 13/11/2026

**Tipo:** reorganização visual da Sala de Espera.

**O que mudou:** a tela agora apresenta cabeçalho com identidade do jogo e
atalho para trocar personagem, chamada de preparação, coluna do grupo com
três slots e painel de chat, e coluna de personagem/progresso, serviços e
botão principal de partida. O personagem local recebe um retrato Canvas
provisório com paleta por classe. A Árvore de Talentos continua acessível;
os serviços ainda não implementados estão identificados.

**Por que mudou:** aproximar a sala do layout de referência solicitado,
reservando a área para formar grupo e conversar sem esconder o progresso
do personagem e os acessos de preparação.

**Impacto no projeto:** novos estilos responsivos da sala ficam agrupados
em `styles.css`, e o retrato de classe é desenhado por `static/js/lobby.js`.
O painel de chat e os espaços de amigos são apenas apresentação: salas,
convites e mensagens Socket.IO dependem da implementação futura de grupo.

**Seções atualizadas:** Seções 1, 13.1, 18 e 21; README.

**Pendências:** validar visualmente em desktop e celular; implementar grupo,
convites e chat Socket.IO quando a etapa de multiplayer social for iniciada.


### v0.51 --- 13/11/2026

**Tipo:** ajustes de grupo e preparação na Sala de Espera.

**O que mudou:** o botão de início agora diz **Começar!** e aparece ao lado
da caixa de busca, com maior peso visual. O cartão com retrato do personagem
mostra também seus resets. Os slots vazios abrem um seletor de amigos; foi
adicionado o painel de lista com contador e área rolável preparada para
mostrar cinco amigos por vez.

**Por que mudou:** melhorar a hierarquia visual do início solo e preparar a
interface para encontrar perfis e convidar amigos tanto pelos espaços do
grupo quanto pela lista.

**Impacto no projeto:** a interface apresenta esses caminhos, mas busca,
lista persistida e envio de convites estão desabilitados porque a camada
social ainda não foi implementada. A tela não inventa amigos: exibe zero até
existirem registros reais.

**Seções atualizadas:** Seções 1, 13.1, 18 e 21; README.

**Pendências:** definir e implementar amizades/perfis, convites de sala,
presença online e integração com grupos Socket.IO.


### v0.52 --- 13/11/2026

**Tipo:** refinamento de hierarquia e distribuição da Sala de Espera.

**O que mudou:** busca de perfil foi movida para a barra superior e reduzida
para um campo fino. A lista social foi movida para a coluna direita, abaixo
dos serviços. Removido o painel de personagem selecionado que repetia nome,
classe, nível e resets já visíveis no cartão do grupo. O progresso de fase e
onda permanece junto ao título do grupo. **Começar!** fica alinhado no canto
inferior do painel, com largura controlada e sem ultrapassar seus limites.

**Por que mudou:** reduzir repetição de informações e organizar melhor o
espaço, conforme a referência visual fornecida.

**Impacto no projeto:** somente apresentação e CSS responsivo foram alterados;
busca e lista social continuam desabilitadas até existir a camada de amizades.

**Seções atualizadas:** Seções 1, 13.1, 18 e 21; README.

**Pendências:** implementar busca de perfis, amizades, convites e presença.


### v0.53 --- 13/11/2026

**Tipo:** compactação do painel de grupo para ampliar o Chat da Sala.

**O que mudou:** o aviso de fase concluída ou de retomada após derrota agora
fica na mesma linha do botão **Começar!**; em telas estreitas, ele se ajusta
acima do botão.

**Por que mudou:** reduzir a altura ocupada pelo painel do grupo e liberar
mais espaço vertical para a área de chat.

**Impacto no projeto:** mudança responsiva de layout, sem alteração no fluxo
de progressão ou no envio do formulário.

**Seções atualizadas:** Seções 1, 13.1 e 21; README.

**Pendências:** validar a composição visual em telas largas e estreitas.


### v0.54 --- 13/11/2026

**Tipo:** consolidação das regras de Reset, preparação e interface do jogo.

**O que mudou:** cada Reset agora concede 1 Ponto de Legado, implementado
junto à atualização do personagem. Na preparação da fase, foi removido o
atalho para Talentos da caixa de contagem regressiva. A mensagem técnica
sobre remoção de cartas ao fim da fase foi substituída por uma orientação
voltada ao jogador. A busca na Sala de Espera passou a usar o texto
“Buscar perfil de jogador”. O aviso de fase concluída/retomada ocupa a
mesma linha do botão **Começar!** em telas largas e fica acima dele em telas
estreitas.

**Decisões e pendências:** o responsável adiou o balanceamento de atributos,
efeitos e limites de nível da Árvore de Talentos até a etapa de balanceamento
do personagem, para que ambos sejam feitos juntos. A redistribuição será
gratuita para VIP e custará Ouro para contas comuns; o valor do custo ainda
precisa ser definido. Busca de perfis, lista de amigos e convites continuam
sem backend.

**Próxima etapa:** iniciar P-025, especificando e implementando a apresentação
de elemento/resistências do chefe e estados (quebra de escudo, sangramento,
paralisia e queimadura), com parâmetros provisórios sujeitos a balanceamento.

**Seções atualizadas:** Seções 1, 6.2, 7, 13.1, 18, 19 e 21; README.


### v0.55 --- 13/11/2026 — Consolidação de andamento

Este registro consolida alterações feitas após a v0.53 e corrige o ponto de
retomada para refletir as decisões mais recentes do responsável.

**Implementado desde a v0.53:**

-   Cada Reset concede 1 Ponto de Legado, salvo junto ao Reset e informado
    ao jogador.
-   Removido o atalho de Talentos da caixa de contagem regressiva de fase.
-   A mensagem de conclusão foi reescrita para o jogador, sem detalhes
    técnicos sobre limpeza de cartas.
-   Na Sala de Espera, a busca diz “Buscar perfil de jogador” e o aviso de
    fase concluída/retomada fica junto ao botão Começar. Busca, lista social
    e convites ainda não têm backend.

**Decisões confirmadas, ainda sem implementação completa:**

-   Redistribuição de talentos grátis para VIP; contas comuns pagarão Ouro.
    O custo ainda precisa ser definido.
-   A árvore poderá ter níveis múltiplos por talento, mas efeitos e limites
    serão definidos junto ao balanceamento dos atributos do personagem.
-   O responsável adiou esse balanceamento conjunto; não inventar bônus ou
    limites provisórios para os talentos antes dessa etapa.

**Próximas pendências:** P-025 (elementos/resistências e estados dos chefes);
P-029 (atributos e balanceamento conjunto dos talentos); P-016/P-026
(inventário e hub de preparação); P-028 (amizades, grupos, convites e chat
em tempo real).

**Validação:** o responsável informa que os recursos implementados até aqui
foram testados e aprovados. As pendências acima ainda não foram validadas.

