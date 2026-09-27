"""
API Flask — Simulador de Escalonamento de Processos
====================================================
Servidor integrado que executa os algoritmos do backend e serve o frontend.
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
if not os.path.exists(FRONTEND_DIR):
    FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from processo import Processo
from algoritmos import (
    FCFS,
    SJF,
    SRTF,
    PrioridadeNaoPreemptiva,
    PrioridadePreemptiva,
    RoundRobin,
    RoundRobinPrioridadeAging,
)

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

ALGORITMOS = {
    "FCFS":        lambda processos, cfg: FCFS(processos),
    "SJF":         lambda processos, cfg: SJF(processos),
    "SRTF":        lambda processos, cfg: SRTF(processos),
    "PRIO":        lambda processos, cfg: PrioridadeNaoPreemptiva(processos),
    "PRIO_P":      lambda processos, cfg: PrioridadePreemptiva(processos),
    "RR":          lambda processos, cfg: RoundRobin(processos, cfg["quantum"]),
    "RR_PRIO_AGE": lambda processos, cfg: RoundRobinPrioridadeAging(
                                              processos,
                                              cfg["quantum"],
                                              cfg["aging"]
                                          ),
    "Prioridade_Nao_Preemptiva": lambda processos, cfg: PrioridadeNaoPreemptiva(processos),
    "Prioridade_Preemptiva":     lambda processos, cfg: PrioridadePreemptiva(processos),
    "RoundRobin":                lambda processos, cfg: RoundRobin(processos, cfg["quantum"]),
    "RoundRobin_Prioridade_Aging": lambda processos, cfg: RoundRobinPrioridadeAging(
                                              processos,
                                              cfg["quantum"],
                                              cfg["aging"]
                                          ),
}


def parse_processos(lista_json):
    processos = []
    for i, p in enumerate(lista_json):
        id_proc  = p.get("id", f"P{i + 1}")
        chegada  = int(p.get("chegada",   0))
        duracao  = int(p.get("duracao",   1))
        prioridade = int(p.get("prioridade", 0))
        processos.append(Processo(id_proc, chegada, duracao, prioridade))
    return processos


def adaptar_resposta(resultado):
    metricas_backend = resultado.get("metricas", {})

    metricas_frontend = {
        "tempoMedioVida":     metricas_backend.get("tempo_turnaround_medio", 0),
        "tempoMedioEspera":   metricas_backend.get("tempo_espera_medio",     0),
        "trocasContexto":     metricas_backend.get("trocas_contexto",        0),
        "tempoMedioResposta": metricas_backend.get("tempo_resposta_medio",   0),
        "tempoTotalSimulacao": metricas_backend.get("tempo_total_simulacao", 0),
    }

    diagrama = []
    for tick in resultado.get("historico_timeline", []):
        diagrama.append({
            "tempo":            tick["tempo"],
            "processoExecucao": tick["cpu"],
            "filaProntos":      tick.get("fila_prontos", []),
        })

    return {
        "algoritmo": resultado.get("algoritmo", ""),
        "metricas":  metricas_frontend,
        "diagramaTempo": diagrama,
        "processos": resultado.get("processos", []),
    }


@app.route("/")
def index():
    if os.path.exists(FRONTEND_DIR):
        return send_from_directory(FRONTEND_DIR, "index.html")
    return jsonify({"status": "Backend ativo. Pasta frontend não encontrada."})


@app.route("/<path:filename>")
def static_files(filename):
    if os.path.exists(FRONTEND_DIR):
        return send_from_directory(FRONTEND_DIR, filename)
    return jsonify({"erro": "Arquivo não encontrado"}), 404


@app.route("/simular", methods=["POST"])
def simular():
    dados = request.get_json(force=True, silent=True)
    if not dados:
        return jsonify({"erro": "Corpo da requisição inválido ou vazio."}), 400

    algoritmo_key = dados.get("algoritmo")
    if algoritmo_key not in ALGORITMOS:
        return jsonify({
            "erro": f"Algoritmo '{algoritmo_key}' desconhecido. Opções: {list(ALGORITMOS.keys())}"
        }), 400

    lista_json = dados.get("processos", [])
    if not lista_json:
        return jsonify({"erro": "Nenhum processo informado."}), 400

    config = dados.get("config", {})
    try:
        config["quantum"] = int(config.get("quantum", 2))
        config["aging"]   = int(config.get("aging",   1))
    except (ValueError, TypeError):
        config["quantum"] = 2
        config["aging"]   = 1

    try:
        processos  = parse_processos(lista_json)
        escalonador = ALGORITMOS[algoritmo_key](processos, config)
        escalonador.exportar_para_json = lambda *args, **kwargs: None

        resultado   = escalonador.executar()
        resposta    = adaptar_resposta(resultado)
        return jsonify(resposta)
    except Exception as e:
        return jsonify({"erro": f"Erro durante a simulação: {str(e)}"}), 500


if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    print("\n" + "=" * 65)
    print(" 🚀 Simulador de Escalonamento de Processos (SO)")
    print(f" 🌐 Frontend e Backend ativos em: http://localhost:{porta}")
    print("=" * 65 + "\n")
    app.run(host="0.0.0.0", port=porta, debug=True)
