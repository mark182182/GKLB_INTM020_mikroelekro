import configparser


class Config:
  __parser = configparser.ConfigParser()
  __content: any

  def get_content(self):
    return self.__content

  def read(self):
    __config = self.__parser.read('./config.ini')
