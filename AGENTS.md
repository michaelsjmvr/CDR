# Instruções obrigatórias para agentes de IA

> Atualizado em: 15/11/2026 10:07:11 (UTC−03:00).

## Documentação faz parte da entrega

Manter a documentação atualizada é requisito de conclusão para toda tarefa do
projeto, não uma preferência. Antes de trabalhar, leia o Documento Mestre mais
recente e os guias temáticos ligados ao escopo. Para comportamento, regras,
fórmulas, bugs, arquitetura, UX ou validação, atualize na mesma tarefa cada
fonte afetada, incluindo Roadmap, Pendências, Registro de Bugs ou Documento
Mestre quando o estado desses arquivos mudar.

Não pule a documentação por a alteração ser pequena. Verifique a necessidade
de atualização em toda tarefa; se uma tarefa realmente não muda comportamento,
decisão, evidência ou estado, não invente mudanças documentais.

## Precisão e consistência

- Separe claramente o que está implementado, coberto por teste automatizado,
  simulado, exercitado em E2E, validado manualmente ou ainda não validado.
- Trate valores do protótipo como candidatos até haver aprovação explícita.
- Ao atualizar o estado vigente, identifique afirmações antigas como históricas
  ou superadas; não deixe duas especificações incompatíveis parecendo atuais.
- Registre data e hora em UTC−03:00 em cada documento modificado.
- Consulte [`documentacao/09_historico_e_regras_de_documentacao.md`](documentacao/09_historico_e_regras_de_documentacao.md)
  para o processo permanente e siga o índice do Documento Mestre.
- Nunca declare leitura, execução de teste ou validação que não tenha ocorrido.

## Geometria do protótipo

Para dados geométricos do mapa, confirme os valores no código-fonte e mantenha
`documentacao/06_arquitetura_e_integridade.md` como referência técnica atual.
Distinga unidades lógicas do mundo de pixels e de qualquer escala física ainda
não aprovada.
