# a script for testing things out, away from main
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
berm = ec.Constituency("Bermondsey and Old Southwark", 20, corn, corn.parties)
trey = ec.Ward("Treyarnon", 5, pad, pad.parties)
const = ec.Ward("Constantine", 5, pad, pad.parties)
wal = ec.Ward("Walworth", 10, berm, berm.parties)
enc = ec.Ward("Elephant & Castle", 10, berm, berm.parties)

print(trey)
print(pad)
print(corn)
print(eng)
print(uk)

print('\n')

wards = [trey, const, wal, enc]
wards_pad = [x for x in wards if x.cons == pad]
print("Printing all wards in 'wards'")
for x in wards:
    print(x)

print('\n')
print("Printing only wards in 'wards_pad'")
for x in wards_pad:
    print(x)