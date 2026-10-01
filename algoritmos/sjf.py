from escalonador import EscalonadorBase


class SJF(EscalonadorBase):
    # Shortest Job First não preemptivo.

    def executar(self):
        self.reset()

        while not self.todos_concluidos():
            self.atualizar_chegadas()

            if self.processo_atual is None and self.fila_prontos:
                self.fila_prontos.sort(
                    key=lambda p: (
                        p.duracao,
                        p.tempo_chegada,
                        p.id
                    )
                )
                self.iniciar_processo(self.fila_prontos.pop(0))

            self.registrar_historico()
            self.executar_um_tick()
            self.finalizar_processo_atual()
            self.avancar_relogio()
        self.exportar_para_json(nome_algoritmo="SJF")

        return self.resultado("SJF")
