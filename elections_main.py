import numpy as np
import pandas as pd
import random as rnd
import elections_classes as ec

# import source data
data_popn_by_ward = pd.DataFrame(pd.read_csv("data/data_popn_by_ward.csv"))
data_eu_ref_by_con = pd.DataFrame(pd.read_csv("data/data_eu_ref_by_con.csv"))

# Test code for setting up one area

lab = ec.Party("Labour", -2, -6, -5, 0.3)
con = ec.Party("Conservatives", 3, 8, 9, 0.4)
lib = ec.Party("Liberal Democrats", -8, 0, -10, 0.1)
ukip = ec.Party("UKIP", 8, 10, 10, 0.05)

parties = [lab, con, lib, ukip]

here = ec.Area("Treyarnon", 10, parties, 0.7)

# here.call_election(parties,"FPTP")
# print(here.votes)
# print(here.winner)
# here.declare_winner("FPTP")

# testing setting up various tiers of area
uk = ec.Nation("UK", 150, parties)
eng = ec.Country("England", 100, uk, parties)
corn = ec.LocalAuthority("Cornwall", 25, eng, uk.parties)
pad = ec.Constituency("Padstow", 10, corn, corn.parties)
trey = ec.Ward("Treyarnon", 5, pad, pad.parties)

print(trey)
print(pad)
print(corn)
print(eng)
print(uk)


# Order of precedence:
# Initialise each party with national properties (lib_auth etc, vote share for countries where it operates, std devs of lib_auth etc)
# Define national lists of parties (lists in _maps.py)
# Create countries, for each country give it a subset of all parties
# For each country, create a set of LAs
# For each LA, create a set of Cons
# For each Cons, create a set of Wards
# Give each Ward a population
# For each Cons, sum its Wards' popn
# Repeat for LAs and Countries
# Give each Cons a historic voteshare for each of its parties
# For each Ward, take its Cons' historic voteshare
# For each LA, take a popn-based weighted average of each of its Cons' voteshares
# For each Country, the same
# now we have a set of countries, their LAs, their cons, and their wards, each with a popn, a set of parties, and those parties' historic vote shares (or nat'l averages where no data available)
# add a check - compare newly calculated country vote shares to input average vote shares - are we close?
# can now run a national election under FPTP?