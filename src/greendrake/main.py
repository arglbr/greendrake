from __future__ import annotations
import codecs
import sys
import csv
from datetime import datetime
from ofxparse import OfxParser # github.com/jseutter/ofxparse
import uuid
import logging

from dotenv import load_dotenv
from pathlib import Path
env_path = Path('config/') / '.env'

# load_dotenv(verbose=True, dotenv_path=env_path)
load_dotenv(dotenv_path=env_path)

from OFXProcessor import OFXProcessor
from FileStrategyLocal import FileStrategyLocal

if __name__ == "__main__":
  ofxp    = OFXProcessor(FileStrategyLocal)
  fs      = ofxp.filestrategy()
  rawfile = fs.readRawFile(sys.argv[1]) # 'bradesco_201902.ofx'

  try:
    with codecs.open(rawfile) as rf:
      ofx = OfxParser.parse(rf)
  except FileNotFoundError as fnf:
    logging.error('Exception while opening raw file: ' + fnf.strerror)
    exit(1)

  # Account & Statement
  account   = ofx.account
  statement = account.statement
  initdate  = datetime.strftime(statement.start_date, '%Y%m%d')
  enddate   = datetime.strftime(statement.end_date, '%Y%m%d')

  try:
    opt = fs.getOptFileForWrite('bdn', initdate, enddate)

    with opt as af:
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
    logging.warning('Exception while trying to convert data: ' + ve)
  except Exception as exc1:
    logging.error('Exception while trying to process file [' + opt + ']')
    logging.error(exc1)
    exit(2)
  finally:
    fs.moveArchiveFile(rawfile)

