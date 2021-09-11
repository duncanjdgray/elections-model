import numpy as np 
import pandas as pd 
import math
import elections_classes as ec

# map of priority axes to human-readable
map_priority_axes = {0: "No priority axis",
                     1: "Left-Right",
                     2: "Lib-Auth",
                     3: "Remain-Leave"}


# map wards to constituencies and constituencies to local authorities
ward_con_la = pd.DataFrame(pd.read_csv("data/map_ward_con_la.csv")).apply(lambda x: x.astype(str).str.lower())
map_ward_con = pd.Series(ward_con_la['PCON18NM'].values,index=ward_con_la['WD18NM']).to_dict()
map_con_la = pd.Series(ward_con_la['LAD18NM'].values,index=ward_con_la['PCON18NM']).to_dict()

# list wards, constituencies and local authorities
ward_con_la_lists = [ward_con_la[i].unique().tolist() for i in ward_con_la.columns]
list_ward_code = ward_con_la_lists[0]
list_ward = ward_con_la_lists[1]
list_con_code = ward_con_la_lists[2]
list_con = ward_con_la_lists[3]
list_la_code = ward_con_la_lists[4]
list_la = ward_con_la_lists[5]
