import smtplib
from email.mime.text import MIMEText

from config import cfg
from env_var import read_env_var

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
  loader=FileSystemLoader("./templates"),
  autoescape=select_autoescape())


class SmtpClient:
  __server = None

  def __init__(self):
    self.__server = smtplib.SMTP_SSL(cfg['smtp']['Host'], cfg['smtp']['Port'])

    resolvedUsername = read_env_var(cfg['smtp']['User'])
    resolvedPassword = read_env_var(cfg['smtp']['Password'])

    self.__server.login(resolvedUsername, resolvedPassword)
    debugLevel = cfg['smtp']['DebugLevel']
    self.__server.set_debuglevel(int(debugLevel))

  def send_email_on_unauthorized(self, rErtek: str, fhId: str, belepIdok: list[str]):
    fromAddr = read_env_var(cfg['smtp']['FromAddress'])
    toAddr = read_env_var(cfg['smtp']['ToAddress'])

    template = env.get_template("unauthorized.html")

    renderedTemplate = template.render(rErtek=rErtek, fhId=fhId, belepIdok=belepIdok)

    msg = MIMEText(renderedTemplate)
    msg.set_type("text/html")
    msg['Subject'] = "Többszörös tiltott belépési kísérlet"
    msg['From'] = fromAddr
    msg['To'] = toAddr

    self.__server.sendmail(fromAddr, toAddr, msg.as_string())


smtp = SmtpClient()
