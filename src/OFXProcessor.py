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

    def getCategory (p_memo):
      categs = '/Users/arglbr/src/greendrake/data/db/gd-categories-ca342569/class_items.csv'
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

    def setCategory (self, p_memo) -> None:
        # Call the abstract classs
        result = self._filestrategy.readCategoryFile(["a", "b", "c", "d", "e"])
        print(",".join(result))

    def similarityRatio(p_seq1, p_seq2, p_ratio):
      return difflib.SequenceMatcher(a = p_seq1.lower(), b = p_seq2.lower()).ratio() >= p_ratio

class FileStrategy(ABC):
    @abstractmethod
    def readCategoryFile(self):
        pass

class FileStrategyLocal(FileStrategy):
    def readCategoryFile(self):
        # Use the TempFIle showed: https://www.logilab.org/blogentry/17873
        return sorted(data)

class FileStrategyAWSS3(FileStrategy):
    def readCategoryFile(self):
        return reversed(sorted(data))

if __name__ == "__main__":
    ofxp = OFXProcessor(FileStrategyLocal())
    print("Client: FileStrategy is set to normal sorting.")
    ofxp.setCategory('blablabla')
    print()
    ofx

    print("Client: FileStrategy is set to reverse sorting.")
    ofxp.filestrategy = FileStrategyAWSS3()
    ofxp.setCategory('blablabla')
