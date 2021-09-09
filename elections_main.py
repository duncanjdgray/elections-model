import numpy as np 
import pandas as pd 
import elections_classes

# Test code for setting up one area
here = Area("Treyarnon",10,0.7)

lab = Party("Labour",-2,-6,0.3)
con = Party("Conservatives", 3, 8, 0.4)
lib = Party("Liberal Democrats", 0, -8, 0.1)
ukip = Party("UKIP", 8, 10, 0.05)

parties = [lab,con,lib,ukip]

here.create_voters()

here.gen_voter_prefs(parties)