import numpy as np
import pandas as pd
import random as rnd
import elections_classes as ec
from elections_maps import *
from elections_inputs import *

# %% import source data
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

# %% create Areas
uk = ec.Country("united kingdom",0)

dict_nations = dict()
for nation in list_nation:
    dict_nations[nation] = ec.Nation(nation, 0, uk, parties=map_nation_parties[nation])
    uk.append_children(dict_nations[nation])

dict_localauthorities = dict()
for la in list_la:
    dict_localauthorities[la] = ec.LocalAuthority(la, 0, dict_nations[map_la_nation[la]], parties=dict_nations[map_la_nation[la]].parties)
    dict_localauthorities[la].parent.append_children(dict_localauthorities[la])

dict_constituencies = dict()
for con in list_con:
    dict_constituencies[con] = ec.Constituency(con, 0, dict_localauthorities[map_con_la[con]], parties=dict_localauthorities[map_con_la[con]].parties)
    dict_constituencies[con].parent.append_children(dict_constituencies[con])

dict_wards = dict()
for ward in list_ward:
    dict_wards[ward] = ec.Ward(ward, 0, dict_constituencies[map_ward_con[ward]], parties=dict_constituencies[map_ward_con[ward]].parties)
    dict_wards[ward].parent.append_children(dict_wards[ward])

# %% add populations
voting_ages = [str(x) for x in range(min_voter_age,90)]
voting_ages.append('90+')
data_popn_by_ward['voting_popn'] = data_popn_by_ward[voting_ages].apply(pd.to_numeric).sum(axis=1)
dict_ward_popn = data_popn_by_ward.set_index('Ward Name 1').to_dict()['voting_popn']

for ward in dict_wards.values():
    try: 
        ward.population = dict_ward_popn[ward.name]
    except KeyError:
        ward.population = data_popn_by_ward['voting_popn'].mean()

for con in dict_constituencies.values():
    con.population = 0
    for ward in con.children:
        con.population += ward[0].population

for la in dict_localauthorities.values():
    la.population = 0
    for con in la.children:
        la.population += con[0].population

for nation in dict_nations.values():
    nation.population = 0
    for la in nation.children:
        nation.population += la[0].population

uk.population = 0
for nation in uk.children:
    uk.population += nation[0].population

# %% add historic voteshares

# for each party in each constituency, get historic share. if con not found ('birmingham, selly oak'), use national shares. If NaN found, set to 0
for con in dict_constituencies.values():
    for party in con.parties:
        if con.name in ge_results_2019_long.index.get_level_values(0):
            if float(ge_results_2019_long.loc[con.name,map_party_name_code[party.name]].share) >= 0:
                con.local_voteshares[party] = float(ge_results_2019_long.loc[con.name,map_party_name_code[party.name]].share)
            else:
                con.local_voteshares[party] = 0
        else:
            con.local_voteshares[party] = party.voteshare

for con in dict_constituencies.values():
    for ward in con.children:
        ward.local_voteshares = con.local_voteshares



# %% generate voters
# example code:
# dict_constituencies["ynys mon"].create_voters(list(dict_constituencies["ynys mon"].local_voteshares.keys()),list(dict_constituencies["ynys mon"].local_voteshares.values()))

# Order of precedence:
# done in inputs - Initialise each party with national properties (lib_auth etc, vote share for countries where it operates, std devs of lib_auth etc)
# done in inputs - Define national lists of parties (lists in _maps.py)
# done - Create countries, for each country give it a subset of all parties
# done - For each country, create a set of LAs
# done - For each LA, create a set of Cons
# done - For each Cons, create a set of Wards
# done -  Give each Ward a population
# done - For each Cons, sum its Wards' popn
# done - Repeat for LAs and Countries
# done - Give each Cons a historic voteshare for each of its parties
# done - For each Ward, take its Cons' historic voteshare
# todo: For each LA, take a popn-based weighted average of each of its Cons' voteshares
# todo: For each Country, the same
# todo: now we have a set of countries, their LAs, their cons, and their wards, each with a popn, a set of parties, and those parties' historic vote shares (or nat'l averages where no data available)
# todo: add a check - compare newly calculated country vote shares to input average vote shares - are we close?
# todo: can now run a national election under FPTP?

# useful techniques
# [x for x in list if x.property == condition]
# e.g. [x for x in wards if x.cons == specific_consituency]
# looking in a multiindexed df requires .loc[]