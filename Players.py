class Players:
  def __init__(self, player):
    self.player = player
    self.__score = 0
  
  def setScore(self, score):
    self.__score = score

  def getScore(self):
    return self.__score

  def setChannel(self, channel):
    self.__channel = channel

  def getChannel(self):
    return self.__channel