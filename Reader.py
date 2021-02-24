#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
from difflib import SequenceMatcher
from datetime import datetime
import yaml
import banan
import hollidays
import pandas as pd
from matplotlib import style
import sqlite3
import os
from docopt import docopt
import numpy as np
from datetime import date

class Account():
    List = {
        90237888701 :  "Fredrik lön",
        90237888728 :  "Hus och räkning",
        90247206239 :  "Månadspeng",
        90237889813 :  "Aktielikvid",
        90239908416 :  "Används ej",
        90251606718 :  "Avänds ej",
        90238924027 :  "Freja spar",
        90238924035 :  "Gustaf spar",
    }

    def __init__(self, number):
        try:
            self._number = int(number)
        except:
             self._number = 0

        try:
             self.name = Account.List[self._number]
        except:
             self.name = ''

class DataSet():
    def __init__(self):
        self.storage = []

    def getAll(self):
        return self.storage

    def _add(self, row):
        self.storage.append(row)

    def fillWithData(self, inData, samples, indices):
        dataSet = DataSet()

        for i,j in enumerate(indices):
            waytopay                = samples.getTypeOfPayment()[j][0]
            account                 = inData.getAcount()
            fixedOrVariableCost     = samples.getFixOrVaraibleCost()[j][0]
            maincategory            = samples.getCategories(0)[j][0]
            category_1              = samples.getCategories(1)[j][0]
            category_2              = samples.getCategories(2)[j][0]
            category_3              = samples.getCategories(3)[j][0]
            message                 = inData.getMessages()[i]
            date                    = inData.getDate()[i]            
            amount                  = inData.getAmount()[i]

            row  = Row(date,waytopay,account,fixedOrVariableCost,maincategory,category_1,category_2,category_3, message ,amount)

            self._add(row)

class Row():
    def __init__(self, date, waytopay, account, fixedOrVariableCost, maincategory, category_1, category_2, category_3, message, amount):

        ignore = [  'Överf ISK',
                    '832796936540829',
                    '832796936540654'
                ]

        if (amount < 0):
            inout = "Utgifter"
        else:
            inout = "Inkomster" 

        if (waytopay == 'Överföring' ):
            if (message in ignore) :
                #print("ignore")
                pass
            else:
                if (amount < 0):
                    maincategory = 'ÖverföringUt'
                else:
                    maincategory = 'ÖverföringIn'



        self.date         = date


        self.inout        = inout
        self.waytopay     = waytopay
        self.account      = account
        self.fixedOrVariableCost = fixedOrVariableCost
        self.maincategory = maincategory
        self.category_1   = category_1
        self.category_2   = category_2
        self.category_3   = category_3
        self.message      = message
        self.amount       = amount


    def __str__(self):
        return __repr__()
    
    def __repr__(self):
        return "[{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]\n".format(
                        self.date, self.inout, self.waytopay, self.account, self.fixedOrVariableCost, self.maincategory,
                        self.category_1, self.category_2, self.category_3, self.message, self.amount)

    def toDict(self):
                
        temp  = {'Datum'         : self.date,
                'In/ut'          : self.inout, 
                'Betalsätt'      : self.waytopay,
                'Konto'          : self.account,
                'Typ'            : self.fixedOrVariableCost,
                'Huvudkategori'  : self.maincategory,
                'Kategori 1'     : self.category_1,
                'Kategori 2'     : self.category_2,
                'Kategori 3'     : self.category_3,
                'Message'        : self.message,
                'Summa'          : self.amount,
            }

        temp.update(self.months)

        return temp

class InData():
    def __init__(self, filename):
        tempdf =  pd.read_csv(filename,sep=';',header = 0,index_col=False, nrows = 1)
        acountnumber = int(tempdf['Kontonummer'][0])
        self._acount = Account(acountnumber).name
                
        self._df =  pd.read_csv(filename,sep=';',header = 3,index_col=False,skip_blank_lines = False)

        for index, row in self._df.iterrows():            
            if(pd.isnull(row['Meddelande'])):
                row['Meddelande'] = row['Transaktionstyp']

            row['Belopp'] = round(float(row['Belopp'].replace(',','.').replace(' ','')))


    def getMessages(self):
        return (self._df['Meddelande'].values)

    def getDate(self):
        
        #return self._df['Transaktionsdatum']
        return self._df['Bokföringsdatum']

    def getAmount(self):
        return self._df['Belopp']

    def getAcount(self):
        return self._acount

class Samples():
    def __init__(self, filename):          
        self.df = pd.read_csv(filename, sep=';')
    
        self.samples_unique = self.df[['value', 'TypeofPayment','fixedOrVariableCost', 'Category','Category_1','Category_2','Category_3']].drop_duplicates()
        
    def getValues(self):
        return self.samples_unique['value'].values

    def getTypeOfPayment(self):
        return self.samples_unique['TypeofPayment'].values

    def getFixOrVaraibleCost(self):
        return self.samples_unique['fixedOrVariableCost'].values

    def getCategories(self, index = 0):
        if (index == 1):
            return self.samples_unique['Category_1'].values
        elif (index == 2):
            return self.samples_unique['Category_2'].values
        elif (index == 3):
            return self.samples_unique['Category_3'].values    
        else:
            return self.samples_unique['Category'].values



class Convert():
    months = ['Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli', 'Augusti', 'September', 'Oktober', 'November', 'December']
    def __init__(self):
        pass


    def _toPayDateMonth(self,d):
        d = datetime.strptime(d , '%Y-%m-%d').date()
        p = hollidays.PayDates(d.year)
        return p.getPayMonth(d)

    def _toWorkMonth(self,date):

        l  =[
            [( 1,  1), ( 1, 22),  0 ],
            [( 1, 23), ( 2, 23),  1 ], 
            [( 2, 24), ( 3, 24),  2 ],
            [( 3, 24), ( 4, 24),  3 ],
            [( 4, 23), ( 5, 21),  4 ],
            [( 5, 22), ( 6, 23),  5 ],
            [( 6, 24), ( 7, 22),  6 ],
            [( 7, 23), ( 8, 23),  7 ],
            [( 8, 24), ( 9, 23),  8 ],
            [( 9, 24), (10, 21),  9 ],
            [(10, 22), (11, 23), 10 ],
            [(11, 24), (12, 21), 11 ],
            [(12, 22), (12, 31),  0 ]
        ]


        d = datetime.strptime(date , '%Y-%m-%d').date()
        d = (d.month , d.day)

        month = ''
        for key in l:
            start = key[0]
            end =   key[1]
            if start <= d <= end:
                month = key[2]
                break

        return Convert.months[month]


    def _toMonth(self, date):

        monthInteger = datetime.strptime(date , '%Y-%m-%d').month -1  

        return Convert.months[monthInteger]
    
    def tosDict(self, dataSet):
        temp = {}
        i = 0
        for row in  dataSet.getAll():
        
            rowTemp  = {
                    'In/ut'          : row.inout, 
                    'Betalsätt'      : row.waytopay,
                    'Konto'          : row.account,
                    'Typ'            : row.fixedOrVariableCost,
                    'Huvudkategori'  : row.maincategory,
                    'Kategori 1'     : row.category_1,
                    'Kategori 2'     : row.category_2,
                    'Kategori 3'     : row.category_3,
                    'Message'        : row.message,
                    Convert.months[0]        : 0, 
                    Convert.months[1]        : 0, 
                    Convert.months[2]        : 0, 
                    Convert.months[3]        : 0, 
                    Convert.months[4]        : 0, 
                    Convert.months[5]        : 0, 
                    Convert.months[6]        : 0, 
                    Convert.months[7]        : 0, 
                    Convert.months[8]        : 0, 
                    Convert.months[9]        : 0, 
                    Convert.months[10]       : 0, 
                    Convert.months[11]       : 0,
                    'Date'                   : row.date
                }

                    

            
            
            month = self._toPayDateMonth(row.date)

            rowTemp[month] = row.amount

            temp[i] = rowTemp

            i += 1

        return temp

    def toCompressDict(self, dataSet):
        temp = {}
        
        for row in  dataSet.getAll():
            rowTemp  = {
                    'In/ut'          : row.inout, 
                    'Betalsätt'      : row.waytopay,
                    'Konto'          : row.account,
                    'Typ'            : row.fixedOrVariableCost,
                    'Huvudkategori'  : row.maincategory,
                    'Kategori 1'     : row.category_1,
                    'Kategori 2'     : row.category_2,
                    'Kategori 3'     : row.category_3,
                    'Message'        : row.message,
                    Convert.months[0]        : 0, 
                    Convert.months[1]        : 0, 
                    Convert.months[2]        : 0, 
                    Convert.months[3]        : 0, 
                    Convert.months[4]        : 0, 
                    Convert.months[5]        : 0, 
                    Convert.months[6]        : 0, 
                    Convert.months[7]        : 0, 
                    Convert.months[8]        : 0, 
                    Convert.months[9]        : 0, 
                    Convert.months[10]       : 0, 
                    Convert.months[11]       : 0
                }
            month = self._toWorkMonth(row.date)

            rowTemp[month] = row.amount

            if row.message in temp:
                temp[row.message][month] += row.amount
            else:
                temp[row.message] = rowTemp

        return temp


    def toDict(self, dataSet):
        temp = {}
        i = 0
        for row in  dataSet.getAll():
            rowTemp  = {
                    'Datum'          : row.date,
                    'In/ut'          : row.inout, 
                    'Betalsätt'      : row.waytopay,
                    'Konto'          : row.account,
                    'Typ'            : row.fixedOrVariableCost,
                    'Huvudkategori'  : row.maincategory,
                    'Kategori 1'     : row.category_1,
                    'Kategori 2'     : row.category_2,
                    'Kategori 3'     : row.category_3,
                    'Message'        : row.message,
                    
                    'Summa'          : row.amount
                }                    
            temp[i] = rowTemp
            i += 1

        return temp
# Database 

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con

def addRow(cur, row):
    ind = """INSERT INTO transactions (ix, Transactiondate, in_out, Ways_to_pay, Account, Type, Maincategory,Category_1, Category_2, Category_3, Message, Amount) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
 
    for i in range(10): 
        data = (i, row.date, row.inout, row.waytopay, row.account, row.fixedOrVariableCost, row.maincategory, row.category_1, row.category_2, row.category_3, row.message, row.amount)
        try:
            cur.execute(ind, data)
            break
        except sqlite3.Error as er:
            print(data)
            print("########################")

def create_table(db_cursor) -> bool:
    table_create = """
                    CREATE TABLE transactions (
                    ix INTEGER,
                    Transactiondate NUMERIC,
                    in_out TEXT,
                    Ways_to_pay TEXT,
                    Account INTEGER,
                    Type  TEXT,
                    Maincategory  TEXT,
                    Category_1  TEXT,
                    Category_2  TEXT,
                    Category_3  TEXT,
                    Message   TEXT,
                    Amount INTEGER, 
                    CONSTRAINT PK_Person PRIMARY KEY (ix, Transactiondate, Message, Amount)); """

    try:
        db_cursor.execute(table_create)
        return True
    except sqlite3.Error as e:
        print(e)
        return False 


def createFile(outfile, dataSet, compact = False):
    if (compact):
        theDict = Convert().toCompressDict(dataSet)        
    else:
        theDict = Convert().tosDict(dataSet)

    df = pd.DataFrame.from_dict(theDict,orient='index').reset_index(drop=True)
    df = df.replace(0, '') 
    df.to_csv(outfile, index=False, sep=';')

#"Constants"
INDATA      = 'in'
SAMPLES     = 'samples'
OUT         = 'out'
COMPACT     = 'compact'
RESULT      = 'result'


def interpretUserParams( params):            
    helptext = """  Somthing inspiring
  Usage:  
  Reader.py [--in=<file>] [--samples=<file>] [-o] [-c] [--result=<file>]
  Reader.py -h | --help
  Reader.py --version

Options:
  -i --in=<file>        File to convert [default: rakning_2020.csv].
  -s --samples=<file>   Name of the file to use as samples [default: samples.csv].
  -o --out              Return outout.
  -c --Compact          Make output data compact
  -r --result=<file>    Output file name, [default: result.csv].
  -h --help             Show this screen.
  --version             Show version.
"""
    args = docopt(helptext,  version='1.0.0')

    params = {}

    params[INDATA]  = args['--in']
    params[SAMPLES] = args['--samples']
    params[OUT]     = args['--out']
    params[COMPACT] = args['--Compact']
    params[RESULT ] = args['--result']

    return params

# =======================
#      MAIN PROGRAM
# =======================
if __name__ == "__main__":

    exit(0)
    # Get the input parameters
    params = interpretUserParams(sys.argv)

    # Read the input file
    inData = InData(params[INDATA])
    messages = inData.getMessages()

    # Read the sample files
    samples = Samples(params[SAMPLES])
    values = samples.getValues()

    (distances, indices) = banan.findpartner(values, messages)

    # Create a dataset
    dataSet = DataSet()
    dataSet.fillWithData(inData, samples, indices)

    # Write to file
    if (params[OUT]):
        createFile(params[RESULT], dataSet, params[COMPACT])

        #sys.stdout.flush()



    con = db_connect()

    cur = con.cursor() 

    create_table(cur)

    con.commit()

    # matches = []

    # for i,j in enumerate(indices):
    #     temp = [distances[i][0], values[j],categories[j], messages[i]]
    #     matches.append(temp)

    # matches = pd.DataFrame(matches, columns=['Match confidence (lower is better)','Value','Category', 'From data'])

    # print(matches)

    #allData[1].printa()

 

