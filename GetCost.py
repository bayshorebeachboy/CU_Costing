#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      nmyers
#
# Created:     18/08/2014
# Copyright:   (c) nmyers 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
#!/usr/bin/env python
Cost = []
Cost = [['11149', 'Bracket', 13.86]]
Cost.append(['99005', 'Bolt - 5/8', 1.15])
Cost.append(['99043', 'Washer - Square', .13])
Cost.append(['11037', 'Stirrup', 18.75])
Cost.append(['12311', 'Cond. #6', .35])
Cost.append(['99017', 'Clamp, Hot', 5.76])
Cost.append(['12311', 'Cond. #6', .35])
Cost.append(['99023', 'Connector, Squeeze On', 3.62])
Cost.append(['99005', 'Bolt - 5/8', 1.15])
Cost.append(['99043', 'Washer - Square', .13])
Cost.append(['12557', 'Cutout, 25kv', 119.69])
Cost.append(['12674', 'Connductor, #4', .99])
Cost.append(['12409', 'Cutout, Gate', 36.85])

# i = 0
Test = [[[] for i in range(4)] for i in range(len(Cost))]
# print Test

for i in range(0, len(Cost)):
    for j in range(0, 3):
        # print i, j
        Test[i][j] = Cost[i][j]
        Test[i][3] = 1
        # print Cost[i][j]

print Test
Consolidate = []
for i in range(0,len(Cost)):
    # print"Cost ", i, " - ", Cost[i]
    if Cost[i] not in Test:
        print "Not In"
        Consolidate.append(Test[i])
        qty = Cost.count(Cost[i])
        Consolidate[i][3] = qty
    else:
        print "Dupe"
    # ci = ci + 1

for i in range (0, len(Consolidate)):
    for ci in range(0, 4):
        # print i, ci
        print Consolidate[i][ci]

print Test
print Consolidate
