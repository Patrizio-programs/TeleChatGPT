from json import loads
from queue import Queue, Empty
from re import findall
from threading import Thread
from typing import Generator, Optional

from curl_cffi import requests
from fake_useragent import UserAgent


class Completion:
  part1 = '{"role":"assistant","id":"chatcmpl'
  part2 = '"},"index":0,"finish_reason":null}]}}'
  regex = rf'{part1}(.*){part2}'

  timer = None
  message_queue = Queue()
  stream_completed = False
  last_msg_ids = {}

  @staticmethod
  def request(prompt: str, chat_id: int, proxy: Optional[str] = None):
    headers = {
      'authority': 'chatbot.theb.ai',
      'content-type': 'application/json',
      'origin': 'https://chatbot.theb.ai',
      'user-agent': UserAgent().random,
    }

    proxies = {
      'http': 'http://' + proxy,
      'https': 'http://' + proxy
    } if proxy else None

    options = {}
    if chat_id in Completion.last_msg_ids:
      options['parentMessageId'] = Completion.last_msg_ids[chat_id]

    response = requests.post('https://chatbot.theb.ai/api/chat-process',
                         headers=headers,
                         proxies=proxies,
                         json={
                           'prompt': prompt,
                           'options': options
                         },
                         timeout=100000)

for chunk in response.iter_content(chunk_size=1024):
  Completion.handle_stream_response(chunk)

  @staticmethod
  def create(prompt: str,
             chat_id: int,
             proxy: Optional[str] = None) -> Generator[str, None, None]:
    Completion.stream_completed = False

    Thread(target=Completion.request, args=[prompt, chat_id, proxy]).start()

    while not Completion.stream_completed or not Completion.message_queue.empty(
    ):
      try:
        message = Completion.message_queue.get(timeout=0.01)
        for message in findall(Completion.regex, message):
          message_json = loads(Completion.part1 + message + Completion.part2)
          Completion.last_msg_ids[chat_id] = message_json['id']
          yield message_json['delta']

      except Empty:
        pass

  @staticmethod
  def handle_stream_response(response):
    Completion.message_queue.put(response.decode())

  @staticmethod
  def get_response(prompt: str, proxy: Optional[str] = None) -> str:
    response_list = []
    for message in Completion.create(prompt, proxy):
      response_list.append(message)
    return ''.join(response_list)

    Completion.message_queue.put(response.decode(errors='replace'))
