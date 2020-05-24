Select All bt.PAFRM, cu.CUDESC, bt.PATO, jde.ItemDesc, bt.PAQTY 
From PIP00100 bt Inner Join CNSTUNT cu On cu.CUUNIT = bt.PAFRM 
Inner Join JDE_COST jde On jde.WarehouseNbr = bt.PATO
Where bt.PAFRM In (Select bt.PATO From PIP00100 As bt Where bt.PAFRM = '21.21')