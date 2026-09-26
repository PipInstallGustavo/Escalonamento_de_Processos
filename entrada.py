import sys
from processo import Processo


def ler_processos_stdin():
    """
    Lê processos da entrada padrão.

    Cada linha deve possuir:
        instante_de_chegada duracao prioridade
    """
    processos = []

    for numero_linha, linha in enumerate(sys.stdin, start=1):
        linha = linha.strip()

        if not linha:
            continue

        partes = linha.split()

        if len(partes) != 3:
            raise ValueError(
                f"Linha {numero_linha}: esperado 'chegada duracao prioridade'."
            )

        try:
            chegada, duracao, prioridade = map(int, partes)
        except ValueError:
            raise ValueError(
                f"Linha {numero_linha}: todos os valores devem ser inteiros."
            )

        if chegada < 0:
            raise ValueError(f"Linha {numero_linha}: chegada não pode ser negativa.")

        if duracao <= 0:
            raise ValueError(f"Linha {numero_linha}: duração deve ser maior que zero.")

        if prioridade < 0:
            raise ValueError(f"Linha {numero_linha}: prioridade deve ser positiva.")

        id_proc = f"P{len(processos) + 1}"
        processos.append(
            Processo(id_proc, chegada, duracao, prioridade)
        )

    return processos
