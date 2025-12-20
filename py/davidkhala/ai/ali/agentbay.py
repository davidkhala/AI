from agentbay import AgentBay, Session
from davidkhala.utils.syntax.interface import ContextAware

class Client(ContextAware):
    def __init__(self, api_key):
        self.agent = AgentBay(api_key=api_key)
        self.session: Session | None = None

    def open(self):
        r = self.agent.create()
        if not r.success:
            return False
        self.session = r.session
        return True

    def close(self):
        self.agent.delete(self.session)
        del self.session

