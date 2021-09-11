import numpy as np
import pandas as pd
import random as rnd
import elections_classes as ec

# import source data
data_popn_by_ward = pd.DataFrame(pd.read_csv("data/data_popn_by_ward.csv"))
data_eu_ref_by_con = pd.DataFrame(pd.read_csv("data/data_eu_ref_by_con.csv"))

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

# useful techniques
# [x for x in list if x.property == condition]
# e.g. [x for x in wards if x.cons == specific_consituency]