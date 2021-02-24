#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
from difflib import SequenceMatcher

class Info():
    def __init__(self,acountnumber = 0, acountname = '', saldo = 0, availamount = 0):
        self.acountnumber = acountnumber
        self.acountname   = acountname
        self.saldo        = saldo
        self.availamount  = availamount 

    def printa(self):
        print('acountnumber: {}'.format(self.acountnumber))
        print('acountname: {}'.format(self.acountname))
        print('saldo: {}'.format(self.saldo))
        print('availamount: {}'.format(self.availamount))

class Data():
    def __init__(self):
        self.bookdate     = 20200101
        self.transdate    = 20200101
        self.transtype    = 'empty'
       
        self.inout        = 'empty' 
        self.waytopay     = 'empty'
        self.account      = 'empty'
        self.fixedOrVariableCost = 'empty'
        self.maincategory = 'empty'
        self.category_1   = 'empty'
        self.category_2   = 'empty'
        self.category_3   = 'empty'
        self.message      = 'empty'
        self.amount       = 0

    def printa(self):
        print('bookdate: {}'.format(self.bookdate))
        print('transdate: {}'.format(self.transdate))
        print('transtype: {}'.format(self.transtype))
        print('inout: {}'.format(self.inout))
        print('waytopay: {}'.format(self.waytopay))
        print('account: {}'.format(self.account))
        print('fixedOrVariableCost: {}'.format(self.fixedOrVariableCost))

        print('maincategory: {}'.format(self.maincategory))
        print('category_1: {}'.format(self.category_1))
        print('category_2: {}'.format(self.category_2))
        print('category_3: {}'.format(self.category_3))
        print('message: {}'.format(self.message))
        print('amount: {}'.format(self.amount))

    def write(self, file1):
        date = datetime.strptime(self.bookdate , '%Y-%m-%d')

        file1.write("{};{};{};{};{};{};{};{};{}{}{}\n".format(
                                                self.inout, 
                                                self.waytopay, 
                                                self.account, 
                                                self.fixedOrVariableCost, 
                                                self.maincategory,
                                                self.category_1, 
                                                self.category_2,
                                                self.category_3,
                                                self.message, 
                                                ";" * date.month,
                                                self.amount))

        
        #print(date.month)


class Category():
    def __init__(self, value, fixedOrVariableCost, category, category_1= '', category_2= '', category_3= '', comment = ''):
        self.value = value
        self.fixedOrVariableCost = fixedOrVariableCost
        self.category = category
        self.category_1 = category_1
        self.category_2 = category_2
        self.category_3 = category_3
        self.comment = comment

    def printa(self):
        print('value: {}'.format(self.value))
        print('fixedOrVariableCost: {}'.format(self.fixedOrVariableCost))
        print('category: {}'.format(self.category))
        print('category_1: {}'.format(self.category_1))
        print('category_2: {}'.format(self.category_2))
        print('category_3: {}'.format(self.category_3))
        print('comment: {}'.format(self.comment))

def analyzeData(data, categories):

    # Check if in or out
    if (data.amount < 0):
        data.inout = "Utgifter"
    else:
        data.inout = "Inkomster" 

    if (data.message == ''):
        data.message = data.transtype    
     
        
    (category, prob)  = findMatch(data.message, categories)

    #print("Probability: {} {} {}".format(prob, category.value, category.fixedOrVariableCost))

    data.fixedOrVariableCost = category.fixedOrVariableCost
    data.maincategory = category.category

def findMatch(value, categories):
    prevProb = 0
    
    for category in categories:       
        prob = SequenceMatcher(None, value, category.value).ratio()
        
        if (prob > prevProb):
            prevCategory = category
            prevProb = prob

    #print("Message: {}, ListValue: {}, ListCategory: {}, Propability: {}".format(value,prevCategory.value, prevCategory.category, prevProb))

    return prevCategory, prevProb

def getCategories():
    categories = []

    file1 = open('category', 'r') 
  
    while True: 
        line = file1.readline() 
        if not line: 
            break

        lines = line.split(';')
        category = Category(lines[0], lines[1], lines[2], lines[3],lines[4], lines[5], lines[5])
        categories.append(category)

    file1.close() 

    return categories

def getInfo(line):
    info = Info()

    line = line.rstrip()
    line = line.replace('"','')

    lines = line.split(';')
    
    info.acountnumber  = int(lines[0])
    info.acountname    = lines[1]    
    info.saldo         = float(lines[3].replace(',','.').replace(' ',''))
    info.availamount   = float(lines[4].replace(',','.').replace(' ',''))

    return info

def getData(filename):
    allData = []

    file1 = open(filename, 'r') 
    count = 0
    file1.readline() 
    line  = file1.readline()
    info = getInfo(line) 

    file1.readline() 
    file1.readline() 

    while True: 
        data = Data()
        line = file1.readline() 
        if not line: 
            break
        line = line.rstrip()
        line = line.replace('"','')

        lines = line.split(';')

        data.bookdate  = lines[0]
        data.transdate = lines[1]
        data.transtype = lines[2]
        data.message   = lines[3]
        data.amount    = float(lines[4].replace(',','.').replace(' ',''))

        data.account = info.acountname

        allData.append(data)

    file1.close() 

    return allData

def writeToFile():
    file1 = open('output.csv', 'w')
    
    file1.write("In/ut;Betalsätt;Konto;Typ;Huvudkategori;Kategori 2;Kategori 3;Kategori 4;Vad;Januari;Februari;Mars;April;Maj;Juni;Juli;Augusti;September;Oktober;November;December\n")
    for data in allData:
        data.write(file1)



def getData(filename):
    data =  pd.read_csv(filename,sep=';',header = 3,index_col=False)

    # Replace empty meddelande
    for index, row in data.iterrows():
        if(pd.isnull(row['Meddelande'])):
            row['Meddelande'] = row['Transaktionstyp']

    #unique_org = set(data['Meddelande'].values) # set used for increased performance
    return (data['Meddelande'].values)

# =======================
#      MAIN PROGRAM
# =======================
from datetime import datetime
import yaml
import banan
import pandas as pd

# Main Program
if __name__ == "__main__":

    #a_yaml_file = open("category.yaml")
    #parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
    #print(parsed_yaml_file)


    filename = 'data.csv'
 
    if (len(sys.argv) == 2):
        filename = sys.argv[1]

    data = getData(filename)


    categories = pd.read_csv('categories.csv', sep=';')
    categories_unique = categories[['value', 'fixedOrVariableCost', 'Category']].drop_duplicates()

    value_unique = categories_unique['value'].values
    category_unique = categories_unique['Category'].values




    print(value_unique)









    banan.findpartner(value_unique,data)


    exit(0)









    filename = 'data.csv'
 
    if (len(sys.argv) == 2):
        filename = sys.argv[1]

    categories = getCategories()

    allData = getData(filename)
    
    for data in allData:
        analyzeData(data, categories)

    writeToFile()

    #allData[1].printa()

 

