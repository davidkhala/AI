import json

import requests

from davidkhala.ai.agent.dify.base import API


class Feedbacks(API):
    def paginate_feedbacks(self, page=1, size=20):
        """
        when 'rating'='like', content=None
        when 'rating'='dislike', content can be filled by end user
        NOTE: for security reason, api cannot access conversation context associated with the feedback. End user should copy the conversation to comment by themselves.
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
    """
    Note: The Service API does not share conversations created by the WebApp. Conversations created through the API are isolated from those created in the WebApp interface.
    It means you cannot get user conversation content from API, API call has only access to conversation created by API
    """
    def __init__(self, api_key: str, user: str):
        super().__init__(api_key) # base_url need to be configured afterward if not default
        self.user = user  # user_id, from_end_user_id

    def paginate_messages(self, conversation_id):
        return self.request(f"{self.base_url}/messages", "GET", params={
            'conversation_id': conversation_id,
            'user': self.user,
        })
