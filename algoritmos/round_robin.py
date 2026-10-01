from escalonador import EscalonadorBase


class RoundRobin(EscalonadorBase):
    # Round-Robin simples, sem prioridade.

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
    # Round-Robin com prioridade e envelhecimento (aging)

    def __init__(self, lista_processos, quantum, aging):
        self.quantum = quantum
        self.aging = aging
        super().__init__(lista_processos)


    def reset(self):
        super().reset()
        # Cada processo recebe um contador de aging acumulado.
        for processo in self.processos:
            processo.aging_aplicado = 0

    def prioridade_efetiva(self, processo):
        """
        Quanto menor o valor, maior a prioridade.

        O aging acumulado reduz a prioridade efetiva.
        O valor mínimo é 0 (não permite prioridades negativas).
        """
        efetiva = processo.prioridade - processo.aging_aplicado
        return max(efetiva, 0)


    def aplicar_aging(self, processo_excluido=None):
        """
        Aplica aging em todos os processos que estão na fila de prontos,
        EXCETO no processo que acabou de executar (se informado).

        O aging NÃO é aplicado no processo atual que está executando,
        pois ele não está esperando.
        """
        if self.aging <= 0:
            return

        for processo in self.fila_prontos:
            if processo is processo_excluido:
                continue
            processo.aging_aplicado += self.aging

    def escolher_proximo(self):
        """
        Escolhe o processo com menor prioridade efetiva.
        Desempate:
            1. menor tempo restante
            2. menor tempo de chegada
            3. menor ID
        """
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
        ticks_desde_ultimo_aging = 0

        while not self.todos_concluidos():
            self.atualizar_chegadas()

            # Escolhe um processo se a CPU estiver livre
            if self.processo_atual is None and self.fila_prontos:
                processo = self.escolher_proximo()
                self.fila_prontos.remove(processo)
                # NÃO reseta aging_aplicado aqui: o aging é cumulativo.
                self.iniciar_processo(processo)
                quantum_restante = self.quantum
                # Reinicia o contador de aging ao trocar de processo
                ticks_desde_ultimo_aging = 0

            self.registrar_historico()
            self.executar_um_tick()

            if self.processo_atual is not None:
                quantum_restante -= 1
                ticks_desde_ultimo_aging += 1

            # ----------------------------------------------------------
            # Aging: ocorre a cada quantum COMPLETO de execução,
            # independentemente de o processo ter terminado ou não.
            # ----------------------------------------------------------
            if (self.processo_atual is not None
                    and ticks_desde_ultimo_aging >= self.quantum):
                # Aplica aging em todos os processos da fila,
                # EXCETO no processo que está executando.
                self.aplicar_aging(processo_excluido=self.processo_atual)
                ticks_desde_ultimo_aging = 0

            # ----------------------------------------------------------
            # Processo terminou
            # ----------------------------------------------------------
            if self.processo_atual and self.processo_atual.esta_concluido():
                self.finalizar_processo_atual()
                quantum_restante = 0
                ticks_desde_ultimo_aging = 0

            # ----------------------------------------------------------
            # Quantum esgotado, mas o processo ainda tem trabalho
            # ----------------------------------------------------------
            elif self.processo_atual and quantum_restante == 0:
                processo = self.processo_atual
                processo.estado = "PRONTO"
                self.fila_prontos.append(processo)
                self.processo_atual = None
                ticks_desde_ultimo_aging = 0

            self.avancar_relogio()

        self.exportar_para_json(nome_algoritmo="RoundRobin_Prioridade_Aging")
        return self.resultado("Round-Robin + Prioridade + Aging")