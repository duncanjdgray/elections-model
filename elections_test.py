# a script for testing things out, away from main
import numpy as np
import pandas as pd
import random as rnd
import elections_classes as ec
from elections_maps import *

# import source data
data_popn_by_ward = pd.DataFrame(pd.read_csv("data/data_popn_by_ward.csv")).apply(lambda x: x.astype(str).str.lower())
data_eu_ref_by_con = pd.DataFrame(pd.read_csv("data/data_eu_ref_by_con.csv")).apply(lambda x: x.astype(str).str.lower())
ge_results_2019_wide = pd.DataFrame(pd.read_excel(
                                    io="data/1918-2019election_results_by_pcon.xlsx", 
                                    sheet_name="2019", 
                                    header=3,
                                    nrows=650,
                                    usecols="B:G,I:J,L:M,O:P,R:S,U:V,X:Y,AA:AB,AD:AE,AG:AH,AJ:AK,AM:AN,AP:AQ,AS:AV",
                                    names=["ons_id","constituency","county","country_region","country","electorate","votes_con","share_con","votes_lab","share_lab","votes_lib","share_lib","votes_bxp","share_bxp","votes_grn","share_grn","votes_snp","share_snp","votes_plaid","share_plaid","votes_dup","share_dup","votes_sf","share_sf","votes_sdlp","share_sdlp","votes_uup","share_uup","votes_all","share_all","votes_oth","share_oth","votes_total","turnout"])) \
                                .apply(lambda x: x.astype(str).str.lower())

# reshape ge2019 data
ge_results_2019_long = pd.DataFrame(ge_results_2019_wide[["constituency", "votes_con","share_con","votes_lab","share_lab","votes_lib","share_lib","votes_bxp","share_bxp","votes_grn","share_grn","votes_snp","share_snp","votes_plaid","share_plaid","votes_dup","share_dup","votes_sf","share_sf","votes_sdlp","share_sdlp","votes_uup","share_uup","votes_all","share_all","votes_oth","share_oth"]])
ge_results_2019_long = pd.wide_to_long(df=ge_results_2019_long,
                                        stubnames=["votes","share"],
                                        sep="_",
                                        i="constituency",
                                        j="party",
                                        suffix=r'\w+')

ge_results_constituencies = pd.DataFrame(data=ge_results_2019_long.index.get_level_values(0).unique().values, columns=["constituency"])
ge_results_constituencies["in_map"] = ge_results_constituencies['constituency'].isin(map_con_la)
ge_results_constituencies["in_map"].describe()

test_la = pd.DataFrame(list_la)
test_la['check'] = test_la[0].isin(map_la_nation)

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
# todo: update calling of areas to account for new arguments
uk = ec.Country("UK", 150, parties)
eng = ec.Nation("England", 100, uk, parties)
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