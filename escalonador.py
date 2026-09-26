import copy
import json


class EscalonadorBase:
    """
    Classe base para os algoritmos de escalonamento.

    Mantém:
    - processos;
    - fila de prontos;
    - relógio;
    - processo atual;
    - histórico da CPU;
    - trocas de contexto;
    - métricas.
    """

    def __init__(self, lista_processos):
        self.processos_originais = lista_processos
        self.reset()

    def reset(self):
        self.processos = [
            copy.deepcopy(p) for p in self.processos_originais
        ]
        self.relogio = 0
        self.fila_prontos = []
        self.processo_atual = None
        self.ultimo_processo_id = None
        self.trocas_contexto = 0
        self.historico = []

    def atualizar_chegadas(self):
        """Coloca na fila os processos que chegaram no instante atual."""
        for processo in self.processos:
            if (
                processo.tempo_chegada <= self.relogio
                and processo.estado == "NOVO"
            ):
                processo.estado = "PRONTO"
                if processo not in self.fila_prontos:
                    self.fila_prontos.append(processo)

    def registrar_troca_contexto(self, proximo_processo):
        """
        Conta uma troca somente quando a CPU passa diretamente
        de um processo para outro.

        A primeira execução não conta como troca.
        """
        if (
            self.ultimo_processo_id is not None
            and self.ultimo_processo_id != proximo_processo.id
        ):
            self.trocas_contexto += 1

        self.ultimo_processo_id = proximo_processo.id

    def iniciar_processo(self, processo):
        self.registrar_troca_contexto(processo)

        self.processo_atual = processo
        processo.estado = "EXECUTANDO"
        processo.registrar_primeira_execucao(self.relogio)

    def executar_um_tick(self):
        """Executa exatamente um segundo do processo atual."""
        if self.processo_atual is None:
            return

        self.processo_atual.tempo_restante -= 1

    def finalizar_processo_atual(self):
        if self.processo_atual is None:
            return

        if self.processo_atual.esta_concluido():
            self.processo_atual.finalizar(self.relogio + 1)
            self.processo_atual = None

    def registrar_historico(self):
        self.historico.append({
            "tempo": self.relogio,
            "cpu": (
                self.processo_atual.id
                if self.processo_atual is not None
                else "IDLE"
            ),
            "fila_prontos": [
                p.id for p in self.fila_prontos
            ],
        })

    def todos_concluidos(self):
        return all(
            processo.esta_concluido()
            for processo in self.processos
        )

    def avancar_relogio(self):
        self.relogio += 1

    def obter_metricas(self):
        if not self.processos:
            return {}

        turnarounds = [
            p.tempo_fim - p.tempo_chegada
            for p in self.processos
            if p.tempo_fim is not None
        ]

        esperas = [p.tempo_espera for p in self.processos]
        respostas = [
            p.tempo_resposta
            for p in self.processos
            if p.tempo_resposta is not None
        ]

        return {
            "trocas_contexto": self.trocas_contexto,
            "tempo_total_simulacao": self.relogio,
            "tempo_espera_medio": round(
                sum(esperas) / len(esperas), 2
            ),
            "tempo_turnaround_medio": round(
                sum(turnarounds) / len(turnarounds), 2
            ) if turnarounds else 0,
            "tempo_resposta_medio": round(
                sum(respostas) / len(respostas), 2
            ) if respostas else 0,
        }

    def resultado(self, nome_algoritmo):
        return {
            "algoritmo": nome_algoritmo,
            "metricas": self.obter_metricas(),
            "processos": [
                p.to_dict() for p in self.processos
            ],
            "historico_timeline": self.historico,
        }

    def exportar_para_json(
        self,
        nome_algoritmo,
        caminho_arquivo="resultados/simulacao_output"
    ):
        dados = self.resultado(nome_algoritmo)

        with open(caminho_arquivo+f"_{nome_algoritmo}.json", "w", encoding="utf-8") as arquivo:
            json.dump(
                dados,
                arquivo,
                indent=4,
                ensure_ascii=False
            )

        return dados

    @staticmethod
    def desempate(processo, melhor, chave):
        """
        Implementa a ideia geral do enunciado:
        1. mantém o processo que já está executando quando possível;
        2. depois usa a chave do algoritmo;
        3. usa chegada e ID apenas como desempates determinísticos.

        A decisão de manter a CPU deve ser feita antes desta função
        quando houver preempção.
        """
        if melhor is None:
            return True

        valor_processo = chave(processo)
        valor_melhor = chave(melhor)

        if valor_processo != valor_melhor:
            return valor_processo < valor_melhor

        if processo.tempo_chegada != melhor.tempo_chegada:
            return processo.tempo_chegada < melhor.tempo_chegada

        return processo.id < melhor.id
