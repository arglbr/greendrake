from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

import codecs
import sys
import csv
from datetime import datetime
from ofxparse import OfxParser # github.com/jseutter/ofxparse
import shutil
import difflib
import uuid

class OFXProcessor():
  def __init__(self, filestrategy: FileStrategy) -> None:
    self._filestrategy = filestrategy

  @property
  def filestrategy(self) -> FileStrategy:
    return self._filestrategy

  @filestrategy.setter
  def filestrategy(self, filestrategy: FileStrategy) -> None:
    self._filestrategy = filestrategy

  def setCategory (self, p_memo):
    categs = self._filestrategy.readCategoryFile(self)
    ret    = 'INDEFINIDO'
    accsim = 0.8

    try:
      with open(categs) as cf:
        reader = csv.DictReader(cf)
        c_diffratio = 0
        r_diffratio = 0

        for row in reader:
          categid     = row['CATEGORY_ID']
          pattern     = row['PATTERN'].lower().replace('visa electron ', '')
          memo        = p_memo.lower().replace('visa electron ', '')
          c_diffratio = difflib.SequenceMatcher(a = memo, b = pattern).ratio()

          if c_diffratio >= accsim and c_diffratio > r_diffratio:
            r_diffratio = c_diffratio
            ret = categid
    except Exception as exc3:
      msg = 'Error on setCategory() method.'
      print("[WRN]" + msg + ". Exception: " + exc3.fnferror)
      ret = msg

    return ret

  def similarityRatio(p_seq1, p_seq2, p_ratio):
    return difflib.SequenceMatcher(a = p_seq1.lower(), b = p_seq2.lower()).ratio() >= p_ratio

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

class FileStrategyLocal(FileStrategy):
  def readCategoryFile(self):
    categories_file = '/Users/arglbr/src/arglbr/greendrake/data/db/gd-categories-ca342569/class_items.csv'
    return categories_file

  def readRawFile(self, p_fname):
    raw_file = '/Users/arglbr/src/arglbr/greendrake/data/db/gd-raw-be3bc2c/' + p_fname
    return raw_file

  def moveArchiveFile(self, p_fname):
    archive = '/Users/arglbr/src/arglbr/greendrake/data/db/gd-archive-ec5e29c8/'

    try:
      shutil.move(p_fname, archive)
    except Exception as exc2:
      print('[ERR] Exception while trying to move file: ' + exc2.strerror)
      print('[ERR] File: ' + p_fname)
      print('[ERR] To: ' + archive)
      exit(3)

class FileStrategyAWSS3(FileStrategy):
  def readCategoryFile(self):
    return 'path_tmp' # Bring the file from S3, copy to tmp dir and return the path

  def readRawFile(self, p_fname):
    return 'path_raw' # Bring the file from S3, copy to tmp dir and return the path

  def moveArchiveFile(self, p_fname):
    pass

if __name__ == "__main__":
  ofxp    = OFXProcessor(FileStrategyLocal)
  fs      = ofxp.filestrategy()
  rawfile = fs.readRawFile(sys.argv[1]) # 'bradesco_201902.ofx'
  optpath = '/Users/arglbr/src/arglbr/greendrake/data/db/gd-optimized-4bf3bb45/'

  try:
    with codecs.open(rawfile) as rf:
      ofx = OfxParser.parse(rf)
  except FileNotFoundError as fnf:
    print('[ERR] Exception while opening raw file: ' + fnf.strerror)
    exit(1)

  # Account & Statement
  account   = ofx.account
  statement = account.statement
  initdate  = datetime.strftime(statement.start_date, '%Y%m%d')
  enddate   = datetime.strftime(statement.end_date, '%Y%m%d')

  try:
    datafile = optpath + 'bdn_' + initdate + '_' + enddate + '.csv'

    with open(datafile, mode='w') as af:
      afw = csv.writer(af, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      afw.writerow(['RowID', 'Bank', 'AccountID', 'BalStartDate', 'BalEndDate', 'TrDate', 'TrChecknum', 'TrType', 'TrMemo', 'TrAmount', 'TrID', 'TrSic', 'TrMcc', 'TrPayee', 'Category'])

      # Transaction
      for transaction in statement.transactions:
        afw.writerow([uuid.uuid4().hex,
                    'BDO',
                    account.account_id + account.routing_number,
                    initdate,
                    enddate,
                    datetime.strftime(transaction.date, '%Y%m%d'),
                    transaction.checknum,
                    transaction.type,
                    transaction.memo,
                    str(transaction.amount),
                    transaction.id,
                    str(transaction.sic),
                    str(transaction.mcc),
                    transaction.payee,
                    ofxp.setCategory(transaction.memo)])
  except ValueError as ve:
    print("[WRN] Exception while trying to convert data: " + ve)
  except Exception as exc1:
    print("[ERR] Exception while trying to process file [" + datafile + "]")
    print(exc1)
    exit(2)
  finally:
    fs.moveArchiveFile(rawfile)
