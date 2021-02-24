#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
from difflib import SequenceMatcher
from datetime import datetime
import yaml
import banan
import pandas as pd
from matplotlib import style
import sqlite3
import os
from docopt import docopt

months = ['Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli', 'Augusti', 'September', 'Oktober', 'November', 'December']

class Account():
    List = {
        90237888701 :  "Fredrik lön",
        90237888728 :  "Hus och räkning",
        90251606912 :  "Ej bestämt", 
        90251945776 :  "Hushåll",
        90237888736 :  "Gemensamt spar",
        90239430761 :  "Månadspeng",
        90243464349 :  "Resa",
        90243464357 :  "Avbetalning bil",
        90247206212 :  "Månadspeng",
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

    def toCompressDict(self):
        temp = {}

        for row in  self.storage:
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
                    months[0]        : 0, 
                    months[1]        : 0, 
                    months[2]        : 0, 
                    months[3]        : 0, 
                    months[4]        : 0, 
                    months[5]        : 0, 
                    months[6]        : 0, 
                    months[7]        : 0, 
                    months[8]        : 0, 
                    months[9]        : 0, 
                    months[10]       : 0, 
                    months[11]       : 0
                }
            month = toMonth(row.date)

            rowTemp[month] = row.amount

            if row.message in temp:
                temp[row.message][month] += row.amount
            else:
                temp[row.message] = rowTemp

        return temp

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
            maincategory            = samples.getCategories()[j][0]
            category_1              = ''
            category_2              = ''
            category_3              = ''
            message                 = inData.getMessages()[i]
            date                   = inData.getDate()[i]            
            amount                  = inData.getAmount()[i]

            row  = Row(date,waytopay,account,fixedOrVariableCost,maincategory,category_1,category_2,category_3, message ,amount)

            self._add(row)




class convert():
    def __init__(self)
        pass

    def toMonth(date):
        monthInteger = datetime.strptime(date , '%Y-%m-%d').month -1  

        return months[monthInteger]
    
    def toCompressDict(self):
        temp = {}

        for row in  self.storage:
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
                    months[0]        : 0, 
                    months[1]        : 0, 
                    months[2]        : 0, 
                    months[3]        : 0, 
                    months[4]        : 0, 
                    months[5]        : 0, 
                    months[6]        : 0, 
                    months[7]        : 0, 
                    months[8]        : 0, 
                    months[9]        : 0, 
                    months[10]       : 0, 
                    months[11]       : 0
                }
            month = toMonth(row.date)

            rowTemp[month] = row.amount

            if row.message in temp:
                temp[row.message][month] += row.amount
            else:
                temp[row.message] = rowTemp

        return temp

class Row():


    def __init__(self, date, waytopay, account, fixedOrVariableCost, maincategory, category_1, category_2, category_3, message, amount):

        if (amount < 0):
            inout = "Utgifter"
        else:
            inout = "Inkomster" 

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

class Row2():
    months = ['Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli', 'Augusti', 'September', 'Oktober', 'November', 'December']
    
    def __init__(self,waytopay,account,fixedOrVariableCost,maincategory,category_1,category_2,category_3,message,date,amount):
        amount = float(amount.replace(',','.').replace(' ',''))
        
        if (amount < 0):
            inout = "Utgifter"
        else:
            inout = "Inkomster" 

        month = datetime.strptime(date , '%Y-%m-%d').month -1
        self.date = date
        self.inout        = inout
        self.waytopay     = waytopay
        self.account      = account
        self.fixedOrVariableCost = fixedOrVariableCost
        self.maincategory = maincategory
        self.category_1   = category_1
        self.category_2   = category_2
        self.category_3   = category_3
        self.message      = message

        self.months        = {Row.months[0] : 0, 
                             Row.months[1]  : 0, 
                             Row.months[2]  : 0, 
                             Row.months[3]  : 0, 
                             Row.months[4]  : 0, 
                             Row.months[5]  : 0, 
                             Row.months[6]  : 0, 
                             Row.months[7]  : 0, 
                             Row.months[8]  : 0, 
                             Row.months[9]  : 0, 
                             Row.months[10] : 0, 
                             Row.months[11] : 0
                              }

        monthStr     = Row.months[month]
        self.months[monthStr] = amount
        self.amount = amount

    def getAsDict(self):
                
        temp  = {'In/ut'         : self.inout, 
                'Betalsätt'      : self.waytopay,
                'Konto'          : self.account,
                'Typ'            : self.fixedOrVariableCost,
                'Huvudkategori'  : self.maincategory,
                'Kategori 1'     : self.category_1,
                'Kategori 2'     : self.category_2,
                'Kategori 3'     : self.category_3,
                'Message'        : self.message,                
            }

        temp.update(self.months)

        return temp

    def concate(self, row):
        for key in self.months:
            self.months[key]  += row.months[key]


class InData():
    def __init__(self, filename):
        tempdf =  pd.read_csv(filename,sep=';',header = 0,index_col=False, nrows = 1)
        acountnumber = int(tempdf['Kontonummer'][0])
        self._acount = Account(acountnumber).name
                
        self._df =  pd.read_csv(filename,sep=';',header = 3,index_col=False,skip_blank_lines = False)

        for index, row in self._df.iterrows():            
            if(pd.isnull(row['Meddelande'])):
                row['Meddelande'] = row['Transaktionstyp']

            row['Belopp'] = float(row['Belopp'].replace(',','.').replace(' ',''))


    def getMessages(self):
        return (self._df['Meddelande'].values)

    def getDate(self):
        return self._df['Bokföringsdatum']

    def getAmount(self):
        return self._df['Belopp']

    def getAcount(self):
        return self._acount


class Samples():
    def __init__(self, filename):          
        self.df = pd.read_csv(filename, sep=';')
    
        self.samples_unique = self.df[['value', 'TypeofPayment','fixedOrVariableCost', 'Category']].drop_duplicates()
        
    def getValues(self):
        return self.samples_unique['value'].values

    def getTypeOfPayment(self):
        return self.samples_unique['TypeofPayment'].values

    def getFixOrVaraibleCost(self):
        return self.samples_unique['fixedOrVariableCost'].values

    def getCategories(self):
        return self.samples_unique['Category'].values


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

def interpretUserParams( params):            
    helptext = """ Convert länsförsäkringar csv to my likings
      Usage:
      Reader.py [-h] [-i <file>] [-o <file>] [-s <file>]
      
      Options:
          -i --in <file> : File to convert
          -o --out <file> : Name of the outfile
          -s --sample <file> : Name of the file to use as samples

          -h --help             : show this help message

    """

    args = docopt(helptext,  version=1)

    inFile     = 'data.csv'
    outFile    = 'test_out.csv'
    sampleFile = 'samples.csv'

    if (args['--in']):
        inFile = args['--in']

    if (args['--out']):
        outFile = args['--out']

    if (args['--sample']):
        sampleFile = args['--sample']

    return (inFile, outFile, sampleFile)

import numpy as np

# =======================
#      MAIN PROGRAM
# =======================
if __name__ == "__main__":
    # Get the input parameters
    (inFile, outFile, sampleFile) = interpretUserParams(sys.argv)

    # Read the input file
    inData = InData(inFile)
    messages = inData.getMessages()

    # Read the sample files
    samples = Samples(sampleFile)
    values = samples.getValues()

    (distances, indices) = banan.findpartner(values, messages)

    #total_list = np.array(indices)
    #np.set_printoptions(threshold=np.inf)
    #print(total_list)

    dataSet = DataSet()

    dataSet.fillWithData(inData, samples, indices)

    #print(dataSet.getAll())


    #if (saveToDatabase)

    #if (toCsv)

    print (dataSet.toCompressDict())

    df = pd.DataFrame.from_dict(dataSet.toCompressDict(),orient='index').reset_index(drop=True)

    df = df.replace(0, '') 

    df.to_csv(outFile, index=False, sep=';')

    exit(0)

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

 

