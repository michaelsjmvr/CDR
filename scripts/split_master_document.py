"""Split the approved master document into topic guides without discarding the source."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "documentacao"
SOURCE = DOCS / "historico" / "Cronicas_do_Recomeco_Documento_Mestre_v0.55.md"
ARCHIVE = SOURCE

GROUPS = [
    ("01_conceito_e_jogabilidade.md", "Conceito e jogabilidade", range(2, 6)),
    ("02_progressao_e_personagens.md", "Personagens e progressão", range(6, 8)),
    ("03_itens_e_economia.md", "Itens, inventário e economia", range(8, 13)),
    ("04_multiplayer_e_sala_de_espera.md", "Multiplayer e recursos sociais", range(13, 14)),
    ("05_arte_e_interface.md", "Arte e interface", range(14, 16)),
    ("06_arquitetura_e_integridade.md", "Arquitetura e integridade", range(16, 18)),
    ("07_roadmap_e_estado_atual.md", "Roadmap e estado atual", range(18, 19)),
    ("08_pendencias_e_decisoes.md", "Pendências e decisões", range(19, 21)),
    ("09_historico_e_regras_de_documentacao.md", "Histórico e regras de documentação", range(21, 24)),
]


def main():
    source_text = SOURCE.read_text(encoding="utf-8")
    DOCS.mkdir(exist_ok=True)
    ARCHIVE.parent.mkdir(exist_ok=True)
    ARCHIVE.write_text(source_text, encoding="utf-8")

    # Top-level numbered sections are the source units. Any text after section 23
    # (including later appended version entries) stays attached to the history file.
    matches = list(re.finditer(r"(?m)^## (\d+)\. .+$", source_text))
    sections = {}
    for index, match in enumerate(matches):
        number = int(match.group(1))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source_text)
        sections[number] = source_text[match.start():end].strip()

    index_text = """# Crônicas do Recomeço — Documento Mestre v0.57

Este é o índice leve da documentação. Leia primeiro este arquivo e depois
abra apenas o guia do assunto da tarefa. O conteúdo integral da versão
anterior foi preservado em `historico/Cronicas_do_Recomeco_Documento_Mestre_v0.55.md`.

## Como escolher o documento

| Tarefa | Documento |
| --- | --- |
| Conceito, câmera, classes, ondas, chefes, combate | [Conceito e jogabilidade](01_conceito_e_jogabilidade.md) |
| Personagens, atributos, cartas, Reset, Legado e Talentos | [Personagens e progressão](02_progressao_e_personagens.md) |
| Equipamentos, raridades, inventário, baú, moedas e loja | [Itens, inventário e economia](03_itens_e_economia.md) |
| Sala de Espera, grupos, amigos, convites, trade e PvP | [Multiplayer e recursos sociais](04_multiplayer_e_sala_de_espera.md) |
| Direção de arte, paleta, HUD, menus e acessibilidade | [Arte e interface](05_arte_e_interface.md) |
| Flask, SQLite, Socket.IO, segurança e integridade | [Arquitetura e integridade](06_arquitetura_e_integridade.md) |
| Etapas, validação, ponto de retomada e próxima etapa | [Roadmap e estado atual](07_roadmap_e_estado_atual.md) |
| Questões sem resposta e decisões que precisam de aprovação | [Pendências e decisões](08_pendencias_e_decisoes.md) |
| Registro completo de versões e como atualizar a documentação | [Histórico e regras](09_historico_e_regras_de_documentacao.md) |

## Regras de manutenção

- Atualize o guia temático afetado e o roadmap quando uma implementação mudar o estado de uma tarefa.
- Registre decisões aprovadas no guia temático e no histórico.
- Não converta ideias em regras aprovadas sem autorização do responsável.
- Preserve o histórico antigo; não apague decisões substituídas, registre a mudança e o motivo.
- Ao iniciar uma tarefa, leia este índice, o guia indicado e os arquivos de código relacionados.

## Estado consolidado na divisão

- O responsável informa que os recursos implementados até aqui foram testados e aprovados.
- 1 Ponto de Legado é concedido por Reset.
- Balanceamento dos atributos e da Árvore de Talentos será feito em conjunto; valores e limites de talentos seguem pendentes.
- Redistribuição de talentos será grátis para VIP e custará Ouro para contas comuns; o valor ainda precisa ser definido.
- Próxima tarefa registrada: P-025, apresentação dos elementos/resistências dos chefes e estados de combate.
- Busca social, amizades, convites, grupos e chat continuam sem backend.

## Fonte integral anterior

O arquivo em `historico/` mantém a versão v0.55 completa, sem cortes, para consulta e auditoria. Os guias temáticos abaixo foram extraídos das seções numeradas correspondentes; o histórico integral permanece preservado.
"""
    index_text += "\n\n" + sections.get(1, "") + "\n"
    (DOCS / "Cronicas_do_Recomeco_Documento_Mestre_v0.57.md").write_text(index_text, encoding="utf-8")

    for filename, title, numbers in GROUPS:
        content = [f"# {title}\n\n> Guia temático extraído do Documento Mestre v0.55. Consulte `Cronicas_do_Recomeco_Documento_Mestre_v0.57.md` para navegar entre assuntos.\n"]
        for number in numbers:
            if number in sections:
                content.append(sections[number])
        if filename.startswith("09_"):
            # Appended version entries that followed section 23 in the source are
            # already included in section 23's captured tail.
            pass
        (DOCS / filename).write_text("\n\n".join(content).rstrip() + "\n", encoding="utf-8")

    # Check that every numbered source section has exactly one thematic destination.
    assigned = [number for _, _, numbers in GROUPS for number in numbers]
    expected = set(range(2, 24))
    if set(assigned) != expected:
        raise RuntimeError(f"Unassigned source sections: {sorted(expected - set(assigned))}")
    if len(assigned) != len(set(assigned)):
        raise RuntimeError("A source section was assigned more than once")


if __name__ == "__main__":
    main()
