# Arquitetura e integridade

> Guia temático iniciado a partir do Documento Mestre v0.55 e atualizado com decisões posteriores. Consulte `Cronicas_do_Recomeco_Documento_Mestre_v0.139.md` para navegar entre assuntos.
>
> Atualizado em: 15/11/2026 21:54:32 (UTC−03:00).


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

O protótipo P-036 também usa Socket.IO para transmitir avisos de ataques
inimigos e resolver acertos no instante do impacto. O servidor guarda os avisos
ativos, confere onda, inimigo, janela temporal e área de perigo antes de
persistir o dano recebido e emitir o novo estado de Vida. A posição do jogador
ainda é simulada localmente pelo cliente e enviada na resolução; tornar o
movimento autoritativo no servidor permanece parte da evolução multiplayer.

**Regra de atualização do jogo:** carregamento inicial pode vir do estado
persistido renderizado por Flask; depois que a sala está aberta, mudanças de
onda/fase, surgimento de inimigos, contagem restante, Vida/Mana, dano, EXP,
orbes, escolhas de cartas e telegráficos devem ser comunicados por eventos
Socket.IO quando afetarem a tela em tempo real. Não depender de atualização
manual da página para refletir uma ação de combate.

A página `/jogo/atributos` também usa Socket.IO: distribuir pontos e alternar a
automação Premium/VIP são eventos autenticados por sessão e CSRF, validados e
gravados pelo servidor em transação. O servidor devolve atributos, pontos
restantes e estatísticas de combate; a interface atualiza sem recarregar. Ao
ativar a automação, os pontos livres existentes são distribuídos segundo os
pesos da classe e os próximos pontos ganhos seguem a mesma regra. A notificação
de sucesso some após cinco segundos.

Escolhas de cartas também usam um botão com evento Socket.IO tanto na oferta
inicial quanto nas ofertas liberadas durante a run. O ACK devolve erros de sessão,
conexão ou validação para a interface e permite liberar novamente o botão quando
a escolha não foi salva.

Cada escolha também envia o ID exato da oferta, validado no servidor. Uma revisão
monotônica por personagem ordena os estados enviados e descarta mensagens atrasadas
sem confundir IDs globais do banco entre personagens.

Recomendações de cartas são calculadas no servidor e persistidas junto à oferta.
Somente Premium/VIP recebe horário-limite Unix de 10 segundos; cada nova oferta
pendente inicia seu próprio prazo, mantido ao atualizar a página. Contas comuns
não recebem cronômetro. Ao ativar Premium/VIP com uma oferta já aberta, o
servidor inicia um prazo novo de 10 segundos. Ofertas antigas recebem uma
migração única de prazo por versão, sem reiniciar a contagem a cada conexão.
A escolha automática usa um evento
Socket.IO próprio, valida dono, oferta vigente e horário no servidor e não
aceita que o cliente escolha qual carta será automática. A recomendação
automática é exclusiva de Premium/VIP; contas comuns recebem destaque visual e
fazem a escolha manual.
Com a coleção cheia, a conta comum também decide qual carta substituir ou manter.
Para Premium/VIP, o servidor compara a utilidade das passivas para a classe e a
situação atual, com raridade como fator secundário. Se a nova carta tiver
utilidade menor que a ativa menos útil, a coleção é mantida; caso contrário,
substitui a carta ativa de menor utilidade e, em empate, a mais antiga. A
permissão e a alteração da coleção são validadas na mesma transação. O estado
de afinidade/resistência dos chefes e a
Vida do alvo são exibidos no cliente com os dados iniciais do Flask e os eventos
de combate Socket.IO. O retrato do alvo é desenhado localmente em Canvas.

O controle flutuante de Premium/VIP para testes envia a solicitação por
Socket.IO; o servidor valida sessão e CSRF, altera somente a conta autenticada
e persiste o estado. O botão pode ser desativado em configuração pela variável
`CRONICAS_ENABLE_PREMIUM_TEST_TOGGLE=0`; é temporário e deve sair antes da versão
final. Ao fechar uma fase, a interface encerra a seleção temporária, limpa
entradas mantidas e mantém a pausa até o jogador escolher a próxima ação.

Subidas de nível devem restaurar Vida/Mana e publicar os máximos novos no
mesmo evento de combate. A derrota de um inimigo grava a posição do drop do
orbe junto à posição final do inimigo e transmite as mesmas coordenadas. Morte
limpa coleção temporária, EXP de cartas, ofertas e orbes em uma transação; a
interface recebe a limpeza por Socket.IO.

O servidor deverá ser a autoridade sobre ações importantes do jogo. O
cliente envia intenções; o servidor valida e atualiza o estado oficial.

**Alcance dos ataques:** o cliente limita a seleção do alvo pelo raio da classe
e pela carta ativa; o evento Socket.IO também rejeita golpes cujo alvo informado
esteja além do mesmo alcance calculado no servidor. A colisão usa contato:
distância entre centros pode chegar ao alcance somado ao raio do monstro
(17 comuns, 24 semichefes, 28 chefes). A leitura e o acerto por contato foram
validados manualmente nas quatro classes, inclusive com carta de alcance.
A posição do jogador e o deslocamento dos inimigos ainda são simulados no
cliente; tornar a movimentação autoritativa continua pendente.

**EXP de cartas por conta:** a coleta permanece validada/transacionada no
servidor por Socket.IO. Orbes concedem 25 EXP a contas comuns e 40 EXP ao
Premium/VIP; a diferença é aplicada no momento da coleta, nunca pelo valor
declarado pelo cliente. O novo valor VIP é provisório e aguarda validação de
ritmo.

### 16.5 Validação do protótipo

A suíte automatizada fica em `tests/` e usa `unittest`. Execute da raiz com
`python -m unittest discover -s tests -v`. Os testes de banco usam SQLite
temporário e nunca devem acessar dados reais.

Os scripts JavaScript first-party do cliente têm uma suíte separada em
`tests/js/`. Requer Node.js 20 ou superior e Chromium do Playwright; instale
com `npm install` e `npx playwright install chromium`, então execute
`npm run test:js`. A suíte verifica a sintaxe dos scripts em
`game_app/static/js/` (exceto código vendorizado) e executa em Chromium os
fluxos de seleção de fase e capacidade de espólios usando HTML mínimo de teste.
Não carrega templates Flask, backend ou Socket.IO e não substitui E2E completo
do aplicativo ou avaliação visual manual.

Toda mudança de comportamento deve incluir ou atualizar testes de regressão que
exercitem o código real; execute a suíte antes de concluir a tarefa. Ao surgir
uma área sem cobertura, estenda o software de testes com cenários determinísticos
ou clientes de teste, em vez de pedir ao responsável que repita verificações
manuais. A cobertura, a política de extensão e as áreas atuais estão em
`tests/README.md`. Testes de lógica não afirmam, por si sós, que equilíbrio ou
experiência subjetiva estão aprovados.


### 16.6 Segurança e integridade

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

### 16.7 Grafo radial de talentos

`game_app/talents.py` gera um grafo não direcionado separado para cada classe,
com exatamente três ramos, um para cada evolução aprovada. Os IDs `v105`
distinguem os nós atuais dos grafos anteriores; nomes, descrições e efeitos
dos talentos são definidos individualmente para cada uma das 12
especializações. Cada ramo tem 11 nós: três de trilha, cinco de roda, um
aprimoramento lateral, um talento especial e um talento principal.
`characters.specialization_id` persiste o único caminho ativo e
`character_talents` persiste as compras. `characters.talent_root_id` aponta
para a raiz fixa da classe; não há seletor adicional de ponto de partida.

Antes da evolução, nenhuma compra dos três ramos é permitida. O servidor exige
nível 100 para a primeira escolha, valida que a opção pertence à classe e
permite apenas compras do ramo persistido. Os outros dois ramos ficam
bloqueados mesmo que o cliente envie um pedido diretamente. Só com Premium/VIP
ativo o servidor aceita trocar uma escolha existente. A troca ocorre numa
transação: remove os nós comprados no ramo atual, devolve seu custo ao saldo de
Pontos de Legado, subtrai os atributos concedidos e persiste a nova evolução.
O privilégio VIP é consultado novamente durante a operação.

Cada caminho custa 58 ou 64 PL: 42 em atributos, 2 em aprimoramento de combate,
4 no talento principal, 4 em maestrias da habilidade-base e da assinatura e
6 por habilidade suprema (4 para desbloquear e 2 para aprimorar). Nove caminhos
têm uma suprema e custam 58 PL; três têm duas e custam 64 PL. O total das 12
especializações é 714 PL, mas cada personagem escolhe um único caminho. A fórmula
em `progression.py` é `level // 10 + level // 50 + level // 25`, que concede
64 PL no nível 400 e cobre qualquer caminho individual.

Esse trecho descreve o código anterior à decisão v0.135: o teto-alvo decidido
é 170 e a curva de PL será recalculada, mas a implementação segue em 400 até a
pendência ser executada. Os valores aqui não especificam a nova curva.

Ao abrir `/talentos`, `_refund_v104_talents()` remove os nós v0.104 comprados,
devolve os pontos pelo custo legado e subtrai os atributos persistidos. A
operação é transacional e idempotente: os nós removidos não são devolvidos uma
segunda vez. Investimentos v0.102/v0.103 continuam registrados como legado,
com custos contabilizados, mas não abrem os ramos novos.

`game_app/abilities.py` é a fonte única das habilidades-base, 12 pares
passiva/habilidade assinatura e 15 habilidades supremas. `game_app/talents.py`
cria nós exclusivos de desbloqueio e maestria para cada suprema, além das
maestrias das habilidades-base e assinaturas. `derived_combat_stats()` aplica
passivas e talentos comprados; `combat.py` agrega os bônus de dano específicos
por habilidade. O servidor só libera habilidades correspondentes a talentos
comprados e valida os três espaços, duplicatas e o limite de uma suprema.
`socket_events.py` resolve acerto, dano, alvos secundários, atração/repulsão,
imobilização e efeitos temporários. **Erga-se** transforma um inimigo derrotado
em aliado temporário: até três soldados somam 35% do dano-base nos próximos três
ataques cada e desaparecem após 15 segundos; a lista é mantida na memória do
servidor e é apagada ao morrer. O **Poço de Inércia** atrai e imobiliza alvos por
1,5 segundo. A posição simulada dos inimigos em área ainda é enviada pelo
cliente e restringida pelo servidor aos inimigos vivos da onda.

A tela `/talentos` apresenta atributos, passiva, habilidades, habilidades
supremas, custo de Mana, recarga e custo total do ramo; etiquetas visíveis usam
português do Brasil. A prévia acompanha mouse e foco de teclado; a inspeção dos
nós do grafo também acompanha hover, clique e foco.
`tests/test_talents_and_abilities.py` exercita os custos agregados, desbloqueio
e maestria das 15 supremas, loadout, ataques em área/encadeados, repulsão,
imobilização, invocação temporária, defesa e crítico.

### 16.8 Opções, controles e câmera v0.108

Preferências por conta ficam na tabela `users`: `control_scheme`,
`skill_slot_1` a `skill_slot_4`, `mouse_left_slot` e `mouse_right_slot`.
`database.py` adiciona esses campos por migração incremental para bancos
existentes. A tela de opções na partida salva pelo evento autenticado e
protegido por CSRF `options:update_controls`; `options:controls_updated`
sincroniza outras abas da mesma conta, e o ACK atualiza a aba que salvou. O
servidor valida o esquema, os quatro espaços e os vínculos do mouse antes de
gravar. O espaço 1 fica fixo no Ataque básico. O único espaço de magia ocupado
usa a habilidade-base da classe até a compra do talento principal; então recebe a
habilidade assinatura da evolução. A posição salva do espaço é preservada, mas
o conteúdo é resolvido por personagem, não por conta, evitando equipar uma
habilidade incompatível ao alternar entre personagens de classes diferentes.
As teclas Digit/Numpad 1–4 mantêm o mapeamento nos dois esquemas de controle.
Os botões do mouse aceitam apenas espaços de magia 2–4 e só respondem no modo
Teclado + Mouse. A migração preserva magias únicas existentes, compacta-as nos
espaços 2–4 e remapeia os botões do mouse.
O marcador `control_options_version` faz a conversão só uma vez, sem desfazer
preferências remapeadas em inicializações futuras. Novas magias por classe
permanecem pendentes em P-018.

Se a habilidade equipada estiver em recarga ou sem Mana, `combat:attack`
converte a intenção em Ataque básico dentro da mesma validação de personagem,
onda, alvo, distância, dano e recarga. Isso vale para a habilidade-base ou
assinatura atual de cada classe; Corte Rúnico é específico da Lâmina Arcana.
`combat:enemy_updated` e o ACK informam ação pedida, ação executada e motivo do
fallback. A recarga básica continua valendo e não há fila de ataques. O cliente
antecipa recarga e Mana baixa a partir do HUD para evitar tentativas repetidas
enquanto o jogador segura um botão.

Nos dois esquemas, somente entradas explícitas do jogador chamam `attackWith`:
teclas 1–4, Numpad 1–4 ou, no modo Teclado + Mouse, botões do mouse vinculados
a magias. O alvo assistido do modo `keyboard_only` serve apenas ao HUD e à
seleção do alvo quando o jogador aciona uma habilidade; não há ataque no loop
de movimento. P-035 fica suspenso pela decisão atual e não autoriza automação.

Os parâmetros visuais ficam em `CAMERA_CONFIG` no início de
`game_app/static/js/game.js`. O pitch configurado é 58° para baixo a partir do
horizonte, aproximado por `tiltY = cos(58°)` no Canvas afim. `screenToWorld` e
`worldToScreen` convertem cursor e elementos com zoom/projeção; o servidor
continua recebendo coordenadas do mundo. O zoom é interpolado no cliente e
limitado por `world.width`, `world.height` e pela resolução atual para manter a
visão dentro das bordas do mapa. Personagens, inimigos, nomes e barras são
compensados para permanecer eretos; efeitos e elementos apoiados no chão seguem
a projeção. Movimento e simulação de inimigos ainda são locais ao navegador. A
E2E v0.119 exercitou movimento e zoom; continuam pendentes a mira por mouse e
a validação do pitch em várias resoluções.

**Exceção visual da Fase 1:** a arte fornecida do Terminal de Vilar já contém
uma projeção 2.5D. `game.js` a desenha como imagem de fundo em coordenadas
proporcionais ao mundo lógico 4:3 e usa `cameraTiltY = 1`, sem comprimir o eixo
Y uma segunda vez. As outras fases mantêm o `cos(58°)` configurado. A arte é
carregada de `game_app/static/images/maps/terminal_vilar_fase1.jpg`; em caso de
falha, o renderizador mantém a alternativa procedural e registra o erro no
console. A cada quadro, `game.js` calcula o recorte visível da imagem a partir
da origem e das dimensões da câmera, posicionando-o no viewport para o fundo
acompanhar o jogador.

#### Geometria atual da arena de protótipo

Os valores abaixo descrevem a implementação presente em
`game_app/static/js/game.js`, `game_app/combat.py`, `game_app/game.py` e
`game_app/classes.py`. São unidades lógicas do mundo, não pixels nem metros; não
há conversão aprovada para escala física ou para a arte final. O cenário jogável
é uma sala retangular única, sem subáreas, elevação ou eixo Z.

**Mundo e limites**

| Propriedade | Valor atual |
|---|---:|
| Área lógica | X=0–2.400, Y=0–1.800 |
| Proporção do mundo | 4:3 |
| Centro e início do jogador | (1.200, 900) |
| Limites padrão (demais fases) | X=130–2.270, Y=130–1.670 |
| Limite inicial de movimento da Fase 1 | X=130–2.270, Y=130–1.670 (editável no JSON) |
| Área inicial de spawn da Fase 1 | X=180–2.220, Y=180–1.620 (editável no JSON) |
| Raio do jogador | 13 |
| Velocidade do jogador | 245 unidades/s |
| Avanço | 720 unidades/s por 0,2 s (144 unidades nominais, antes dos limites) |

O movimento é contínuo em coordenadas X/Y, não preso à grade do piso. Nas
arenas genéricas, as paredes de ruína são desenhadas a 110 unidades das bordas,
enquanto o limite do centro dos personagens é 130; as paredes continuam
decorativas. Na Fase 1, os objetos sólidos listados abaixo bloqueiam jogador e
inimigos. O jogador colide com inimigos vivos no movimento comum; Avanço ainda
atravessa inimigos, mas não atravessa a cenografia sólida da Fase 1.

**Mapa da Fase 1 — Terminal de Vilar:** a missão usa a arte de 1.200 × 896 px
em `game_app/static/images/maps/terminal_vilar_fase1.jpg`, ajustada ao mundo
lógico de 2.400 × 1.800. O Canvas do jogo recorta a imagem conforme a câmera;
na Fase 1, `cameraTiltY = 1`, sem uma segunda compressão vertical da arte. A
prévia `/mapas/terminal-vilar-fase1` usa a mesma imagem e configurações
persistidas. O arquivo JSON atual contém 23 retângulos orientados, 16 polígonos
sólidos, quatro paredes lineares e `wall_thickness = 13`; os valores e pontos
vigentes devem ser consultados diretamente em
[`terminal_vilar_fase1.json`](../game_app/data/maps/terminal_vilar_fase1.json),
pois os dados geométricos são editáveis.

`game_app/map_geometry.py` valida a fonte JSON, calcula colisão de círculos com
retângulos, polígonos e paredes e expõe os dados ao Flask. O cliente do jogo e a
prévia usam a mesma configuração; a prévia combina as formas estáticas com os
retângulos editáveis. O editor local permite selecionar, adicionar, remover,
mover, redimensionar e rotacionar retângulos e alterar os limites de movimento e
spawn. Ele não edita polígonos nem paredes; essas formas permanecem fixas na
interface visual e devem ser alteradas no JSON. O mundo continua fixo em
2.400 × 1.800; spawn deve ficar dentro do limite de movimento, que deve incluir
o ponto inicial (1.200, 900).

O botão **Salvar no projeto** envia JSON com token CSRF a
`POST /mapas/terminal-vilar-fase1/salvar`. O endpoint aceita apenas conexões
loopback, valida o esquema, IDs, limites, dimensões e valores finitos, grava o
arquivo por substituição atômica e atualiza a configuração em memória. Falhas
de validação retornam erro; falhas de disco permanecem erros explícitos do
servidor. Uma sessão de jogo já aberta precisa ser recarregada para receber os
novos dados do cliente. As demais fases preservam seus limites atuais.

O jogador usa seu raio atual de 13 unidades; inimigos usam o raio individual
(17/24/28). Colisões impedem movimento do jogador e da IA, inclusive durante
Avanço. Spawns da Fase 1 e reposicionamento legado de inimigos evitam os
colisores com margem de 28 unidades. Repulsão/atração do servidor mantém um
inimigo em sua posição anterior quando o destino colide. A colisão não altera
os limites do mundo lógico ou o spawn seguro (1.200, 900); a região permitida
para movimento/spawn pode ser alterada pelo editor. A distância mínima inicial
dos inimigos continua em 380 unidades.

Poças, rachaduras, detritos, postes, cobertura acima do chão e névoa não são
sólidos; a geometria não bloqueia linha de visão, ataques ou projéteis. A cena
também usa efeitos de poças/reflexos, energia animada, iluminação, névoa,
oclusão e chuva, renderizados pelo módulo
`game_app/static/js/terminal-vilar-effects.js`. Movimento do jogador continua
simulado no cliente e não é autoritativo no servidor. Os valores são proxies
aproximados em unidades lógicas, sem escala física aprovada. A arte e a
composição final continuam sujeitas à revisão visual do responsável.

**Integração v0.139:** a imagem e os efeitos do HTML atualizado foram conectados
à missão; a prévia passou a usar a configuração JSON e recebeu novamente o
editor local. Nenhum teste, checagem de sintaxe, build ou inspeção no navegador
foi executado, a pedido do responsável. A evidência automatizada anterior cobre
somente a implementação precedente e não valida a arte, efeitos ou geometria
atuais.

**Piso e adornos cenográficos**

- Nas arenas genéricas, `drawFloor` repete módulos de 96 × 96 unidades,
  preenchidos em 94 × 94 para deixar uma junta visual de 2 unidades. A malha é
  um tratamento gráfico, não uma grade de navegação. Na Fase 1, a ilustração
  cobre o piso e a malha procedural só aparece no fallback.
- O contorno externo usa `strokeRect(110, 110, 2.180, 1.580)`, traço de
  12 unidades e padrão tracejado 68/18. Um segundo contorno fino fica em
  (119, 119), com 2.162 × 1.562 unidades.
- Na Fase 1, os proxies de colisão da ilustração são a tabela anterior. Seus
  valores persistentes ficam em
  [`terminal_vilar_fase1.json`](../game_app/data/maps/terminal_vilar_fase1.json)
  e são expostos em `TERMINAL_VILAR_COLLIDERS` por
  [`map_geometry.py`](../game_app/map_geometry.py); a geometria de colisão não
  depende do código procedural de fallback.

**Nascimento e escala dos atores**

`enemy_spawn_positions` usa uma semente estável no formato
`enemy:<character_id>:<phase>:<wave>`. Fora da Fase 1, as posições candidatas
inteiras vão de X=180 a 2.220 e Y=180 a 1.620, inclusive. Na Fase 1, a área
configurada em `spawn_bounds` no JSON é usada. O algoritmo mantém no mínimo 380
unidades da origem segura do jogador e 92 entre inimigos; tenta amostras
pseudoaleatórias e, se necessário, completa por uma grade de 120 unidades. Ao
abrir a sala sem posições anteriores, a origem segura é (1.200, 900). Na
transição de onda, o servidor usa a posição do jogador recebida no comando e a
limita aos mesmos limites de movimento. A quantidade e a semente determinam o
resultado. Somente na Fase 1, candidatos também são rejeitados se o círculo do
inimigo de raio 28 tocar um colisor; os demais riscos e fases mantêm o algoritmo
sem geometria ambiental própria.

| Ator | Raio de colisão no cliente |
|---|---:|
| Jogador | 13 |
| Inimigo comum | 17 |
| Semichefe | 24 |
| Chefe | 28 |

Distâncias de comportamento que ajudam a interpretar o espaço ocupado, também
em unidades lógicas entre centros:

| Tipo de inimigo | Velocidade de perseguição | Alcance que aciona ataque | Faixa preferida |
|---|---:|---:|---:|
| Comum corpo a corpo | 62, 70 ou 78 | 150 | — |
| Comum à distância | 54 | 390 | 250 |
| Semichefe | 52 | 430 | órbita em torno de 205 |
| Chefe | 43 | 430 | órbita em torno de 265 |

As velocidades comuns corpo a corpo alternam por inimigo; os valores são
unidades por segundo. Alcance de ataque é uma distância centro a centro que
aciona a solicitação de ataque, não uma hitbox de obstáculo.

Raios-base de alcance (ataque básico / habilidade), em unidades de mundo,
antes dos modificadores de cartas/talentos:

| Classe | Básico | Habilidade |
|---|---:|---:|
| Guerreiro | 125 | 170 |
| Tecelão | 190 | 255 |
| Caçador | 225 | 305 |
| Lâmina Arcana | 155 | 210 |

**Projeção e enquadramento**

O pitch de 58° aplica `tiltY = cos(58°) ≈ 0,529919` ao eixo Y do chão. Assim,
em zoom 1, os 1.800 unidades de profundidade ocupam cerca de 953,85 unidades
verticais projetadas; largura e profundidade visuais ficam em aproximadamente
2,52:1. Não há coordenada de altura: o volume é sugerido por desenhos,
sombras e compensação vertical dos atores.

Para viewport CSS `W × H`, o ajuste mínimo de enquadramento é
`fitZoom = max(W / 2400, H / (1800 × tiltY))`. Os limites usados são
`minZoom = max(0,72, fitZoom)` e `maxZoom = max(1,6, fitZoom)`; o zoom inicial é
1, suavizado pelo fator 8, com passo de roda 0,12. Portanto, uma viewport que
exija mais que 1,6 para caber no mapa aumenta também o limite máximo. A tela
visível no mundo mede `W / zoom` por `H / (zoom × tiltY)`.

As transformações são `screenX = (worldX − cameraX) × zoom` e
`screenY = (worldY − cameraY) × zoom × tiltY`; `screenToWorld` aplica as
inversas. A câmera acompanha o jogador e limita sua origem para não mostrar
fora do retângulo do mundo. O Canvas usa o tamanho da janela e limita
`devicePixelRatio` a 2. Piso, sombras e círculos de alcance sofrem compressão
vertical; atores, nomes e barras são compensados para permanecerem eretos.

**Status para uso como referência:** dimensões, posições e fórmulas acima estão
no código atual. A arena é uma sala visual de teste, não uma definição final de
escala ou layout. Permanecem pendentes a validação dos afastamentos em combate
ativo, da leitura do pitch em várias resoluções e da futura arte/profundidade.

### 16.9 Escolha manual de cartas com coleção cheia v0.108

`card:choose` valida no servidor a oferta atual, a carta clicada, a capacidade
da coleção e o identificador da carta ativa escolhida para remoção. Se os
espaços estiverem cheios, o primeiro clique abre imediatamente no cliente o
seletor de substituição e envia `selected_card_id` ao servidor sem equipar a
nova carta. O servidor devolve `replacement_required` com as cartas ativas, e a
confirmação só é habilitada após essa validação. Cada opção ativa exibe nome,
raridade e a descrição do efeito atual. O servidor só troca as cartas após
receber `replacement_card_id` válido. A ação `keep` resolve a oferta, mantém os
ativos e reduz `pending_card_choices`; a mesma oferta não reaparece. Se a
página for recarregada com essa decisão pendente, o seletor abre ao carregar.

Na tela de ofertas, o botão **Manter cartas ativas · descartar estas 3 opções**
fica abaixo das três cartas quando a coleção está cheia. Essa ação também pode
ser feita na etapa de substituição. IDs mostrados são registrados em
`card_offer_history` e ficam fora dos sorteios durante aquela onda, inclusive
se a oferta for descartada; em ondas futuras, cartas não ativas voltam a ser
elegíveis. Se o catálogo restante não comportar três opções inéditas, o sorteio
reutiliza cartas não ativas para manter três opções. O prazo VIP continua
podendo selecionar automaticamente uma recomendação se nenhuma escolha manual
tiver começado; se o jogador já clicou numa carta, o servidor mantém a decisão
manual de substituição.

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

-------------------------------------------------------------------------

## 18. Missões, recompensas e staging — P-048

O protótipo de código v0.126 usa SQLite e mantém `mission_progress` por usuário,
dificuldade e fase; `mission_runs` registra início, dificuldade, resultado,
status e quantidades de Ouro; `gold_ledger` registra créditos inteiros com
chave única por origem; `users.wallet_gold` mantém o saldo compartilhado da
conta; `inventory_items` armazena itens-baú resgatados; e `staging_inventory`
mantém cada baú pendente, resgatado ou descartado. Não há subdivisão decimal,
cotação ou integração com pagamentos reais.

Na migração dos bancos existentes, os campos legados em centavos e a tabela
`wallet_ledger` são renomeados para os nomes de Ouro, preservando exatamente
os valores inteiros. Assim, valores candidatos anteriores, por exemplo `5`
centavos, passam a representar `5 Ouro`; isso não é taxa de câmbio nem
conversão monetária.

`staging_inventory` é o fluxo temporário de Baús de Recompensa da missão.
`account_stashes` é apenas um registro-base da conta; a interface e as
operações de depósito/retirada do Baú da Conta ainda não existem. Portanto,
nenhum desses baús de missão é armazenamento compartilhado nem é transferido
automaticamente para o Baú da Conta.

`game_app/mission_system.py` concentra a progressão de desbloqueio, as regras
candidatas de moeda/baús e a transferência condicionada à capacidade. As rotas
do lobby e da entrada de fase conferem autorização no servidor; a run é criada
em transação `BEGIN IMMEDIATE`, após conferir que não há outra run ativa nem
staging pendente na conta. `active_mission_run` só libera a run mais recente
da conta e retorna nenhuma run enquanto houver espólios pendentes; assim, os
eventos Socket.IO de combate/orbes não avançam runs de outras sessões. Em
registros legados com múltiplas runs ativas, as mais antigas ficam pausadas,
sem abandono ou remoção automáticos. O horário oficial de início é definido
cinco segundos após a entrada. Socket.IO bloqueia ataques no período de
preparação e, ao derrotar o
último inimigo da última onda da fase, finaliza a run, credita a recompensa
idempotentemente, grava progresso e cria staging. Venda, descarte e resgate
verificam propriedade e capacidade no backend; o cliente só auxilia com
feedback de espaço.

Os números de dificuldade, chance/pesos de raridade, quantias de Ouro e
capacidade de 30 itens são parâmetros candidatos, não regras aprovadas. A suíte
Python v0.131 passou com 84 testes e cobre progressão, crédito idempotente,
staging/capacidade, autorização, bloqueio na contagem, conclusão da última
onda, parâmetros das quatro dificuldades e bloqueio entre sessões/personagens.
A suíte JavaScript tem três verificações: sintaxe dos scripts first-party e
fluxos de seleção de fase e
resolução de espólios em Chromium com Playwright e HTML de teste. Um E2E em navegador com banco
descartável percorreu as dez ondas da Fase 10 por ataques Socket.IO até o chefe
de ato e o resgate de três baús. O teste pré-carregou o progresso das Fases 1–9
para liberar a Fase 10 e usou atributos e coordenadas de ataque preparados para
acelerar a execução; comprova o fluxo servidor/interface, mas não gameplay
representativo, movimento, mira manual, IA ou equilíbrio. Os testes JavaScript
não carregam o aplicativo real, não validam Socket.IO e não substituem E2E
completo. Fluxos completos nas outras
dificuldades, inventário cheio em navegador e calibração em combate continuam
pendentes. Consultar P-048 no Roadmap e `03_itens_e_economia.md`.
