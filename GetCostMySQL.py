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
import pymysql 
import itertools

# Get SPEC info
spec = '80.14A'
connCost = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='CU_COST')

# Define functions

def getCUatt(spec):
   curCost = connCost.cursor()
   query = "Select CUUNIT, CUDESC, CUFERC from CNSTUNT Where CUUNIT = '" + spec + "'"
   curCost.execute(query)
   rows = curCost.fetchall()
   for row in rows:
      SPEC = row[0]
      SPEC_DESC = row[1]
      FERC_Overriding = row[2] 
   return SPEC , SPEC_DESC, FERC_Overriding
   
def getAssem(spec):
   
   query = "Select bt.PAFRM, cu.CUDESC, cu.CUFERC, bt.PATO, jde.ItemDesc, bt.PAQTY \
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
   return Assem
   
def getStock(spec):
   query = "Select bt.PAFRM, cu.CUDESC, cu.CUFERC, bt.PATO, jde.ItemDesc, bt.PAQTY \
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
###################################################################################

# Get CU attributes
r1 = getCUatt(spec)
spec = r1[0]
spec_desc = r1[1]
ferc = r1[2]

print "SPEC :", r1

# Get Components
r2 = getAssem(spec)
if len(r2) == 0:
   r2 = getStock(spec)
print ""
print "Initial R2:"
for i in range(0, len(r2)):
   print i + 1, '. ', r2[i]
print ""








## Get Component2
#r3 = []
#for i in range(0, len(r2)):
   #spec = r2[i][0]
   #r3.append(getAssem(spec))
## print r3
#if r3[0] == []:
   ## print 'True'
   #r3 = r2
##print ""
##print "Initial R3:"
##for i in range(0, len(r3)):
   ##print i + 1, '. ', r3[i]   
##print ""

#singles=[]
## print "One at a Time..."
## print 
#for i in range(0, len(r3)):
   #for j in range(0, len(r3[i])):
      #singles.append(r3[i][j])
      ## print r3[i][j]

##print
##print "Singles ", singles


##Test = [[[] for i in range(4)] for i in range(len(r3))]
##for i in range(0, len(r3)):
   ##Test[i] = r3[i][0]

#Test = []
#for i in range(0, len(r3)):
   #for j in range(0, len(r3[i])):
      #Test.append(r3[i][j][0])
      ## Test.append(r3[i][j][1])


##print ""
##print "Initial Test:"
##for i in range(0, len(Test)):
   ##print i + 1, '. ', Test[i]
##print ""

#Test.sort()
#Consolidate = list(Test for Test,_ in itertools.groupby(Test))
#print ""
#print "Initial Consolidate:"
#for i in range(0, len(Consolidate)):
   #print i + 1, '. ', Consolidate[i]
#print ""
 
### Get Stock Item Desciptions and Cost parameters from JDE1ItemCosts
## print Consolidate

#Cost = []
### for item in Stock:
#for ci in range(0, len(Test)):
   #curCost3 = connCost.cursor()
   #temp = Test[ci]
   ## print Consolidate[ci][0]
   #target = temp
   ## print target
   #query = "Select WarehouseNbr, UOM, Category, Cost, ItemDesc from JDE_COST Where WarehouseNbr = '" + str(target) + "'"
   ## print (query)
   #curCost3.execute(query)
   #crows = curCost3.fetchall()
   #for crow in crows:
      #Cost.append(crow)
       ## print "Appended " + str(crow)
       ## ci = ci + 1
##print ""
##print "Initial Cost:"
##for i in range(0, len(Cost)):
   ##print 
   ##print i + 1, '. ', Cost[i]

##print ""

#curInsert = connCost.cursor()
#curInsert.execute("Start Transaction")
#for s in range(0, len(Cost)):
   #si = Cost[i][0]
   ## gotcha = curInsert.execute("Select * From STOCK_SCRATCH Where STOCK = '" + str(si) + "'")
   ## if not gotcha:
   #stock = Cost[s][0]
   #uom = Cost[s][1]
   #cat = Cost[s][2]
   #cost = Cost[s][3]
   #desc = Cost[s][4]
   #qty = singles[s][1]
   #queryInsert = "Insert Into STOCK_SCRATCH (STOCK, UOM, Catagory, Cost, stockDesc, Qty, FERC) Values ('" + str(stock) + "', '" + uom + "', '" + cat + "', '" + cost + "', '" + desc + "', '" + str(qty) + "', '')"
   #print queryInsert
   #curInsert.execute(queryInsert)
   
#curInsert.execute("Commit")      



##print "##################################################################################"
##print ""
### Report
##print "Summary for ", r1[0]
##print ""
##print "R1 (Spec):"
##print ""
##for i in range(0, len(r1)):
   ##print i + 1, '. ', r1[i]
##print ""
##print "R2:"
##for i in range(0, len(r2)):
   ##print i + 1, '. ', r2[i]
##print ""
##print "R3:"
##for i in range(0, len(r3)):
   ##print i + 1, '. ', r3[i]
##print ""
##print "Test:"
##for i in range(0, len(Test)):
   ##print i + 1, '. ', Test[i]
##print ""
##print "Consolidate:"
##for i in range(0, len(Consolidate)):
   ##print i + 1, '. ', Consolidate[i]
##print ""
##print "Cost:"
##for i in range(0, len(Cost)):
   ##print 
   ##print i + 1, '. ', Cost[i]


