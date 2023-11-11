import smtplib
from email.mime.text import MIMEText

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

  def send_email_on_unauthorized(self, rErtek: str, fhNev: str, belepIdok: list[str]):
    fromAddr = read_env_var(config.get_content()['stmp']['FromAddress'])
    toAddr = read_env_var(config.get_content()['stmp']['ToAddress'])

    template = env.get_template("unauthorized.html")

    renderedTemplate = template.render(rErtek=rErtek, fhNev=fhNev, belepIdok=belepIdok)

    msg = MIMEText(renderedTemplate)
    msg.set_type("text/html")
    msg['Subject'] = "Többszörös tiltott belépési kísérlet"
    msg['From'] = fromAddr
    msg['To'] = toAddr

    self.__server.sendmail(fromAddr, toAddr, msg.as_string())
