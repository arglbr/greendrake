from __future__ import annotations
import shutil
import logging
import os
import re

from FileStrategy import FileStrategy

class FileStrategyLocal(FileStrategy):
  def readCategoryFile(self):
    # categories_file = '/Users/arglbr/src/arglbr/greendrake/data/db/gd-categories-ca342569/class_items.csv'
    categories_file = os.getenv("CATEGORIES_DATA")
    return categories_file

  def readRawFile(self, p_fname):
    # raw_file = '/Users/arglbr/src/arglbr/greendrake/data/db/gd-raw-be3bc2c/' + p_fname
    raw_location = os.getenv("RAW_DATA")
    pattern      = '/$'
    result       = re.match(pattern, raw_location)

    if not result:
      raw_file = raw_location + '/' + p_fname

    return raw_file

  def moveArchiveFile(self, p_fname):
    # archive = '/Users/arglbr/src/arglbr/greendrake/data/db/gd-archive-ec5e29c8/'
    archive_location = os.getenv("ARCHIVE_DATA")
    pattern          = '/$'
    result           = re.match(pattern, archive_location)

    if not result:
      archive_location = archive_location + '/'

    try:
      shutil.move(p_fname, archive_location)
    except Exception as exc2:
      logging.error('Exception while trying to move file: ' + exc2.strerror)
      logging.error('File: ' + p_fname)
      logging.error('To: ' + archive_location)
      exit(3)

  def getOptFileForWrite(self, p_prefix, p_initdate, p_enddate):
    # optpath  = '/Users/arglbr/src/arglbr/greendrake/data/db/gd-optimized-4bf3bb45/'
    optimized_location = os.getenv("OPTIMIZED_DATA")
    pattern            = '/$'
    result             = re.match(pattern, optimized_location)

    if not result:
      optimized_location = optimized_location + '/'

    datafile = optimized_location + p_prefix + '_' + p_initdate + '_' + p_enddate + '.csv'
    return open(datafile, mode='w')

'abc.ABC'
'abc.abstractmethod'
'typing.List'
'codecs'
'sys'
'csv'
'datetime.datetime'
'ofxparse.OfxParser'
'difflib'
'uuid'
