#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
from difflib import SequenceMatcher
from datetime import datetime
import yaml
import banan
import pandas as pd
from matplotlib import style


accounts = {
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






# class Category():
#     def __init__(self, value, fixedOrVariableCost, category, category_1= '', category_2= '', category_3= '', comment = ''):
#         self.value = value
#         self.fixedOrVariableCost = fixedOrVariableCost
#         self.category = category
#         self.category_1 = category_1
#         self.category_2 = category_2
#         self.category_3 = category_3
#         self.comment = comment

#     def printa(self):
#         print('value: {}'.format(self.value))
#         print('fixedOrVariableCost: {}'.format(self.fixedOrVariableCost))
#         print('category: {}'.format(self.category))
#         print('category_1: {}'.format(self.category_1))
#         print('category_2: {}'.format(self.category_2))
#         print('category_3: {}'.format(self.category_3))
#         print('comment: {}'.format(self.comment))

# def analyzeData(data, categories):

#     # Check if in or out
#     if (data.amount < 0):
#         data.inout = "Utgifter"
#     else:
#         data.inout = "Inkomster" 

#     if (data.message == ''):
#         data.message = data.transtype    
     
        
#     (category, prob)  = findMatch(data.message, categories)

#     #print("Probability: {} {} {}".format(prob, category.value, category.fixedOrVariableCost))

#     data.fixedOrVariableCost = category.fixedOrVariableCost
#     data.maincategory = category.category

# def findMatch(value, categories):
#     prevProb = 0
    
#     for category in categories:       
#         prob = SequenceMatcher(None, value, category.value).ratio()
        
#         if (prob > prevProb):
#             prevCategory = category
#             prevProb = prob

#     #print("Message: {}, ListValue: {}, ListCategory: {}, Propability: {}".format(value,prevCategory.value, prevCategory.category, prevProb))

#     return prevCategory, prevProb

class Test():
    def __init__(self):
       
        self.theDict= {}
       
    # def add(self,row):


        # if row.message in self.key:  # Already exist

        #     self.amount[key[message]] += row.amount  
        # else:
        #     self.theDict[row.message] = 
        #     self.inout.append( row.inout )
        #     self.waytopay.append( row.waytopay )
        #     self.account.append( row.account )
        #     self.fixedOrVariableCost.append( row.fixedOrVariableCost )
        #     self.maincategory.append( row.maincategory )
        #     self.category_1.append( row.category_1 )
        #     self.category_2.append( row.category_2 )
        #     self.category_3.append( row.category_3 )
        #     self.message.append( row.message )
        #     self.month.append( row.month )
        #     self.amount.append( row.amount )


        #     self.index += 1    

class Gustaf():

    def __init__(self, data1, data2):
        self.data1 = data1
        self.data2 = data2


class theBoss():
    def __init__(self):
        self.theDict = {}

    def add(self, row):
        self.theDict[row.message] = {'In/ut'          : row.inout, 
                                     'Betalsätt'      : row.waytopay,
                                     'Konto'          : row.account,
                                     'Typ'            : row.fixedOrVariableCost,
                                     'Huvudkategori'  : row.maincategory,
                                     'Kategori 1'     : row.category_1,
                                     'Kategori 2'     : row.category_2,
                                     'Kategori 3'     : row.category_3,
                                     'Message'        : row.message,
                                     'Kostnad'        : row.amount,
                                     'month'        : row.month

                                     
                                    }


    def getAll(self):
        return self.theDict


class Row():
    def __init__(self,inout,waytopay,account,fixedOrVariableCost,maincategory,category_1,category_2,category_3,message,month,amount):
      
        self.inout        = inout
        self.waytopay     = waytopay
        self.account      = account
        self.fixedOrVariableCost = fixedOrVariableCost
        self.maincategory = maincategory
        self.category_1   = category_1
        self.category_2   = category_2
        self.category_3   = category_3
        self.message      = message
        self.month        = month
        self.amount       = amount

    def get(self):
        return [self.inout,self.waytopay]

class Freja():
    def __init__(self, filename):
        tempdf =  pd.read_csv(filename,sep=';',header = 0,index_col=False, nrows = 1)
        self.info = self.__getInfo(tempdf)
                
        self.df =  pd.read_csv(filename,sep=';',header = 3,index_col=False,skip_blank_lines = False)

        for index, row in self.df.iterrows():            
            if(pd.isnull(row['Meddelande'])):
                row['Meddelande'] = row['Transaktionstyp']


    def __getInfo(self, df):
        info = Info()       
        info.acountnumber  = int(df['Kontonummer'][0])
        #info.acountname    = df['Kontonamn'][0]
        try:
             info.acountname = accounts[info.acountnumber]
        except:
             info.acountname = ''
       

        return info

    def getMessages(self):
        #unique_org = set(data['Meddelande'].values) # set used for increased performance
        return (self.df['Meddelande'].values)

    def writeToFile(self, filename, samples, indices):
        #file1 = open(filename, 'w')

        #file1.write("In/ut;Betalsätt;Konto;Typ;Huvudkategori;Kategori 2;Kategori 3;Kategori 4;Vad;Januari;Februari;Mars;April;Maj;Juni;Juli;Augusti;September;Oktober;November;December\n")

        tB = theBoss()
        for i,j in enumerate(indices):
            
            #In/ut	Betalsätt	Konto	Typ	Huvudkategori	Kategori 2	Kategori 3	Kategori 4	Vad	Januari	Februari	Mars	April	Maj	Juni	Juli	Augusti	September	Oktober	November	December	Per månad		Kommentar									
            
            amount                  = float(self.df['Belopp'][i].replace(',','.').replace(' ',''))
          
            if (amount < 0):
                inout = "Utgifter"
            else:
                inout = "Inkomster" 

            waytopay                = samples.getTypeOfPayment()[j][0]
            account                 = self.info.acountname
            fixedOrVariableCost     = samples.getFixOrVaraibleCost()[j][0]
            maincategory            = samples.getCategories()[j][0]
            category_1              = ''
            category_2              = ''
            category_3              = ''
            message                 = self.df['Meddelande'][i]
            month                   = datetime.strptime(self.df['Bokföringsdatum'][i] , '%Y-%m-%d').month            
           
            row  = Row(inout, waytopay,account,fixedOrVariableCost,maincategory,category_1,category_2,category_3, message, month ,amount)

            tB.add(row)

            
            #file1.write("{};{};{};{};{};{};{};{};{}{}{}\n".format(
            #                                    inout, 
            #                                    waytopay,
            #                                    account, 
            #                                    fixedOrVariableCost, 
            #                                    maincategory,
            #                                    category_1, 
            #                                    category_2,
            #                                    category_3,
            #                                    message, 
            #                                    ";" * month,
            #                                    amount))
        
        df =pd.DataFrame.from_dict(tB.getAll(),orient='index').reset_index(drop=True)

        df.to_csv('test_out.csv', index=False)
        
       

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

# =======================
#      MAIN PROGRAM
# =======================

from collections import defaultdict




if __name__ == "__main__":


    # theB = theBoss()

    # g = Gustaf('key1',222)
    # theB.add(g)
    # g = Gustaf('key2',4444)
    # theB.add(g)

    #print(theB.getAll())

    # df =pd.DataFrame.from_dict(theB.getAll(),orient='index').reset_index(drop=True)

    # df.to_csv('test_out.csv', index=False)

    # test.add(row)

    # theDict = {}
    # DictWatch = {'jack': 222, 'sape': 3333}
    #theDict['nummer1'] = defaultdict
    #DictWatch = {'jack': 4444, 'sape': 5555}
    #theDict['nummer2'] = defaultdict

    #DictWatch = {999}
    #theDict['nummer3'] = defaultdict
    #print(DictWatch)



    #s = pd.Series(list(theDict.values())) 

    #print(theDict.values())

    #df =pd.DataFrame.from_dict(theDict,orient='index').reset_index(drop=True)

    #df.to_csv('test_out.csv', index=False)


    # exit(0)

    pd.set_option('display.max_colwidth', -1)
    style.use('fivethirtyeight')

    dataFile = 'data.csv'
    sampleFile = 'samples.csv'
 
    if (len(sys.argv) == 2):
        dataFile = sys.argv[1]

    if (len(sys.argv) == 3):
        sampleFile = sys.argv[2]

    freja = Freja(dataFile)
    messages = freja.getMessages()

    samples = Samples(sampleFile)
    values = samples.getValues()
    categories = samples.getCategories()

    distances, indices = banan.findpartner(values, messages)


    freja.writeToFile('output.csv',samples,indices)

    # matches = []

    # for i,j in enumerate(indices):
    #     temp = [distances[i][0], values[j],categories[j], messages[i]]
    #     matches.append(temp)

    # matches = pd.DataFrame(matches, columns=['Match confidence (lower is better)','Value','Category', 'From data'])

    # print(matches)

    #allData[1].printa()

 

