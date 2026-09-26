from config import carregar_config
from entrada import ler_processos_stdin

from algoritmos import (
    FCFS,
    SJF,
    SRTF,
    PrioridadeNaoPreemptiva,
    PrioridadePreemptiva,
    RoundRobin,
    RoundRobinPrioridadeAging,
)


def imprimir_resultado(resultado):
    print("\n" + "=" * 70)
    print(resultado["algoritmo"])
    print("=" * 70)

    metricas = resultado["metricas"]

    print(f"Tempo médio de espera: "
          f"{metricas['tempo_espera_medio']:.2f}")
    print(f"Tempo médio de turnaround: "
          f"{metricas['tempo_turnaround_medio']:.2f}")
    print(f"Tempo médio de resposta: "
          f"{metricas['tempo_resposta_medio']:.2f}")
    print(f"Trocas de contexto: "
          f"{metricas['trocas_contexto']}")
    print()

    print("Diagrama de execução:")
    print("Tempo | CPU | Fila de Prontos")

    for tick in resultado["historico_timeline"]:
        fila = ", ".join(tick["fila_prontos"])
        print(
            f"{tick['tempo']:>5} | "
            f"{tick['cpu']:<3} | "
            f"{fila}"
        )

    print("\nProcessos:")
    for processo in resultado["processos"]:
        print(
            f"{processo['id']}: "
            f"início={processo['tempo_inicio']}, "
            f"fim={processo['tempo_fim']}, "
            f"espera={processo['tempo_espera']}, "
            f"turnaround={processo['tempo_turnaround']}, "
            f"resposta={processo['tempo_resposta']}"
        )


def executar_algoritmos(processos, config):
    algoritmos = [
        FCFS(processos),
        SJF(processos),
        SRTF(processos),
        PrioridadeNaoPreemptiva(processos),
        PrioridadePreemptiva(processos),
        RoundRobin(processos, config["quantum"]),
        RoundRobinPrioridadeAging(
            processos,
            config["quantum"],
            config["aging"]
        ),
    ]

    resultados = []

    for algoritmo in algoritmos:
        resultado = algoritmo.executar()
        resultados.append(resultado)
        imprimir_resultado(resultado)

    return resultados


# def main():
#     try:
#         config = carregar_config()
#         processos = ler_processos_stdin()

#         if not processos:
#             print("Nenhum processo foi informado.")
#             return

#         resultados = executar_algoritmos(processos, config)

#         print("\nSimulação concluída com sucesso.")

#     except FileNotFoundError:
#         print("Erro: arquivo config.txt não encontrado.")

#     except ValueError as erro:
#         print(f"Erro de entrada/configuração: {erro}")


# if __name__ == "__main__":
#     main()



def main():
    try:
        config = carregar_config()
    except FileNotFoundError:
        print("Erro: arquivo config.txt não encontrado.")
        return
    except ValueError as erro:
        print(f"Erro de configuração: {erro}")
        return

    try:
        processos = ler_processos_stdin()
    except ValueError as erro:
        print(f"Erro de entrada: {erro}")
        return

    if not processos:
        print("Nenhum processo foi informado.")
        return

    try:
        executar_algoritmos(processos, config)
    except Exception as erro:
        print(f"Erro durante a simulação: {erro}")
        raise

    print("\nSimulação concluída com sucesso.")


if __name__ == "__main__":
    main()
