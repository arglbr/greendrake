from abc import ABC, abstractmethod

class FileStrategy(ABC):
  @abstractmethod
  def readCategoryFile(self):
    pass

  @abstractmethod
  def readRawFile(self, p_fname):
    pass

  @abstractmethod
  def moveArchiveFile(self, p_fname):
    pass

  @abstractmethod
  def getOptFileForWrite(self, p_prefix, p_initdate, p_enddate):
    pass

