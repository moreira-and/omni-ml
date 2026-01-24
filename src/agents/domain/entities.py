from src.agents.domain.interfaces import Agent

class ResearcherAgent(Agent):
    name = "researcher"

    def run(self, state):
        topic = state["topic"]
        return {
            "research": f"Dados relevantes sobre {topic}"
        }

class AnalystAgent(Agent):
    name = "analyst"

    def run(self, state):
        research = state["research"]
        return {
            "analysis": f"Análise crítica baseada em {research}"
        }

class CriticAgent(Agent):
    name = "critic"

    def run(self, state):
        analysis = state["analysis"]
        if "fraco" in analysis:
            return {"valid": False}
        return {"valid": True}
