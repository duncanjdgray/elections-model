import numpy as np
import pandas as pd
import random as rnd
import elections_classes as ec
from elections_inputs import *

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

# Order of precedence:
# done in inputs - Initialise each party with national properties (lib_auth etc, vote share for countries where it operates, std devs of lib_auth etc)
# done in inputs - Define national lists of parties (lists in _maps.py)
# todo: Create countries, for each country give it a subset of all parties
# todo: For each country, create a set of LAs
# todo: For each LA, create a set of Cons
# todo: For each Cons, create a set of Wards
# todo: Give each Ward a population
# todo: For each Cons, sum its Wards' popn
# todo: Repeat for LAs and Countries
# todo: Give each Cons a historic voteshare for each of its parties
# todo: For each Ward, take its Cons' historic voteshare
# todo: For each LA, take a popn-based weighted average of each of its Cons' voteshares
# todo: For each Country, the same
# todo: now we have a set of countries, their LAs, their cons, and their wards, each with a popn, a set of parties, and those parties' historic vote shares (or nat'l averages where no data available)
# todo: add a check - compare newly calculated country vote shares to input average vote shares - are we close?
# todo: can now run a national election under FPTP?

# useful techniques
# [x for x in list if x.property == condition]
# e.g. [x for x in wards if x.cons == specific_consituency]
# looking in a multiindexed df requires .loc[]