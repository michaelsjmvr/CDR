# Multiplayer e recursos sociais

> Guia temático iniciado a partir do Documento Mestre v0.55 e atualizado com decisões posteriores. Consulte `Cronicas_do_Recomeco_Documento_Mestre_v0.139.md` para navegar entre assuntos.
>
> Atualizado em: 15/11/2026 21:54:32 (UTC−03:00).


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
vagas para amigos. Os serviços Árvore de Talentos e Inventário têm fluxos funcionais limitados;
Baú, Máquina do Caos e Troca permanecem indisponíveis/planejados.

Na barra superior fica a busca de perfis, fina e discreta, junto à identidade
do jogo e aos atalhos para trocar personagem e sair da conta. A lista de amigos fica na coluna
direita, abaixo dos serviços. O cartão de grupo mostra as informações do
personagem e o botão **Começar!**, contido e alinhado ao canto inferior, sem
painel separado de personagem que repita esses dados. Cada vaga vazia abre um
seletor da lista de amigos; a página exibe o total de amigos e uma lista com
até cinco linhas visíveis, rolável se for maior.
O aviso de intervalo após concluir uma fase fica ao lado do botão Começar,
na mesma linha quando houver espaço, para preservar altura para o Chat da Sala.

Em **Serviços**, Atributos abre a tela de consulta e distribuição dos pontos do
personagem; enquanto digita uma quantidade, a tela mostra o total estimado e
avisa se ultrapassar pontos livres ou o teto. Árvore de Talentos também está
ativa. Cada serviço mostra um indicador quando há pontos não gastos (pontos de
atributo ou Pontos de Legado livres). Atributos e Talentos são ajustados na Sala
de Espera, não durante a partida; as rotas verificam esse estado da sessão. Os
atalhos de Atributos e Talentos não aparecem na tela de jogo. Inventário
abre uma mochila de protótipo, limitada a Baús de Recompensa resgatados. O
saldo compartilhado de Ouro e a ocupação da mochila são mostrados nessa página,
não como resumo solto na Sala de Espera. Isso não equivale ao sistema final de
equipamentos. Baú da Conta (armazenamento),
Máquina do Caos e Troca continuam
indisponíveis/planejados.

**Estado atual do protótipo:** busca de perfis, amizades persistentes,
convites, grupos e chat em tempo real ainda não existem. Busca e botões de
convite aparecem desabilitados; contagem inicia em zero e não há amigos
falsos no protótipo. Clicar numa vaga abre o seletor com o estado vazio. A
área de chat é somente visual e permanece desabilitada até a infraestrutura
de salas e associação de jogadores. Não transmitir mensagens em sala global.

Na sala de espera deverão ficar disponíveis Inventário, Baú, Máquina do Caos
para criação de itens, Talentos, troca direta (*trade*) e gerenciamento de
amigos. As funções ainda não implementadas aparecem identificadas como
indisponíveis no protótipo.

**Missões e dificuldades — P-048, base v0.124 e robustez v0.131:** o lobby
permite selecionar uma das quatro dificuldades e uma fase liberada. A lista
agrupa as opções em Ato 1 (Fases 1–10), Ato 2 (11–20) e Ato 3 (21–30). A fase
seguinte depende da conclusão da anterior na mesma dificuldade; a próxima
dificuldade só libera após concluir as 30 fases da dificuldade anterior. A
rota de entrada e o backend validam o acesso independentemente do estado
visual dos seletores. Ao começar, há uma contagem de 5 segundos com combate e
movimento congelados.

O bloqueio de missão é por conta, não por personagem: somente uma run pode
ficar ativa por vez. O servidor verifica isso dentro da transação de início,
para que sessões concorrentes em personagens diferentes não iniciem duas runs.
Espólios pendentes de qualquer personagem também bloqueiam novas missões e
suspendem ações de combate em runs ainda ativas até que o staging seja resolvido.
Runs legadas simultâneas não são apagadas: somente a mais recente aceita ações;
as demais podem ser retomadas depois que as anteriores terminarem e os espólios
forem resolvidos.

Um painel recolhível no lobby apresenta, para os quatro riscos, multiplicadores
de Vida/dano, inimigos extras por onda comum, Ouro, chance de terceiro baú e
pesos de raridade. Esses valores são identificados como candidatos, não regras
finais. Testes automatizados verificam os quatro perfis e a renderização do HTML;
isso não equivale a uma validação visual em navegador.
Desde v0.130, a suíte Node verifica a sintaxe dos scripts first-party e executa
os fluxos de seleção de fase e capacidade de espólios em Chromium via Playwright.
Os fluxos usam HTML de teste; não percorrem uma partida nem integram os
templates/backend reais, e não substituem o E2E completo da missão.

Depois da última onda, o jogador vai à tela obrigatória de resultado e
resolução de espólios. O resumo modal mostra tempo, Ouro creditado na carteira
da conta e saldo de Ouro. Ouro é moeda virtual do jogo, sem valor real, saque
ou conversão. Baús ficam em
staging até manter/descartar; itens antigos podem ser vendidos ou descartados
para liberar espaço. O retorno à Sala de Espera é bloqueado enquanto houver
espólios pendentes. Os multiplicadores, recompensas, raridades e limite de
30 espaços são candidatos ainda sem aprovação/calibração em combate ativo
(consulte P-048 em
`07_roadmap_e_estado_atual.md`).

**Baú de Recompensa não é Baú da Conta:** os primeiros são espólios de missão
(inclusive recompensas de chefe), mantidos em staging até resgate; o segundo
é o depósito compartilhado planejado. A tela/serviço de armazenamento não
recebe automaticamente os baús de missão e ainda não está implementada.

O jogador poderá: - Criar uma sala aberta para qualquer pessoa entrar; -
Criar uma sala privada/trancada; - Permitir entrada apenas de amigos
adicionados à lista de amigos.

### 13.2 Salas cooperativas

**Direção definida (P-005):** o jogo é prioritariamente solo, com opção de
salas cooperativas de até três jogadores (o jogador e até dois amigos). O trio
pode combinar quaisquer classes. A Sala de Espera será o ponto de encontro e
organização. Limite e composição do grupo estão definidos; a infraestrutura
cooperativa ainda não está implementada.

**Pendente:** implementar convites, expulsão, liderança da sala, reconexão,
entrada durante uma partida, sincronização e escala de dificuldade/recompensas
para grupos. A lista de amigos e convites presentes na interface são
placeholders, não funcionalidades de cooperação.

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
