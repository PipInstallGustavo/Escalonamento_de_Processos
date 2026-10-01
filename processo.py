class Processo:
    # Representa um processo usado pelo simulador de escalonamento.

    def __init__(self, id_proc, tempo_chegada, duracao, prioridade=0):
        self.id = str(id_proc)
        self.tempo_chegada = int(tempo_chegada)
        self.duracao = int(duracao)
        self.prioridade = int(prioridade)

        # Estado da execução
        self.tempo_restante = self.duracao
        self.tempo_inicio = None
        self.tempo_fim = None
        self.tempo_resposta = None
        self.tempo_espera = 0
        self.estado = "NOVO"

    def esta_concluido(self):
        return self.tempo_restante <= 0

    def registrar_primeira_execucao(self, tempo):
        # Registra o primeiro instante em que o processo usa a CPU.
        if self.tempo_inicio is None:
            self.tempo_inicio = tempo
            self.tempo_resposta = tempo - self.tempo_chegada

    def finalizar(self, tempo):
        # Finaliza o processo e calcula seu tempo de espera.
        self.tempo_restante = 0
        self.tempo_fim = tempo
        self.estado = "CONCLUIDO"

        turnaround = self.tempo_fim - self.tempo_chegada
        self.tempo_espera = turnaround - self.duracao

    def to_dict(self):
        turnaround = (
            self.tempo_fim - self.tempo_chegada
            if self.tempo_fim is not None
            else None
        )

        return {
            "id": self.id,
            "tempo_chegada": self.tempo_chegada,
            "duracao": self.duracao,
            "prioridade": self.prioridade,
            "tempo_restante": self.tempo_restante,
            "tempo_inicio": self.tempo_inicio,
            "tempo_fim": self.tempo_fim,
            "tempo_resposta": self.tempo_resposta,
            "tempo_espera": self.tempo_espera,
            "tempo_turnaround": turnaround,
            "estado": self.estado,
        }
