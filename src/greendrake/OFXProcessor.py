from __future__ import annotations
import csv
import difflib
import logging
from FileStrategy import FileStrategy
from FileStrategyAWSS3 import FileStrategyAWSS3
from FileStrategyLocal import FileStrategyLocal

class OFXProcessor():
  def __init__(self, p_filestrategy) -> None:
    if p_filestrategy == 'aws':
      self._filestrategy = FileStrategyAWSS3
    else:
      self._filestrategy = FileStrategyLocal

  @property
  def filestrategy(self) -> FileStrategy:
    return self._filestrategy

  @filestrategy.setter
  def filestrategy(self, p_filestrategy) -> None:
    if p_filestrategy == 'aws':
      self._filestrategy = FileStrategyAWSS3()
    else:
      self._filestrategy = FileStrategyLocal()

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
      logging.warning(msg + '. Exception: ' + exc3.fnferror)
      ret = msg

    return ret

  def similarityRatio(p_seq1, p_seq2, p_ratio):
    return difflib.SequenceMatcher(a = p_seq1.lower(), b = p_seq2.lower()).ratio() >= p_ratio

