from davidkhala.ai.agent.dify.ops.console import API
class ConsoleKnowledge(API):
    def website_sync(self, dataset, document):
        url = f"{self.base_url}/datasets/{dataset}/documents/{document}/website-sync"
        r = self.request(url, "GET")
        assert r == {"result": "success"}