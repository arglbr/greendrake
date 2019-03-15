import codecs
import csv
from datetime import datetime
from ofxparse import OfxParser # github.com/jseutter/ofxparse
import shutil

if __name__ == '__main__':
  fname   = 'Bradesco_05032019_150334.ofx'
  rawfile = '/Users/arglbr/src/greendrake/data/db/gd-raw-be3bc2c/' + fname
  archive = '/Users/arglbr/src/greendrake/data/db/gd-archive-ec5e29c8/'
  optpath = '/Users/arglbr/src/greendrake/data/db/gd-optimized-4bf3bb45/'

  try:
    with codecs.open(rawfile) as rf:
      ofx = OfxParser.parse(rf)
  except FileNotFoundError as fnf:
    print('[ERR] Exception while opening file: ' + fnf.strerror)
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
      afw.writerow(['Bank', 'AccountID', 'BalStartDate', 'BalEndDate', 'TrDate', 'TrChecknum', 'TrType', 'TrMemo', 'TrAmount', 'TrID', 'TrSic', 'TrMcc', 'TrPayee'])

      # Transaction
      for transaction in statement.transactions:
        afw.writerow(['BDN',
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
                    transaction.payee])
  except ValueError as ve:
    print("[WRN] Exception while trying to convert data: " + ve)
  except Exception as exc1:
    print('[ERR] Exception while trying to write on file [' + datafile + ']: ' + exc1)
    exit(2)
  finally:
    try:
      shutil.move(rawfile, archive)
    except Exception as exc2:
      print('[ERR] Exception while trying to move file: ' + exc2)
      exit(3)
