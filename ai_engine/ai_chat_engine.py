from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from pydantic import BaseModel,Field
import os
from typing import List, Optional, Union
from server.settings import GROQ_API_KEY

class ChatEngine:
    def __init__(self, system_prompt=None, config=None):
        self.history = []
        self.system_prompt = system_prompt or self.__default_prompt()
        self.config = config or {}

        self.model = ChatOpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
            model=self.config.get("model", "llama3-70b-8192"),
            temperature=self.config.get("temperature", 0.7)
        )

    def __setup_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{query}")
        ])
        return prompt | self.model

    def chat(self, query):
        chain = self.__setup_chain()
        response = chain.invoke({
            "chat_history": self.history,
            "query": query
        })
        return response.content

    def __default_prompt(self) -> str:
        return "You are a helpful AI."

    def get_history(self) -> List[Union[HumanMessage, AIMessage]]:
        return self.history

    def set_history(self, chat_history):
        self.history = chat_history

    def clear_history(self):
        self.history = []

    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt
        self.chain = None  # Reset chain to apply new prompt
