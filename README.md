# Crônicas do Recomeço — protótipo

> Atualizado em: 15/11/2026 21:54:32 (UTC−03:00).

## Estrutura do projeto

```text
.
├── AGENTS.md                      # obrigações para agentes de IA
├── app.py                         # ponto de entrada local
├── game_app/
│   ├── __init__.py                # fábrica e configuração Flask
│   ├── auth.py                    # cadastro, login e logout
│   ├── characters.py              # criar, selecionar, jogar e deletar
│   ├── cards.py                   # catálogo e sorteio de cartas temporárias
│   ├── classes.py                 # classes iniciais e rótulos
│   ├── database.py                # conexão SQLite, opções de conta e personagens
│   ├── attributes.py              # distribuição autenticada de atributos
│   ├── extensions.py              # extensões Flask compartilhadas
│   ├── game.py                    # rotas do jogo que exigem login
│   ├── map_geometry.py            # validação e geometria dos mapas
│   ├── data/maps/terminal_vilar_fase1.json # colisores e limites editáveis
│   ├── mission_system.py          # dificuldades, recompensas e staging dos baús
│   ├── socket_events.py           # eventos autenticados de jogo e opções em tempo real
│   ├── progression.py             # experiência, nível, atributos e marcos de Legado
│   ├── security.py                # tokens CSRF
│   ├── talent_routes.py           # árvore de talentos por personagem
│   ├── talents.py                 # grafo radial e especializações por classe
│   ├── abilities.py               # habilidades-base, passivas e assinaturas
│   ├── templates/
│   │   ├── auth.html              # telas de login e cadastro
│   │   ├── attributes.html        # distribuição de pontos de atributo
│   │   ├── characters.html        # seleção e criação de personagens
│   │   ├── delete_character.html  # confirmação de exclusão
│   │   ├── game.html              # sala do protótipo
│   │   ├── lobby.html             # sala de espera e acesso aos serviços
│   │   ├── post_mission.html      # resumo e resolução de espólios
│   │   ├── inventory.html         # inventário provisório de conta
│   │   └── talents.html           # árvore de talentos
│   ├── static/
│   │   ├── css/styles.css         # estilos
│   │   ├── images/maps/terminal_vilar_fase1.jpg # arte de fundo da Fase 1
│   │   └── js/
│   │       ├── attributes.js      # estimativas e ações de atributos via Socket.IO
│   │       ├── game.js            # controles, mira, câmera, combate e Socket.IO
│   │       ├── terminal-vilar-effects.js # efeitos visuais do mapa da Fase 1
│   │       ├── terminal-vilar-map-editor.js # editor local de colisões/limites
│   │       ├── lobby.js           # interações da Sala de Espera
│   │       ├── lobby-missions.js  # seleção de dificuldade e fase
│   │       ├── mission-resolution.js # modal, capacidade e espólios
│   │       ├── talents.js         # nós e escolha de 1 entre 3 evoluções
│   │       ├── portrait.js        # retratos Canvas compartilhados
│   │       └── vendor/socket.io.min.js # cliente Socket.IO local
│   └── instance/                  # banco e chave local, gerados ao iniciar
├── documentacao/                 # índice, guias temáticos e histórico do projeto
│   ├── Cronicas_do_Recomeco_Documento_Mestre_v0.139.md # índice leve; começar por aqui
│   ├── 01_conceito_e_jogabilidade.md
│   ├── 02_progressao_e_personagens.md
│   ├── 03_itens_e_economia.md
│   ├── 04_multiplayer_e_sala_de_espera.md
│   ├── 05_arte_e_interface.md
│   ├── 06_arquitetura_e_integridade.md
│   ├── 07_roadmap_e_estado_atual.md
│   ├── 08_pendencias_e_decisoes.md
│   ├── 09_historico_e_regras_de_documentacao.md
│   ├── 10_registro_de_bugs_e_regressoes.md
│   ├── 11_lore_historia_e_mapas.md
│   ├── balanceamento/base_enviada_personagens.md # fórmulas recebidas
│   ├── balanceamento/base_enviada_itens_mu_online.md # referência de itens
│   ├── balanceamento/norte_de_balanceamento.md # metas de calibração
│   ├── balanceamento/decisoes_aprovadas.md # direção oficial aprovada
│   └── balanceamento/auditoria_e_primeira_simulacao.md # auditoria e resultados
├── tests/                          # regressões automatizadas; veja tests/README.md
├── package-lock.json               # versões fixadas para os testes Playwright
├── package.json                    # testes JS com Playwright
├── scripts/split_master_document.py # recria os guias a partir da fonte integral
├── scripts/simulate_balance_model.py # simula fórmulas sem alterar o jogo
└── requirements.txt
```

## Documentação do projeto

> Atualizado em: 15/11/2026 21:54:32 (UTC−03:00).

Os documentos do projeto estão em [`documentacao/`](documentacao/Cronicas_do_Recomeco_Documento_Mestre_v0.139.md). Comece pelo índice mestre e consulte o guia temático correspondente à tarefa. A base integral v0.55 está preservada em `documentacao/historico/`; as mudanças posteriores constam nos guias e no histórico de versões.

## Regra obrigatória para agentes de IA

A documentação é parte obrigatória da entrega, não uma etapa opcional de
polimento. Agentes devem seguir [`AGENTS.md`](AGENTS.md), consultar as fontes
temáticas antes de alterar o jogo e atualizar, na mesma tarefa, os documentos
afetados por mudanças de comportamento, decisões, bugs, validações ou estado.

## Progressão atual

Na Temporada 1, o personagem percorre 30 fases em três atos. A direção decidida
é alterar o teto-alvo para 170 e rebalancear XP, Pontos de Legado e combate, mas
a mudança ainda está pendente: o código continua em 400. A projeção anterior
de nível 170/26 PL e as simulações até 400 são resultados do modelo antigo,
não metas finais nem validação do novo equilíbrio. Nenhuma nova fórmula ou
recompensa foi aprovada. Na implementação atual, um caminho da árvore pode ser
concluído até o nível 400; a curva de PL será recalculada para a meta 170.
A árvore oferece passivas e habilidades
assinaturas para as 12 evoluções, com talentos próprios e efeitos conectados ao
combate. A passiva ativa ao escolher o caminho; a habilidade do talento
principal (4 PL) substitui a habilidade-base. Um caminho custa 58 ou 64 PL e
pode ser concluído até o nível 400. Regressões de progressão, talentos e
habilidades são verificadas pela suíte em `tests/`.

O protótipo também inclui quatro dificuldades em cascata, contagem regressiva
inicial de 5 segundos, Ouro inteiro compartilhado pela conta, baús por raridade e
inventário temporário de staging obrigatório após a fase. Baú de Recompensa
(missão/chefe) é espólio; Baú da Conta é armazenamento compartilhado planejado.
São funções distintas. As quantias seguem candidatas sem aprovação final;
Ouro não tem valor real, saque ou conversão. A suíte v0.128 passou com 82
testes, incluindo cobertura determinística dos quatro perfis e do HTML do lobby.
Na v0.130, três verificações JavaScript passaram: sintaxe dos scripts do
cliente e dois fluxos executados em Chromium com Playwright (seleção de fase e
capacidade/modal de espólios). Os fluxos usam HTML de teste; não carregam o
Flask, Socket.IO ou uma sessão autenticada.
Na v0.131, a suíte Python passou com 84 testes e `compileall` sem erros;
foram adicionadas regressões para missões simultâneas em personagens diferentes
e espólios pendentes entre sessões. Os valores de balanceamento continuam
candidatos, sem validação em combate ativo ou aprovação.
Na atualização documental v0.132, a suíte Python foi reexecutada: 84 testes
passaram e `compileall` concluiu sem erros. A suíte JavaScript não foi
reexecutada porque Node.js/npm não estão disponíveis nesta sessão; a última
execução registrada permanece a v0.130.

Na v0.133 (snapshot histórico, parcialmente superado pela v0.134),
`npm run test:js` passou com sete testes em Node.js 24.20.0 e
Chromium; o runtime preexistente foi executado pelo caminho local do cache
WinGet, sem instalação. O conjunto agora inclui E2E do Flask/Socket.IO real
para combate inicial nos riscos Moderado, Alto e Extremo, e resolução de
inventário cheio por venda e resgate. A suíte Python passou com 84 testes e
`compileall` sem erros. Esses E2E não concluem uma fase completa nos outros
riscos, não avaliam combate prolongado e não calibram os parâmetros candidatos.
O código de gameplay não foi alterado.

Na v0.134, três E2E adicionais percorreram a Fase 10 em Moderado, Alto e
Extremo até derrotar o chefe e chegar à tela pós-fase. Cada cenário durou
aproximadamente 66–80 segundos e observou dano inimigo. O harness semeou os
desbloqueios, usou nível 400, atributos no teto de 10.000 e coordenadas de alvo;
portanto, não é uma avaliação representativa de movimento, mira, esquiva ou
equilíbrio. `npm run test:js` passou com 10 testes; a suíte Python passou com
84 e `compileall` sem erros. A simulação de balanceamento também foi executada,
mas não aprova os valores candidatos. A avaliação manual e a decisão sobre os
parâmetros continuam pendentes do responsável.

O E2E v0.125 no navegador percorreu as dez ondas da Fase 10,
derrotou o chefe e resgatou três baús em banco descartável; o progresso das
Fases 1–9 foi pré-carregado para liberar a fase, e atributos/coordenadas do
harness aceleraram os ataques. Movimento, mira manual, IA e calibração em
combate representativo não foram validados por aquela execução. Em v0.133,
movimento por teclado e dano inimigo foram exercitados somente no combate
inicial; mira manual e gameplay representativo continuam pendentes (P-048).
O lobby mostra os perfis
candidatos dos quatro riscos; os testes confirmam suas escalas, recompensas e
raridades. A cobertura E2E autenticada v0.133 percorria a primeira onda nos
riscos Moderado/Alto/Extremo e a resolução de inventário cheio; a conclusão
integral nessas dificuldades foi acrescentada na v0.134, sem validação visual
manual.
A compra com dinheiro real
será separada da carteira e do ledger de Ouro.
Na Sala de Espera, as fases estão agrupadas por ato; o saldo e a ocupação da
mochila são exibidos na página Inventário. A tela v0.127 foi verificada por
testes de rota, não por novo E2E visual autenticado.

## Testes automatizados

Execute do diretório raiz após mudanças de comportamento:

```powershell
python -m unittest discover -s tests -v
npm run test:js
```

Os testes JavaScript requerem Node.js 20 ou superior. Na primeira execução,
instale as dependências e o Chromium do Playwright:

```powershell
npm install
npx playwright install chromium
```

Instruções para adicionar cenários e interpretar a cobertura estão em
[`tests/README.md`](tests/README.md). Atualize a suíte junto com cada nova
funcionalidade ou correção; não dependa de testes manuais repetitivos.

## Executar localmente

Requer Python 3.10 ou mais recente. No PowerShell, a partir desta pasta:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000`, entre ou crie uma conta e selecione um
personagem para jogar. O banco e a chave local de sessão são criados
automaticamente dentro de `game_app/instance/`.

O cadastro local pede nome de usuário e senha. As senhas são armazenadas
em formato de hash. Este protótipo não inclui recuperação de senha nem
limitação de tentativas de login. Para publicar online, configure uma
chave secreta própria em `CRONICAS_SECRET_KEY`, sirva por HTTPS e defina
`CRONICAS_COOKIE_SECURE=1`.









