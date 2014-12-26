from ofxclient import config
from ofxparse import OfxParser
import sqlite3

from StringIO import StringIO

DOWNLOAD_DAYS = 30
GlobalConfig = config.OfxConfig()

db = sqlite3.connect(r'C:\temp\usaa.db')


def parse_file():
    f = open(r'C:\temp\download_5.ofx', 'r')
    ofx_data = OfxParser.parse(f)
    return ofx_data


def create_table():
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usaa_checking_transactions(
            id INTEGER PRIMARY KEY,
            posted_date TEXT,
            transaction_date TEXT,
            payee TEXT,
            memo TEXT,
            checknum INTEGER,
            type TEXT,
            sic TEXT,
            mcc TEXT,
            cleared TEXT,
            amount TEXT,
            cat1 TEXT,
            amt1 TEXT,
            cat2 TEXT,
            amt2 TEXT,
            cat3 TEXT,
            amt3 TEXT,
            cat4 TEXT,
            amt4 TEXT,
            cat5 TEXT,
            amt5 TEXT,
            cat6 TEXT,
            amt6 TEXT,
            cat7 TEXT,
            amt7 TEXT);
    ''')

    db.commit()

def populate_table(ofx_data):
    cursor = db.cursor()

    cursor.execute('''SELECT * FROM usaa_checking_transactions''')
    rows = cursor.fetchall()

    for act in ofx_data.accounts:
        for t in act.statement.transactions:
             cursor.execute('''INSERT OR IGNORE INTO usaa_checking_transactions(payee, type, posted_date, amount, id, memo, sic, mcc, checknum)
                              VALUES(?,?,?,?,?,?,?,?,?)''', (t.payee, t.type, t.date, str(t.amount), t.id, t.memo, t.sic, t.mcc, t.checknum))

    db.commit()

    cursor.execute('''SELECT * FROM usaa_checking_transactions''')
    rows = cursor.fetchall()

    for r in rows:
        print r


def download_accounts_and_save_to_ofx_files():
    accounts = GlobalConfig.accounts()

    i = 0
    for act in accounts:
        i += 1
        ofx_data = act.download(days=DOWNLOAD_DAYS)
        ofx = OfxParser.parse(ofx_data)
        f = r'C:\temp\download_{0:d}.ofx'.format(i)
        outfile = open(f, 'w')
        ofx_data.seek(0)
        outfile.write(ofx_data.read())
        outfile.close()

if __name__ == '__main__':
    #download_accounts_and_save_to_ofx_files()
    ofx_data = parse_file()
    create_table()
    populate_table(ofx_data)