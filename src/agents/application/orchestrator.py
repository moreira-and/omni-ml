class Orchestrator:
    def __init__(self, agents):
        self.agents = agents

    def run(self, initial_state):
        state = initial_state

        for agent in self.agents:
            output = agent.run(state)
            state.update(output)

            if state.get("valid") is False:
                raise ValueError("Resultado inválido")

        return state