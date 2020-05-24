import pymysql, string, locale
from decimal import *
getcontext().prec = 2
locale.setlocale( locale.LC_ALL, 'en_US' )

connCost = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='CU_COST')


def AddCost(current, next):
    result = current + next
    return locale.currency(result)
curTest = connCost.cursor()
query = "Select All Cost From JDE_COST Where Stock = '11001'"
curTest.execute(query)
rows = curTest.fetchall()
for row in rows:
    testCost = row
    
print row
strCost = str(row)
strCost = strCost.lstrip("(Decimal('")
strCost = strCost.rstrip("'),")
print strCost
Test = AddCost(float(1.2345), float(strCost))
print (Test)