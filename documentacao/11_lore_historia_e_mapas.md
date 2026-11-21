# Lore, história e mapas

> Guia temático oficial integrado em v0.121; consulte o Documento Mestre v0.139.
>
> Atualizado em: 15/11/2026 21:54:32 (UTC−03:00).
>
> Escopo narrativo: Temporada 1, Ato 1, Fases 1 a 10. Conteúdo organizado a partir de
> [`temporario.md`](../temporario.md); o arquivo bruto foi preservado.

## 1. Escopo e estado do material

**Temporada 1 — O Despertar da Glória Caída** está estruturada no jogo em 30
fases, três atos de dez fases e nove grupos visuais. A campanha mantém uma
arena lógica única; a Fase 1 já usa uma composição visual própria do Terminal
de Vilar, enquanto os demais grupos não correspondem a geometrias físicas
distintas. A ambientação autoral proposta toma a Baixada Fluminense e São João
de Meriti, RJ, como referências geográficas.

Este guia traz a proposta narrativa do Ato 1 (Fases 1–10), incluindo Setor 01 —
A Baixada Possuída, fichas de Level Design e roteiros. Esses nomes, cenas,
personagens e acontecimentos não são conteúdo narrativo já implementado: o
jogo implementa a progressão de atos/fases, os grupos visuais, a arte e os
colisores aproximados da Fase 1 e a cadência de encontros, mas ainda não exibe os
diálogos nem confirma a identidade narrativa dos chefes. As Fases 11–30
continuam sem roteiro aprovado.

As fichas e cenas deste guia são **propostas de narrativa e Level Design**.
Elas não afirmam que os nove temas visuais sejam nove mapas físicos, nem que
hazards, cutscenes ou diálogos já existam no jogo. O protótipo atual reutiliza
uma arena lógica única de 2.400 × 1.800 unidades; a Fase 1 usa uma ilustração
própria e colisões aproximadas para ônibus, pilares e bancos. Para medidas,
limites e elementos sem colisão, consulte
[Arquitetura e integridade](06_arquitetura_e_integridade.md).

As descrições de balanceamento em cada fase são intenções de design, não
valores implementados ou aprovados. Qualquer proposta de densidade, dano,
resistência, controle de grupo, tempo para matar, hazard ou recompensa precisa
ser compatibilizada com as regras e o orçamento de EXP por fase vigentes em
[Personagens e progressão](02_progressao_e_personagens.md), testada e aprovada
antes de virar especificação. A história deve acompanhar a progressão de
níveis; não deve criar, por diálogo, uma regra de XP ou uma curva conflitante.
O teto-alvo 170 e o rebalanceamento de XP, Pontos de Legado e combate foram
decididos, mas ainda não implementados; até a atualização da curva, não usar a
projeção antiga de nível 170/26 PL como regra narrativa ou promessa de
recompensa.

## 2. Diretrizes permanentes para a IA

Ao escrever, revisar ou expandir a história e os mapas:

1. **Acople narrativa e progressão.** Planeje revelações, inimigos, chefes e
   pausas em diálogo considerando o nível esperado, o ritmo de XP, a
   dificuldade e a economia de recursos. Use a regra atual documentada em
   `02_progressao_e_personagens.md`; não altere o orçamento total de XP de uma
   fase nem prometa níveis/recompensas sem aprovação. Trate estimativas de TTK,
   densidade e mecânicas ambientais como hipóteses até serem validadas.
2. **Preserve o tom autoral:** horror dark, ameaça cósmica e consequências
   emocionais convivem com humor de observação, referências à vida digital de
   2026 e gírias cariocas. A comédia deve aliviar a tensão sem ridicularizar as
   vítimas da possessão ou apagar o peso do que ocorreu.
3. **Use a quebra da quarta parede com propósito.** Os protagonistas podem
   falar com o Jogador, chamado também de Operador, e comentar comandos, mouse,
   teclado, builds, atualizações e decisões. A interação deve reforçar a trama
   e a relação entre agência divina, controle e livre-arbítrio, sem substituir
   cenas ou decisões dramáticas.
4. **Mantenha nomes e expressão originais.** Lugares reais podem servir de
   referência geográfica, mas estabelecimentos, empresas, personagens
   secundários, marcas, logos e entidades comerciais devem receber nomes
   fictícios ou satíricos. Não atribua eventos fictícios a pessoas ou empresas
   reais; não copie personagens, diálogos, desenhos, músicas, mapas ou
   elementos distintivos de obras de terceiros. Use apenas material próprio,
   licenciado ou autorizado. A ficcionalização é uma diretriz de redução de
   risco, não uma garantia jurídica; encaminhe dúvidas de publicação para
   revisão apropriada.
5. **Separe roteiro de implementação.** Antes de descrever um recurso como
   existente, confira o código e a documentação técnica. Se for apenas uma
   ideia narrativa, identifique-a como proposta.

## 3. Premissa do Setor 01

Uma ruptura digital abre caminho para espíritos obscuros do Vazio, que
sequestram corpos humanos e corrompem máquinas, infraestrutura e dados. Quatro
protagonistas enfrentam os hospedeiros e percebem que sua própria consciência
está sincronizada com uma entidade divina — o Jogador/Operador, que os controla
por uma interface. A primeira trilha atravessa terminal, viaduto, comércio,
rio, shopping, cemitério, zona industrial, subestação e morro, até chegar ao
topo de um edifício comercial no centro.

No roteiro proposto, o Ato 1 termina sem resolver a origem da ruptura: o
Administrador de Rede Possuído é libertado, a fenda recua para o subsolo e os
heróis descobrem uma conexão entre o Operador e os Espíritos do Vazio. Isso não
descreve uma cena existente no protótipo.

### 3.1 Divisão implementada de atos e grupos visuais

| Ato | Fases | Grupos visuais declarados no código | Encontro especial implementado |
|---|---:|---|---|
| Ato 1 | 1–10 | 1–3 Perímetro do Terminal de Vilar; 4–6 Setor das Ruínas de Meriti; 7–10 Distrito da Antena | Semichefe na Fase 5; chefe na Fase 10 |
| Ato 2 | 11–20 | 11–13 Setor 1 (provisório); 14–16 Setor 2 (provisório); 17–20 Setor 3 (provisório) | Semichefe na Fase 15; chefe na Fase 20 |
| Ato 3 | 21–30 | 21–23 Setor 1 (provisório); 24–26 Setor 2 (provisório); 27–30 Setor 3 (provisório) | Semichefe na Fase 25; chefe na Fase 30 |

O nome e a divisão dos atos/fases, os nove grupos e a cadência dos encontros
acima correspondem ao código da campanha. Os setores provisórios dos Atos 2 e
3 não definem lore, localidades ou mapas aprovados. As três fases finais de
cada ato ainda seguem o grupo visual indicado; apenas as fases 10, 20 e 30
encerram ato com chefe. Todas as fases reutilizam a arena lógica atual; os
grupos não representam geometrias físicas diferentes. A Fase 1 é a exceção
visual já integrada, não uma arena ou regra de navegação separada.

### 3.2 Episódios propostos do Ato 1

| Fase | Episódio | Local/referência | Imagem-base e marco narrativo |
|---:|---|---|---|
| 1 | Quem foi que deixou o portão do terminal aberto? | Terminal Rodoviário de Vilar dos Teles | Concreto quebrado, ônibus abandonados e fendas sobre a praça da matriz; descoberta dos hospedeiros e do Operador |
| 2 | Cuidado com o vão entre o trem... digo, o abismo no viaduto | Viaduto da Via Principal — Trecho Meriti | Tráfego parado, carcaças fumegantes e abismo de código; mutação de carne e metal |
| 3 | Promoção relâmpago: leve dois espíritos obscuros, pague com a sua alma | Calçadão de São João — Centro | Comércio coberto por neblina, tendas rasgadas e manequins corrompidos; horda ágil |
| 4 | Lama, bicho e bitola: bem-vindo ao spa ecológico do Vazio | Margens do Rio Pavuna | Lama escura, manguezal cibernético e passarelas podres; mutação viscosa |
| 5 | Liquidação total de HP: o gerente enlouqueceu | Shopping Regional de Meriti — Ruínas | Centro comercial saqueado e parcialmente desabado; primeiro semichefe |
| 6 | Ressurreição sem agendamento: o cemitério virou servidor público | Cemitério Municipal do Araruí | Túmulos abertos e mutações ósseas; ameaça necrótica |
| 7 | Turno da noite eterno: o relógio de ponto bateu no Vazio | Avenida Automóvel — Setor Industrial | Galpões escuros, faíscas e neblina ácida; mutação industrial e ataques cadenciados |
| 8 | Gato de luz cósmico: a conta de energia veio no débito automático da alma | Subestação de Energia de Éden | Torres, cabos e arcos azuis; mutação elétrica e reação em cadeia |
| 9 | Labirinto de laje e glitch: quem subiu o morro sem mapa? | Complexo de Ladeiras — Morro Oculto | Becos labirínticos, população tomada e barreiras de corpos fundidos; preparação para o chefe |
| 10 | Tela Azul no Olimpo da Baixada: O Administrador Caiu | Topo do Edifício Comercial — Centro | Vista da Baixada sob tempestade de dados; chefe do Ato 1 e revelação sobre o Operador |

Os locais da tabela são subáreas e referências do roteiro proposto, agrupadas
nos três temas visuais do Ato 1; não significam dez mapas implementados. A
identidade do chefe da Fase 10 como Administrador de Rede também é narrativa
proposta, não um dado do sistema de combate.

## 4. Episódio 1 — Fase 1: “Quem foi que deixou o portão do terminal aberto?”

### Ficha de Level Design

- **Mapa:** Terminal Rodoviário de Vilar — Setor 01.
- **Dimensão lógica implementada:** 2.400 × 1.800; spawn central em (1.200,
  900). Unidades do mundo, sem escala física aprovada.
- **Ambiente e iluminação:** noite abafada e escura em São João de Meriti,
  neon roxo e postes falhando; poças no asfalto refletem corpos contorcidos.
- **Piso:** asfalto esburacado, lixo e detritos urbanos.
- **Bordas e referências:** ônibus municipais abandonados da fictícia Viação
  Roda-Presa, com sombras se debatendo atrás das janelas; seis colunas de
  concreto cobertas por cartazes rasgados.
- **Spawn:** plataforma central de embarque, onde o grupo surge enquanto as
  primeiras pessoas possuídas emergem da neblina.
- **Entrada de inimigos:** neblina e interior dos ônibus.
- **Intenção de balanceamento na lore:** abertura do jogo; apresenta a
  ameaça, o horror de combater moradores possuídos e a interface com o
  Operador. Não define uma curva numérica de XP ou combate.

### Estado implementado e acesso à prévia

O HTML atualizado foi integrado à Fase 1 (índice visual 0): a arte de 1.200 ×
896 px é desenhada no mundo lógico de 2.400 × 1.800 unidades, sem segunda
compressão vertical. A cena também apresenta poças/reflexos, energia animada,
iluminação, névoa, oclusão e chuva. A colisão da Fase 1 combina retângulos,
polígonos sólidos e paredes lineares aproximados, definidos em
`game_app/data/maps/terminal_vilar_fase1.json` e compartilhados entre cliente e
servidor.

A rota Flask `/mapas/terminal-vilar-fase1` apresenta a mesma arte e efeitos,
com controles para ligar/desligar ambiente, voltar ao spawn e mostrar as áreas
de depuração. Em conexões locais, **Editar mapa** abre ferramentas para
adicionar, mover, redimensionar, rotacionar e remover colisores retangulares e
ajustar limites de movimento e spawn. O painel não edita polígonos nem paredes;
essas formas devem ser alteradas no JSON. O salvamento exige conexão local e
token CSRF. Partidas abertas precisam ser recarregadas para usar alterações.

A arte e as colisões continuam candidatas: não houve aprovação visual nem
medição de semelhança percentual. A pedido do responsável, a integração v0.139
não foi testada nem inspecionada no navegador; evidências anteriores referem-se
à versão precedente. Nenhuma outra fase foi objeto desta entrega.

### Como usar e editar com qualquer IA

1. **Para integrar em outro protótipo:** use a imagem
   `game_app/static/images/maps/terminal_vilar_fase1.jpg` (1.200 × 896 px) e
   a configuração `game_app/data/maps/terminal_vilar_fase1.json` no mundo
   lógico de 2.400 × 1.800 unidades. A imagem já contém perspectiva; não aplique
   novamente `cos(58°)` ao eixo Y. Recorte a arte conforme o viewport e adapte
   os helpers de colisão ao motor de destino. Neste jogo, arte, configuração e
   efeitos já são consumidos por `game.js` e `terminal-vilar-effects.js`.
2. **Para pedir alterações à IA:** forneça o HTML, a imagem e o JSON atual e
   peça mudanças objetivas, como *“ajuste os ônibus inferiores sem bloquear a
   praça”*, *“suavize a névoa nos cantos”* ou *“reposicione as paredes de
   colisão”*. Mudanças em colisões devem manter `map_geometry.py`, o JSON e os
   consumidores do cliente/servidor consistentes. Trate elementos novos como
   visuais até que colisões e regras correspondentes sejam implementadas.

### Roteiro e diálogos

#### Cena 1 — O Horror no Terminal

O grupo surge no meio do pátio escuro. Das sombras e de dentro dos ônibus da
Viação Roda-Presa, dezenas de pessoas cambaleiam. Seus corpos estalam, as
roupas rasgam com mutações e os olhos brilham com um roxo doentio.

**Guerreiro** (arquejando, recuando um passo ao reconhecer um dos rostos):
— Mano... aquele ali não é o Seu Zé da lanchonete da esquina?! O maluco tá
com o braço triplicado de tamanho e rasgando a própria camisa! Que porra de
bicho é esse?!

**Tecelão** (ajustando os óculos, a voz tremendo de pânico e adrenalina):
— Não são bichos, seu jegue! Os relatórios espectrais tão mostrando
assinatura biológica humana! Entidades espirituais obscuras invadiram o
sistema nervoso central dessa galera! Eles ainda tão dentro dos corpos
mutados!

**Lâmina Arcana** (girando as adagas, com um sorriso tenso e sombrio):
— Caraca... então a gente tá literalmente descerrando a porrada nos moradores
locais que tiveram o corpo sequestrado por capeta cibernético? Pesadíssimo.
Mas se eles vierem pra cima pra arrancar nossa cabeça, eu não vou chorar no
enterro deles, não!

**Caçador** (puxando a corda do arco, suando frio):
— Olha como aquele ali tá se contorcendo... O osso do cara tá saindo pra fora
da pele virando lâmina! Merda, olha aquilo!

De repente, um clarão estelar rasga o céu de Meriti, e uma interface
holográfica flutuante surge na frente de cada um deles, com a voz do sistema
ecoando nos alto-falantes chiados do terminal.

**Voz do Sistema/Servidor** (com eco robótico e distorcido):
— Alerta de Sistema: Sincronização de DNA e Consciência Divina detectada na
Zona 01 (São João de Meriti). Hospedeiros humanos tomados por espíritos do
Vazio. Ah... olá, Operador (Jogador). Suas unidades perceberam sua presença
enquanto fatiam seus vizinhos possuídos. Divirta-se.

**Guerreiro** (olhando para a própria mão brilhando dourada e depois para a
horda avançando):
— Espera... nós somos semi-deuses criados por... por um ser que fica clicando
na tela sentado na cadeira, enquanto a gente desce a lenha na população
virada em monstro?! Mano, eu trabalhava com suporte de TI até três horas
atrás, agora eu sou cabo de enxada cósmico?!

**Tecelão** (sorrindo de nervoso, digitando comandos no ar):
— Estatisticamente macabro! Significa que o livre-arbítrio dessa galera foi
sobrescrito por parasitas dimensionais, e o nosso livre-arbítrio depende de
cliques de um maluco na internet. Genial. Absolutamente trágico, mas genial.

#### Cena de transição — Fechamento da Fase 1

A última horda de mutantes humanos é derrotada, os corpos caem no asfalto e a
energia escura se dissipa de volta para as fendas, deixando o terminal em
silêncio fúnebre.

**Guerreiro** (guardando a espada pesada, olhando para o chão com pesar):
— Caraca... pesado demais, mano. Imagina o susto dessa galera. Se a Fase 1 já
tá nesse nível de terror psicológico, imagina o que a gente vai encontrar lá
no viaduto.

**Lâmina Arcana** (limpando o sangue das adagas):
— Menos drama, guerreiro. A culpa não é nossa, é de quem deixou o servidor
abrir as portas pro inferno. Operador, garante que na próxima fase a nossa
build tá forte, porque eu não quero virar petisco de espírito obscuro mutado,
hein!

## 5. Episódio 2 — Fase 2: “Cuidado com o vão entre o trem... digo, o abismo no viaduto”

### Ficha de Level Design

- **Mapa:** Viaduto da Via Principal — Trecho Meriti, Setor 01.
- **Dimensão proposta:** 2.400 × 1.800; spawn central em (1.200, 900).
- **Ambiente e iluminação:** madrugada densa, neblina baixa subindo do vale;
  linhas geométricas roxas rasgam o céu sobre carcaças de carros engavetados,
  e faróis quebrados piscam em luz fria.
- **Piso:** asfalto elevado rachado, marcas de frenagem e manchas de óleo
  refletindo o céu glitchado.
- **Bordas e referências:** muretas quebradas com vista para um vazio escuro e
  pixelado; caminhões e carros fumegantes bloqueiam as extremidades norte e
  sul. Quatro postes inclinados soltam faíscas; duas placas rodoviárias caídas
  exibem “SAÍDA: ERRO 404” e “VELOCIDADE MÁX: NULL”.
- **Spawn:** trecho livre entre dois carros tombados no meio da pista.
- **Entrada de inimigos:** portas de carros trancados são arrombadas por
  dentro; fendas escuras aparecem sob caminhões nas bordas.
- **Intenção de balanceamento na lore:** nível inicial-intermediário do Ato 1;
  apresenta mutação de fusão metálica, resistência física e ataques de
  investida/arremesso telegrafados. O dano ambiental citado no roteiro é uma
  proposta, não mecânica confirmada.

### Roteiro e diálogos

#### Cena 1 — O Engarrafamento do Inferno

Os quatro protagonistas surgem no meio do viaduto escuro. O vento assobia
entre as carcaças dos carros. De dentro de um sedã amassado, um motorista
começa a gritar enquanto seu braço esquerdo se funde literalmente à porta de
ferro do carro, transformando-se num escudo pontiagudo de carne e lataria.

**Guerreiro** (olhando para a mureta quebrada na beira do viaduto e depois para
a câmera):
— Ô, chefe aí de cima! Tu viu que esse viaduto tá sem guarda-corpo nenhum,
né?! Se tu clicar errado e mandar meu boneco cair nesse abismo roxo aí embaixo,
eu juro que volto como assombração pra queimar tua fonte de alimentação! Cadê
a norma de segurança nessa bagaça?!

**Caçador** (preparando o arco atrás de uma placa caída, apontando para o
sedã):
— Esquece a mureta e olha aquele carro ali! O maluco virou um só com o capô!
A lataria tá crescendo por cima da pele dele igual casca de ferida!

**Tecelão** (ajustando os óculos, analisando a estrutura do mutante):
— Fascinante e completamente nojento! Os espíritos obscuros tão usando a
matéria inorgânica ao redor pra compensar a fragilidade do tecido humano! Ou
seja: a armadura física desses hospedeiros acabou de subir consideravelmente.
Jogador, espero que você não tenha gastado ponto de atributo à toa na Fase 1!

**Lâmina Arcana** (girando as adagas com um sorriso irônico):
— Ih, agora os motoristas da baixada ganharam blindagem de fábrica. Vem cá, ô
lataria ambulante, deixa eu ver se meu dano crítico fura esse funileiro do
capeta!

#### Cena 2 — O Perigo do Abismo e a Bronca no Jogador

A horda aperta o cerco no meio da pista estreita. Um mutante gigante com um
eixo de roda fundido ao braço prepara um ataque telegrafado em área.

**Voz do Sistema/Servidor** (ecoando nos rádios estáticos dos carros
abandonados):
— Alerta de Atualização: Densidade de horda ajustada na Fase 02. Dano de
colisão ambiental ativo. Operador, lembre-se: seus semideuses possuem esquiva,
mas não possuem asas.

**Lâmina Arcana** (deslizando no último segundo antes do golpe):
— Boa, operador! Quase que eu viro panqueca no asfalto! Continua nesse ritmo
que a gente limpa esse engarrafamento rapidinho.

**Guerreiro** (segurando o impacto de dois mutados na linha de frente):
— Rápido nada, tô tankando três latas-velhas aqui! Tecelão, solta logo uma
magia de área antes que a minha barra de vida vire saudade!

**Tecelão** (conjurando enquanto olha para cima):
— Tô esperando o Operador apertar a tecla certa! A mana não se gasta sozinha,
meu consagrado! Clica logo!

#### Cena 3 — O Silêncio Pós-Batalha

O último hospedeiro fundido cai sobre o capô de um caminhão, dissipando a
fumaça roxa. À frente, a rampa de descida do viaduto leva direto para as ruas
estreitas e cobertas de neblina do centro comercial.

**Caçador** (olhando para baixo do viaduto, vendo a névoa cobrindo as tendas
lá embaixo):
— Gente... olha lá embaixo. O Calçadão de São João tá completamente tomado
por aquela fumaça roxa. Se no terminal tinha dezenas e aqui tinha centenas...
lá embaixo vai ser um formigueiro.

**Guerreiro** (suspirando, apoiando a espada no ombro):
— É o horário de pico do apocalipse, parceiro. Bora descer essa rampa antes
que o servidor resolva dar respawn nesse viaduto inteiro. E aí, jogador,
prepara o dedo que na Fase 3 o espaço pra correr vai ser bem menor!

## 6. Episódio 3 — Fase 3: “Promoção relâmpago: leve dois espíritos obscuros, pague com a sua alma”

### Ficha de Level Design

- **Mapa:** Calçadão de São João — Centro, Setor 01.
- **Dimensão proposta:** 2.400 × 1.800; spawn central em (1.200, 900).
- **Ambiente e iluminação:** rua comercial estreita e claustrofóbica, neblina
  roxa densa, vitrines quebradas, letreiros de neon falhando e lonas rasgadas.
- **Piso:** blocos de concreto e lajotas escorregadias, marcados por fuligem e
  resíduos digitais.
- **Bordas e referências:** fachadas de lojas populares com grades retorcidas
  e caixas corrompidas pelo Vazio; quatro postes antigos com alto-falantes
  chiados e duas bancas de jornal destruídas.
- **Spawn:** cruzamento principal do calçadão, em frente à entrada de uma
  galeria comercial abandonada.
- **Entrada de inimigos:** galerias laterais, bueiros estourados e espaço sob
  as lonas das tendas.
- **Intenção de balanceamento na lore:** hordas rápidas e numerosos inimigos
  leves, para testar controle de grupo (Crowd Control) e habilidades de área
  (AoE). A fala sobre densidade 30% maior e a reclamação sobre XP são
  dramáticas, não parâmetros atuais: a EXP segue o orçamento por fase
  documentado em `02_progressao_e_personagens.md`.

### Roteiro e diálogos

#### Cena 1 — O Comércio do Apocalipse

O grupo desce a ladeira e chega ao famoso calçadão central. O lugar, que
costumava ser tomado por pedestres e som de lojistas chamando para promoções,
agora está em silêncio mortal, cortado apenas por estática digital e passos
arrastados. Dezenas de figuras cambaleiam para fora das lojas escuras, com os
corpos esticados e vestimentas rasgadas.

**Guerreiro** (olhando para as vitrines estouradas e recuando o passo):
— Caraca... o calçadão no sábado de manhã já era um inferno de gente, mas
isso aqui superou todas as expectativas. Olha o estado dessas lojas, velho!

**Tecelão** (ajustando os óculos, com uma expressão cética enquanto olha o
painel de status flutuante):
— Atenção aos números, equipe. A densidade de spawn aqui é 30% maior que no
terminal. Os espíritos tão usando os corredores estreitos do comércio pra
funilar a gente. Jogador, se você não posicionar a gente direito agora, a taxa
de mortalidade vai disparar!

**Lâmina Arcana** (girando as adagas com um sorriso afiado):
— Ah, relaxa, nerd. O comércio tá aberto e a liquidação é na base da porrada.
Olha ali na frente, até os manequins da loja de roupa ganharam vida com essa
fumaça roxa. Que bizarria!

**Caçador** (puxando a corda do arco e respirando fundo):
— Menos gracinha e mais foco. Eles tão vindo em massa pelos dois lados da rua.
Sem espaço pra erro de rotação!

#### Cena 2 — A Opressão do Calçadão e a Cobrança de XP

A horda de lojistas e pedestres possuídos aperta o cerco pelas laterais
estreitas do calçadão. As caixas de som das lojas soltam um chiado ensurdecedor
antes de cuspir uma voz robotizada.

**Voz do Sistema/Servidor** (ecoando pelos alto-falantes enferrujados do
comércio):
— Atenção, freguesia: Queima total de estoque de almas na Fase 03. Aproveite
os descontos de HP antes que sua barra chegue a zero.

**Tecelão** (bravo, olhando fixamente para o alto):
— Você tá ouvindo isso, operador?! O sistema ainda tem audácia de fazer piada
com o nosso sofrimento comercial! E o pior: o XP acumulado por abate nesse
corredor estreito tá vindo picotado! Dá uma aliviada na build e solta um dano
em área logo!

**Guerreiro** (desferindo um golpe giratório de espada que empurra três
mutantes para trás):
— Deixa o jogador em paz, Tecelão! Ele tá fazendo o que pode com o mouse
dele! Foca em limpar a retaguarda antes que eu vire cabide nessa loja de
departamento!

**Lâmina Arcana** (esquivando por baixo de um ataque e contra-atacando com
crítico):
— Isso, operador! Bom timing de dash! Se continuar assim, talvez eu não peça
o reembolso da minha classe no próximo patch!

#### Cena 3 — O Fim da Linha Comercial

A última onda de mutantes do calçadão desaba no chão pavimentado,
dissolvendo-se na névoa escura. O caminho à frente se abre em direção às
margens enlameadas do rio local.

**Caçador** (enxugando o suor da testa e guardando a flecha):
— Uf... Essa foi por um triz. O espaço apertado desse calçadão quase sufocou a
gente. Se o piso escorregador pegasse a gente desprevenido, tava todo mundo no
SPC cósmico.

**Guerreiro** (olhando para a placa da rua torcida):
— É... comercialmente falando, o dia foi péssimo. Próxima parada: a beira do
rio. E pelo cheiro de lama podre vindo lá debaixo, preparem as botas, porque a
coisa só vai piorar. Operador, salva o progresso e prepara o dedo, que a Fase
4 vai ser barra limpa... ou melhor, de lama pura!

## 7. Episódio 4 — Fase 4: “Lama, bicho e bitola: bem-vindo ao spa ecológico do Vazio”

### Ficha de Level Design

- **Mapa:** Margens do Rio Pavuna — Setor 01.
- **Dimensão proposta:** 2.400 × 1.800; spawn central em (1.200, 900).
- **Ambiente e iluminação:** manguezal urbano degradado e soturno; falhas
  digitais roxas e verde-doentias no céu, água densa e escura, bioluminescência
  cibernética e resíduos flutuantes.
- **Piso:** lamaçal escorregadio, poças de dejetos tóxicos e trechos de concreto
  afundados.
- **Bordas e referências:** passarelas de madeira podre e corrimãos de ferro
  enferrujados sobre o rio; lixo e entulho digital bloqueiam a saída. Quatro
  estacas de pontes antigas e duas carcaças de eletrodomésticos gigantes
  servem de referências.
- **Spawn:** laje de concreto quebrada, plataforma firme no meio do manguezal.
- **Entrada de inimigos:** lama tóxica nas bordas e área sob as passarelas.
- **Intenção de balanceamento na lore:** mutação aquática/viscosa, resistência
  a lentidão, ataques tóxicos em área e investidas pela lama; a fala propõe
  lentidão de movimento de 15%. Esse percentual e os hazards precisam de
  aprovação e validação antes de serem tratados como mecânica.

### Roteiro e diálogos

#### Cena 1 — O Cheiro da Ruptura

O grupo chega às margens do rio. O ar é pesado, úmido e fétido. A lama
borbulha com faíscas roxas e, de dentro do manguezal escuro, figuras humanas
cobertas de lodo e cabos de fibra óptica começam a se erguer, arrastando-se de
forma grotesca.

**Caçador** (torcendo o nariz e olhando para as próprias botas afundando na
lama):
— Caraca... se o apocalipse já tava fedido no asfalto, aqui na beira do rio
superou todas as expectativas. Minha bota nova já era, virou oferenda pro
Vazio.

**Guerreiro** (segurando a espada pesada e encarando os mutantes saindo do
lodo):
— Reclama não, caçador! Olha o estado daqueles malucos ali na lama! Os caras
fundiram com o lixo do rio e tão vindo com a mó disposição pra cima da gente.
Jogador, pelo amor de Deus, não deixa meu boneco cair nessa poça de lodo
tóxico, senão eu perco até o dignity!

**Tecelão** (ajustando os óculos com uma careta de nojo, olhando o tablet
holográfico):
— Estatisticamente falando, a acidez dessa lama reduz nossa velocidade de
movimento em 15%. Ou seja: se a gente vacilar no espaçamento, vira adubo de
mangue digital. Foca no posicionamento nas lajes secas!

**Lâmina Arcana** (sorrindo de canto, limpando o visor dos óculos):
— Ah, que delícia de spa ecológico. Banho de argola cósmica com direito a
monstro radioativo. Vem cá, zumbi do mangue, deixa eu ver se meu corte rasga
essa lama dura!

#### Cena 2 — A Pressão do Manguezal

A horda avança pelas passarelas de madeira e pela lama. O chão treme
levemente enquanto um mutante maior, com entulho preso ao corpo, surge
rugindo.

**Voz do Sistema/Servidor** (chiando através de um rádio velho boiando no rio):
— Alerta ambiental: Nível de toxicidade elevado na Fase 04. Limpeza de cache
de almas em andamento. Operador, mantenha as unidades fora da lama ou o HP vai
derreter.

**Tecelão** (apontando o dedo para o céu, indignado):
— Você tá ouvindo isso, operador?! O servidor bota um bioma insalubre desses
e ainda reclama que a gente pisa na lama! Joga uma magia de suporte ou um buff
de agilidade aí, senão eu vou refatorar o código da sua interface com um
chute!

**Lâmina Arcana** (esquivando agilmente para uma laje seca e desferindo um
crítico):
— Boa, operador! Essa esquiva foi na pixel-art perfeita! Continua mandando
bem no mouse que a gente sai desse mangue sem pegar leptospirose digital.

**Guerreiro** (bloqueando um golpe pesado com o escudo e cuspindo pro lado):
— Menos papo, mais reflexo! Tem mais bicho saindo debaixo da passarela!
Segura a onda que o bagulho tá louco!

#### Cena 3 — A Travessia do Pântano

O último mutante do manguezal desaba na lama, dissolvendo-se em partículas de
luz roxa que são absorvidas pelo leito do rio. O caminho continua pela margem,
subindo em direção à estrutura imponente do shopping regional ao fundo.

**Caçador** (sacudindo o excesso de lama das pernas, suspirando aliviado):
— Uf... Passamos dessa fossa séptica dimensional. Minha paciência com a
Baixada mutante chegou no limite.

**Guerreiro** (apontando para a silhueta escura do shopping logo adiante):
— Calma que piora, parceiro. Olha lá na frente: o Shopping Regional de
Meriti. E se a gente conhece o padrão desse jogo, lá dentro vai ter chefe de
faturar alto. Operador, recarrega as energias e prepara o loadout, porque a
Fase 5 vai ser de tirar o fôlego!

## 8. Episódio 5 — Fase 5: “Liquidação total de HP: o gerente enlouqueceu”

### Ficha de Level Design

- **Mapa:** Shopping Regional de Meriti — Ruínas, Setor 01.
- **Dimensão proposta:** 2.400 × 1.800; spawn central em (1.200, 900).
- **Ambiente e iluminação:** interior de centro comercial às escuras,
  iluminado por letreiros falhando em roxo e vermelho e por feixes que passam
  pelo teto desabado. Porcelanato coberto de detritos, panfletos rasgados e
  poças de dados estáticos.
- **Piso:** porcelanato escorregadio e rachado; manequins pixelados caídos nas
  laterais.
- **Bordas e referências:** vitrines blindadas estouradas, portas de aço
  retorcidas e escadas rolantes travadas por escombros; quatro pilares
  estruturais revestidos de granito falso e dois quiosques destruídos.
- **Spawn:** átrio principal, diante de uma fonte seca e corrompida.
- **Entrada de inimigos:** lojas laterais e corredores estreitos de acesso ao
  cinema.
- **Chefe e intenção de balanceamento na lore:** primeiro semichefe, o Gerente
  de Segurança Automatizado e Mutado; foco em alvo único, recargas e desvio de
  ataques lineares. O roteiro não aprova dano, HP nem TTK.

### Roteiro e diálogos

#### Cena 1 — O Luxo do Apocalipse

O grupo entra no saguão principal do shopping. O ambiente é silencioso,
abafado e claustrofóbico. No centro do átrio, em cima da fonte seca, um enorme
totem de segurança eletrônica com braços mecânicos gigantes e cabos de rede
enroscados na carne de um ex-funcionário se ergue, emitindo um som metálico e
aterrorizante.

**Guerreiro** (assobiando baixo, olhando para a carcaça do robô-gerente):
— Caraca... olha o naipe do funcionário do mês. O maluco fundiu com a central
de monitoramento do shopping! Se eu soubesse que trabalhar no varejo terminava
em mutação cibernética com tentáculos de fibra óptica, eu tinha virado eremita.

**Tecelão** (ajustando os óculos rapidamente, digitando no ar):
— Alerta máximo de ameaça! Assinatura de Semichefe detectada! Os protocolos
de segurança desse estabelecimento foram corrompidos por uma entidade do
Vazio. A barra de HP dele é grossa, então o Operador vai ter que coordenar
nosso dano focado, senão a gente vai virar estatística de balanço trimestral!

**Lâmina Arcana** (girando as adagas, com um sorriso afiado e irônico):
— Um gerente mutado de shopping? Perfeito. Sempre quis pedir o reembolso da
minha vida em dobro direto no balcão de atendimento. Vem cá, robocop da
Baixada, deixa eu testar meu crítico na tua central de atendimento!

**Caçador** (puxando a corda do arco e buscando cobertura atrás de um quiosque
quebrado):
— Menos piada e mais atenção! Ele tá armando o feixe laser! Espalhem-se pelo
átrio agora!

#### Cena 2 — O Desespero no Corredor das Lojas

O Mini-Chefe dispara rajadas de energia pelas mãos de cabos de aço, destruindo
o chão de porcelanato e forçando o grupo a se mover constantemente entre os
pilares de granito.

**Voz do Sistema/Servidor** (ecoando pelas caixas de som centrais do shopping):
— Atenção, clientes e lojistas: O caixa foi fechado permanentemente.
Preparando limpeza total de inventário na Fase 05.

**Tecelão** (esquivando por pouco de um laser e gritando para o alto):
— Você tá vendo isso, operador?! O chefe tá focando o dano bem na minha build
de papel! Joga uma cura ou um escudo de invulnerabilidade antes que eu vire pó
de pixel!

**Guerreiro** (avançando com o escudo para atrair a atenção do mini-chefe):
— Segura a onda, nerd! Eu tô com o aggro dele! Operador, manda o dash de
recuo pra mim agora! Isso! Boa, excelente timing no mouse!

**Lâmina Arcana** (deslizando por baixo do braço mecânico do chefe e
desferindo uma sequência rápida de golpes):
— Toma essa de brinde, gerentão! O bônus de rescisão vai em formato de aço na
tua fuça!

#### Cena 3 — O Fechamento do Caixa

O Semichefe de Segurança emite um último chiado digital estridente. Sua
estrutura metálica e orgânica implode em partículas de luz roxa, e o grande
letreiro central do shopping desaba com um estrondo.

**Caçador** (enxugando o suor da testa e guardando a flecha):
— Uf... Funcionário do mês mandado direto para o olho da rua. Ou melhor,
direto para o lixo do servidor.

**Guerreiro** (apoiando as mãos nos joelhos, respirando fundo):
— Caraca, se o mini-chefe do shopping deu esse trabalho todo, imagina o que
nos espera lá no cemitério municipal na Fase 6. Operador, dá uma revisada nas
nossas cartas e itens, porque a próxima parada vai ser de arrepiar até os
cabelos da alma!

## 9. Episódio 6 — Fase 6: “Ressurreição sem agendamento: o cemitério virou servidor público”

### Ficha de Level Design

- **Mapa:** Cemitério Municipal do Araruí — Madrugada Sombria, Setor 01.
- **Dimensão proposta:** 2.400 × 1.800; spawn central em (1.200, 900).
- **Ambiente e iluminação:** noite densa e fria; neblina rasteira absorve a
  luz. Lápides de concreto cinzento exibem falhas de código holográficas
  (erros de sintaxe e `NULL`) em lugar de epitáfios; o céu pisca em roxo
  profundo.
- **Piso:** terra batida e lamacenta entre lajes de túmulos rachadas e grama
  seca e cinzenta.
- **Bordas e referências:** muros de alvenaria cobertos por musgo digital e
  portões de ferro retorcidos; quatro mausoléus de família e duas cruzes de
  pedra corrompidas por fibra óptica.
- **Spawn:** pátio principal, diante da capela, onde a terra começa a se
  romper.
- **Entrada de inimigos:** covas se abrem ao redor da arena e liberam mortos-
  vivos com mutações ósseas.
- **Intenção de balanceamento na lore:** segunda metade do Ato 1; inimigos
  necróticos/ósseos com maior alcance corpo a corpo e reanimação parcial de
  lacaios. A mecânica de reanimação é uma proposta narrativa a validar.

### Roteiro e diálogos

#### Cena 1 — A Visita Indesejada

O grupo chega ao pátio do cemitério municipal. O silêncio é cortado pelo som
de brita estalando e terra sendo arremessada para fora das covas. Lápides
começam a brilhar com erros de sistema, e esqueletos cobertos por resíduos
digitais e carne corrompida emergem do subsolo.

**Guerreiro** (engolindo em seco, segurando o escudo com força):
— Mano... eu juro que paguei em dia a taxa de manutenção do jazigo da minha
família, mas pelo jeito o sistema bugou até o pós-vida! Olha esses malucos
saindo debaixo da terra com osso virando lâmina de neon!

**Tecelão** (ajustando os óculos rapidamente, com os olhos vidrados no tablet
holográfico):
— Fascinante! Os espíritos obscuros não tão invadindo só os vivos, eles tavam
acessando o cache profundo do subsolo de Meriti! As assinaturas espectrais
indicam que os corpos enterrados aqui foram recompilados como unidades de
combate. Operador, prepara as magias de área, porque o respawn aqui é em
cadeia!

**Lâmina Arcana** (girando as adagas com um sorriso irônico e macabro):
— Ah, que beleza. O cemitério local virou polo de atendimento 24 horas para
zumbi cibernético. Vem cá, meu antigo vizinho, deixa eu ver se teu esqueleto
aguenta meu crítico adaptado!

**Caçador** (puxando a corda do arco e mirando na primeira horda que avança):
— Menos piada macabra e mais atenção nas covas ao redor. O chão tá afundando
em toda parte. Se a gente cair num buraco desses, o operador vai ter que dar
load save com força!

#### Cena 2 — O Pânico no Mausoléu

A horda de mortos-vivos mutados cerca os heróis por todos os lados. Mausoléus
tremem com a energia do Vazio e avisos digitais vermelhos piscam no ar.

**Voz do Sistema/Servidor** (ecoando de dentro da capela abandonada):
— Alerta de integridade: Violação de diretório no setor cemiterial. Despejo
de arquivos inativos autorizado na Fase 06.

**Tecelão** (gritando indignado enquanto desvia de um esqueleto saltador):
— Você tá ouvindo isso, operador?! O servidor chama os defuntos de “arquivos
inativos”! Joga logo um buff de velocidade ou uma skill de recarga rápida,
porque esses esqueletos tavam na fila do INSS há séculos e tão correndo com
raiva!

**Lâmina Arcana** (esquivando agilmente de um golpe de osso e contra-atacando):
— Boa, operador! Essa esquiva salvou meu coro de virar relíquia arqueológica!
Continua focando o mouse nos esqueletos maiores!

**Guerreiro** (desferindo um golpe pesado que estilhaça um mausoléu frágil):
— Cuidado com o pilar! Não deixa os bichos acuarem a gente contra o muro,
senão o combo deles vai solar o nosso time inteiro!

#### Cena 3 — O Silêncio dos Túmulos

O último esqueleto mutado desaba em uma pilha de ossos e poeira digital, que
se dissolve na névoa rasteira. O cemitério volta a um silêncio fúnebre, exceto
por um portão ao fundo que range ao vento.

**Caçador** (enxugando o suor e guardando a flecha no coldre):
— Uf... Essa foi por pouco. Se a gente demorasse mais um minuto, quem ia virar
morador permanente desse cemitério éramos nós.

**Guerreiro** (olhando para a estrada que sobe em direção aos galpões
industriais):
— Amém por essa vitória. Mas olha o breu daquela estrada ali na frente.
Próxima parada: a Avenida Automóvel e os galpões industriais. Operador,
confere o inventário e as cartas, porque o bicho vai pegar fogo na Fase 7!

## 10. Episódio 7 — Fase 7: “Turno da noite eterno: o relógio de ponto bateu no Vazio”

### Ficha de Level Design

- **Mapa:** Avenida Automóvel — Setor Industrial, Setor 01.
- **Dimensão proposta:** 2.400 × 1.800; spawn central em (1.200, 900).
- **Ambiente e iluminação:** galpões industriais escuros, névoa amarelada e
  estática roxa; asfalto marcado por óleo e resíduos de dados; tambores
  químicos vazios acumulam estática.
- **Piso:** asfalto industrial áspero e oleoso, poças de graxa e marcações
  desbotadas.
- **Bordas e referências:** portões corrugados e cercas eletrificadas por
  falhas de código; quatro pilares metálicos sustentam vigas de aço e duas
  empilhadeiras abandonadas piscam os faróis em loop.
- **Spawn central:** pátio de carga e descarga diante de um relógio de ponto
  eletrônico travado em 03:33 AM.
- **Entrada de inimigos:** galpões escuros e esteiras de carga nas laterais.
- **Intenção de balanceamento na lore:** mutação industrial/mecânica com
  padrões cadenciados de ataque; propõe leitura de ritmo, esquiva e controle
  de fluxo, sem definir velocidade ou intervalo numérico.

### Roteiro e diálogos

#### Cena 1 — O Ponto Eletrônico do Inferno

O grupo chega ao pátio industrial da Avenida Automóvel. O som de engrenagens
rangendo e alarmes de ré distorcidos ecoa no ar. De dentro dos galpões
escuros, dezenas de figuras vestindo uniformes de operário com marcas de
graxa e cabos cibernéticos emergem marchando de forma robótica.

**Guerreiro** (arquejando, olhando para o relógio de ponto gigante travado na
parede):
— Mano... o relógio de ponto ali tá marcando três e trinta e três da manhã
numa segunda-feira eterna. Se isso não é a definição exata de inferno
corporativo, eu não sei o que é. Olha o estado desses operários!

**Tecelão** (ajustando os óculos, digitando freneticamente no tablet
holográfico):
— Alerta de padrão rítmico! Os espíritos obscuros sincronizaram o sistema
nervoso dessa galera com o clock das máquinas industriais abandonadas. Eles
atacam em ciclos exatos de cadência de montagem. Operador, se você não ajustar
nosso espaçamento de acordo com o tempo de recarga deles, a gente vai ser
triturado na linha de produção!

**Lâmina Arcana** (girando as adagas com um sorriso cínico e afiado):
— Operário do mês na base do chicote cibernético? Adoro. Vem cá, turma do
turno da madrugada, deixa eu ver se meu crítico fura esse macacão reforçado!

**Caçador** (puxando a corda do arco, olhando para as empilhadeiras nas
laterais):
— Foco, pessoal! Eles estão vindo em formação fechada pelas esteiras de
carga. Se fechar o cerco aqui no pátio, a gente não vai ter para onde correr!

#### Cena 2 — A Esteira da Destruição

A horda de operários possuídos avança em bloco, desferindo golpes pesados com
chaves inglesas gigantes e barras de ferro fundidas aos braços. O relógio de
ponto na parede emite um som estridente de erro.

**Voz do Sistema/Servidor** (ecoando pelos alto-falantes industriais):
— Atenção, colaboradores: A jornada de trabalho foi estendida para a
eternidade. Produtividade de abate exigida na Fase 07.

**Tecelão** (gritando indignado para o alto enquanto desvia de uma investida):
— Você tá ouvindo isso, operador?! O servidor quer hora extra sem
remuneração e ainda bota os chefes de seção pra bater em a gente! Joga uma
magia de lentidão ou um escudo de área agora, senão meu índice de estresse vai
estourar a tela!

**Lâmina Arcana** (esquivando por baixo de um golpe e contra-atacando com
precisão):
— Boa, operador! Timing de dash impecável na linha de montagem! Continua
focando o mouse nos capatazes da ponta!

**Guerreiro** (bloqueando um golpe de chave inglesa com o escudo e empurrando
o mutante):
— Segura a pressão! Tem mais operário saindo de dentro daquele galpão escuro!
Operador, manda o combo de recarga para o Tecelão solar a retaguarda!

#### Cena 3 — O Fim do Turno

O último operário mutado desaba no asfalto oleoso, desfazendo-se em partículas
de luz roxa que são sugadas pelo relógio de ponto, que finalmente se desliga
com uma fagulha elétrica.

**Caçador** (enxugando o suor e guardando a flecha):
— Uf... Fim de expediente forçado. Se eu passar mais um minuto ouvindo
barulho de engrenagem corrompida, eu vou coringar de vez.

**Guerreiro** (apoiando a espada no ombro e olhando para a estrada que leva a
Éden):
— Bem vindo ao mundo real da Baixada industrial, parceiro. Mas não relaxa
ainda não, porque logo ali na frente fica a subestação de energia de Éden. E
com tanta eletricidade acumulada, a próxima fase vai dar choque até na alma.
Operador, prepara os equipamentos, porque a Fase 8 está logo ali!

## 11. Episódio 8 — Fase 8: “Gato de luz cósmico: a conta de energia veio no débito automático da alma”

### Ficha de Level Design

- **Mapa:** Subestação de Energia de Éden — Setor 01.
- **Dimensão proposta:** 2.400 × 1.800; spawn central em (1.200, 900).
- **Ambiente e iluminação:** pátio elétrico aberto e soturno, torres de alta
  tensão zumbindo com estática, transformadores estourados e faíscas azuis e
  roxas em meio à neblina.
- **Piso:** brita cinzenta e placas de concreto rachadas, atravessadas por
  cabos desencapados que soltam descargas periódicas.
- **Bordas e referências:** grades energizadas por código corrompido e muros
  com placas “PERIGO DE MORTE — VOLTAGEM INFINITA”; quatro transformadores
  cilíndricos vazam óleo e faíscas, e duas torres treliçadas estão inclinadas.
- **Spawn:** plataforma de manutenção de concreto no centro da subestação.
- **Entrada de inimigos:** fendas elétricas nos transformadores e portões de
  serviço laterais.
- **Intenção de balanceamento na lore:** reta final do Ato 1; técnicos
  mutados com ataques elétricos em cadeia e explosão ao morrer. Evitar
  agrupamento e cabos no chão é uma intenção para mecânicas futuras, não uma
  regra já implementada.

### Roteiro e diálogos

#### Cena 1 — O Apagão da Baixada

O grupo entra no pátio da subestação de Éden. O som de alta tensão faz os
cabelos arrepiarem. De trás dos transformadores, antigos técnicos de
manutenção elétrica emergem com bobinas de cobre fundidas às costas e olhos
brilhando como lâmpadas de mercúrio prestes a estourar.

**Guerreiro** (arrepiado, segurando o cabo da espada com cuidado):
— Mano... eu mexia com cabo de rede e rack de servidor, não com subestação de
treze mil volts! Olha o tamanho daquelas bobinas nas costas dos malucos! Se eu
encostar essa espada de ferro aí, eu viro churrasco elétrico na hora!

**Tecelão** (ajustando os óculos, os cabelos levemente arrepiados pela
estática):
— Fascinante e letal! Os espíritos obscuros usaram a rede elétrica de Éden
como condutor neural! Esses hospedeiros agora operam como capacitores humanos:
quando morrem, liberam uma descarga de área. Operador, pelo amor da física,
não manda a gente colar neles na hora do último hit!

**Lâmina Arcana** (girando as adagas enquanto faíscas roxas saltam da lâmina):
— Ah, perfeito. Sempre quis fazer um “gato” de energia direto na fonte do
apocalipse. Vem cá, ô poste ambulante, deixa eu ver se meu corte fecha
curto-circuito nessa tua armadura!

**Caçador** (puxando a corda do arco e apontando para os cabos grossos no
chão):
— Atenção no piso! Aqueles cabos desencapados tão pulsando energia a cada
poucos segundos. Jogador, mantém a movimentação limpa entre os
transformadores!

#### Cena 2 — Sobrecarga no Sistema

A horda de mutantes elétricos avança em alta velocidade, disparando arcos
voltaicos entre si. Um alarme ensurdecedor dispara nos painéis da subestação.

**Voz do Sistema/Servidor** (chiando com interferência eletromagnética):
— Alerta de sobrecarga: Consumo de energia divina excedeu a bandeira
vermelha na Fase 08. Preparando corte de fornecimento vital.

**Tecelão** (gritando para o céu enquanto desvia de um raio em cadeia):
— Bandeira vermelha?! A gente tá salvando o servidor de vocês e ainda querem
cobrar taxa extra na conta de luz?! Operador, solta uma skill de controle ou
atordoamento nesses caras antes que o disjuntor da nossa barra de vida desarme!

**Lâmina Arcana** (usando o Avanço para atravessar um cerco de mutantes sem
tomar choque):
— Boa, operador! Atravessou o cerco no pelo! Só toma cuidado com a explosão
quando eles caírem, hein!

**Guerreiro** (usando conhecimento técnico para gritar instruções no meio do
caos):
— Foca primeiro nos que tão brilhando mais forte! Se eles descarregarem perto
dos transformadores, vai dar reação em cadeia no pátio inteiro!

#### Cena 3 — Disjuntor Desarmado

O último mutante elétrico implode numa nuvem de faíscas azuis. As torres de
alta tensão param de zumbir violentamente, deixando apenas um chiado baixo na
neblina. Ao fundo, a subida íngreme para os morros e ladeiras da região se
revela.

**Caçador** (abaixando o arco, soltando o ar preso):
— Uf... Sobrevivemos sem virar carvão. Meu coração tá batendo na frequência
de sessenta hertz.

**Guerreiro** (olhando para a subida escura e labiríntica logo à frente):
— Menos mal que a gente não pagou a conta desse mês. Mas olha aquela subida
ali... O Complexo de Ladeiras. Beco estreito, morro íngreme e zero
visibilidade. Operador, economiza bem a nossa Mana na Fase 9, porque logo
depois daquele morro vem o chefe do centro!

## 12. Episódio 9 — Fase 9: “Labirinto de laje e glitch: quem subiu o morro sem mapa?”

### Ficha de Level Design

- **Mapa:** Complexo de Ladeiras — Morro Oculto, Setor 01.
- **Dimensão proposta:** 2.400 × 1.800; spawn central em (1.200, 900).
- **Ambiente e iluminação:** ladeiras íngremes e becos estreitos em penumbra;
  fios embolados (“gatos” digitais) soltam faíscas roxas, e o céu dobrado em
  ângulos impossíveis projeta sombras distorcidas nas paredes de tijolo.
- **Piso:** escadarias de concreto gasto e rampas inclinadas com poças e
  entulho digital.
- **Bordas e referências:** muros altos, portões trancados e fachadas de casas
  empilhadas que falham em estática; quatro caixas d'água azuis corrompidas e
  dois postes tortos sustentam transformadores superaquecidos.
- **Spawn central:** largo de concreto (“campinho improvisado”) na subida, na
  convergência de três vielas.
- **Entrada de inimigos:** becos laterais, portas arrombadas e janelas das
  lajes superiores.
- **Intenção de balanceamento na lore:** penúltima fase antes do chefe;
  inimigos de enxame/simbiose formam barreiras vivas. A cena recomenda guardar
  Mana e recargas, sem fixar valores de inimigos ou recursos.

### Roteiro e diálogos

#### Cena 1 — O Labirinto da Gravidade Bugada

O grupo sobe a ladeira íngreme e chega ao largo de concreto no meio do morro.
O ar é sufocante. Nas paredes das casas ao redor, sombras humanas parecem
estar “coladas” ao reboco, descolando-se lentamente com estalos de ossos e
ruídos de modem discado.

**Guerreiro** (arquejando, olhando para o céu dobrado acima das lajes):
— Mano... eu já subi muita ladeira nessa Baixada, mas nunca vi o céu dobrar em
ângulo reto igual origami bugado! E olha aquelas paredes ali: os caras
fundiram um no outro e viraram uma parede de carne e código!

**Tecelão** (ajustando os óculos, olhando o medidor de Mana com expressão
preocupada):
— Alerta crítico de recursos! A geometria espacial aqui tá completamente
distorcida pela proximidade com o núcleo do centro. Mais importante: Operador,
presta atenção na nossa barra de Mana! A gente tá a um passo do topo do
edifício comercial. Se você torrar nossas supremas agora em bicho comum, a
gente vai chegar no chefe da Fase 10 batendo com graveto!

**Lâmina Arcana** (girando as adagas enquanto observa os becos estreitos):
— Ih, agora virou aula de economia doméstica no meio do apocalipse. Relaxa,
nerd, deixa que eu limpo a ralé no ataque básico mesmo. Ô, jogador, economiza
o clique pesado e foca só na movimentação!

**Caçador** (puxando a corda do arco e apontando para as lajes acima):
— Cuidado com o alto! Tem mutante pulando direto das lajes e das caixas
d'água! Não fiquem parados no meio do largo!

#### Cena 2 — O Cerco nas Vielas

Multidões de hospedeiros fundidos avançam pelos três becos simultaneamente,
tentando esmagar o grupo contra os muros de tijolo.

**Voz do Sistema/Servidor** (ecoando com reverberação metálica entre os
becos):
— Aviso de proximidade: Zona de alta densidade populacional corrompida na
Fase 09. Nível de ameaça iminente detectado no setor adjacente.

**Lâmina Arcana** (usando o Avanço para atravessar uma barreira de mutantes
sem gastar Mana extra):
— Isso, operador! Passou liso no meio do cerco! Continua usando o Avanço pra
sair do aperto sem gastar nossas skills principais!

**Guerreiro** (segurando a linha de frente apenas com golpes básicos e
escudo):
— Tô segurando a onda no braço mesmo! Mas ó, se aparecer algum bicho gigante
aí, libera pelo menos uma habilidade de controle antes que eu vire estatística
na ladeira!

**Tecelão** (olhando para cima, apontando o dedo para a interface):
— Disciplina de cooldown, jogador! Pensa no chefe que tá esperando a gente
logo ali no topo!

#### Cena 3 — A Vista do Topo

O último amálgama de mutantes desaba no concreto do largo, desfazendo-se em
partículas roxas. Ao final da última escadaria, uma passarela improvisada leva
diretamente à cobertura do grande Edifício Comercial do Centro, onde uma
tempestade de dados estáticos gira no céu.

**Caçador** (olhando para o céu acima do prédio central, com expressão séria):
— Gente... olha aquilo ali em cima do edifício comercial. O olho do furacão
tá bem ali. Tudo que tá acontecendo em São João de Meriti tá sendo transmitido
daquela cobertura.

**Guerreiro** (respirando fundo, verificando o estado da espada e da armadura):
— É, rapaziada... chegamos no fim da linha do primeiro setor. Quem quer que
esteja gerenciando esse servidor do inferno tá esperando a gente lá em cima.
Operador, confere cada ponto de atributo, cada carta e cada equipamento agora.
Na Fase 10 não tem espaço pra vacilo!

## 13. Episódio 10 — Fase 10: “Tela Azul no Olimpo da Baixada: O Administrador Caiu”

### Ficha de Level Design

- **Mapa:** Topo do Edifício Comercial — Centro, Setor 01.
- **Dimensão proposta:** 2.400 × 1.800; spawn central em (1.200, 900), diante
  da antena principal e do chefe do Ato 1.
- **Ambiente e iluminação:** laje panorâmica no ponto mais alto do centro de
  São João de Meriti. Tempestade de dados estáticos, código roxo e raios
  cibernéticos rasgam o céu; as luzes da Baixada piscam ao longe.
- **Piso:** concreto impermeabilizado e rachado; cabos grossos de fibra óptica
  convergem para uma antena central corrompida.
- **Bordas e referências:** parapeitos baixos, barreira de energia estática
  que impede quedas e causa choque visual ao encostar, além de unidades de
  ar-condicionado retorcidas; quatro
  torres de antenas entrelaçadas com carne e cabos orgânicos, além de duas
  caixas d'água metálicas amassadas.
- **Entrada de inimigos:** fendas nas torres invocam lacaios durante as
  transições do chefe.
- **Chefe e intenção de balanceamento na lore:** encerramento do Ato 1;
  combate longo, ataques de área, escudo de rede e janela de dano. A meta de
  TTK deve seguir o balanceamento vigente, ser validada com o combate real e
  não é fixada por esta ficha.

### Roteiro e diálogos

#### Cena 1 — O Gerente da Ruptura

O grupo sobe os últimos degraus e pisa na cobertura do Edifício Comercial. O
vento forte balança as roupas dos quatro. No centro da laje, flutuando entre
feixes de cabos de rede e carne pulsante, está O Administrador de Rede
Possuído — um antigo engenheiro de sistemas da região cujo corpo foi
grotescamente fundido a racks de servidores, monitores CRT quebrados e
tentáculos de fibra óptica.

**O Administrador de Rede Possuído** (voz distorcida por dezenas de
frequências simultâneas):
— ACESSO... NEGADO... VOCÊS NÃO TÊM PERMISSÃO DE ROOT NESTE MUNICÍPIO! EU
TENTEI CONTER A RUPTURA... EU TENTEI REINICIAR O SERVIDOR DE MERITI... MAS
ELE ENTROU NA MINHA CABEÇA!

**Guerreiro** (empunhando a espada com firmeza, encarando a criatura):
— Caraca... o maluco virou um rack de servidor ambulante! Mano, eu sei que o
plantão de TI na Baixada destrói a saúde mental de qualquer um, mas você levou
o conceito de “vestir a camisa da empresa” longe demais!

**Tecelão** (ajustando os óculos rapidamente, os olhos arregalados ao ler os
dados da aura do chefe):
— Cuidado, pessoal! A assinatura espectral dele tá conectada diretamente com
a fenda no céu! Ele não é só um hospedeiro comum... ele é o roteador principal
que tá mantendo os espíritos obscuros presos nos corpos da população!

**Lâmina Arcana** (girando as adagas com um sorriso sombrio, olhando de
soslaio para a câmera):
— Então derrubar esse bicho limpa o cache da cidade inteira? Perfeito. Ô,
Operador aí em cima: agora é a hora da verdade. Não vai tremer o dedo no mouse
bem na hora do chefe final do Ato 1, hein!

**Caçador** (puxando a corda do arco até o limite):
— Atenção! Ele tá carregando uma sobrecarga nos monitores! Saiam da linha
reta agora!

#### Cena 2 — O Primeiro Grande Plot Twist

Ao atingir metade da barra de vida, o Administrador emite um grito
ensurdecedor que estilhaça os monitores em seu corpo. Uma onda de choque
empurra os heróis para trás, e uma interface holográfica dourada e roxa se
projeta no céu acima da laje, revelando linhas de código de controle.

**O Administrador de Rede Possuído** (rindo de forma macabra e chiada):
— HAHAHA... VOCÊS ACHAM QUE ESTÃO LIVRES?! OLHEM PARA CIMA! OLHEM PARA QUEM
ESTÁ MOVENDO VOCÊS COMO PEÇAS DE TABULEIRO!

**Tecelão** (paralisado por um segundo, lendo as linhas de código projetadas
no céu):
— Espera... o quê?! Gente, olha a assinatura divina do Operador! O protocolo
de controle que tá movendo nossos corpos... tem a mesma assinatura de
criptografia dos Espíritos Obscuros do Vazio!

**Guerreiro** (olhando boquiaberto para cima, para você):
— Peraí... como assim?! Ô, jogador! Tu não era só um maluco aleatório jogando
no PC?! Tu é um dos Deuses que causaram essa bagunça toda?! Fala alguma
coisa, criatura!

**Lâmina Arcana** (apontando a adaga direto para a tela, com um misto de
choque e ironia):
— Ah, pronto! O plot twist de novela das nove! Quer dizer que o “deus do
teclado” que a gente tava zoando desde Vilar dos Teles é na verdade um dos
deuses do Panteão usando a gente de laranja pra limpar a própria sujeira?! Se
a gente sair vivo dessa laje, a gente vai ter uma conversa bem séria!

**Voz do Sistema/Servidor** (ecoando fria e impecável):
— Alerta de segurança: Vazamento de credenciais divinas detectado. Protocolo
de contenção ativado. Elimine a testemunha antes que a sincronização seja
interrompida.

#### Cena 3 — Reinicialização Forçada

Com um golpe final sincronizado das habilidades supremas, o núcleo do
Administrador de Rede explode em um clarão cegante de luz dourada e roxa. Os
cabos de fibra óptica se rompem, e o corpo do antigo engenheiro cai suavemente
no concreto da laje, finalmente livre da possessão.

**Caçador** (abaixando o arco, respirando pesado enquanto a tempestade no céu
recua parcialmente):
— Acabou... O céu sobre o centro tá clareando um pouco. A fenda recuou pro
subsolo!

**Guerreiro** (aproximando-se do corpo do engenheiro caído, fechando os olhos
do homem com respeito):
— Descansa em paz, parceiro. Teu turno finalmente acabou.

**Tecelão** (virando-se lentamente para olhar direto para a câmera, com
expressão séria):
— O sinal dos espíritos obscuros não sumiu, só desceu pras galerias
subterrâneas e pras veias de dados debaixo da Baixada. Mas antes de a gente
descer pra Fase 11... Operador, nós sabemos o que você é agora. Você pode até
controlar nossos cliques, mas a gente tá de olho em você.

**Lâmina Arcana** (guardando as adagas com um meio sorriso desafiador):
— É isso aí, divindade misteriosa. Fechamos o Ato 1. Salva logo esse jogo,
ajusta nossas builds e prepara o psicológico, porque no Ato 2 a gente vai
descobrir a verdade inteira — custe o que custar!

## 14. Continuidade para o Ato 2

O guia deixa estabelecidos estes ganchos para o planejamento das Fases 11 a 20,
primeira etapa do planejamento narrativo ainda pendente das Fases 11 a 30:

- A fenda foi empurrada para as galerias subterrâneas e para as “veias de
  dados” sob a Baixada; não foi destruída.
- O Administrador tentou conter a ruptura e reiniciar o servidor, mas foi
  possuído. Sua queda liberta o engenheiro, não necessariamente as pessoas
  afetadas nem a cidade.
- O Operador e os Espíritos do Vazio compartilham uma assinatura divina/de
  controle. Os protagonistas agora sabem disso e questionam sua agência.
- O próximo arco deve desenvolver consequências e respostas a essa revelação,
  sem invalidar a despedida respeitosa do antigo engenheiro.
- Planejamento de mapas e história deve ocorrer junto do desenho de nível e da
  progressão. O Ato 2 ainda não tem mapas, diálogos, balanceamento ou conteúdo
  declarado como implementado.
