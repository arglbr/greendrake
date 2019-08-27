from __future__ import annotations

from FileStrategy import FileStrategy

class FileStrategyAWSS3(FileStrategy):
  def readCategoryFile(self):
    # Bring the file from S3, copy to tmp dir and return the path
    return 'path_tmp'

  def readRawFile(self, p_fname):
    # Bring the file from S3, copy to tmp dir and return the path
    return 'path_raw'

  def moveArchiveFile(self, p_fname):
    pass

  def getOptFileForWrite(self, p_prefix, p_initdate, p_enddate):
    # Use smart_open module
    pass

