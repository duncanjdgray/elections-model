import elections_classes as ec

# initialise parties using data from https://www.politicalcompass.org/uk2019 plus some guesswork for rem/leave and northern ireland
# scale factors represent how broad a church the party is on that axis - higher = broader. 
p_con = ec.Party(name="Conservatives", 
                lib_auth= 7, 
                scale_la= 3,
                left_right= 9.5, 
                scale_lr= 3,
                rem_leave= 9,
                scale_rl= 3)
p_lab = ec.Party(name="Labour", 
                lib_auth= -1.5, 
                scale_la= 3,
                left_right= -4.5, 
                scale_lr= 2,
                rem_leave= -3,
                scale_rl= 2)
p_lib = ec.Party(name="Liberal Democrats", 
                lib_auth= 2.5, 
                scale_la= 1.5,
                left_right= 4, 
                scale_lr= 2,
                rem_leave= -10,
                scale_rl= 1)
p_grn = ec.Party(name="Greens", 
                lib_auth= -5, 
                scale_la= 1.5,
                left_right= -3, 
                scale_lr= 1.5,
                rem_leave= -8,
                scale_rl= 1)
p_bxp = ec.Party(name="Brexit", 
                lib_auth= 8, 
                scale_la= 1.5,
                left_right= 8.5, 
                scale_lr= 1.5,
                rem_leave= 10,
                scale_rl= 1)
p_snp = ec.Party(name="Scottish Nationals", 
                lib_auth= -1, 
                scale_la= 3,
                left_right= -2, 
                scale_lr= 1.5,
                rem_leave= -6,
                scale_rl= 2)
p_plaid = ec.Party(name="Plaid Cymru", 
                lib_auth= -1, 
                scale_la= 1.5,
                left_right= -1, 
                scale_lr= 1.5,
                rem_leave= -6,
                scale_rl= 2)
p_dup = ec.Party(name="Democratic Unionists", 
                lib_auth= 8, 
                scale_la= 1.5,
                left_right= 7, 
                scale_lr= 1.5,
                rem_leave= 8,
                scale_rl= 1.5)
p_sdlp = ec.Party(name="Social Democrats & Labour", 
                lib_auth= -1, 
                scale_la= 1.5,
                left_right= -2, 
                scale_lr= 1.5,
                rem_leave= -6,
                scale_rl= 1.5)
p_all = ec.Party(name="Alliance",           # basically the lib dems?
                lib_auth= 2.5, 
                scale_la= 1.5,
                left_right= 4, 
                scale_lr= 1.5,
                rem_leave= -8,
                scale_rl= 1.5)
p_uup = ec.Party(name="Ulster Unionists",   # basically diet tories?
                lib_auth= 7, 
                scale_la= 1.5,
                left_right= 6, 
                scale_lr= 1.5,
                rem_leave= 4,
                scale_rl= 1.5)
p_sf = ec.Party(name="Sinn Féin",           # honestly I just don't know
                lib_auth= 5, 
                scale_la= 1.5,
                left_right= -7, 
                scale_lr= 1.5,
                rem_leave= -5,
                scale_rl= 1.5)

# set vote shares (national but restricted to areas they stand in), based on 2019 dataset
p_con = 0.44
p_lab = 0.34
p_lib = 0.12
p_grn = 0.03
p_bxp = 0.05
p_snp = 0.45
p_plaid = 0.12
p_dup = 0.33
p_sdlp = 0.17
p_all = 0.17
p_uup = 0.13
p_sf = 0.26

# create sets of parties
fptp_parties = {p_con, p_lab, p_lib, p_grn, p_bxp, p_snp, p_plaid, p_dup, p_sdlp, p_all, p_uup, p_sf}
fptp_parties_eng = {p_con, p_lab, p_lib, p_grn, p_bxp}
fptp_parties_scot = {p_con, p_lab, p_lib, p_grn, p_snp}
fptp_parties_wal = {p_con, p_lab, p_lib, p_grn, p_plaid}
fptp_parties_ni = {p_dup, p_sdlp, p_all, p_uup, p_sf}
