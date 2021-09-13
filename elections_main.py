import numpy as np
import pandas as pd
import random as rnd
import elections_classes as ec
from elections_maps import *
from elections_inputs import *

# %% import source data
print("Importing source data...")
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
print("Initialising areas...")
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
print("Adding population data to areas...")
voting_ages = [str(x) for x in range(min_voter_age,90)]
voting_ages.append('90+')
data_popn_by_ward['voting_popn'] = data_popn_by_ward[voting_ages].apply(pd.to_numeric).sum(axis=1)
dict_ward_popn = data_popn_by_ward.set_index('Ward Name 1').to_dict()['voting_popn']

for ward in dict_wards.values():
    try: 
        ward.population = dict_ward_popn[ward.name]
    except KeyError:
        ward.population = data_popn_by_ward['voting_popn'].mean()

# scale populations down by a scale factor to make voter sizes tractable
for ward in dict_wards.values():
    ward.population /= population_scale_factor

for con in dict_constituencies.values():
    con.get_pop_from_children()

for la in dict_localauthorities.values():
    la.get_pop_from_children()

for nation in dict_nations.values():
    nation.get_pop_from_children()

uk.get_pop_from_children()

# %% add historic voteshares
print("Generating historic voteshares...")
# for each party in each constituency, get historic share. if con not found ('birmingham, selly oak'), use national shares. If NaN found, set to 0
for con in dict_constituencies.values():
    for party in con.parties:
        if con.name in ge_results_2019_long.index.get_level_values(0):
            if float(ge_results_2019_long.loc[con.name,map_party_name_code[party.name]].share) >= 0:
                con.local_voteshares[party] = float(ge_results_2019_long.loc[con.name,map_party_name_code[party.name]].share)
                con.local_votecounts[party] = float(ge_results_2019_long.loc[con.name,map_party_name_code[party.name]].votes)
            else:
                con.local_voteshares[party] = 0
                con.local_votecounts[party] = 0
        else:
            con.local_voteshares[party] = party.voteshare
            con.local_votecounts[party] = con.local_voteshares[party] * con.population

for ward in dict_wards.values():
    ward.get_local_votes_from_parent()

for la in dict_localauthorities.values():
    la.get_local_votes_from_children()

for nation in dict_nations.values():
    nation.get_local_votes_from_children()


# %% generate voters
# example code:
# dict_constituencies["ynys mon"].create_voters(list(dict_constituencies["ynys mon"].local_voteshares.keys()),list(dict_constituencies["ynys mon"].local_voteshares.values()))
print("Generating voters in constituencies...")
progress = 0
i = 0
for con in dict_constituencies.values():
    i += 1
    if i >= len(dict_constituencies)/10:
        i = 0
        progress += 0.1
        print("    " + str(round(progress * 100)) + "% of areas completed...")
    con.create_voters(list(con.local_voteshares.keys()),list(con.local_voteshares.values()))
print("    100% of areas completed.")

# %% call elections


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
# done - For each LA, take a popn-based weighted average of each of its Cons' voteshares
# done - For each Country, the same
# done - now we have a set of countries, their LAs, their cons, and their wards, each with a popn, a set of parties, and those parties' historic vote shares (or nat'l averages where no data available)
# todo: add a check - compare newly calculated country vote shares to input average vote shares - are we close?
# todo: can now run a national election under FPTP?

# useful techniques
# [x for x in list if x.property == condition]
# e.g. [x for x in wards if x.cons == specific_consituency]
# looking in a multiindexed df requires .loc[]