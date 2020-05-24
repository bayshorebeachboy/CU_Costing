Select bt.PAFRM, cu.CUDESC, cu.CUFERC, bt.PATO, jde.ItemDesc, bt.PAQTY 
From PIP00100 bt, `CNSTUNT` cu, `JDE_COST` jde
Where cu.`CUUNIT` = bt.PAFRM
And bt.PATO = jde.WarehouseNbr
# And bt.PAFRM = '80.14A'
And bt.PAFRM In (Select bt.PATO From PIP00100 As bt Where bt.PAFRM = '80.14A')
Order By PAFRM