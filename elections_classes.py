import numpy as np 
import pandas as pd 
import random as rnd
import math
from elections_maps import *

# %% Area-based classes
class Area:
    # todo: write docstring
    
    def __init__(self, name, population, turnout=1):
        self.name = name
        self.population = population            # todo: investigate to add population from file - may want to input as a series or tuples
        self.turnout = turnout
        self.votes = []
        self.voters = []
        self.winner = []
        self.historical_vote_shares = []

    def __str__(self):
        return 'Area: {name}, Population: {population}, Voters: {voters}'.format(name=self.name, population=self.population, voters=len(self.voters))

    def __repr__(self):
        return 'Area(\'{name}\', {population}, {turnout})'.format(name=self.name, population=self.population, turnout=self.turnout)

    @property
    def population(self):
        return self._population
    
    @population.setter
    def population(self, population):
        if population >= 0:
            self._population = population
        else:
            raise ValueError("population cannot be negative!")

    @property
    def turnout(self):
        return self._turnout

    @turnout.setter
    def turnout(self, turnout):   
        if turnout >=0 and turnout <=1:         # todo: add fuzz around a national turnout input
            self._turnout = turnout
        else:
            raise ValueError("turnout must be between 0 and 1 inclusive!")

    def input_hist_shares(self, list_parties, list_shares):
        self.historical_vote_shares = []
        for i in len(list_parties):
            self.historical_vote_shares.append([list_parties[i].name, list_shares[i]])

    def set_party_voteshares(self, parties):
        self.parties_voteshares = [x.voteshare for x in parties]

    def create_voters(self, parties):
        self.voters = []
        self.set_party_voteshares()
        for i in range(0, 10):
            rnd_party = rnd.choices(parties, self.parties_voteshares, k=1)
            rnd_lib_auth, rnd_left_right, rnd_rem_leave = -11, -11, -11             # set arguments out of bounds so while loops run at least once
            while rnd_lib_auth < -10 or rnd_lib_auth >10:
                rnd_lib_auth = np.random.normal(loc=rnd_party[0].lib_auth, scale=rnd_party.scale_la)
            while rnd_left_right < -10 or rnd_left_right >10:
                rnd_left_right = np.random.normal(loc=rnd_party[0].left_right, scale=rnd_party.scale_lr)
            while rnd_rem_leave < -10 or rnd_rem_leave >10:
                rnd_rem_leave = np.random.normal(loc=rnd_party[0].rem_leave, scale=rnd_party.scale_rl)
            self.voters.append(
                Voter(name=str(i),
                      lib_auth=rnd_lib_auth,
                      left_right=rnd_left_right,
                      rem_leave=rnd_rem_leave,
                      priority_axis=rnd.choices([0,1,2,3],[10,1,2,2],k=1)[0]))      # most voters care about all axes, some prioritise one, but fewer prioritise lib-auth than left-right or rem-leave

    def print_voters(self):
        for i in self.voters:
            print(i + "\n")

    def gen_voter_prefs(self, list_parties):
        for i in self.voters:
            i.gen_parties_dist(list_parties)
            i.order_parties()

    def cast_votes(self, system):
        for i in self.voters:
            i.vote(system)

    def tally_votes(self, system):
        self.votes = []
        for i in self.voters:
            self.votes.append(i.vote_cast)
        if system == "FPTP":
            self.votes = [(x,self.votes.count(x)) for x in set(self.votes)]
            self._votes_sorted = sorted(self.votes, reverse=True, key=lambda tup: tup[1])
        else:
            raise ValueError("system not set to recognised value. Recognised values are: FPTP")

    def decide_winner(self, system):
        if system == "FPTP":
            self.winner = self._votes_sorted[0][0]
            # todo: account for ties
        else:
            raise ValueError("system not set to recognised value. Recognised values are: FPTP")

    def declare_winner(self, system):
        self.decide_winner(system)
        if system == "FPTP":
            print("The winner in " + self.name + " is " + self.winner + " with " + str(self._votes_sorted[0][1]) + \
                    " votes, beating the next closest party " + self._votes_sorted[1][0] + " which got " + \
                    str(self._votes_sorted[1][1]) + " votes.")
        else:
            raise ValueError("system not set to recognised value. Recognised values are: FPTP")


    def call_election(self, list_parties, system):
        self.create_voters(list_parties)
        self.gen_voter_prefs(list_parties)
        self.cast_votes(system)
        self.tally_votes(system)
        self.decide_winner(system)

    # todo: allow areas to hold historical vote shares for parties

class Country(Area):
    # todo: write docstrings

    def __init__(self, name, population, parties=[], turnout=1):
        Area.__init__(self, name, population, turnout)
        self.parties = parties

    def __str__(self):
        return """Country: {name}, Population: {population}, Turnout: {turnout}%, 
        Parties: {parties}""".format(
            name=self.name, 
            population=self.population, 
            turnout=self.turnout*100, 
            parties=[x.name for x in self.parties])

    def __repr__(self):
        return 'Country(\'{name}\', {population}, {parties}, {turnout})'.format(
            name=self.name, 
            population=self.population, 
            parties=self.parties, 
            turnout=self.turnout)

    @property
    def parties(self):
        return self._parties

    @parties.setter
    def parties(self, parties):   
        if all(isinstance(x, Party) for x in parties):
            self._parties = parties
        else:
            raise TypeError("all elements of parties must be Party-type objects!")

class LocalAuthority(Area):
    # todo: write docstrings
    
    def __init__(self, name, population, country, turnout=1):
        Area.__init__(self, name, population, turnout)
        self.country = country

    def __str__(self):
        return """Local Authority: {name}, part of {country}.
        Population: {population}, Turnout: {turnout}%, Voters: {voters}""".format(
            name=self.name, 
            country=self.country.name, 
            population=self.population, 
            turnout=self.turnout*100, 
            voters=len(self.voters))

    def __repr__(self):
        return 'LocalAuthority(\'{name}\', {population}, {country}, {turnout})'.format(
            name=self.name, 
            population=self.population, 
            country=self.country, 
            turnout=self.turnout)

    @property
    def country(self):
        return self._country
    
    @country.setter
    def country(self, country):
        if isinstance(country, Country):
            self._country = country
        else:
            raise ValueError("country must be a Country-type object!")

class Constituency(Area):
    # todo: write docstrings

    def __init__(self, name, population, localauthority, turnout=1):
        Area.__init__(self, name, population, turnout)
        self.la = localauthority

    def __str__(self):
        return """Constituency: {name}, part of the {localauthority} local authority. 
        Population: {population}, Turnout: {turnout}%, Voters: {voters}""".format(
            name=self.name, 
            localauthority=self.la.name, 
            population=self.population, 
            turnout=self.turnout*100, 
            voters=len(self.voters))

    def __repr__(self):
        return 'Constituency(\'{name}\', {population}, {localauthority}, {turnout})'.format(
            name=self.name, 
            population=self.population, 
            localauthority=self.la, 
            turnout=self.turnout)

    @property
    def la(self):
        return self._la
    
    @la.setter
    def la(self, localauthority):
        if isinstance(localauthority, LocalAuthority):
            self._la = localauthority
        else:
            raise ValueError("localauthority must be a LocalAuthority-type object!")

class Ward(Area):
    # todo: write docstrings

    def __init__(self, name, population, constituency, turnout=1):
        Area.__init__(self, name, population, turnout)
        self.cons = constituency

    def __str__(self):
        return """Ward: {name}, part of the {constituency} constituency. 
        Population: {population}, Turnout: {turnout}%, Voters: {voters}""".format(
            name=self.name, 
            constituency=self.cons.name, 
            population=self.population, 
            turnout=self.turnout*100, 
            voters=len(self.voters))

    def __repr__(self):
        return 'Ward(\'{name}\', {population}, {constituency}, {turnout})'.format(
            name=self.name, 
            population=self.population, 
            constituency=self.cons, 
            turnout=self.turnout)

    @property
    def cons(self):
        return self._cons
    
    @cons.setter
    def cons(self, constituency):
        if isinstance(constituency, Constituency):
            self._cons = constituency
        else:
            raise ValueError("constituency must be a Constituency-type object!")

# %% Actor-based classes
class Actor:
    # todo: write docstring
    
    def __init__(self, name, lib_auth=0, left_right=0, rem_leave=0):
        self.name = name
        self.lib_auth = lib_auth
        self.left_right = left_right
        self.rem_leave = rem_leave

    def __str__(self):
        return """Name: {name}, Lib-Auth: {lib_auth}, Left-Right: {left_right}, Remain-Leave: {rem_leave}""".format(
            name=self.name, 
            lib_auth=self.lib_auth, 
            left_right=self.left_right,
            rem_leave=self.rem_leave)

    def __repr__(self):
        return 'Actor(\'{name}\', {lib_auth}, {left_right})'.format(
            name=self.name, 
            lib_auth=self.lib_auth, 
            left_right=self.left_right,
            rem_leave=self.rem_leave)

    @property
    def lib_auth(self):
        return self._lib_auth
    
    @lib_auth.setter
    def lib_auth(self, lib_auth):
        if lib_auth >= -10 and lib_auth <= 10:
            self._lib_auth = lib_auth
        else:
            raise ValueError("lib_auth must be between -10 and 10 inclusive!")

    @property
    def left_right(self):
        return self._left_right

    @left_right.setter
    def left_right(self, left_right):
        if left_right >= -10 and left_right <= 10:
            self._left_right = left_right
        else:
            raise ValueError("left_right must be between -10 and 10 inclusive!")

    @property
    def rem_leave(self):
        return self._rem_leave
    
    @rem_leave.setter
    def rem_leave(self, rem_leave):
        if rem_leave >= -10 and rem_leave <= 10:
            self._rem_leave = rem_leave
        else:
            raise ValueError("rem_leave must be between -10 and 10 inclusive!")

class Party(Actor):
    # todo: write docstring
    
    def __init__(self, name, lib_auth=0, left_right=0, rem_leave=0, voteshare=0, scale_la=2, scale_lr=2, scale_rl=2):
        Actor.__init__(self, name, lib_auth, left_right, rem_leave)
        self.voteshare = voteshare
        self.scale_la = scale_la
        self.scale_lr = scale_lr
        self.scale_rl = scale_rl

    def __str__(self):
        return """Name: {name}, Lib-Auth: {lib_auth}, Left-Right: {left_right},
        Remain-Leave: {rem_leave}, Vote share: {voteshare}%""".format(
                name=self.name, 
                lib_auth=self.lib_auth, 
                left_right=self.left_right, 
                rem_leave = self.rem_leave, 
                voteshare=self.voteshare*100)

    def __repr__(self):
        return 'Party(\'{name}\', {lib_auth}, {left_right}, {rem_leave}, {voteshare}, {scale_la}, {scale_lr}, {scale_rl})'.format(
            name=self.name, 
            lib_auth=self.lib_auth, 
            left_right=self.left_right, 
            rem_leave=self.rem_leave, 
            voteshare=self.voteshare,
            scale_la=self.scale_la,
            scale_lr=self.scale_lr,
            scale_rl=self.scale_rl)
    
    @property
    def voteshare(self):
        return self._voteshare

    @voteshare.setter
    def voteshare(self, voteshare):
        if voteshare >= 0 and voteshare <= 1:
            self._voteshare = voteshare
        else:
            raise ValueError("voteshare must be between 0 and 1 inclusive!")

    @property
    def scale_la(self):
        return self._scale_la

    @scale_la.setter
    def scale_la(self, scale_la):
        if scale_la >= 0 and scale_la <= 5:
            self._scale_la = scale_la
        else:
            raise ValueError("scale_la must be between 0 and 5 inclusive!")

    @property
    def scale_lr(self):
        return self._scale_lr

    @scale_lr.setter
    def scale_lr(self, scale_lr):
        if scale_lr >= 0 and scale_lr <= 5:
            self._scale_lr = scale_lr
        else:
            raise ValueError("scale_lr must be between 0 and 5 inclusive!")

    @property
    def scale_rl(self):
        return self._scale_rl

    @scale_rl.setter
    def scale_rl(self, scale_rl):
        if scale_rl >= 0 and scale_rl <= 5:
            self._scale_rl = scale_rl
        else:
            raise ValueError("scale_rl must be between 0 and 5 inclusive!")

class Voter(Actor):
    # todo: write docstring
    
    """
        priority_axis will force voter to only care about one axis. check map_priority_axes for details
    """
    def __init__(self, name, lib_auth=0, left_right=0, rem_leave=0, priority_axis=0):
        Actor.__init__(self, name, lib_auth, left_right, rem_leave)
        self.priority_axis = priority_axis
        self.parties_dist = []
        self.ordered_parties = []
        self.vote_cast = []

    def __str__(self):
        return """Name: {name}, Lib-Auth: {lib_auth}, Left-Right: {left_right}, Remain-Leave: {rem_leave}, Priority: {priority_axis}""".format(
            name=self.name, 
            lib_auth=self.lib_auth, 
            left_right=self.left_right,
            rem_leave = self.rem_leave, 
            priority_axis=map_priority_axes[self.priority_axis])

    def __repr__(self):
        return 'Actor(\'{name}\', {lib_auth}, {left_right}, {rem_leave}, {priority_axis})'.format(
            name=self.name, 
            lib_auth=self.lib_auth, 
            left_right=self.left_right, 
            rem_leave=self.rem_leave,
            priority_axis=self.priority_axis)

    @property
    def priority_axis(self):
        return self._priority_axis

    @priority_axis.setter
    def priority_axis(self, priority_axis):
        if priority_axis in map_priority_axes:
            self._priority_axis = priority_axis
            self.priority_axis_readable = map_priority_axes[priority_axis]
        else:
            raise ValueError("priority_axis can only have values from " + map_priority_axes.keys())

    def gen_parties_dist(self, list_parties):
        self.parties_dist = []            # Empty existing list
        for party in list_parties:
            if self.priority_axis == 0:
                self.parties_dist.append( \
                    ((party).name, \
                    math.sqrt( \
                        (self.lib_auth - (party).lib_auth)**2 + 
                        (self.left_right - (party).left_right)**2 +
                        (self.rem_leave - (party).rem_leave)**2)))
            elif self.priority_axis == 1:
                self.parties_dist.append( \
                    ((party).name, \
                    abs(self.left_right - (party).left_right)))
            elif self.priority_axis == 2:
                self.parties_dist.append( \
                    ((party).name, \
                    abs(self.lib_auth - (party).lib_auth)))
            elif self.priority_axis == 3:
                self.parties_dist.append( \
                    ((party).name, \
                    abs(self.rem_leave - (party).rem_leave)))
            

    def order_parties(self):
        self.ordered_parties = sorted(self.parties_dist, key=lambda tup: tup[1])

    def vote(self, system):
        if system == "FPTP":
            self.vote_cast = self.ordered_parties[0][0] # vote for nearest party
            # todo: allow tactical voting?
        else:
            raise ValueError("system not set to recognised value. Recognised values are: FPTP")