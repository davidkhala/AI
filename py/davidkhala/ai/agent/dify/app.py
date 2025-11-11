import json

import requests

from davidkhala.ai.agent.dify.base import API


class Feedbacks(API):
    def paginate_feedbacks(self, page=1, size=20):
        """
        when 'rating'='like', content=None
        when 'rating'='dislike', content can be filled by end user
        """
        response = requests.get(f"{self.base_url}/app/feedbacks", params={"page": page, "limit": size}, **self.options)
        if not response.ok:
            response.raise_for_status()
        else:
            return json.loads(response.text)

    def list_feedbacks(self):
        # TODO https://github.com/langgenius/dify/issues/28067
        return self.paginate_feedbacks()['data']

class Conversation(API):
    def __init__(self, api_key: str,user:str, *, base_url=None):
        super().__init__(api_key, base_url)
        self.user = user # user_id, from_end_user_id

    def messages(self, conversation_id):
        self.request(f"{self.base_url}/messages", "GET", params={
            'conversation_id':conversation_id,
            'user':self.user,
        })

