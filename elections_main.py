import numpy as np 
import pandas as pd 
import elections_classes as ec

# import source data
data_popn_by_ward = pd.DataFrame(pd.read_csv("data/data_popn_by_ward.csv"))

# Test code for setting up one area
here = ec.Area("Treyarnon",10,0.7)

lab = ec.Party("Labour", -2, -6, -5, 0.3)
con = ec.Party("Conservatives", 3, 8, 9, 0.4)
lib = ec.Party("Liberal Democrats", -8, 0, -10, 0.1)
ukip = ec.Party("UKIP", 8, 10, 10, 0.05)

parties = [lab,con,lib,ukip]

here.call_election(parties,"FPTP")
print(here.votes)
print(here.winner)
here.declare_winner("FPTP")