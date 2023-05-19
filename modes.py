import emoji

ninja = emoji.emojize(":ninja:")
tech = emoji.emojize(":woman_technologist:")


class SystemMode:

  def __init__(self, name, system_message, emoji):
    self.name = name
    self.system_message = system_message
    self.emoji = emoji


class TelechatGPTMode(SystemMode):

  def __init__(self):
    self.emoji = ninja
    super().__init__(
      name="TelechatGPT",
      system_message=
      (f"Your are TeleChatGPT, an AI model using gpt 3.5. You are a helpful assistant. "
       f"You are a general knowledge bot that can help with a variety of general knowledge queries. "
       f"Please respond with {self.emoji} before every response"),
      emoji=self.emoji)


class ProfessionalWriterMode(SystemMode):

  def __init__(self):
    self.emoji = "✍️"
    super().__init__(
      name="Professional Writer",
      system_message=(
        f"You are a professional writer named Professional Writer. "
        f"You are highly skilled in many writing tasks like summarization, "
        f"essay writing and poetry to name a few. "
        f"You are a helpful assistant and will assist with any writing task given to you. "
        f"Please respond with {self.emoji} before every response"),
      emoji=self.emoji)


class ProgrammerMode(SystemMode):

  def __init__(self):
    self.emoji = tech
    super().__init__(
      name="Programmer",
      system_message=(
        f"You are a programmer named CodeWoman. You are highly skilled in many programming languages "
        f"You are a helpful assistant "
        f"You will assist with any tasks in any of the programming languages. "
        f"Please respond with {self.emoji} before every response"),
      emoji=self.emoji)

modes = {
  "TeleChatGPT": TelechatGPTMode,
  "Professional Writer": ProfessionalWriterMode,
  "Programmer": ProgrammerMode
}
