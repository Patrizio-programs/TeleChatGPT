
from revChatGPT.V1 import Chatbot
import requests
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
from langchain import PromptTemplate, LLMChain
from time import sleep
from langchain.prompts import (
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)


system_message = "You are a helpful assistant called TeleChatGPT."
system_message_prompt = SystemMessagePromptTemplate.from_template(
    system_message)

human_message = "What is your name?"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_message)
chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt])
messages = chat_prompt.format_prompt().to_messages()

chat_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJwYXRyaXppb21lZGxleUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci1Nd2pLT1FIa3VESE51Z3hHR1R3a0NOYW4ifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA0MDM5ODE5NTY0NzAwNTc0NzgzIiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY4NTM4NTg1NiwiZXhwIjoxNjg2NTk1NDU2LCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9yZ2FuaXphdGlvbi53cml0ZSJ9.0InxXAPC7KGAi64uvW-bZ3dB8ygJycEN2SHfst9rA3z4kbyIe-RZpCbtroiwD89Hu87TJw-WFUULNjt5FYou_WkJKsFvxyzPxb_ytbnkLvPA-Q3_6a8uF1SeyoVsPyRpoEppZwvgnOVZrGqW6WkiHrwif_6721oHtoDaNQ5pNKO03RbisVYjxau7pWxqQpzpmGOkRQ8jGIX3zXgiXrkD7mEumqmanV_d8kQm9yGmgOXtMe2l-hYquWdkX3J0RbarccUldPa5AZv1oMghXbVi6r6FFXGXYaGfoonAlau2Tgfo3z3LTD4O0d07swbQE4s7D1R-GVY89niIeMFNeXCmcQ"


class ChatGPT(LLM):

    history_data: Optional[List] = []
    token: Optional[str]
    chatbot: Optional[Chatbot] = None
    call: int = 0
    conversation: Optional[str] = ""
    prev_message: str = ""

    # WARNING : for each api call this library will create a new chat on chat.openai.com

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, system: Optional[str] = None) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        # token is a must check
        if self.token is None:
            raise ValueError(
                "Need a token , check https://chat.openai.com/api/auth/session for get your token")
        else:
            if self.conversation == "":
                self.chatbot = Chatbot(config={"access_token": self.token})
            elif self.conversation != "" and self.prev_message == "":
                self.chatbot = Chatbot(
                    config={"access_token": self.token}, conversation_id=self.conversation)
            elif self.conversation != "" and self.prev_message != "":
                self.chatbot = Chatbot(config={
                    "access_token": self.token}, conversation_id=self.conversation, parent_id=self.prev_message)
            else:
                raise ValueError("Something went wrong")

            response = ""
            # OpenAI: 50 requests / hour for each account
            if self.call >= 45:
                raise ValueError(
                    "You have reached the maximum number of requests per hour ! Help me to Improve. Abusing this tool is at your own risk")
            else:
                sleep(2)
                for data in self.chatbot.ask(prompt, conversation_id=self.conversation, parent_id=self.prev_message):
                    response = data["message"]
                    FullResponse = data

                self.conversation = FullResponse["conversation_id"]
                self.prev_message = FullResponse["parent_id"]
                self.call += 1

            # add to history
            self.history_data.append({"prompt": prompt, "response": response})

            if system is not None:
                print(system)

            return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "ChatGPT", "token": self.token}


llm = ChatGPT(token=chat_token)  # for start new chat
# llm = ChatGPT(token = "YOUR-TOKEN", conversation = "Add-XXXX-XXXX-Convesation-ID") #for use a chat already started

# print(llm("Hello, how are you?"))
# response = llm(str(chat_prompt.format_prompt()))
# print(response)
# print(llm._generate(prompts="what is your name"))
# print(llm("Can you resume your previus answer?")) #now memory work well
