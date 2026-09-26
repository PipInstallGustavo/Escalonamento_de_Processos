# def carregar_config(caminho="config.txt"):
#     """Lê quantum e taxa de envelhecimento do arquivo de configuração."""
#     config = {}

#     with open(caminho, "r", encoding="utf-8") as arquivo:
#         for numero_linha, linha in enumerate(arquivo, start=1):
#             linha = linha.strip()

#             if not linha or linha.startswith("#"):
#                 continue

#             if ":" not in linha:
#                 raise ValueError(
#                     f"Configuração inválida na linha {numero_linha}: {linha}"
#                 )

#             chave, valor = linha.split(":", 1)
#             chave = chave.strip()
#             valor = valor.strip()

#             try:
#                 config[chave] = int(valor)
#             except ValueError:
#                 raise ValueError(
#                     f"Valor inválido para '{chave}' na linha {numero_linha}."
#                 )

#     if "quantum" not in config:
#         raise ValueError("A configuração precisa conter 'quantum'.")

#     if "aging" not in config:
#         raise ValueError("A configuração precisa conter 'aging'.")

#     if config["quantum"] <= 0:
#         raise ValueError("O quantum deve ser maior que zero.")

#     if config["aging"] < 0:
#         raise ValueError("O aging não pode ser negativo.")

#     return config


from pathlib import Path


def carregar_config(caminho=None):
    """Lê quantum e taxa de envelhecimento do arquivo de configuração."""

    if caminho is None:
        caminho = Path(__file__).resolve().parent / "config.txt"
    else:
        caminho = Path(caminho)

    config = {}

    with open(caminho, "r", encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            linha = linha.strip()

            if not linha or linha.startswith("#"):
                continue

            if ":" not in linha:
                raise ValueError(
                    f"Configuração inválida na linha {numero_linha}: {linha}"
                )

            chave, valor = linha.split(":", 1)
            chave = chave.strip()
            valor = valor.strip()

            try:
                config[chave] = int(valor)
            except ValueError:
                raise ValueError(
                    f"Valor inválido para '{chave}' na linha {numero_linha}."
                )

    if "quantum" not in config:
        raise ValueError("A configuração precisa conter 'quantum'.")

    if "aging" not in config:
        raise ValueError("A configuração precisa conter 'aging'.")

    if config["quantum"] <= 0:
        raise ValueError("O quantum deve ser maior que zero.")

    if config["aging"] < 0:
        raise ValueError("O aging não pode ser negativo.")

    return config