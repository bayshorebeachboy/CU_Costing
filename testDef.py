#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      nmyers
#
# Created:     18/07/2014
# Copyright:   (c) nmyers 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
   pass

if __name__ == '__main__':
   main()

import pymysql, string, locale
from decimal import *
getcontext().prec = 2
locale.setlocale( locale.LC_ALL, 'en_US' )




# Define functions

def getCUatt(spec):
   curCost = connCost.cursor()
   query = "Select CUUNIT, CUDESC, CUFERC from CNSTUNT Where CUUNIT = '" + spec + "'"
   # curCost.execute("Select CUUNIT, CUDESC, CUFERC from CNSTUNT Where CUUNIT = '" + spec + "'")
   curCost.execute(query)
   rows = curCost.fetchall()
   for row in rows:
      SPEC = row[0]
      SPEC_DESC = row[1]
      FERC_Overriding = row[2] 
   return SPEC , SPEC_DESC, FERC_Overriding
   # print SPEC, SPEC_DESC, FERC_Overriding

def getAssem(spec):
   
   query = "Select bt.PAFRM, cu.CUDESC, cu.CUFERC, bt.PATO, jde.ItemDesc, jde.UOM, jde.Category, jde.Cost, bt.PAQTY \
From PIP00100 bt, `CNSTUNT` cu, `JDE_COST` jde \
Where cu.`CUUNIT` = bt.PAFRM \
And bt.PATO = jde.WarehouseNbr \
And bt.PAFRM In (Select bt.PATO From PIP00100 As bt Where bt.PAFRM = '" + spec + "') \
Order By PAFRM"
   curCost2 = connCost.cursor()
   curCost2.execute(query)
   rows = curCost2.fetchall()
   Assem = []
   # Populate Assem object
   for row in rows:
      Assem.append(row)
      # print "Assems: ", Assem
   return Assem

def getStock(spec):
   query = "Select bt.PAFRM, cu.CUDESC, cu.CUFERC, bt.PATO, jde.ItemDesc, jde.UOM, jde.Category, jde.Cost, bt.PAQTY \
From PIP00100 bt, `CNSTUNT` cu,`JDE_COST` jde \
Where cu.`CUUNIT` = bt.`PAFRM` \
And bt.PATO = jde.WarehouseNbr \
And bt.PAFRM In (Select bt.PAFRM From PIP00100 As bt Where bt.PAFRM = '" + spec + "') \
Order By `PATO`"
   curCost3 = connCost.cursor()
   curCost3.execute(query)
   rows = curCost3.fetchall()
   stockOnly = []
   # Populate Stock object
   for row in rows:
         stockOnly.append(row)   
   return stockOnly

def Consolidate(list):
   curInsert = connCost.cursor()
   curInsert.execute("Truncate Table STOCK_SCRATCH")
   curInsert.execute("Commit")
   curInsert.execute("Start Transaction")   
   for s in range (0, len(list)):
      si = list[s][3]
      # print si
      query = "Select * From STOCK_SCRATCH Where STOCK = '" + str(si) + "'"
      # print query
      gotcha = curInsert.execute(query)
      # print "gotcha :", gotcha
      if not gotcha:
         #assem = list[s][0]
         #assemDesc = list[s][1]
         #ferc = list[s][2]
         stock = list[s][3]
         stockDesc = connCost.escape_string(list[s][4])
         # print stockDesc
         uom = list[s][5]
         cat = list[s][6]
         cost = list[s][7]
         qty = list[s][8]
         queryInsert = "Insert Into STOCK_SCRATCH (STOCK, UOM, Category, Cost, StockDesc, Qty) Values ('" + stock + "', '" + uom + "', '" + cat +"', " + str(cost) + ", '" + stockDesc +"', "+ str(qty) + ")"
         #queryInsert = "Insert Into ASSEM_SCRATCH (ASSEM, assemDesc, FERC, PATO, ItemDesc, PAQTY, UOM, Category, Cost) Values ('" + str(assem) + "', '" + assemDesc + "', '" + str(ferc) + "', '" + stock + "', '" + stockDesc + "', '" + str(qty) + "', '" + uom + "', '" + cat + "', '" + str(cost) + "')"
         # print queryInsert
         curInsert.execute(queryInsert)
         curInsert.execute("Commit")
      else:
         # print "Update Qty"
         curUpdate = connCost.cursor()
         qty  = list[s][8]
         existing = curInsert.fetchall()
         existQty = existing[0][6]
         # print qty, "   ", existQty
         newQty = existQty + qty
         # print newQty
         queryUpdate = "UPDATE STOCK_SCRATCH SET Qty = " + str(newQty) + " Where STOCK = '" + str(si) + "'"
         # print queryUpdate
         curUpdate.execute(queryUpdate)
         curUpdate.execute("Commit")

def AddCost(current, addMe):
   # current = str(current)
   # result = Decimal(current) + Decimal(next)
   result = Decimal(current) + Decimal(addMe)
   print current, " + ", addMe, " + ", result
   # print result
   return result

def AddCost(current, next, sqty):
   result = current + (next * sqty)
   # return locale.currency(result)
   return result

spec = '213.12'
connCost = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='CU_COST')

r2 = getAssem(spec)
if len(r2) == 0:
   r2 = getStock(spec)


consolidateStock = Consolidate(r2)
curInsert = connCost.cursor()
curInsert.execute("Truncate Table ASSEM_SCRATCH")
curInsert.execute("Commit")
curInsert.execute("Start Transaction")   
for i in range(0, len(r2)):
   # print r2[i]
   assem = r2[i][0]
   desc = r2[i][1]
   ferc = r2[i][2]
   stock = r2[i][3]
   stock_desc = connCost.escape_string(r2[i][4])
   uom = r2[i][5]
   # print "5 uom", r2[i][5]
   cat = r2[i][6]
   # print "6 cat", r2[i][6]
   cost = r2[i][7]
   # print "7 cost", r2[i][7]
   qty = r2[i][8] #strCost
   # print "8 qty", r2[i][8]
   
   queryAssem = "Insert Into ASSEM_SCRATCH (ASSEM, assemDesc, FERC, PATO, ItemDesc, PAQTY, UOM, Category, Cost) Values ('" + assem + "', '" + desc + "', '" + str(ferc) + "', '" + str(stock) + "', '" + stock_desc + "', " + str(qty) + ", '" + uom + "', '" + str(cat) + "', '" + str(cost) +"')"
   # print queryAssem
   curInsert.execute(queryAssem)
## Test = [[[] for i in range(4)] for i in range(len(r3))]
curInsert.execute("Commit")
# Get config file
cf = open('/etc/SpecReport/SpecReport.txt', 'r')
for line in cf:
   file = line
# Get CU attributes and write
pf = open(line, 'w')
pf.truncate()
line = '=========================================================================================================================='
pf.write('\n')

r1 = getCUatt(spec)
spec = r1[0]
spec_desc = r1[1]
ferc = r1[2]
pf.write(line)
pf.write('\n')
pf.write('Spec: {} - Desc: {} - FERC(Overriding: {}' .format(spec, spec_desc, ferc))
pf.write('\n')
pf.write(line)
pf.write('\n')
# spec, spec_desc, ferc

curAssems = connCost.cursor()
curAssems.execute("Select Distinct ASSEM, assemDesc, FERC From ASSEM_SCRATCH")
rowsAssem = curAssems.fetchall()
# stocks = [[[] for i in range(6)] for i in range(len(rows))]
# stocks = [len(rowsAssem)]
tcost = 0
for row in rowsAssem:
   theAssem = str(row[0])
   pAssem = str(row)
   pAssem = pAssem.rstrip(')')
   pAssem = pAssem.lstrip('(')
   # print row
   # stripped = theAssem.rstrip('),')
   # stripped2 = stripped.lstrip('(')
   writeMe = "Assembly: " + row[0] + ', ' +row[1] + ', ' + str(row[2])
   pf.write(writeMe)
   pf.write('\n')
   pf.write('')
   pf.write('\n')
   curAssems2 = connCost.cursor()
   curAssems2.execute("Select PATO, ItemDesc, PAQTY, UOM, Category, Cost From ASSEM_SCRATCH Where Assem =  '" + theAssem + "'")
   rows2 = curAssems2.fetchall()
   stocks = []
   pf.write("Stock Item(s):")
   pf.write('\n')
   acost = 0.00
   format_string = '{:8s} | {:75s} | {:>3s} | {:>4s} | {:>6s} | {:>10s}'
   # writeMe = format_string.format('Stock', 'Stock Desc.', 'Qty', 'UOM', 'Type', 'Cost')
   writeMe = format_string.format('Stock', 'Stock Desc.', 'Qty', 'UOM', 'Per Cost', 'Extended Cost')
   pf.write(writeMe)
   pf.write('\n')
   format_string = '{:8s} | {:75s} | {:>3d} | {:>4s} | {:>6s} | {:>10s}'
   format_assembly_string = '{:>121}'
   for c in range(0, len(rows2)):
      stocks.insert(c, rows2[c])
      scost = float(stocks[c][5]) * stocks[c][2]
      #print locale.currency(scost)
      # writeMe = format_string.format(stocks[c][0], stocks[c][1], stocks[c][2], stocks[c][3], stocks[c][4], locale.currency(scost))
      strCost = str(stocks[c][5])
      strCost = strCost.lstrip("(Decimal('")
      strCost = strCost.rstrip("'),")
      #print strCost
      #print "Qty " , stocks[c][2]
      acost = AddCost(float(acost), float(strCost), stocks[c][2])
      ecost = float(strCost) * stocks[c][2]
      # "Calcs ", float(strCost), " ", stocks[c][2]
      # print "Extended ", ecost
      writeMe = format_string.format(stocks[c][0], stocks[c][1], stocks[c][2], stocks[c][3], locale.currency(float(strCost)), locale.currency(scost))
      pf.write(writeMe)
      pf.write('\n')
      wcost = format_assembly_string.format("Assembly Cost: " + locale.currency(acost))
      pf.write('')
      pf.write('\n')       
   pf.write(wcost)
   pf.write('\n')
   pf.write(line)
   pf.write('\n')
   #stcost = str(tcost)
   #sacost = str(acost)
   tcost = AddCost(tcost, acost, 1)
   #print "T cost ", tcost
pf.write(line)
pf.write('\n')
pf.write("Total Cost for " + spec + ": " + str (locale.currency(tcost)))
pf.close()
   
