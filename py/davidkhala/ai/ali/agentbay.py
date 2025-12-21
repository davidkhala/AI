from agentbay import AgentBay, Session, Config, AgentBayLogger
from davidkhala.utils.syntax.interface import ContextAware

AgentBayLogger.setup(level='WARNING') # Default to INFO

class Client(ContextAware):
    def __init__(self, api_key, *, timeout_ms=10000):
        self.agent = AgentBay(
            api_key=api_key,
            cfg=Config(endpoint="wuyingai.ap-southeast-1.aliyuncs.com", timeout_ms=timeout_ms)
        )
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
