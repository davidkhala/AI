from davidkhala.ai.agent.dify.ops.console import API


class ConsoleUser(API):
    def login(self, email, password,
              *,
              remember_me=True,
              language="en-US"
              ):
        url = f"{self.base_url}/login"

        r = self.request(url, "POST", json={
            'email': email,
            'password': password,
            'remember_me': remember_me,
            'language': language,
        })
        assert r == {"result": "success"}
        return self.session.cookies
