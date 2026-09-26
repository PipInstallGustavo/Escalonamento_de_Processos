from escalonador import EscalonadorBase


class SRTF(EscalonadorBase):
    """Shortest Remaining Time First - preemptivo."""

    def executar(self):
        self.reset()

        while not self.todos_concluidos():
            self.atualizar_chegadas()

            if self.fila_prontos:
                candidato = min(
                    self.fila_prontos,
                    key=lambda p: (
                        p.tempo_restante,
                        p.tempo_chegada,
                        p.id
                    )
                )

                # Só troca se o candidato realmente tiver o menor tempo restante que o processo atual.
                if self.processo_atual is None:
                    self.fila_prontos.remove(candidato)
                    self.iniciar_processo(candidato)

                elif candidato.tempo_restante < self.processo_atual.tempo_restante:
                    self.processo_atual.estado = "PRONTO"
                    self.fila_prontos.append(self.processo_atual)
                    self.fila_prontos.remove(candidato)
                    self.iniciar_processo(candidato)

            self.registrar_historico()
            self.executar_um_tick()
            self.finalizar_processo_atual()
            self.avancar_relogio()
            self.exportar_para_json(nome_algoritmo="SRTF")

        return self.resultado("SRTF")
