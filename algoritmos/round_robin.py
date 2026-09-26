from escalonador import EscalonadorBase


class RoundRobin(EscalonadorBase):
    """Round-Robin simples, sem prioridade."""

    def __init__(self, lista_processos, quantum):
        self.quantum = quantum
        super().__init__(lista_processos)

    def executar(self):
        self.reset()
        quantum_restante = 0

        while not self.todos_concluidos():
            self.atualizar_chegadas()

            if self.processo_atual is None and self.fila_prontos:
                processo = self.fila_prontos.pop(0)
                self.iniciar_processo(processo)
                quantum_restante = self.quantum

            self.registrar_historico()
            self.executar_um_tick()

            if self.processo_atual is not None:
                quantum_restante -= 1

            if self.processo_atual and self.processo_atual.esta_concluido():
                self.finalizar_processo_atual()
                quantum_restante = 0

            elif self.processo_atual and quantum_restante == 0:
                processo = self.processo_atual
                processo.estado = "PRONTO"
                self.fila_prontos.append(processo)
                self.processo_atual = None

            self.avancar_relogio()
            self.exportar_para_json(nome_algoritmo="Round-Robin")

        return self.resultado("Round-Robin")


class RoundRobinPrioridadeAging(EscalonadorBase):
    """
    Round-Robin com prioridade e envelhecimento.

    O enunciado especifica que:
    - o envelhecimento ocorre a cada quantum;
    - não existe preempção por prioridade.

    Portanto, a prioridade não interrompe o processo atual.
    Ela influencia a escolha do próximo processo.
    """

    def __init__(self, lista_processos, quantum, aging):
        self.quantum = quantum
        self.aging = aging
        super().__init__(lista_processos)

    def prioridade_efetiva(self, processo):
        """
        Quanto menor o valor, maior a prioridade.

        aging reduz a prioridade efetiva dos processos que
        ficaram esperando.
        """
        return processo.prioridade - processo.aging_aplicado

    def reset(self):
        super().reset()

        for processo in self.processos:
            processo.aging_aplicado = 0

    def aplicar_aging(self):
        if self.aging <= 0:
            return

        for processo in self.fila_prontos:
            processo.aging_aplicado += self.aging

    def escolher_proximo(self):
        return min(
            self.fila_prontos,
            key=lambda p: (
                self.prioridade_efetiva(p),
                p.tempo_restante,
                p.tempo_chegada,
                p.id
            )
        )

    def executar(self):
        self.reset()
        quantum_restante = 0

        while not self.todos_concluidos():
            self.atualizar_chegadas()

            if self.processo_atual is None and self.fila_prontos:
                processo = self.escolher_proximo()
                self.fila_prontos.remove(processo)

                # Ao ser escolhido, o efeito de aging é consumido.
                processo.aging_aplicado = 0

                self.iniciar_processo(processo)
                quantum_restante = self.quantum

            self.registrar_historico()
            self.executar_um_tick()

            if self.processo_atual is not None:
                quantum_restante -= 1

            if self.processo_atual and self.processo_atual.esta_concluido():
                self.finalizar_processo_atual()
                quantum_restante = 0

            elif self.processo_atual and quantum_restante == 0:
                processo = self.processo_atual
                processo.estado = "PRONTO"
                self.fila_prontos.append(processo)
                self.processo_atual = None

                # Aging ocorre ao final de cada quantum.
                self.aplicar_aging()

            self.avancar_relogio()
            self.exportar_para_json(nome_algoritmo="RoundRobin_Prioridade_Aging")

        return self.resultado("Round-Robin + Prioridade + Aging")
