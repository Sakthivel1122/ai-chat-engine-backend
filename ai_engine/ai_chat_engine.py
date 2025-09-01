# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from pydantic import BaseModel,Field
import os
from typing import List, Optional, Union
from server.settings import GROQ_API_KEY
from queue import Queue  
from langchain.callbacks.base import BaseCallbackHandler

class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_llm_new_token(self, token: str, **kwargs):
        self.queue.put(token)

    def on_llm_end(self, *args, **kwargs):
        self.queue.put("[DONE]")

class ChatEngine:
    def __init__(self, system_prompt=None, config=None):
        self.history = []
        self.system_prompt = system_prompt or self.__default_prompt()
        self.config = config or {}

        self.model = ChatOpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
            model=self.config.get("model", "llama-3.3-70b-versatile"), # llama-3.3-70b-versatile
            temperature=self.config.get("temperature", 0.7)
        )

    def __setup_chain(self, model=None):
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{query}")
        ])
        return prompt | (model or self.model)

    def chat(self, query):
        chain = self.__setup_chain()
        response = chain.invoke({
            "chat_history": self.history,
            "query": query
        })
        return response.content
    
    def streaming_chat(self, query, queue: Queue):
        streaming_model = ChatOpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
            model=self.config.get("model", "llama-3.3-70b-versatile"),
            temperature=self.config.get("temperature", 0.7),
            streaming=True,
            callbacks=[StreamingHandler(queue)]
        )

        chain = self.__setup_chain(model=streaming_model)
        chain.invoke({
            "chat_history": self.history,
            "query": query
        })

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
