# Itens, inventário e economia

> Guia temático iniciado a partir do Documento Mestre v0.55 e atualizado com decisões posteriores. Consulte `Cronicas_do_Recomeco_Documento_Mestre_v0.139.md` para navegar entre assuntos.
>
> Atualizado em: 15/11/2026 21:54:32 (UTC−03:00).


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

**Nova base de referência:** o responsável enviou uma descrição dos atributos
de armas, armaduras, escudos, asas, pets, montarias e acessórios inspirados em
MU Online. A transcrição organizada e a análise de adaptação estão em
`documentacao/balanceamento/base_enviada_itens_mu_online.md`. Ela amplia os
fatores que precisam entrar no balanceamento, mas seus valores não foram
adotados como estatísticas do nosso jogo.

No balanceamento também deverão entrar dano elemental causado e roubo de
Vida. Dano elemental precisa ser avaliado junto à resistência do alvo; roubo de
Vida deve ser separado de regeneração passiva e recuperação ao eliminar um
monstro. Fontes, fórmulas, limites e interações permanecem pendentes em
`documentacao/balanceamento/base_enviada_itens_mu_online.md`.

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

### 9.4 Coleta de drops por proximidade — proposta para balanceamento

Os drops de equipamento, materiais e Ouro deverão exigir que o jogador se
aproxime. Sem pet, usar como referência o alcance atual de coleta do orbe de
EXP de cartas: **24 unidades do mundo**. No código, isso equivale ao raio do
personagem (13) mais 11 unidades de tolerância, aproximadamente 1,85 raio do
personagem.

Com um pet ativo, propor coleta automática em **72 unidades** (3 vezes o
alcance-base). Para Premium/VIP com pet, propor **108 unidades** (1,5 vez o
alcance do pet e 4,5 vezes o alcance-base). O bônus de alcance VIP não se
aplica sem pet. A distância deve ser medida do centro do personagem até o
drop, e não da posição visual animada do pet, para manter regra estável mesmo
depois da mudança de câmera. Esses são pontos de partida para simulação, não
valores finais: validar tempo de coleta, risco de atravessar áreas perigosas,
densidade de drops e efeito na progressão antes de implementar.

O pet deve recolher automaticamente apenas drops dentro do próprio alcance;
fora dele, o personagem ainda precisa chegar perto. O servidor deverá validar
distância e propriedade no mundo, sem confiar na distância visual informada
pelo cliente. O sistema atual não tem drops de equipamento nem coleta por pet;
somente orbes de EXP de cartas. Esses orbes têm atração visual iniciada até
155 unidades e coleta final a aproximadamente 24 unidades do personagem, regra
separada do alcance futuro dos itens.

Antes de implementar em partidas cooperativas, definir se cada jogador terá
seu drop individual ou se haverá disputa/compartilhamento. A decisão afeta a
justiça do alcance de pet e VIP e permanece em aberto.

------------------------------------------------------------------------

## 10. Persistência de itens, inventário e baú

### 10.1 Regra de persistência

**Decisão definida:** equipamentos, asas, Ouro e joias não deverão
desaparecer simplesmente por causa da morte do personagem ou do encerramento
de uma partida. Não existe Reset de nível.

Os itens conquistados serão mantidos no inventário ou no Baú da Conta,
conforme as regras de armazenamento.

**Distinção obrigatória de termos:**

- **Baú de Recompensa** (baú de missão ou de chefe) é espólio concedido ao
  concluir uma missão. Na resolução da fase, é resgatado para o inventário ou
  descartado do staging. Depois de resgatado, pode ser vendido ou descartado
  no inventário conforme as ações do protótipo. Não serve para armazenar
  outros itens.
- **Baú da Conta** ou **baú de armazenamento** é o depósito compartilhado
  planejado para guardar e organizar itens entre personagens da mesma conta.
  Não é uma recompensa de chefe nem o staging de missão.

  No protótipo, `account_stashes` contém apenas o registro-base da conta; ainda
  não há operações para depositar ou retirar itens. `staging_inventory` é
  separado e mantém os Baús de Recompensa pendentes de resolução.

No P-048, os Baús de Recompensa são representados por registros temporários
em `staging_inventory`; não possuem conteúdo interno nem ação de abertura.
Esse protótipo não implementa o Baú da Conta. Nunca tratar os dois sistemas
como sinônimos.

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

**Distinção de escopo:** o fluxo de missões v0.124 já tem um inventário
temporário de conta, limitado a 30 itens, para demonstrar resolução de baús.
Esse limite é candidato de protótipo e não substitui a capacidade planejada
acima (mochila inicial de 16 espaços e Baú de 24). Equipamentos, slots,
expansões e o Baú persistente ainda não foram implementados.

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
equipado; exibição do saldo de Ouro da conta e validação no servidor de
qualquer gasto futuro. No protótipo, o saldo e a ocupação atual são exibidos
na página `/inventario`. Como o saldo é compartilhado pela conta, não há
depósito nem saque entre personagem e Baú da Conta.

### 10.6 Validação

Toda movimentação deverá ser validada pelo servidor. O cliente não
poderá decidir sozinho se um item existe, se pertence à conta ou se um
slot está desbloqueado.

A validação deverá conferir: - Propriedade do item; - Localização
atual; - Espaço de destino; - Compatibilidade com o equipamento; -
Capacidade desbloqueada; - Quantidade disponível; - Regras de bloqueio e
transação.

### 10.7 Espólios de missão — protótipo P-048

Ao concluir a fase, os baús são gravados em `staging_inventory`, separados da
mochila persistente. O fluxo exige resolver os espólios antes de voltar à Sala
de Espera, independentemente de a mochila estar cheia. A tela permite manter
baús, descartar os antigos ou vendê-los por saldo virtual; o servidor confere
propriedade, IDs da run e capacidade antes da transferência. O botão de
transferência só aceita a seleção se `itens atuais + itens mantidos` não
exceder o limite candidato de 30.

As raridades visuais dos **Baús de Recompensa** são Comum (cinza), Raro (azul),
Épico (roxo) e Lendário (dourado). Elas são uma escala própria do espólio e não substituem a
escala de seis raridades planejada para equipamentos. Fases com encontro comum
na onda 10 concedem um baú Comum/Raro; fases de semichefe elevam a chance de
Raro; fases de chefe concedem dois baús e uma chance por dificuldade de um
terceiro, com pesos candidatos para as quatro raridades. O catálogo de itens
reais ainda não está integrado: nesta etapa, os objetos resgatados são
registros de Baú de Recompensa, não equipamentos nem Baú da Conta. O limite de
30 espaços e os perfis de raridade/recompensa seguem candidatos e não foram
calibrados em combate ativo. Staging pendente em qualquer personagem bloqueia
iniciar outra missão na conta e pausa outras runs até os itens serem resolvidos.

------------------------------------------------------------------------

## 11. Economia do jogo

### 11.1 Moedas e recursos

O projeto já menciona os seguintes recursos:

-   **Ouro:** moeda virtual de jogo, obtida durante as partidas e usada em
    sistemas internos, como a Forja do Caos. O saldo é da conta e compartilhado
    entre seus personagens; não é perdido por morte, encerramento de partida
    ou exclusão de um personagem.
-   **Pontos de Legado:** moeda de meta-progressão recebida por marcos
    de nível, sem Reset ou encerramento de partida.
-   **Gemas Premium:** moeda associada à loja paga, ainda sujeita à
    decisão final sobre monetização.
-   **Joias e materiais:** recursos de aprimoramento e fabricação, não
    necessariamente moedas de uso geral.
-   **Ouro de missão (P-048):** o protótipo credita unidades inteiras de Ouro
    à carteira da conta por abates, bônus de conclusão e venda de espólios.
    Não representa dinheiro real, não pode ser sacado ou convertido e não é
    usado em transações de compra com dinheiro real. Essas operações reais
    deverão usar fluxo e registros separados; os valores de Ouro continuam
    candidatos, não aprovação da economia final.

**Pendente:** fechar a lista oficial de moedas, fontes, usos, limites e
regras de transferência.

### 11.4 Parâmetros candidatos do sistema de missões

Os valores abaixo refletem o código v0.128 para permitir teste e discussão;
não são balanceamento aprovado. O avanço de dificuldade é sequencial:
Risco Baixo → Moderado → Alto → Extremo. O primeiro perfil usa escala 1,0
de Vida/dano; Moderado usa 1,2/1,25 e +1 inimigo; Alto, 1,75/1,8; Extremo,
2,4/2,5. Os níveis Alto e Extremo não adicionam inimigos no protótipo.

| Dificuldade | Ouro base por abate | Bônus da fase (Ouro) | Bônus extra em chefe (Ouro) | Chance de 3º baú em chefe | Pesos de raridade em chefe (C/R/E/L) |
| --- | ---: | ---: | ---: | ---: | --- |
| Risco Baixo | 5 | 100 | 150 | 15% | 75/20/4/1 |
| Risco Moderado | 10 | 200 | 300 | 35% | 58/28/12/2 |
| Risco Alto | 20 | 350 | 500 | 60% | 34/36/25/5 |
| Risco Extremo | 30 | 500 | 800 | 85% | 12/23/40/25 |

Na validação automatizada v0.128, testes determinísticos verificam para os
quatro riscos o Ouro por abate, os bônus de conclusão/chefe, a chance de
terceiro Baú de Recompensa e os pesos usados para sortear suas raridades.
Também conferem as chances de Raro em fase comum e semichefe. Isso valida a
aplicação das configurações do protótipo, não a experiência de combate nem a
calibração ou aprovação da economia.

O drop por monstro soma ao valor base `min(nível inimigo // 10, 100)` Ouro.
Fora de chefes, a chance base de Raro é 15%, elevada a 30% em semichefes;
raridades Épica e Lendária não saem dessas fases no modelo atual. Valores de
venda por baú são 25 / 75 / 200 / 500 Ouro para Comum/Raro/Épico/Lendário.
Esses números, multiplicadores e probabilidades exigem simulação e teste em
combate, avaliação de ritmo e aprovação explícita antes de se tornarem regras.

**Inteiros e migração:** os números inteiros de recompensa permanecem iguais
aos valores brutos do protótipo anterior (por exemplo, o antigo valor `5`
representado como centavos passa a ser `5 Ouro`). Isso não define cotação nem
conversão para dinheiro real. As colunas antigas terminadas em `_cents` são
renomeadas para `_gold` na migração, preservando seus valores numéricos; as
quantias agora são Ouro inteiro e os parâmetros continuam candidatos.

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

**Auto-ataque PvE (P-035): suspenso pela decisão v0.107.** Todo ataque exige
comando explícito do jogador. Não há regras de uso pendentes nem implementação
planejada; só reabrir o tema mediante nova aprovação.

**Auto-poções de Vida e Mana:** implementadas como opção Premium/VIP
individual por personagem. O jogador pode ativar/desativar cada uma; o servidor
faz a ativação em tempo real quando o recurso cruza o limite configurado. O
protótipo não consome unidades porque inventário/estoque de consumíveis ainda
não existe. Limites, recuperação e recargas atuais são valores provisórios e
precisam entrar na simulação de sobrevivência e economia antes de serem finais.

**Pontos que precisam ser definidos:** - Preço, duração e renovação; -
Benefícios exatos; - Se os bônus afetam partidas cooperativas de forma
justa; - Se vantagens de drop serão aplicadas individualmente ou ao
grupo; - Como evitar que a assinatura crie desequilíbrio competitivo; - Regras de
cancelamento, expiração e reembolso, quando aplicáveis.

------------------------------------------------------------------------
