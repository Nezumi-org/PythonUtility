#!/bin/python
import sys, string

class Transaction:
    '''This class represents a transaction record
    param date: transaction date
    param discription: details containing merchant name
    param amount: amount spent in this transaction'''
    def __init__(self,date, discription, amount):
        self.date = date
        self.discription = string.upper(discription)
        self.amount = amount
        self.isClasified = False
    def __str__(self):
        return '%s | %s | $%s' %(self.date, self.discription, self.amount)

class Categorizer:
    '''This class represents a meachant categorized by the caller
    param name: sets the name of the object'''
    def __init__(self, name):
        self.name = name
        self.total = 0

    def addAmount(self, amt):
        self.total += float(amt)

    def __str__(self):
        return '%-23s | $%-20s ' %(self.name, self.total)

class Category:
    '''This class contains a list of Categorizer objects and defines a categoy for the collection. 
    param name: pass the name of the Category object
    param list is a list of Categoizer object'''
    def __init__(self, name, list):
        self.name = name
        self.categorizedList = list
        self.index = 0

    def getGrandTotal(self):
        '''returns a total amount spent in the category'''
        totalPerCategory = 0
        for merchant in self.categorizedList:
            totalPerCategory += float(merchant.total)
        return totalPerCategory

    #def __str__(self):
    #    return 'Category Name => %s |' %(self.name)

    def printList(self):
        for category in self.categorizedList:
            print category

        print '-----------\nCategory => %-5s Total | $%s\n' %(self.name,self.getGrandTotal())
    def __iter__(self):
        return self

    def next(self):
        if self.index >= len(self.categorizedList):
            self.index = 0
            raise StopIteration
        result = self.categorizedList[self.index]
        self.index += 1
        return result


class Statement:
    '''This is the top level class that reads in a csv file, sets types of category 
    to inquire, and prints out the total spendings by mechant and/or category.
 
    Assumptions: The input file is cvs file, regularlly formatted, and 
    each listing is sorted by decending date. '''

    def __init__(self, filename, *args):
        self.categoryList = list(args)
        self.grandTotal = 0
        self.transactionList = []
        self.buildTransactionList(filename)

    def buildTransactionList(self, filename):
        infile = open(filename, 'r')
        lines = infile.readlines()
        for line in lines:
            fieldList =line.split(',')
            record = Transaction( fieldList[0], fieldList[2], fieldList[4])
            self.transactionList.append(record)
  
    def processTransaction(self):
        '''Public function '''
        for record in self.transactionList:
            for category in self.categoryList:
                for merchant in category.categorizedList:
                    if record.discription.find(merchant.name)!= -1:
                        merchant.addAmount( record.amount)
                        #print record.date, record.discription, record.amount
                        record.isClasified = True
                        break

    def printGrandTotal(self):
        print 'Period: %s--%s' %(self.transactionList[1].date, self.transactionList[-1].date)
        for category in self.categoryList:
            category.printList()
            #print category

    def printUnknownMerchants(self):
       for record in self.transactionList:
           if record.isClasified == False:
               print 'Unknow merchants: %s' %(record.discription)

    def __str__(self):
       #  return '%s | Total Grocery => $%s' %(self.period, self.getGrandTotal())
        pass

if __name__=='__main__':

    Food = Category('Food', [ Categorizer('CENTRAL MARKET'),
                              Categorizer( 'FRED-MEYER'),
                              Categorizer('PCC'),
                              Categorizer('QFC'),
                              Categorizer('TRADER JOE\'S'),
                              Categorizer('UWAJIMAYA')] )

    Hobby = Category('Hobby',[ Categorizer('AMAZON'),
                               Categorizer('UNCLES GAMES'),
                               Categorizer('LOWES')] )

    Gas = Category('Gas', [Categorizer('CHEVRON'),
                           Categorizer('UNION'),
                           Categorizer('SHELL')])

    if len(sys.argv) < 2:
        print 'Usage: \'python ', sys.argv[0], ' xxx.csv\''
        sys.exit(1)

    s = Statement( sys.argv[1], Food, Hobby, Gas)

    s.processTransaction()
    s.printGrandTotal()
#    s.printUnknownMerchants()
    
