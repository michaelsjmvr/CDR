# Arte e interface

> Guia temático iniciado a partir do Documento Mestre v0.55 e atualizado com decisões posteriores. Consulte `Cronicas_do_Recomeco_Documento_Mestre_v0.139.md` para navegar entre assuntos.
>
> Atualizado em: 15/11/2026 21:54:32 (UTC−03:00).


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

**Surgimento funcional implementado:** a arena de teste mede 2.400 × 1.800
unidades de mundo. Monstros surgem em pontos determinísticos dentro da área
X=180–2.220/Y=180–1.620, a pelo menos 380 unidades do jogador e 92 entre si.
Nas arenas genéricas, o piso procedural usa módulos de 96 unidades e as ruínas
e pilares são decorativos, sem colisores. A Fase 1 usa arte de fundo própria e
colisores aproximados para ônibus, colunas e bancos; os valores continuam em
unidades lógicas e não são uma escala física aprovada. Consulte
[Arquitetura e integridade](./06_arquitetura_e_integridade.md) para geometria,
projeção e limites. A revisão visual e validação em combate ativo continuam
pendentes. Teletransporte, saída do chão, queda do céu, animações, partículas,
som e sincronização visual ficam para a etapa futura de polimento.

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

### 14.6 Resultado e espólios de missão

Ao concluir a missão, a tela pós-fase abre um `<dialog>` nativo com tempo
formatado em `MM:SS`, recompensa em Ouro e saldo de Ouro da conta. O jogador fecha o
resumo para acessar a tela dividida de inventário/staging. Baús de Recompensa
usam cores específicas: Comum cinza, Raro azul, Épico roxo e Lendário dourado.
Essa paleta é independente das seis cores de raridade de equipamentos
planejadas na Seção 14.2 e não representa o Baú da Conta (armazenamento).
A contagem regressiva de entrada dura 5 segundos e
mostra `5, 4, 3, 2, 1, VAI!`; movimento, ataques e IA ficam congelados nesse
período. Um E2E de navegador com harness percorreu as dez ondas da Fase 10,
derrotou o chefe, mostrou o modal e resgatou três baús; usou atributos de teste
e ataques Socket.IO com coordenadas fornecidas, portanto não valida movimento,
mira manual, IA nem equilíbrio. Leitor de tela e calibração visual completa
ainda não foram exercitados (P-048). Os valores seguem candidatos.

Na Sala de Espera, o seletor de fase agrupa as opções por ato: 1–10, 11–20 e
21–30. O saldo de Ouro da conta e a contagem da mochila ficam juntos no topo da
página Inventário; não são repetidos como uma linha solta no lobby.
O lobby também inclui um painel recolhível com os perfis dos quatro riscos:
escalas de Vida e dano, inimigos extras, Ouro e regras candidatas de Baú de
Recompensa. Testes de rota verificam o HTML renderizado, mas não houve E2E
visual autenticado desta apresentação; os valores continuam sem calibração
final. A suíte Node verifica a sintaxe dos scripts e executa os fluxos de fase
e espólios em Chromium com HTML de teste. Isso não comprova a aparência do
template real, acessibilidade, carregamento do aplicativo ou E2E completo.

### 14.5 Câmera oblíqua e leitura de profundidade

A câmera Canvas do protótipo usa uma projeção oblíqua 2.5D com pitch visual de
58° para baixo a partir do horizonte. O fator `tiltY` aplica `cos(58°)` ao eixo
vertical do piso, simulando a compressão de profundidade de uma câmera inclinada
sem alterar coordenadas do mundo. O jogador permanece no centro enquanto a
câmera ainda pode ser limitada pelas bordas do mapa. É uma aproximação afim em
Canvas, não perspectiva 3D real. Personagens, monstros, nomes e barras recebem
uma compensação vertical para permanecerem eretos e legíveis, enquanto piso,
sombras e círculos de alcance seguem a inclinação. Movimento, colisões, alcance
e mira continuam em coordenadas do mundo; a conversão tela/mundo usa a mesma
projeção. Exceção: a ilustração da Fase 1 já contém a perspectiva 2.5D, então o
mapa usa fator vertical 1 para não comprimir a arte duas vezes; as demais fases
mantêm o fator `cos(58°)`.

A projeção ainda não substitui sprites com volume nem ordenação final de
profundidade. Após concluir P-031, revisar o enquadramento junto à arte final de
personagens, armas, pets, montarias, asas e mapa. Garantir que elementos à
frente cubram os de trás e que hordas, projéteis e avisos permaneçam legíveis.

**Zoom pelo scroll — implementado e exercitado na E2E v0.119:** roda para cima
aproxima e para baixo afasta; a transição é suave e mantém o jogador como foco.
`CAMERA_CONFIG` no começo de `game_app/static/js/game.js` concentra `minZoom`,
`maxZoom`, `initialZoom`, `zoomSmoothing`, `tiltY` e `wheelStep`. O limite de
afastamento aumenta quando necessário para que a viewport nunca ultrapasse as
bordas do mapa, inclusive em resoluções largas/altas. Zoom não altera
movimento, alcance, colisões ou mira. A E2E confirmou movimento/zoom, mas não
valida o pitch em várias resoluções nem a mira por mouse; esses testes continuam
pendentes.

#### Referência técnica para produção visual por código

Estas opções ficam registradas como repertório para tarefas futuras. São
ferramentas possíveis, não uma decisão de que todo o jogo será desenhado por
código; cada recurso deverá ser escolhido conforme legibilidade, desempenho e
identidade visual.

- **Ícones, itens e elementos de interface:** preferir SVG vetorial embutido
  quando formas, contornos e gradientes forem adequados. Espadas, cajados,
  poções, armaduras e botões podem ser descritos em SVG/XML, escalando sem
  pixelar. Usar brilho e gradientes com moderação para respeitar a paleta e a
  leitura do HUD.
- **Personagens, monstros e animações:** protótipos podem usar pixel art por
  matrizes de cor em JavaScript/Canvas ou partes articuladas (cabeça, tronco,
  membros e arma). Animar com quadros ou ângulos calculados ao longo do tempo
  usando `requestAnimationFrame`; não agendar um quadro a cada milissegundo.
  `OffscreenCanvas` pode ajudar em tarefas compatíveis, sempre com alternativa
  para navegadores sem suporte.
- **Mapas e cenários:** gerar tilemaps em grade, combinando tiles desenhados
  em Canvas e regras procedurais. Ruído Perlin/Simplex pode apoiar variação de
  terreno, desde que haja limites de navegação, leitura clara de combate e
  possibilidade de reproduzir o mapa por uma semente.
- **Magias e efeitos visuais:** usar emissores de partículas para golpes,
  projéteis, auras e cura, controlando vida útil, quantidade, cor, tamanho e
  transparência. `globalCompositeOperation = 'lighter'` pode criar brilho
  aditivo, com limite de partículas e contraste para não esconder personagens,
  projéteis ou telegráficos de chefe.

**Estado:** referência técnica registrada; padrão final de arte continua
pendente. Aplicar a direção Dark Fantasy e a paleta oficial da Seção 14.2 em
qualquer abordagem escolhida.

------------------------------------------------------------------------

## 15. Interface e experiência do usuário (UI/UX)

### 15.1 Padrão geral

A interface deverá usar tema escuro, painéis de aparência metálica,
bordas discretas e detalhes em bronze/dourado.

Janelas principais: - Inventário; - Baú; - Forja do Caos; - Loja; -
Trade; - Árvore de Talentos; - Perfil/personagem; - Configurações.

**Página de Atributos:** tela centralizada e responsiva para consultar e
distribuir Força, Agilidade, Vitalidade e Energia. A tela fica disponível nos
Serviços da Sala de Espera e retorna para lá após o uso. Seus efeitos em combate
continuam pendentes do balanceamento conjunto. O campo de pontos mostra uma
estimativa do valor resultante e avisos de limite antes do envio. Serviços de
Atributos e Talentos usam um pequeno indicador dourado no canto superior direito
do ícone correspondente quando há pontos livres.
O menu da partida não oferece Atributos, Talentos nem Trocar Personagem; a troca
fica concentrada na Sala de Espera, que apresenta **Sair** junto do atalho de
troca.

**Árvore de Talentos:** abrir o grafo radial da classe com exatamente três
ramos de evolução, nomes e afinidades de atributos próprios. Não exibir
seletor de origem nem ramos adicionais. O painel lateral apresenta os detalhes
do nó selecionado. No nível 100, um botão destacado abre uma caixa com as três
especializações da classe; após a escolha, somente o ramo ativo aceita pontos.
Premium/VIP pode trocar o caminho enquanto estiver ativo. A tela do protótipo
está descrita na Seção 6.4.

**Tela inicial definida:** após autenticar, exibir a seleção de
personagens antes de entrar na sala. A composição tem três zonas sobre
um cenário noturno: prévia grande e central do personagem selecionado
com animação idle provisória; caixa escura semitransparente com nome,
classe e nível; painel vertical à direita com slots, seleção,
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

**Direção e controles do protótipo v0.108:** WASD ou setas direcionais controlam
a movimentação. No modo Teclado + Mouse, o personagem acompanha o cursor e o
painel superior mostra o monstro sob ele. No modo Apenas Teclado, o personagem
mantém a última direção do movimento e o painel acompanha o alvo assistido à
frente; mirar ou selecionar um alvo não ataca. Todo ataque exige comando do
jogador. Espaço avança na direção atual, com colisão e recarga visual.

**Atalhos e ações:** 1 sempre executa o Ataque básico. 2, 3 e 4 executam as
magias equipadas nos espaços de magia 1, 2 e 3, respectivamente; a fileira
superior e o Numpad têm o mesmo comportamento. A tela Opções permite equipar
ou esvaziar cada espaço. No modo Teclado + Mouse, os botões esquerdo e direito
podem ser vinculados a espaços de magia 2–4. As preferências são persistidas
na conta e atualizadas por Socket.IO.

**Fallback de combate:** qualquer habilidade equipada que esteja em recarga ou
sem Mana usa Ataque básico automaticamente. O nome da habilidade depende da
classe/especialização; Corte Rúnico é específico da Lâmina Arcana. Cliente
antecipa casos já conhecidos para evitar solicitações repetidas, e o servidor
repete a validação antes de aplicar dano e recarga. Se o Ataque básico também
estiver em recarga ou fora do alcance, nenhum dano é aplicado nessa tentativa.

**Escolha de cartas com coleção cheia:** clicar em uma das três opções primeiro
abre a etapa de substituição. As cartas ativas aparecem como opções selecionáveis;
o destaque deixa claro qual será removida, e a troca só ocorre ao confirmar.
Logo abaixo das três ofertas há **Manter cartas ativas · descartar estas 3
opções**. Essa ação fecha a escolha, preserva a coleção e resolve a oferta atual
sem ativar nenhuma carta. A escolha manual funciona da mesma forma para contas
comuns e Premium/VIP; a escolha automática Premium/VIP por prazo continua sendo
um fluxo separado.

**Apresentação de capítulos e ondas:** a introdução de cada capítulo usa
a faixa narrativa superior do cenário uma única vez por personagem e
capítulo no navegador. Depois da introdução, transições exibem somente
fase/onda ou chefe; o início de um capítulo novo mostra a introdução nessa
faixa e, em seguida, a fase/onda.

**Controles contínuos:** não permitir seleção de texto dentro da sala. No modo
Teclado + Mouse, segurar o botão esquerdo/direito repete a ação do espaço
vinculado, respeitando a recarga. Espaço repete o avanço enquanto continuar
pressionado e a recarga permitir. O ataque básico também possui recarga curta.

**Informações de combate:** exibir a quantidade de monstros restantes e
atualizá-la a cada derrota. P-037 implementa um painel superior central para o
monstro mirado, com retrato procedural em Canvas, tipo, nome, nível, barra de
Vida, elemento, resistência e ponto fraco. No cenário, o monstro mostra somente
nome e barra de Vida. Quando a fraqueza não está definida, o painel informa que
ela ainda não foi identificada; esses dados visuais não criam novas regras de
dano. Escudo quebrado, sangramento, paralisia e queimadura continuam pendentes
em P-025/P-031.

**Círculos de alcance:** dois círculos suaves e centrados no personagem
distinguem o alcance real do ataque básico (dourado) e da habilidade-base ou
assinatura atualmente equipada (azul).
O primeiro tem linha contínua e o segundo tracejada; ambos usam brilho/pulso
discreto. As cores reaparecem nas respectivas caixas de ação do HUD. Raios por
classe: Guerreiro 125/170, Tecelão 190/255, Caçador 225/305 e Lâmina Arcana
155/210 unidades. O cliente seleciona alvos dentro do raio e o servidor confere
a mesma distância antes de aplicar dano. O contorno do inimigo precisa apenas
encostar no círculo para o ataque alcançar; o cálculo soma o raio de colisão do
inimigo ao raio do personagem. Cartas de alcance expandem círculos e ataques em
conjunto. A leitura visual e o acerto por contato foram validados manualmente
nas quatro classes, inclusive com carta de alcance;
os valores continuam provisórios para o balanceamento.

**HUD compacto do personagem:** a caixa inferior reúne retrato de classe,
nível atual/limite, barra e quantidade de EXP restante até o próximo nível,
Vida, Mana e habilidades. A contagem de monstros foi integrada à barra
superior, junto de fase e onda, e recebe atualizações por Socket.IO. O retrato
Canvas reutiliza a ilustração provisória da Sala de Espera; a arte final
individual do personagem continua futura. A prioridade imediata de design é
desktop; controles próprios para tablets e celulares ficam para uma etapa
posterior.

**Escolha de cartas:** contas comuns não têm cronômetro e escolhem manualmente.
No Premium/VIP, o prazo de 10 segundos aparece em destaque e é independente
para cada oferta pendente. A recomendação leva em conta classe, efeitos e
raridade. A barra informa EXP por orbe: 25 normal e 40 Premium/VIP; o valor
VIP é provisório e aguarda validação do ritmo.

**Página de atributos v0.101:** no desktop, organizar em duas colunas:
distribuição à esquerda e efeitos de combate à direita. A classe do personagem
aparece na barra superior. O destaque continua reservado aos pontos livres; a
linha secundária informa a EXP restante para o próximo nível e os 5 pontos que
serão recebidos. O painel de combate agrupa dano, Vida/Mana, críticos, esquiva,
alcances, recargas, mitigação e movimento. Efeitos ainda sem sistema próprio
devem dizer “Não implementado” ou “Não separado”, sem exibir números fictícios.
Prioridade visual imediata: desktop; a adaptação para dispositivos móveis fica
para etapa posterior.

**Árvore de Talentos v0.105:** mostrar exatamente três ramos por classe, cada
um associado a uma das três evoluções aprovadas. Remover a lista de seis
pontos de partida e os caminhos extras. Cada ramo mantém nós Pequenos, Notáveis,
aprimoramentos laterais e talentos principais como nós internos, não como
novas evoluções. Nomes, explicações e efeitos dos talentos são próprios de
cada especialização; não reaproveitar nós genéricos entre classes. Os
atributos concedidos seguem a combinação própria da classe e do ramo.

Exibir o custo real do caminho escolhido: **58 ou 64 Pontos de Legado**. Cada
caminho inclui 42 PL em atributos, 2 PL em aprimoramento de combate, 4 PL no
talento principal, 4 PL nas maestrias da habilidade-base e da assinatura, além
de 6 PL por habilidade suprema (4 para desbloqueio e 2 para maestria). Nove
caminhos custam 58 PL e três custam 64 PL; os 64 PL recebidos até o nível 400
permitem concluir qualquer caminho escolhido. A soma de 714 PL corresponde às
12 opções, não ao custo de um personagem. Esses totais descrevem a
implementação anterior: o teto-alvo 170 e a nova curva de PL estão pendentes.
Revalidar limite exibido, ritmo de evolução e disponibilidade de talentos após
o rebalanceamento; não inferir números novos para a interface. O antigo espaço
de melhoria deve funcionar como talento próprio da especialização, não aparecer
como recurso indisponível.

Ao atingir o nível 100, destacar o botão de evolução. O botão abre uma caixa
com somente as três opções da classe. Depois da escolha, destacar o único ramo
ativo e deixar os outros dois bloqueados. Mostrar a opção de troca apenas para
Premium/VIP ativo; a troca informa que talentos e atributos investidos no ramo
atual serão devolvidos. Se o VIP expirar, conservar o ramo atual e ocultar a
troca. Mostrar os investimentos antigos numa seção colapsada de legado, sem
apresentá-los como opções de evolução.

**Sala de Espera e configuração:** a tela individual já existe e contém
espaços visuais para dois amigos. O Inventário tem um fluxo parcial de baús em
P-048; Baú da Conta, Máquina do Caos, grupo em tempo real, convites, lista de
amigos e troca continuam pendentes em P-028/P-005/P-016/P-014/P-017. Os
sistemas completos de configuração deverão poder ser usados na Sala de Espera
e na preparação de fase assim que forem implementados.

**IA, avisos e ataques dos monstros (P-027/P-036):** monstros corpo a corpo
tentam se aproximar e telegráficos são marcados no chão antes do impacto;
inimigos à distância mantêm espaço e lançam projéteis com sombra. O semichefe e
o chefe alternam padrões de área em ciclos legíveis. A zona de perigo, o nome
do golpe e a contagem aparecem no Canvas. A IA contorna aliados no caminho
quando encontra rota livre. O chefe também circula e se reposiciona durante o
combate para não permanecer imóvel ao redor do jogador. O movimento do chefe
foi exercitado manualmente; isso não valida por si só a esquiva de todos os
padrões nem a movimentação autoritativa. O cliente simula o movimento; o
servidor valida o ataque e aplica dano por Socket.IO. Esses pontos continuam
pendentes.

------------------------------------------------------------------------
