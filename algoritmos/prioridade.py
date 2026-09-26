from escalonador import EscalonadorBase


class PrioridadeNaoPreemptiva(EscalonadorBase):
    """Prioridade sem preempção. Menor número = maior prioridade."""

    def executar(self):
        self.reset()

        while not self.todos_concluidos():
            self.atualizar_chegadas()

            if self.processo_atual is None and self.fila_prontos:
                self.fila_prontos.sort(
                    key=lambda p: (
                        p.prioridade,
                        p.tempo_chegada,
                        p.id
                    )
                )
                self.iniciar_processo(self.fila_prontos.pop(0))

            self.registrar_historico()
            self.executar_um_tick()
            self.finalizar_processo_atual()
            self.avancar_relogio()
            self.exportar_para_json(nome_algoritmo="Prioridade_Não_Preemptiva")

        return self.resultado("Prioridade Não Preemptiva")


class PrioridadePreemptiva(EscalonadorBase):
    """Prioridade preemptiva. Menor número = maior prioridade."""

    def executar(self):
        self.reset()

        while not self.todos_concluidos():
            self.atualizar_chegadas()

            if self.fila_prontos:
                candidato = min(
                    self.fila_prontos,
                    key=lambda p: (
                        p.prioridade,
                        p.tempo_restante,
                        p.tempo_chegada,
                        p.id
                    )
                )

                if self.processo_atual is None:
                    self.fila_prontos.remove(candidato)
                    self.iniciar_processo(candidato)

                elif candidato.prioridade < self.processo_atual.prioridade:
                    self.processo_atual.estado = "PRONTO"
                    self.fila_prontos.append(self.processo_atual)
                    self.fila_prontos.remove(candidato)
                    self.iniciar_processo(candidato)

            self.registrar_historico()
            self.executar_um_tick()
            self.finalizar_processo_atual()
            self.avancar_relogio()
            self.exportar_para_json(nome_algoritmo="Prioridade_Preemptiva")

        return self.resultado("Prioridade Preemptiva")
