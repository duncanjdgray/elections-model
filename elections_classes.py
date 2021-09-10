import numpy as np 
import pandas as pd 
import math
import random
from elections_maps import *

# %% Area-based classes
class Area:
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

    def create_voters(self):
        self.voters = []                        # clear any existing list of voters
        for i in range(0,math.ceil(self.population * self.turnout)):
            self.voters.append(
                Voter(name=str(i),
                      lib_auth=random.uniform(-10,10),
                      left_right=random.uniform(-10,10),
                      rem_leave=random.uniform(-10,10),
                      priority_axis=random.choices([0,1,2,3],[5,1,1,2],k=1)[0]))         # todo: make voters not purely random

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
        self.create_voters()
        self.gen_voter_prefs(list_parties)
        self.cast_votes(system)
        self.tally_votes(system)
        self.decide_winner(system)

    # todo: allow areas to hold historical vote shares for parties

class Constituency(Area):
    def __init__(self, name, population, turnout=1):
        Area.__init__(self, name, population, turnout)

    def __str__(self):
        return 'Area: {name}, Population: {population}, Turnout: {turnout}, Voters: {voters}'.format(name=self.name, population=self.population, turnout=self.turnout, voters=len(self.voters))

    def __repr__(self):
        return 'Constituency(\'{name}\', {population}, {turnout})'.format(name=self.name, population=self.population, turnout=self.turnout)

class LocalAuthority(Area):
    def __init__(self, name, population, turnout=1):
        Area.__init__(self, name, population, turnout)

    def __str__(self):
        return 'Area: {name}, Population: {population}, Turnout: {turnout}, Voters: {voters}'.format(name=self.name, population=self.population, turnout=self.turnout, voters=len(self.voters))

    def __repr__(self):
        return 'Constituency(\'{name}\', {population}, {turnout})'.format(name=self.name, population=self.population, turnout=self.turnout)

# %% Actor-based classes
class Actor:
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
    def __init__(self, name, lib_auth=0, left_right=0, rem_leave=0, voteshare=0):
        Actor.__init__(self, name, lib_auth, left_right, rem_leave)
        self.voteshare = voteshare

    def __str__(self):
        return """Name: {name}, Lib-Auth: {lib_auth}, Left-Right: {left_right}, \
            Remain-Leave: {rem_leave}, Vote share: {voteshare}%""".format(
                name=self.name, 
                lib_auth=self.lib_auth, 
                left_right=self.left_right, 
                rem_leave = self.rem_leave, 
                voteshare=self.voteshare*100)

    def __repr__(self):
        return 'Party(\'{name}\', {lib_auth}, {left_right}, {rem_leave}, {voteshare})'.format(
            name=self.name, 
            lib_auth=self.lib_auth, 
            left_right=self.left_right, 
            rem_leave=self.rem_leave, 
            voteshare=self.voteshare)

    @property
    def voteshare(self):
        return self._voteshare

    @voteshare.setter
    def voteshare(self, voteshare):
        if voteshare >= 0 and voteshare <= 1:
            self._voteshare = voteshare
        else:
            raise ValueError("voteshare must be between 0 and 1 inclusive!")

class Voter(Actor):
    """
        priority_axis will force voter to only care about one axis, not both.
        -1 for lib_auth, 1 for left_right, 0 for both
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