from xgw_data import updateDataLine, CURRENT

updateDataLine("CONTROL", "[C:1 s1000000+23.8 d-0.08 p21.7 q2.0 w00 i999+0.1 a003+0.0 u02051111]\r\n")
updateDataLine("BOILER", "[B: s3 t75 a0007 b0007 c0122 d0691 u01013245]o*\r\n")
updateDataLine("WEATHER", "[4:  22.5 38%    ]\r\n")
updateDataLine("WEATHER", "[P:  24.0 1005.1 ]\r\n")
updateDataLine("WEATHER", "[W:  12  11 SSE  ]\r\n")

print CURRENT.data

assert 1 == CURRENT.data["DC"].value
assert 23.8 == CURRENT.data["DCs1"].value
assert -0.08 == CURRENT.data["DCd"].value

assert 3 == CURRENT.data["DBs"].value
assert 75 == CURRENT.data["DBt"].value

assert 22.5 == CURRENT.data["D4"].value
assert 38 == CURRENT.data["D41"].value

assert 24 == CURRENT.data["DP"].value
assert 1005.1 == CURRENT.data["DP1"].value

assert 12 == CURRENT.data["DW"].value
assert 11 == CURRENT.data["DW1"].value
