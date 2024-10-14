class Tool:
    def __init__(self):
        pass

import openai
import os
from openai import OpenAI
from groq import Groq

api = "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"
api_keyy= "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"

class LLMTool(Tool):
    def __init__(self):
        self.client = Groq(
            api_key=api_keyy
        )

    def respond(self, system_role, user_role):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_role,
                },
                {
                    "role": "user",
                    "content": user_role,
                }
            ],
            temperature = 0,
            max_tokens=100,
            model="llama3-70b-8192",
        )

        text = chat_completion.choices[0].message.content
        return text

from simplegmail import Gmail

class GmailTool(Tool):
    def __init__(self):
        self.gmail = Gmail()
    
    def get_unread_emails(self):
        unread_emails = self.gmail.get_starred_messages()
        #print(unread_emails)
        return unread_emails

    