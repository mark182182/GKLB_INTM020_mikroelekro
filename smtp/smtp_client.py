import smtplib
from email import message_from_string

from app import config, env
from env_var import read_env_var


class SmtpClient:
  __server = None

  def __init__(self):
    self.__server = smtplib.SMTP(config.get_content()['stmp']['Host'], config.get_content()['smtp']['Port'])

    resolvedUsername = read_env_var(config.get_content()['stmp']['User'])
    resolvedPassword = read_env_var(config.get_content()['stmp']['Password'])

    self.__server.login(resolvedUsername, resolvedPassword)
    self.__server.starttls()
    self.__server.set_debuglevel(1)

  def send_email_on_unauthorized(self, rErtek: str, belepIdok: list[str]):
    template = env.get_template("unauthorized.html")

    renderedTemplate = template.render(rErtek=rErtek, belepIdok=belepIdok)
    message = message_from_string(renderedTemplate)

    fromAddr = read_env_var(config.get_content()['stmp']['FromAddress'])
    toAddr = read_env_var(config.get_content()['stmp']['ToAddress'])
    self.__server.send_message(message, fromAddr, toAddr)
